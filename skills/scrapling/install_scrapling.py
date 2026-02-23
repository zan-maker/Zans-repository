#!/usr/bin/env python3
"""
Download and install Scrapling manually
Bypasses pip issues by downloading directly
"""
import subprocess
import sys
import os

def download_scrapling():
    """Download Scrapling from GitHub"""
    print("📦 Downloading Scrapling from GitHub...")
    
    # Clone repository
    repo_url = "https://github.com/D4Vinci/Scrapling"
    clone_dir = "/home/node/.openclaw/workspace/scrapling"
    
    try:
        # Remove existing directory if present
        if os.path.exists(clone_dir):
            subprocess.run(["rm", "-rf", clone_dir], check=True)
        
        # Clone repository
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
        print(f"✅ Scrapling downloaded to {clone_dir}")
        return clone_dir
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Clone failed: {e}")
        return None

def install_scrapling(scrapling_dir):
    """Install Scrapling from source"""
    print()
    print("🔧 Installing Scrapling from source...")
    
    try:
        # Install using setup.py
        subprocess.run([
            sys.executable,
            "-m", "pip", "install", "-e", scrapling_dir
        ], check=True)
        print("✅ Scrapling installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def test_scrapling():
    """Test if Scrapling is installed"""
    print()
    print("🧪 Testing Scrapling installation...")
    
    try:
        # Try importing
        subprocess.run([
            sys.executable,
            "-c",
            "import scraping; print('Scrapling imported successfully')"
        ], check=True, capture_output=True, text=True)
        print("✅ Scrapling is working!")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Scrapling test failed")
        return False

def main():
    """Main installation process"""
    print("="*60)
    print("🎯 Scrapling Manual Installation")
    print("="*60)
    print()
    
    # Download
    scrapling_dir = download_scrapling()
    if not scrapling_dir:
        print()
        print("❌ Installation failed at download stage")
        sys.exit(1)
    
    # Install
    if not install_scrapling(scrapling_dir):
        print()
        print("❌ Installation failed at install stage")
        sys.exit(1)
    
    # Test
    if test_scrapling():
        print()
        print("="*60)
        print("✅ Scrapling is now installed and ready to use!")
        print("="*60)
        print()
        print("📚 Usage:")
        print("  python3 simple_test.py")
        print("  python3 scrapling_cli.py")
        print()
        print("📖 Documentation:")
        print("  https://scrapling.ai/docs")
        print("  https://github.com/D4Vinci/Scrapling")
    else:
        print()
        print("⚠️  Installation completed but test failed")
        print("Check error messages above")

if __name__ == "__main__":
    main()
