# Quick Start Guide

## Black-Scholes Option Pricing Model

This guide will help you get the application running in under 5 minutes.

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Modern web browser

### Installation Steps

1. **Navigate to the project directory:**
   ```bash
   cd bs_pricing_model
   ```

2. **Run the automated setup:**
   ```bash
   python setup.py
   ```
   This will:
   - Check Python version
   - Install all dependencies
   - Create necessary directories
   - Run validation tests
   - Create sample data

3. **Start the web application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   Go to `http://localhost:5000`

### Quick Test

To verify everything is working:

```python
# Test the core model
from src.black_scholes import BlackScholesModel

# Create a model instance
bs = BlackScholesModel(S=100, K=100, T=0.25, r=0.05, sigma=0.2)

# Calculate option prices
call_price = bs.call_price()
put_price = bs.put_price()

print(f"Call Price: ${call_price:.4f}")
print(f"Put Price: ${put_price:.4f}")

# Get all Greeks
greeks = bs.get_all_greeks('call')
for greek, value in greeks.items():
    print(f"{greek.capitalize()}: {value:.6f}")
```

### Web Interface Features

Once the web app is running, you can access:

- **Dashboard** (`/`): Overview and quick calculator
- **Pricing** (`/pricing`): Comprehensive option pricing tool
- **Greeks** (`/greeks`): Interactive Greeks analysis
- **Risk Analysis** (`/risk-analysis`): P&L scenarios and sensitivity analysis

### Troubleshooting

**If you get import errors:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

**If dependencies fail to install:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If the web app doesn't start:**
- Check that port 5000 is available
- Try running with `python -m flask run`

### Next Steps

1. Explore the web interface
2. Run the test suite: `python run_tests.py`
3. Review the comprehensive documentation in `README.md`
4. Customize parameters for your analysis needs

### Support

For detailed documentation, see `README.md`
For technical details, check the code comments and docstrings

---

**Ready to demonstrate your quantitative finance skills!** 🚀
