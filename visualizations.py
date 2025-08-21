"""
Option Pricing Visualizations

This module provides comprehensive visualization tools for Black-Scholes option pricing,
including price surfaces, Greeks analysis, and sensitivity analysis.

Author: Bowen
Date: 2024
Purpose: Risk Analyst Portfolio Project
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

from black_scholes import BlackScholesModel, monte_carlo_option_pricing


class OptionVisualization:
    """
    Comprehensive visualization tools for option pricing and risk analysis.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8'):
        """
        Initialize visualization settings.
        
        Args:
            style (str): Matplotlib style
        """
        plt.style.use('default')  # Use default style as seaborn styles may not be available
        sns.set_palette("husl")
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    def plot_option_price_surface(self, K: float, T: float, r: float, sigma: float,
                                spot_range: Tuple[float, float] = None,
                                time_range: Tuple[float, float] = None,
                                option_type: str = 'call') -> go.Figure:
        """
        Create 3D surface plot of option prices vs spot price and time to expiration.
        
        Args:
            K (float): Strike price
            T (float): Base time to expiration
            r (float): Risk-free rate
            sigma (float): Volatility
            spot_range (Tuple): Range of spot prices (min, max)
            time_range (Tuple): Range of time to expiration (min, max)
            option_type (str): 'call' or 'put'
            
        Returns:
            plotly.graph_objects.Figure: 3D surface plot
        """
        if spot_range is None:
            spot_range = (K * 0.7, K * 1.3)
        if time_range is None:
            time_range = (0.01, T * 2)
        
        # Create meshgrid
        spot_prices = np.linspace(spot_range[0], spot_range[1], 50)
        times = np.linspace(time_range[0], time_range[1], 50)
        S_mesh, T_mesh = np.meshgrid(spot_prices, times)
        
        # Calculate option prices
        prices = np.zeros_like(S_mesh)
        try:
            for i in range(len(times)):
                for j in range(len(spot_prices)):
                    if T_mesh[i,j] <= 0:
                        T_mesh[i,j] = 0.001  # Minimum time to avoid division by zero
                    bs_model = BlackScholesModel(S_mesh[i,j], K, T_mesh[i,j], r, sigma)
                    if option_type.lower() == 'call':
                        prices[i,j] = bs_model.call_price()
                    else:
                        prices[i,j] = bs_model.put_price()
        except Exception as e:
            print(f"Error calculating prices: {e}")
            # Fill with default values if calculation fails
            prices.fill(0)
        
        # Create 3D surface plot with modern styling
        fig = go.Figure(data=[go.Surface(
            x=S_mesh,
            y=T_mesh,
            z=prices,
            colorscale=[[0, '#0a0a0a'], [0.2, '#667eea'], [0.5, '#764ba2'], [0.8, '#f093fb'], [1, '#f5576c']],
            name=f'{option_type.capitalize()} Price',
            hovertemplate='<b>Spot Price</b>: $%{x:.2f}<br>' +
                         '<b>Time to Expiry</b>: %{y:.3f} years<br>' +
                         '<b>Option Price</b>: $%{z:.2f}<extra></extra>'
        )])
        
        fig.update_layout(
            title={
                'text': f'{option_type.capitalize()} Option Price Surface<br><sub>Strike=${K:.0f}, r={r:.1%}, σ={sigma:.1%}</sub>',
                'font': {'color': 'white', 'size': 16},
                'x': 0.5
            },
            scene=dict(
                xaxis_title='Spot Price ($)',
                yaxis_title='Time to Expiration (years)',
                zaxis_title=f'{option_type.capitalize()} Price ($)',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
                bgcolor='rgba(0,0,0,0)',
                xaxis=dict(
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.1)',
                    showbackground=True,
                    zerolinecolor='rgba(255,255,255,0.2)',
                    title_font=dict(color='white'),
                    tickfont=dict(color='white')
                ),
                yaxis=dict(
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.1)',
                    showbackground=True,
                    zerolinecolor='rgba(255,255,255,0.2)',
                    title_font=dict(color='white'),
                    tickfont=dict(color='white')
                ),
                zaxis=dict(
                    backgroundcolor='rgba(0,0,0,0)',
                    gridcolor='rgba(255,255,255,0.1)',
                    showbackground=True,
                    zerolinecolor='rgba(255,255,255,0.2)',
                    title_font=dict(color='white'),
                    tickfont=dict(color='white')
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            width=800,
            height=600
        )
        
        return fig
    
    def plot_greeks_dashboard(self, S: float, K: float, T: float, r: float, sigma: float,
                            spot_range: Tuple[float, float] = None) -> go.Figure:
        """
        Create comprehensive Greeks dashboard.
        
        Args:
            S (float): Current spot price
            K (float): Strike price
            T (float): Time to expiration
            r (float): Risk-free rate
            sigma (float): Volatility
            spot_range (Tuple): Range of spot prices for analysis
            
        Returns:
            plotly.graph_objects.Figure: Greeks dashboard
        """
        if spot_range is None:
            spot_range = (S * 0.7, S * 1.3)
        
        spot_prices = np.linspace(spot_range[0], spot_range[1], 100)
        
        # Calculate Greeks for each spot price
        call_deltas, put_deltas = [], []
        gammas, call_vegas, put_vegas = [], [], []
        call_thetas, put_thetas = [], []
        call_rhos, put_rhos = [], []
        
        for spot in spot_prices:
            bs_model = BlackScholesModel(spot, K, T, r, sigma)
            call_deltas.append(bs_model.delta('call'))
            put_deltas.append(bs_model.delta('put'))
            gammas.append(bs_model.gamma())
            call_vegas.append(bs_model.vega())
            put_vegas.append(bs_model.vega())  # Same for calls and puts
            call_thetas.append(bs_model.theta('call'))
            put_thetas.append(bs_model.theta('put'))
            call_rhos.append(bs_model.rho('call'))
            put_rhos.append(bs_model.rho('put'))
        
        # Create subplots - one per row
        fig = make_subplots(
            rows=5, cols=1,
            subplot_titles=('Delta', 'Gamma', 'Theta', 'Vega', 'Rho'),
            vertical_spacing=0.08
        )
        
        # Delta plot (row 1)
        fig.add_trace(go.Scatter(x=spot_prices, y=call_deltas, name='Call Delta', 
                               line=dict(color='#4ade80', width=3),
                               hovertemplate='<b>Spot</b>: $%{x:.2f}<br><b>Call Delta</b>: %{y:.4f}<extra></extra>'), row=1, col=1)
        fig.add_trace(go.Scatter(x=spot_prices, y=put_deltas, name='Put Delta', 
                               line=dict(color='#f87171', width=3),
                               hovertemplate='<b>Spot</b>: $%{x:.2f}<br><b>Put Delta</b>: %{y:.4f}<extra></extra>'), row=1, col=1)
        
        # Gamma plot (row 2)
        fig.add_trace(go.Scatter(x=spot_prices, y=gammas, name='Gamma', 
                               line=dict(color='#667eea', width=3),
                               hovertemplate='<b>Spot</b>: $%{x:.2f}<br><b>Gamma</b>: %{y:.4f}<extra></extra>'), row=2, col=1)
        
        # Theta plot (row 3)
        fig.add_trace(go.Scatter(x=spot_prices, y=call_thetas, name='Call Theta', 
                               line=dict(color='#4ade80', width=3),
                               hovertemplate='<b>Spot</b>: $%{x:.2f}<br><b>Call Theta</b>: %{y:.4f}<extra></extra>'), row=3, col=1)
        fig.add_trace(go.Scatter(x=spot_prices, y=put_thetas, name='Put Theta', 
                               line=dict(color='#f87171', width=3),
                               hovertemplate='<b>Spot</b>: $%{x:.2f}<br><b>Put Theta</b>: %{y:.4f}<extra></extra>'), row=3, col=1)
        
        # Vega plot (row 4)
        fig.add_trace(go.Scatter(x=spot_prices, y=call_vegas, name='Vega', 
                               line=dict(color='#f093fb', width=3),
                               hovertemplate='<b>Spot</b>: $%{x:.2f}<br><b>Vega</b>: %{y:.4f}<extra></extra>'), row=4, col=1)
        
        # Rho plot (row 5)
        fig.add_trace(go.Scatter(x=spot_prices, y=call_rhos, name='Call Rho', 
                               line=dict(color='#4ade80', width=3),
                               hovertemplate='<b>Spot</b>: $%{x:.2f}<br><b>Call Rho</b>: %{y:.4f}<extra></extra>'), row=5, col=1)
        fig.add_trace(go.Scatter(x=spot_prices, y=put_rhos, name='Put Rho', 
                               line=dict(color='#f87171', width=3),
                               hovertemplate='<b>Spot</b>: $%{x:.2f}<br><b>Put Rho</b>: %{y:.4f}<extra></extra>'), row=5, col=1)
        
        # Current spot price line for each row
        for row in range(1, 6):
            fig.add_vline(x=S, line_dash="dash", line_color="rgba(255,255,255,0.5)", 
                        annotation_text=f"Current: ${S}", row=row, col=1)
        

        
        fig.update_layout(
            height=1200,
            title={
                'text': f'Greeks Analysis Dashboard<br><sub>K=${K:.0f}, T={T:.2f}y, r={r:.1%}, σ={sigma:.1%}</sub>',
                'font': {'color': 'white', 'size': 16},
                'x': 0.5
            },
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(
                bgcolor='rgba(255,255,255,0.1)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1,
                font=dict(color='white')
            )
        )
        
        # Update all subplot backgrounds and axes
        fig.update_xaxes(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)',
            tickfont=dict(color='white'),
            title_font=dict(color='white')
        )
        fig.update_yaxes(
            gridcolor='rgba(255,255,255,0.1)',
            zerolinecolor='rgba(255,255,255,0.2)',
            tickfont=dict(color='white'),
            title_font=dict(color='white')
        )
        
        return fig
    
    def plot_volatility_smile(self, S: float, T: float, r: float, 
                            strikes: List[float], market_prices: List[float],
                            option_type: str = 'call') -> go.Figure:
        """
        Plot implied volatility smile.
        
        Args:
            S (float): Current spot price
            T (float): Time to expiration
            r (float): Risk-free rate
            strikes (List[float]): List of strike prices
            market_prices (List[float]): List of market prices
            option_type (str): 'call' or 'put'
            
        Returns:
            plotly.graph_objects.Figure: Volatility smile plot
        """
        from .black_scholes import ImpliedVolatilityCalculator
        
        implied_vols = []
        moneyness = []
        
        for strike, market_price in zip(strikes, market_prices):
            try:
                iv = ImpliedVolatilityCalculator.calculate_implied_volatility(
                    market_price, S, strike, T, r, option_type
                )
                implied_vols.append(iv)
                moneyness.append(strike / S)  # Moneyness ratio
            except:
                implied_vols.append(np.nan)
                moneyness.append(strike / S)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=moneyness,
            y=np.array(implied_vols) * 100,  # Convert to percentage
            mode='markers+lines',
            name='Implied Volatility',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color='#f093fb'),
            hovertemplate='<b>Moneyness</b>: %{x:.3f}<br><b>Implied Vol</b>: %{y:.2f}%<extra></extra>'
        ))
        
        fig.add_vline(x=1.0, line_dash="dash", line_color="rgba(255,255,255,0.5)", 
                     annotation_text="At-the-Money")
        
        fig.update_layout(
            title={
                'text': f'{option_type.capitalize()} Option Implied Volatility Smile<br><sub>S=${S:.0f}, T={T:.2f}y</sub>',
                'font': {'color': 'white', 'size': 16},
                'x': 0.5
            },
            xaxis_title='Moneyness (K/S)',
            yaxis_title='Implied Volatility (%)',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.2)',
                tickfont=dict(color='white'),
                title_font=dict(color='white')
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.2)',
                tickfont=dict(color='white'),
                title_font=dict(color='white')
            ),
            width=800,
            height=500
        )
        
        return fig
    
    def plot_pnl_analysis(self, S: float, K: float, T: float, r: float, sigma: float,
                         option_type: str = 'call', premium_paid: float = None) -> go.Figure:
        """
        Plot P&L analysis for option positions.
        
        Args:
            S (float): Current spot price
            K (float): Strike price
            T (float): Time to expiration
            r (float): Risk-free rate
            sigma (float): Volatility
            option_type (str): 'call' or 'put'
            premium_paid (float): Premium paid for the option
            
        Returns:
            plotly.graph_objects.Figure: P&L analysis plot
        """
        bs_model = BlackScholesModel(S, K, T, r, sigma)
        
        if premium_paid is None:
            if option_type.lower() == 'call':
                premium_paid = bs_model.call_price()
            else:
                premium_paid = bs_model.put_price()
        
        # Range of spot prices at expiration
        spot_range = np.linspace(S * 0.5, S * 1.5, 100)
        
        # Calculate P&L at expiration
        if option_type.lower() == 'call':
            payoffs = np.maximum(spot_range - K, 0)
        else:
            payoffs = np.maximum(K - spot_range, 0)
        
        pnl = payoffs - premium_paid
        
        # Calculate current option values
        current_values = []
        for spot in spot_range:
            current_bs = BlackScholesModel(spot, K, T, r, sigma)
            if option_type.lower() == 'call':
                current_values.append(current_bs.call_price())
            else:
                current_values.append(current_bs.put_price())
        
        current_pnl = np.array(current_values) - premium_paid
        
        fig = go.Figure()
        
        # P&L at expiration
        fig.add_trace(go.Scatter(
            x=spot_range,
            y=pnl,
            mode='lines',
            name='P&L at Expiration',
            line=dict(color='#667eea', width=3),
            hovertemplate='<b>Spot Price</b>: $%{x:.2f}<br><b>P&L</b>: $%{y:.2f}<extra></extra>'
        ))
        
        # Current P&L
        fig.add_trace(go.Scatter(
            x=spot_range,
            y=current_pnl,
            mode='lines',
            name='Current P&L',
            line=dict(color='#f093fb', width=3, dash='dash'),
            hovertemplate='<b>Spot Price</b>: $%{x:.2f}<br><b>Current P&L</b>: $%{y:.2f}<extra></extra>'
        ))
        
        # Break-even line
        fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.5)", 
                     annotation_text="Break-even")
        
        # Current spot price
        fig.add_vline(x=S, line_dash="dash", line_color="#4ade80", 
                     annotation_text=f"Current Spot: ${S}")
        
        # Strike price
        fig.add_vline(x=K, line_dash="dash", line_color="#fbbf24", 
                     annotation_text=f"Strike: ${K}")
        
        fig.update_layout(
            title={
                'text': f'{option_type.capitalize()} Option P&L Analysis<br><sub>Premium Paid: ${premium_paid:.2f}</sub>',
                'font': {'color': 'white', 'size': 16},
                'x': 0.5
            },
            xaxis_title='Spot Price at Expiration ($)',
            yaxis_title='Profit/Loss ($)',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.2)',
                tickfont=dict(color='white'),
                title_font=dict(color='white')
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.2)',
                tickfont=dict(color='white'),
                title_font=dict(color='white')
            ),
            legend=dict(
                bgcolor='rgba(255,255,255,0.1)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1,
                font=dict(color='white')
            ),
            width=800,
            height=500
        )
        
        return fig
    
    def create_risk_report(self, S: float, K: float, T: float, r: float, sigma: float) -> Dict:
        """
        Generate comprehensive risk report with multiple visualizations.
        
        Args:
            S (float): Current spot price
            K (float): Strike price
            T (float): Time to expiration
            r (float): Risk-free rate
            sigma (float): Volatility
            
        Returns:
            Dict: Dictionary containing all visualization figures
        """
        report = {}
        
        # Price surfaces
        report['call_surface'] = self.plot_option_price_surface(K, T, r, sigma, option_type='call')
        report['put_surface'] = self.plot_option_price_surface(K, T, r, sigma, option_type='put')
        
        # Greeks dashboard
        report['greeks_dashboard'] = self.plot_greeks_dashboard(S, K, T, r, sigma)
        
        # P&L analysis
        report['call_pnl'] = self.plot_pnl_analysis(S, K, T, r, sigma, option_type='call')
        report['put_pnl'] = self.plot_pnl_analysis(S, K, T, r, sigma, option_type='put')
        
        return report


def sensitivity_analysis(base_params: Dict, param_ranges: Dict, option_type: str = 'call') -> pd.DataFrame:
    """
    Perform sensitivity analysis on option pricing parameters.
    
    Args:
        base_params (Dict): Base parameters {S, K, T, r, sigma}
        param_ranges (Dict): Ranges for each parameter
        option_type (str): 'call' or 'put'
        
    Returns:
        pd.DataFrame: Sensitivity analysis results
    """
    results = []
    
    for param, values in param_ranges.items():
        for value in values:
            params = base_params.copy()
            params[param] = value
            
            bs_model = BlackScholesModel(**params)
            
            if option_type.lower() == 'call':
                price = bs_model.call_price()
            else:
                price = bs_model.put_price()
            
            greeks = bs_model.get_all_greeks(option_type)
            
            result = {
                'parameter': param,
                'value': value,
                'price': price,
                **greeks
            }
            results.append(result)
    
    return pd.DataFrame(results)


if __name__ == "__main__":
    # Example usage
    print("Option Visualization Demo")
    print("=" * 30)
    
    # Initialize visualizer
    viz = OptionVisualization()
    
    # Example parameters
    S, K, T, r, sigma = 100, 105, 0.25, 0.05, 0.2
    
    # Create visualizations
    print("Creating price surface...")
    call_surface = viz.plot_option_price_surface(K, T, r, sigma, option_type='call')
    
    print("Creating Greeks dashboard...")
    greeks_dash = viz.plot_greeks_dashboard(S, K, T, r, sigma)
    
    print("Creating P&L analysis...")
    pnl_analysis = viz.plot_pnl_analysis(S, K, T, r, sigma, option_type='call')
    
    print("Visualizations created successfully!")
    print("Use .show() method to display the plots in a Jupyter notebook or web browser.")
