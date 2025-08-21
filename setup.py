#!/usr/bin/env python
"""
Setup script for Black-Scholes Option Pricing Model

This script sets up the project environment and runs initial validation.

Author: Bowen
Date: 2024
Purpose: Risk Analyst Portfolio Project
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print setup banner."""
    print("=" * 70)
    print("BLACK-SCHOLES OPTION PRICING MODEL - SETUP")
    print("=" * 70)
    print("Professional derivatives pricing and risk analysis platform")
    print("Author: Bowen")
    print("Purpose: Risk Analyst Portfolio Project")
    print("=" * 70)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating project directories...")
    
    directories = [
        "data/sample_data",
        "docs/images",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   Created: {directory}")
    
    print("✅ Directories created successfully")

def run_tests():
    """Run initial tests to validate setup."""
    print("\n🧪 Running validation tests...")
    
    try:
        # Import test to check if modules work
        sys.path.insert(0, 'src')
        from black_scholes import BlackScholesModel
        
        # Quick validation test
        bs_model = BlackScholesModel(S=100, K=100, T=0.25, r=0.05, sigma=0.2)
        call_price = bs_model.call_price()
        put_price = bs_model.put_price()
        
        if call_price > 0 and put_price > 0:
            print(f"   ✅ Black-Scholes model working: Call=${call_price:.4f}, Put=${put_price:.4f}")
        else:
            print("   ❌ Black-Scholes model validation failed")
            return False
        
        # Test Greeks
        greeks = bs_model.get_all_greeks('call')
        if all(isinstance(v, (int, float)) for v in greeks.values()):
            print(f"   ✅ Greeks calculation working: Delta={greeks['delta']:.4f}")
        else:
            print("   ❌ Greeks calculation failed")
            return False
        
        print("✅ All validation tests passed")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def create_sample_data():
    """Create sample data files."""
    print("\n📊 Creating sample data...")
    
    sample_data = """# Sample Option Data
# Format: Symbol,Type,Spot,Strike,Expiry,Rate,Volatility,MarketPrice
AAPL,call,150.00,155.00,0.25,0.05,0.25,8.50
AAPL,put,150.00,155.00,0.25,0.05,0.25,12.80
MSFT,call,300.00,305.00,0.33,0.05,0.22,15.75
MSFT,put,300.00,305.00,0.33,0.05,0.22,19.25
GOOGL,call,2500.00,2550.00,0.17,0.05,0.28,45.20
GOOGL,put,2500.00,2550.00,0.17,0.05,0.28,89.80
"""
    
    with open("data/sample_data/options.csv", "w") as f:
        f.write(sample_data)
    
    print("   Created: data/sample_data/options.csv")
    print("✅ Sample data created successfully")

def display_usage_instructions():
    """Display usage instructions."""
    print("\n" + "=" * 70)
    print("🚀 SETUP COMPLETE - USAGE INSTRUCTIONS")
    print("=" * 70)
    print()
    print("1. Start the web application:")
    print("   python app.py")
    print()
    print("2. Access the application:")
    print("   Open your browser and go to: http://localhost:5000")
    print()
    print("3. Run tests:")
    print("   python run_tests.py")
    print()
    print("4. Use the Python API:")
    print("   from src.black_scholes import BlackScholesModel")
    print("   model = BlackScholesModel(S=100, K=100, T=0.25, r=0.05, sigma=0.2)")
    print("   price = model.call_price()")
    print()
    print("5. Generate visualizations:")
    print("   from src.visualizations import OptionVisualization")
    print("   viz = OptionVisualization()")
    print("   chart = viz.plot_greeks_dashboard(100, 100, 0.25, 0.05, 0.2)")
    print()
    print("📚 Documentation: README.md")
    print("🐛 Issues: Check logs/ directory for error logs")
    print("📊 Sample Data: data/sample_data/options.csv")
    print()
    print("=" * 70)
    print("🎯 Ready for your risk analyst portfolio demonstration!")
    print("=" * 70)

def main():
    """Main setup function."""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create sample data
    create_sample_data()
    
    # Run validation tests
    if not run_tests():
        print("\n⚠️  Setup completed with warnings - some tests failed")
        print("   The application may still work, but please review the errors")
    
    # Display instructions
    display_usage_instructions()

if __name__ == "__main__":
    main()
