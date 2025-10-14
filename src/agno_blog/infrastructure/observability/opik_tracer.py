"""Opik integration for LLM observability and tracing."""

import os
from typing import Optional

from agno.utils.log import logger

try:
    import opik
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from openinference.instrumentation.agno import AgnoInstrumentor
    OPIK_AVAILABLE = True
except ImportError:
    OPIK_AVAILABLE = False
    logger.warning("Opik or OpenTelemetry not installed. LLM tracing features will be disabled.")

from ...config import settings


class OpikTracer:
    """Wrapper for Opik LLM tracing."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_name: Optional[str] = None,
        workspace: Optional[str] = None,
        enabled: bool = True,
    ):
        """
        Initialize Opik LLM tracer.

        Args:
            api_key: Opik API key
            project_name: Project name in Opik
            workspace: Workspace name in Opik
            enabled: Whether tracing is enabled
        """
        self.enabled = enabled and OPIK_AVAILABLE
        self.instrumentor: Optional[AgnoInstrumentor] = None
        self._is_instrumented = False

        if not self.enabled:
            if not OPIK_AVAILABLE:
                logger.info("Opik LLM tracing disabled: libraries not available")
            else:
                logger.info("Opik LLM tracing disabled by configuration")
            return

        # Use provided values or fall back to settings
        self.api_key = api_key or settings.opik_api_key
        self.project_name = project_name or settings.opik_project_name
        self.workspace = workspace or settings.opik_workspace

        if not self.api_key:
            logger.warning("Opik API key not provided. LLM tracing disabled.")
            self.enabled = False
            return

        try:
            # Configure Opik
            opik.configure(
                api_key=self.api_key,
                workspace=self.workspace,
                use_local=False  # Use Comet.com cloud
            )
            
            # Set project name via environment variable
            os.environ["OPIK_PROJECT_NAME"] = self.project_name
            
            logger.info(
                f"Opik configured: project={self.project_name}, workspace={self.workspace}"
            )
        except Exception as e:
            logger.error(f"Failed to configure Opik: {str(e)}")
            self.enabled = False

    def instrument_agno(self) -> bool:
        """
        Instrument Agno for automatic LLM tracing.

        Returns:
            True if instrumentation succeeded, False otherwise
        """
        if not self.enabled:
            return False

        if self._is_instrumented:
            logger.debug("Agno already instrumented with Opik")
            return True

        try:
            # Set environment variables for OTLP HTTP exporter
            # According to Opik docs: https://www.comet.com/docs/opik/integrations/agno
            os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://www.comet.com/opik/api/v1/private/otel"
            
            # Build headers string: Authorization=<key>,Comet-Workspace=<workspace>,projectName=<project>
            headers_parts = [
                f"Authorization={self.api_key}",
                f"Comet-Workspace={self.workspace}" if self.workspace else "Comet-Workspace=default",
            ]
            
            if self.project_name:
                headers_parts.append(f"projectName={self.project_name}")
            
            os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = ",".join(headers_parts)
            
            # Configure tracer provider with HTTP exporter
            tracer_provider = TracerProvider()
            tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
            trace.set_tracer_provider(tracer_provider=tracer_provider)

            # Instrument Agno
            self.instrumentor = AgnoInstrumentor()
            self.instrumentor.instrument()
            
            self._is_instrumented = True
            logger.info(f"Agno instrumented successfully with Opik (project: {self.project_name})")
            return True

        except Exception as e:
            logger.error(f"Failed to instrument Agno with Opik: {str(e)}")
            self.enabled = False
            return False

    def uninstrument_agno(self) -> bool:
        """
        Remove Agno instrumentation.

        Returns:
            True if uninstrumentation succeeded, False otherwise
        """
        if not self._is_instrumented or not self.instrumentor:
            return False

        try:
            self.instrumentor.uninstrument()
            self._is_instrumented = False
            logger.info("Agno uninstrumented from Opik")
            return True
        except Exception as e:
            logger.error(f"Failed to uninstrument Agno: {str(e)}")
            return False

    def is_instrumented(self) -> bool:
        """Check if Agno is currently instrumented."""
        return self._is_instrumented

    def __enter__(self):
        """Context manager entry."""
        self.instrument_agno()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.uninstrument_agno()


# Global tracer instance
_global_opik_tracer: Optional[OpikTracer] = None


def get_opik_tracer(
    api_key: Optional[str] = None,
    project_name: Optional[str] = None,
    workspace: Optional[str] = None,
    enabled: Optional[bool] = None,
    force_new: bool = False,
) -> OpikTracer:
    """
    Get or create an Opik LLM tracer instance.

    Args:
        api_key: Opik API key (uses settings if not provided)
        project_name: Project name (uses settings if not provided)
        workspace: Workspace name (uses settings if not provided)
        enabled: Whether tracing is enabled (uses settings if not provided)
        force_new: Force creation of a new tracer

    Returns:
        OpikTracer instance
    """
    global _global_opik_tracer

    if force_new or _global_opik_tracer is None:
        _global_opik_tracer = OpikTracer(
            api_key=api_key,
            project_name=project_name,
            workspace=workspace,
            enabled=enabled if enabled is not None else settings.opik_enabled,
        )

    return _global_opik_tracer


def instrument_agno_globally(
    api_key: Optional[str] = None,
    project_name: Optional[str] = None,
    workspace: Optional[str] = None,
) -> bool:
    """
    Instrument Agno globally for automatic LLM tracing.

    Args:
        api_key: Opik API key (uses settings if not provided)
        project_name: Project name (uses settings if not provided)
        workspace: Workspace name (uses settings if not provided)

    Returns:
        True if instrumentation succeeded, False otherwise
    """
    tracer = get_opik_tracer(
        api_key=api_key,
        project_name=project_name,
        workspace=workspace,
    )
    return tracer.instrument_agno()
