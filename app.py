"""
Black-Scholes Option Pricing Web Application

A professional web interface for option pricing and risk analysis.
Built with Flask and modern web technologies for portfolio demonstration.

Author: Bowen
Date: 2025
Purpose: Risk Analyst Portfolio Project
"""

from flask import Flask, render_template, request, jsonify
import json
import plotly
import plotly.graph_objects as go
from black_scholes import BlackScholesModel, ImpliedVolatilityCalculator, monte_carlo_option_pricing
from visualizations import OptionVisualization, sensitivity_analysis
import numpy as np
import pandas as pd

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize visualization engine
viz = OptionVisualization()


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html')


@app.route('/pricing')
def pricing():
    """Option pricing calculator page."""
    return render_template('pricing.html')


@app.route('/greeks')
def greeks():
    """Greeks analysis page."""
    return render_template('greeks.html')


@app.route('/risk-analysis')
def risk_analysis():
    """Risk analysis and P&L page."""
    return render_template('risk_analysis.html')

@app.route('/risk_metrics')
def risk_metrics():
    """Risk metrics page."""
    return render_template('risk_metrics.html')

@app.route('/monte_carlo')
def monte_carlo():
    """Monte Carlo simulation page."""
    return render_template('monte_carlo.html')

@app.route('/structured')
def structured():
    """Structured products page."""
    return render_template('structured.html')

@app.route('/market_data')
def market_data():
    """Market data page."""
    return render_template('market_data.html')

@app.route('/reports')
def reports():
    """Reports page."""
    return render_template('reports.html')


@app.route('/api/calculate-option', methods=['POST'])
def calculate_option():
    """
    API endpoint to calculate option prices and Greeks.
    
    Expected JSON payload:
    {
        "spot_price": float,
        "strike_price": float,
        "time_to_expiry": float,
        "risk_free_rate": float,
        "volatility": float,
        "option_type": str
    }
    """
    try:
        data = request.get_json()
        
        # Extract parameters
        S = float(data.get('spot_price', 100))
        K = float(data.get('strike_price', 100))
        T = float(data.get('time_to_expiry', 0.25))
        r = float(data.get('risk_free_rate', 0.05))
        sigma = float(data.get('volatility', 0.2))
        option_type = data.get('option_type', 'call').lower()
        
        # Validate inputs
        if any(x <= 0 for x in [S, K, T, sigma]):
            return jsonify({'error': 'All parameters must be positive'}), 400
        
        if not (0 <= r <= 1):
            return jsonify({'error': 'Risk-free rate must be between 0 and 1'}), 400
        
        # Create Black-Scholes model
        bs_model = BlackScholesModel(S, K, T, r, sigma)
        
        # Calculate prices
        call_price = bs_model.call_price()
        put_price = bs_model.put_price()
        
        # Calculate Greeks
        call_greeks = bs_model.get_all_greeks('call')
        put_greeks = bs_model.get_all_greeks('put')
        
        # Monte Carlo validation
        mc_call = monte_carlo_option_pricing(S, K, T, r, sigma, 'call', 50000)
        mc_put = monte_carlo_option_pricing(S, K, T, r, sigma, 'put', 50000)
        
        result = {
            'success': True,
            'parameters': {
                'spot_price': S,
                'strike_price': K,
                'time_to_expiry': T,
                'risk_free_rate': r,
                'volatility': sigma
            },
            'prices': {
                'call_price': round(call_price, 4),
                'put_price': round(put_price, 4)
            },
            'greeks': {
                'call': {k: round(v, 6) for k, v in call_greeks.items()},
                'put': {k: round(v, 6) for k, v in put_greeks.items()}
            },
            'monte_carlo_validation': {
                'call': {
                    'price': round(mc_call['monte_carlo_price'], 4),
                    'confidence_interval': round(mc_call['confidence_interval_95'], 4)
                },
                'put': {
                    'price': round(mc_put['monte_carlo_price'], 4),
                    'confidence_interval': round(mc_put['confidence_interval_95'], 4)
                }
            },
            'analysis': {
                'moneyness': round(S / K, 4),
                'time_value_call': round(call_price - max(S - K, 0), 4),
                'time_value_put': round(put_price - max(K - S, 0), 4),
                'put_call_parity_check': round(call_price - put_price - (S - K * np.exp(-r * T)), 6)
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/implied-volatility', methods=['POST'])
def calculate_implied_volatility():
    """
    Calculate implied volatility from market price.
    
    Expected JSON payload:
    {
        "market_price": float,
        "spot_price": float,
        "strike_price": float,
        "time_to_expiry": float,
        "risk_free_rate": float,
        "option_type": str
    }
    """
    try:
        data = request.get_json()
        
        market_price = float(data.get('market_price'))
        S = float(data.get('spot_price'))
        K = float(data.get('strike_price'))
        T = float(data.get('time_to_expiry'))
        r = float(data.get('risk_free_rate'))
        option_type = data.get('option_type', 'call').lower()
        
        # Calculate implied volatility
        iv = ImpliedVolatilityCalculator.calculate_implied_volatility(
            market_price, S, K, T, r, option_type
        )
        
        # Verify by calculating theoretical price with this IV
        bs_model = BlackScholesModel(S, K, T, r, iv)
        if option_type == 'call':
            theoretical_price = bs_model.call_price()
        else:
            theoretical_price = bs_model.put_price()
        
        result = {
            'success': True,
            'implied_volatility': round(iv, 6),
            'implied_volatility_percent': round(iv * 100, 2),
            'theoretical_price': round(theoretical_price, 4),
            'price_difference': round(abs(theoretical_price - market_price), 6)
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/greeks-chart', methods=['POST'])
def greeks_chart():
    """Generate Greeks visualization chart."""
    try:
        data = request.get_json()
        
        S = float(data.get('spot_price', 100))
        K = float(data.get('strike_price', 100))
        T = float(data.get('time_to_expiry', 0.25))
        r = float(data.get('risk_free_rate', 0.05))
        sigma = float(data.get('volatility', 0.2))
        
        # Generate Greeks dashboard
        fig = viz.plot_greeks_dashboard(S, K, T, r, sigma)
        
        # Convert to JSON
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return jsonify({'success': True, 'chart': graphJSON})
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/price-surface', methods=['POST'])
def price_surface():
    """Generate 3D price surface chart."""
    try:
        data = request.get_json()
        print(f"Price surface request data: {data}")
        
        K = float(data.get('strike_price', 100))
        T = float(data.get('time_to_expiry', 0.25))
        r = float(data.get('risk_free_rate', 0.05))
        sigma = float(data.get('volatility', 0.2))
        option_type = data.get('option_type', 'call').lower()
        
        print(f"Parameters: K={K}, T={T}, r={r}, sigma={sigma}, type={option_type}")
        
        # Validate parameters
        if T <= 0:
            T = 0.01  # Minimum time
        if sigma <= 0:
            sigma = 0.01  # Minimum volatility
        if K <= 0:
            K = 100  # Default strike
        
        # Generate price surface
        print("Generating price surface...")
        fig = viz.plot_option_price_surface(K, T, r, sigma, option_type=option_type)
        print("Price surface generated successfully")
        
        # Convert to JSON
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return jsonify({'success': True, 'chart': graphJSON})
        
    except Exception as e:
        print(f"Error in price_surface: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/pnl-analysis', methods=['POST'])
def pnl_analysis():
    """Generate P&L analysis chart."""
    try:
        data = request.get_json()
        
        S = float(data.get('spot_price', 100))
        K = float(data.get('strike_price', 100))
        T = float(data.get('time_to_expiry', 0.25))
        r = float(data.get('risk_free_rate', 0.05))
        sigma = float(data.get('volatility', 0.2))
        option_type = data.get('option_type', 'call').lower()
        premium_paid = data.get('premium_paid')
        
        if premium_paid:
            premium_paid = float(premium_paid)
        
        # Generate P&L analysis
        fig = viz.plot_pnl_analysis(S, K, T, r, sigma, option_type, premium_paid)
        
        # Convert to JSON
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        return jsonify({'success': True, 'chart': graphJSON})
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/sensitivity-analysis', methods=['POST'])
def api_sensitivity_analysis():
    """Perform sensitivity analysis."""
    try:
        data = request.get_json()
        
        base_params = {
            'S': float(data.get('spot_price', 100)),
            'K': float(data.get('strike_price', 100)),
            'T': float(data.get('time_to_expiry', 0.25)),
            'r': float(data.get('risk_free_rate', 0.05)),
            'sigma': float(data.get('volatility', 0.2))
        }
        
        option_type = data.get('option_type', 'call').lower()
        
        # Define parameter ranges for sensitivity analysis
        param_ranges = {
            'S': np.linspace(base_params['S'] * 0.8, base_params['S'] * 1.2, 20),
            'sigma': np.linspace(base_params['sigma'] * 0.5, base_params['sigma'] * 1.5, 20),
            'T': np.linspace(0.01, base_params['T'] * 2, 20),
            'r': np.linspace(0.01, base_params['r'] * 2, 20)
        }
        
        # Perform sensitivity analysis
        results_df = sensitivity_analysis(base_params, param_ranges, option_type)
        
        # Convert to JSON format
        results = results_df.to_dict('records')
        
        return jsonify({'success': True, 'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('500.html'), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Black-Scholes Option Pricing Web Application")
    print("=" * 60)
    print("Author: Bowen")
    print("Purpose: Risk Analyst Portfolio Project")
    print("=" * 60)
    print("\nStarting Flask development server...")
    print("Access the application at: http://localhost:5001")
    print("\nAvailable endpoints:")
    print("- /                 : Main dashboard")
    print("- /pricing          : Option pricing calculator")
    print("- /greeks           : Greeks analysis")
    print("- /risk-analysis    : Risk analysis and P&L")
    print("\nAPI endpoints:")
    print("- POST /api/calculate-option")
    print("- POST /api/implied-volatility")
    print("- POST /api/greeks-chart")
    print("- POST /api/price-surface")
    print("- POST /api/pnl-analysis")
    print("- POST /api/sensitivity-analysis")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001)
