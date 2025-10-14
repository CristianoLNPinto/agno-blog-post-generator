"""Comet ML integration for observability and experiment tracking."""

import time
from contextlib import contextmanager
from typing import Any, Dict, Optional

from agno.utils.log import logger

try:
    import comet_ml
    COMET_AVAILABLE = True
except ImportError:
    COMET_AVAILABLE = False
    logger.warning("comet_ml not installed. Observability features will be disabled.")

from ...config import settings


class CometTracker:
    """Wrapper for Comet ML experiment tracking."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_name: Optional[str] = None,
        workspace: Optional[str] = None,
        enabled: bool = True,
    ):
        """
        Initialize Comet ML tracker.

        Args:
            api_key: Comet ML API key
            project_name: Project name in Comet ML
            workspace: Workspace name in Comet ML
            enabled: Whether tracking is enabled
        """
        self.enabled = enabled and COMET_AVAILABLE
        self.experiment: Optional[Any] = None
        self._phase_start_times: Dict[str, float] = {}

        if not self.enabled:
            if not COMET_AVAILABLE:
                logger.info("Comet ML tracking disabled: library not available")
            else:
                logger.info("Comet ML tracking disabled by configuration")
            return

        # Use provided values or fall back to settings
        self.api_key = api_key or settings.comet_api_key
        self.project_name = project_name or settings.comet_project_name
        self.workspace = workspace or settings.comet_workspace

        if not self.api_key:
            logger.warning("Comet ML API key not provided. Tracking disabled.")
            self.enabled = False
            return

        try:
            # Initialize experiment
            self.experiment = comet_ml.Experiment(
                api_key=self.api_key,
                project_name=self.project_name,
                workspace=self.workspace,
            )
            logger.info(
                f"Comet ML experiment initialized: {self.project_name} in workspace {self.workspace}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Comet ML experiment: {str(e)}")
            self.enabled = False

    def log_parameters(self, params: Dict[str, Any]) -> None:
        """
        Log parameters to Comet ML.

        Args:
            params: Dictionary of parameters to log
        """
        if not self.enabled or not self.experiment:
            return

        try:
            self.experiment.log_parameters(params)
            logger.debug(f"Logged parameters: {params}")
        except Exception as e:
            logger.error(f"Failed to log parameters: {str(e)}")

    def log_metric(self, name: str, value: Any, step: Optional[int] = None) -> None:
        """
        Log a metric to Comet ML.

        Args:
            name: Metric name
            value: Metric value
            step: Optional step number
        """
        if not self.enabled or not self.experiment:
            return

        try:
            self.experiment.log_metric(name, value, step=step)
            logger.debug(f"Logged metric {name}: {value}")
        except Exception as e:
            logger.error(f"Failed to log metric {name}: {str(e)}")

    def log_metrics(self, metrics: Dict[str, Any], step: Optional[int] = None) -> None:
        """
        Log multiple metrics to Comet ML.

        Args:
            metrics: Dictionary of metrics to log
            step: Optional step number
        """
        if not self.enabled or not self.experiment:
            return

        try:
            self.experiment.log_metrics(metrics, step=step)
            logger.debug(f"Logged metrics: {metrics}")
        except Exception as e:
            logger.error(f"Failed to log metrics: {str(e)}")

    def log_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log text to Comet ML.

        Args:
            text: Text to log
            metadata: Optional metadata dictionary
        """
        if not self.enabled or not self.experiment:
            return

        try:
            self.experiment.log_text(text, metadata=metadata)
            logger.debug(f"Logged text with metadata: {metadata}")
        except Exception as e:
            logger.error(f"Failed to log text: {str(e)}")

    def log_html(self, html: str, name: str = "output") -> None:
        """
        Log HTML content to Comet ML.

        Args:
            html: HTML content to log
            name: Name for the HTML asset
        """
        if not self.enabled or not self.experiment:
            return

        try:
            self.experiment.log_html(html, name=name)
            logger.debug(f"Logged HTML: {name}")
        except Exception as e:
            logger.error(f"Failed to log HTML: {str(e)}")

    def log_other(self, key: str, value: Any) -> None:
        """
        Log other data to Comet ML.

        Args:
            key: Key for the data
            value: Value to log
        """
        if not self.enabled or not self.experiment:
            return

        try:
            self.experiment.log_other(key, value)
            logger.debug(f"Logged other data {key}: {value}")
        except Exception as e:
            logger.error(f"Failed to log other data {key}: {str(e)}")

    def set_name(self, name: str) -> None:
        """
        Set the experiment name.

        Args:
            name: Experiment name
        """
        if not self.enabled or not self.experiment:
            return

        try:
            self.experiment.set_name(name)
            logger.debug(f"Set experiment name: {name}")
        except Exception as e:
            logger.error(f"Failed to set experiment name: {str(e)}")

    def add_tag(self, tag: str) -> None:
        """
        Add a tag to the experiment.

        Args:
            tag: Tag to add
        """
        if not self.enabled or not self.experiment:
            return

        try:
            self.experiment.add_tag(tag)
            logger.debug(f"Added tag: {tag}")
        except Exception as e:
            logger.error(f"Failed to add tag: {str(e)}")

    def add_tags(self, tags: list) -> None:
        """
        Add multiple tags to the experiment.

        Args:
            tags: List of tags to add
        """
        if not self.enabled or not self.experiment:
            return

        try:
            self.experiment.add_tags(tags)
            logger.debug(f"Added tags: {tags}")
        except Exception as e:
            logger.error(f"Failed to add tags: {str(e)}")

    def start_phase(self, phase_name: str) -> None:
        """
        Start tracking a phase.

        Args:
            phase_name: Name of the phase
        """
        if not self.enabled:
            return

        self._phase_start_times[phase_name] = time.time()
        logger.debug(f"Started phase: {phase_name}")

    def end_phase(self, phase_name: str) -> Optional[float]:
        """
        End tracking a phase and log its duration.

        Args:
            phase_name: Name of the phase

        Returns:
            Duration in seconds, or None if phase wasn't started
        """
        if not self.enabled or phase_name not in self._phase_start_times:
            return None

        duration = time.time() - self._phase_start_times[phase_name]
        self.log_metric(f"phase_{phase_name}_duration_seconds", duration)
        del self._phase_start_times[phase_name]
        logger.debug(f"Ended phase {phase_name}: {duration:.2f}s")
        return duration

    @contextmanager
    def track_phase(self, phase_name: str):
        """
        Context manager for tracking a phase.

        Args:
            phase_name: Name of the phase

        Example:
            with tracker.track_phase("research"):
                # do research work
                pass
        """
        self.start_phase(phase_name)
        try:
            yield
        finally:
            self.end_phase(phase_name)

    def end(self) -> None:
        """End the experiment."""
        if not self.enabled or not self.experiment:
            return

        try:
            self.experiment.end()
            logger.info("Comet ML experiment ended")
        except Exception as e:
            logger.error(f"Failed to end experiment: {str(e)}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.end()


# Global tracker instance
_global_tracker: Optional[CometTracker] = None


def get_comet_tracker(
    api_key: Optional[str] = None,
    project_name: Optional[str] = None,
    workspace: Optional[str] = None,
    enabled: Optional[bool] = None,
    force_new: bool = False,
) -> CometTracker:
    """
    Get or create a Comet ML tracker instance.

    Args:
        api_key: Comet ML API key (uses settings if not provided)
        project_name: Project name (uses settings if not provided)
        workspace: Workspace name (uses settings if not provided)
        enabled: Whether tracking is enabled (uses settings if not provided)
        force_new: Force creation of a new tracker

    Returns:
        CometTracker instance
    """
    global _global_tracker

    if force_new or _global_tracker is None:
        _global_tracker = CometTracker(
            api_key=api_key,
            project_name=project_name,
            workspace=workspace,
            enabled=enabled if enabled is not None else settings.comet_enabled,
        )

    return _global_tracker
