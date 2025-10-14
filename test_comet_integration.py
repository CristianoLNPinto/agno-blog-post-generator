#!/usr/bin/env python3
"""Test script for Comet ML integration."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agno_blog.infrastructure.observability import CometTracker, get_comet_tracker
from src.agno_blog.config import settings


def test_basic_tracking():
    """Test basic Comet ML tracking functionality."""
    print("🧪 Testing Comet ML Integration\n")
    print("=" * 60)
    
    # Test 1: Check if Comet ML is available
    print("\n1️⃣ Checking Comet ML availability...")
    try:
        import comet_ml
        print("   ✅ Comet ML library is installed")
    except ImportError:
        print("   ❌ Comet ML library not found")
        print("   Run: uv pip install comet_ml")
        return False
    
    # Test 2: Check configuration
    print("\n2️⃣ Checking configuration...")
    print(f"   API Key: {'✅ Set' if settings.comet_api_key else '❌ Not set'}")
    print(f"   Project: {settings.comet_project_name}")
    print(f"   Workspace: {settings.comet_workspace or '❌ Not set'}")
    print(f"   Enabled: {settings.comet_enabled}")
    
    if not settings.comet_api_key:
        print("\n   ⚠️  Warning: COMET_API_KEY not set in .env")
        print("   Run: ./setup_comet_env.sh")
        print("   Or manually add to .env file")
    
    # Test 3: Initialize tracker
    print("\n3️⃣ Initializing tracker...")
    try:
        tracker = get_comet_tracker()
        print("   ✅ Tracker initialized successfully")
        
        if not tracker.enabled:
            print("   ⚠️  Tracker is disabled (check API key and settings)")
            return False
            
    except Exception as e:
        print(f"   ❌ Failed to initialize tracker: {str(e)}")
        return False
    
    # Test 4: Test basic operations
    print("\n4️⃣ Testing basic operations...")
    try:
        # Set experiment name
        tracker.set_name("test_experiment")
        print("   ✅ Set experiment name")
        
        # Add tags
        tracker.add_tags(["test", "integration"])
        print("   ✅ Added tags")
        
        # Log parameters
        tracker.log_parameters({
            "test_param": "value",
            "number": 42
        })
        print("   ✅ Logged parameters")
        
        # Log metrics
        tracker.log_metric("test_metric", 0.95)
        print("   ✅ Logged metric")
        
        # Test phase tracking
        with tracker.track_phase("test_phase"):
            import time
            time.sleep(0.1)
        print("   ✅ Phase tracking works")
        
        # Log text
        tracker.log_text("Test output", metadata={"type": "test"})
        print("   ✅ Logged text")
        
    except Exception as e:
        print(f"   ❌ Operation failed: {str(e)}")
        return False
    
    # Test 5: End experiment
    print("\n5️⃣ Ending experiment...")
    try:
        tracker.end()
        print("   ✅ Experiment ended successfully")
    except Exception as e:
        print(f"   ❌ Failed to end experiment: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("\n📊 View your experiment at:")
    print(f"   https://www.comet.com/{settings.comet_workspace}/{settings.comet_project_name}")
    
    return True


def test_service_integration():
    """Test integration with BlogGenerationService."""
    print("\n\n🧪 Testing Service Integration\n")
    print("=" * 60)
    
    try:
        from src.agno_blog.application.blog_generation_service import BlogGenerationService
        
        print("\n1️⃣ Creating service with tracker...")
        tracker = get_comet_tracker(force_new=True)
        service = BlogGenerationService(tracker=tracker)
        print("   ✅ Service created with tracker")
        
        print("\n2️⃣ Checking tracker integration...")
        if service.tracker:
            print("   ✅ Tracker is attached to service")
        else:
            print("   ❌ Tracker not attached")
            return False
        
        print("\n✅ Service integration test passed!")
        
        # Clean up
        tracker.end()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Service integration test failed: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "🎯" * 30)
    print("Comet ML Integration Test Suite")
    print("🎯" * 30 + "\n")
    
    # Run tests
    basic_test = test_basic_tracking()
    
    if basic_test:
        service_test = test_service_integration()
    else:
        print("\n⚠️  Skipping service integration test due to basic test failure")
        service_test = False
    
    # Summary
    print("\n\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Basic Tracking: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"Service Integration: {'✅ PASS' if service_test else '❌ FAIL'}")
    print("=" * 60)
    
    if basic_test and service_test:
        print("\n🎉 All tests passed! Comet ML is ready to use.")
        print("\n📚 Next steps:")
        print("   1. Run the Streamlit app: streamlit run streamlit_app.py")
        print("   2. Generate a blog post")
        print("   3. View metrics in Comet ML dashboard")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure .env file has COMET_API_KEY set")
        print("   2. Run: ./setup_comet_env.sh")
        print("   3. Check COMET_ML_SETUP.md for detailed instructions")
        return 1


if __name__ == "__main__":
    sys.exit(main())
