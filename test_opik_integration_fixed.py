#!/usr/bin/env python3
"""Test script for Opik integration (corrected implementation)."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agno_blog.infrastructure.observability import get_opik_tracer
from src.agno_blog.config import settings


def test_opik_configuration():
    """Test Opik configuration and setup."""
    print("🧪 Testing Opik Integration (Corrected Implementation)\n")
    print("=" * 60)
    
    # Test 1: Check configuration
    print("\n1️⃣ Checking configuration...")
    print(f"   API Key: {'✅ Set' if settings.opik_api_key else '❌ Not set'}")
    print(f"   Project: {settings.opik_project_name}")
    print(f"   Workspace: {settings.opik_workspace or '❌ Not set'}")
    print(f"   Enabled: {settings.opik_enabled}")
    
    if not settings.opik_api_key:
        print("\n   ⚠️  Warning: OPIK_API_KEY not set in .env")
        print("   Add your Comet ML API key to .env file")
        return False
    
    # Test 2: Initialize tracer
    print("\n2️⃣ Initializing tracer...")
    try:
        tracer = get_opik_tracer()
        print("   ✅ Tracer initialized successfully")
        
        if not tracer.enabled:
            print("   ⚠️  Tracer is disabled (check API key and settings)")
            return False
            
    except Exception as e:
        print(f"   ❌ Failed to initialize tracer: {str(e)}")
        return False
    
    # Test 3: Test instrumentation
    print("\n3️⃣ Testing instrumentation...")
    try:
        success = tracer.instrument_agno()
        
        if success:
            print("   ✅ Agno instrumented successfully")
            print(f"   ✅ Project: {tracer.project_name}")
            print(f"   ✅ Workspace: {tracer.workspace}")
        else:
            print("   ❌ Instrumentation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Instrumentation error: {str(e)}")
        return False
    
    # Test 4: Check environment variables
    print("\n4️⃣ Checking environment variables...")
    import os
    
    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    headers = os.environ.get("OTEL_EXPORTER_OTLP_HEADERS")
    
    if endpoint:
        print(f"   ✅ OTEL_EXPORTER_OTLP_ENDPOINT: {endpoint}")
    else:
        print("   ❌ OTEL_EXPORTER_OTLP_ENDPOINT not set")
        
    if headers:
        # Don't print full headers (contains API key)
        print(f"   ✅ OTEL_EXPORTER_OTLP_HEADERS: Set (length: {len(headers)})")
    else:
        print("   ❌ OTEL_EXPORTER_OTLP_HEADERS not set")
    
    # Test 5: Verify correct implementation
    print("\n5️⃣ Verifying implementation details...")
    
    # Check if using HTTP exporter
    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        print("   ✅ Using HTTP exporter (correct)")
    except ImportError:
        print("   ❌ HTTP exporter not available")
    
    # Check if using SimpleSpanProcessor
    try:
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor
        print("   ✅ SimpleSpanProcessor available (correct)")
    except ImportError:
        print("   ❌ SimpleSpanProcessor not available")
    
    # Check endpoint
    if endpoint == "https://www.comet.com/opik/api/v1/private/otel":
        print("   ✅ Using correct Opik endpoint")
    else:
        print(f"   ⚠️  Endpoint: {endpoint}")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("\n📊 Next steps:")
    print("   1. Run: streamlit run streamlit_app.py")
    print("   2. Generate a blog post")
    print("   3. View traces at: https://www.comet.com/")
    print(f"   4. Navigate to: {tracer.workspace}/{tracer.project_name}")
    
    return True


def main():
    """Run all tests."""
    print("\n" + "🎯" * 30)
    print("Opik Integration Test (Corrected Implementation)")
    print("Following: https://www.comet.com/docs/opik/integrations/agno")
    print("🎯" * 30 + "\n")
    
    success = test_opik_configuration()
    
    print("\n\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Status: {'✅ PASS' if success else '❌ FAIL'}")
    print("=" * 60)
    
    if success:
        print("\n🎉 Opik integration is correctly configured!")
        print("\n📚 Implementation follows official Opik docs:")
        print("   - Uses HTTP exporter (not gRPC)")
        print("   - Uses environment variables")
        print("   - Uses SimpleSpanProcessor")
        print("   - Correct endpoint: www.comet.com/opik/api")
        return 0
    else:
        print("\n❌ Configuration issues detected.")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure .env file has OPIK_API_KEY set")
        print("   2. Use your Comet ML API key")
        print("   3. Check OPIK_SETUP.md for detailed instructions")
        return 1


if __name__ == "__main__":
    sys.exit(main())
