"""
Black-Scholes Option Pricing Model

This module implements the Black-Scholes model for European option pricing
and calculates the Greeks for risk management purposes.

Author: Bowen
Date: 2024
Purpose: Risk Analyst Portfolio Project
"""

import numpy as np
from scipy.stats import norm
from typing import Dict, Union
import math


class BlackScholesModel:
    """
    Black-Scholes option pricing model implementation.
    
    This class provides methods to calculate option prices and Greeks
    for European call and put options.
    """
    
    def __init__(self, S: float, K: float, T: float, r: float, sigma: float):
        """
        Initialize the Black-Scholes model parameters.
        
        Args:
            S (float): Current stock price
            K (float): Strike price
            T (float): Time to expiration (in years)
            r (float): Risk-free interest rate (annualized)
            sigma (float): Volatility (annualized)
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        
        # Calculate d1 and d2 parameters
        self.d1 = self._calculate_d1()
        self.d2 = self._calculate_d2()
    
    def _calculate_d1(self) -> float:
        """Calculate d1 parameter for Black-Scholes formula."""
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
    
    def _calculate_d2(self) -> float:
        """Calculate d2 parameter for Black-Scholes formula."""
        return self.d1 - self.sigma * np.sqrt(self.T)
    
    def call_price(self) -> float:
        """
        Calculate European call option price using Black-Scholes formula.
        
        Returns:
            float: Call option price
        """
        return (self.S * norm.cdf(self.d1) - 
                self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2))
    
    def put_price(self) -> float:
        """
        Calculate European put option price using Black-Scholes formula.
        
        Returns:
            float: Put option price
        """
        return (self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - 
                self.S * norm.cdf(-self.d1))
    
    def delta(self, option_type: str = 'call') -> float:
        """
        Calculate Delta (price sensitivity to underlying price changes).
        
        Args:
            option_type (str): 'call' or 'put'
            
        Returns:
            float: Delta value
        """
        if option_type.lower() == 'call':
            return norm.cdf(self.d1)
        elif option_type.lower() == 'put':
            return norm.cdf(self.d1) - 1
        else:
            raise ValueError("option_type must be 'call' or 'put'")
    
    def gamma(self) -> float:
        """
        Calculate Gamma (rate of change of Delta).
        
        Returns:
            float: Gamma value (same for calls and puts)
        """
        return norm.pdf(self.d1) / (self.S * self.sigma * np.sqrt(self.T))
    
    def theta(self, option_type: str = 'call') -> float:
        """
        Calculate Theta (time decay).
        
        Args:
            option_type (str): 'call' or 'put'
            
        Returns:
            float: Theta value (per day)
        """
        term1 = -(self.S * norm.pdf(self.d1) * self.sigma) / (2 * np.sqrt(self.T))
        
        if option_type.lower() == 'call':
            term2 = -self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
            return (term1 + term2) / 365  # Convert to daily theta
        elif option_type.lower() == 'put':
            term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
            return (term1 + term2) / 365  # Convert to daily theta
        else:
            raise ValueError("option_type must be 'call' or 'put'")
    
    def vega(self) -> float:
        """
        Calculate Vega (sensitivity to volatility changes).
        
        Returns:
            float: Vega value (same for calls and puts)
        """
        return self.S * norm.pdf(self.d1) * np.sqrt(self.T) / 100  # Per 1% volatility change
    
    def rho(self, option_type: str = 'call') -> float:
        """
        Calculate Rho (sensitivity to interest rate changes).
        
        Args:
            option_type (str): 'call' or 'put'
            
        Returns:
            float: Rho value (per 1% interest rate change)
        """
        if option_type.lower() == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2) / 100
        elif option_type.lower() == 'put':
            return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2) / 100
        else:
            raise ValueError("option_type must be 'call' or 'put'")
    
    def get_all_greeks(self, option_type: str = 'call') -> Dict[str, float]:
        """
        Calculate all Greeks for the option.
        
        Args:
            option_type (str): 'call' or 'put'
            
        Returns:
            Dict[str, float]: Dictionary containing all Greeks
        """
        return {
            'delta': self.delta(option_type),
            'gamma': self.gamma(),
            'theta': self.theta(option_type),
            'vega': self.vega(),
            'rho': self.rho(option_type)
        }
    
    def get_option_summary(self) -> Dict[str, Union[float, Dict[str, float]]]:
        """
        Get comprehensive option pricing summary.
        
        Returns:
            Dict: Complete option analysis including prices and Greeks
        """
        return {
            'parameters': {
                'spot_price': self.S,
                'strike_price': self.K,
                'time_to_expiry': self.T,
                'risk_free_rate': self.r,
                'volatility': self.sigma
            },
            'prices': {
                'call_price': self.call_price(),
                'put_price': self.put_price()
            },
            'call_greeks': self.get_all_greeks('call'),
            'put_greeks': self.get_all_greeks('put')
        }


class ImpliedVolatilityCalculator:
    """
    Calculate implied volatility using Newton-Raphson method.
    """
    
    @staticmethod
    def calculate_implied_volatility(market_price: float, S: float, K: float, 
                                   T: float, r: float, option_type: str = 'call',
                                   max_iterations: int = 100, tolerance: float = 1e-6) -> float:
        """
        Calculate implied volatility using Newton-Raphson method.
        
        Args:
            market_price (float): Market price of the option
            S (float): Current stock price
            K (float): Strike price
            T (float): Time to expiration
            r (float): Risk-free rate
            option_type (str): 'call' or 'put'
            max_iterations (int): Maximum number of iterations
            tolerance (float): Convergence tolerance
            
        Returns:
            float: Implied volatility
        """
        # Initial guess
        sigma = 0.25
        
        for i in range(max_iterations):
            bs_model = BlackScholesModel(S, K, T, r, sigma)
            
            if option_type.lower() == 'call':
                price = bs_model.call_price()
            else:
                price = bs_model.put_price()
            
            vega = bs_model.vega() * 100  # Convert back to per unit change
            
            # Newton-Raphson update
            price_diff = price - market_price
            
            if abs(price_diff) < tolerance:
                return sigma
            
            if vega == 0:
                break
                
            sigma = sigma - price_diff / vega
            
            # Ensure sigma stays positive
            sigma = max(sigma, 0.001)
        
        return sigma


def monte_carlo_option_pricing(S: float, K: float, T: float, r: float, 
                             sigma: float, option_type: str = 'call', 
                             num_simulations: int = 100000) -> Dict[str, float]:
    """
    Price options using Monte Carlo simulation for validation.
    
    Args:
        S (float): Current stock price
        K (float): Strike price
        T (float): Time to expiration
        r (float): Risk-free rate
        sigma (float): Volatility
        option_type (str): 'call' or 'put'
        num_simulations (int): Number of Monte Carlo simulations
        
    Returns:
        Dict[str, float]: Monte Carlo price and confidence interval
    """
    # Generate random price paths
    Z = np.random.standard_normal(num_simulations)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    # Calculate payoffs
    if option_type.lower() == 'call':
        payoffs = np.maximum(ST - K, 0)
    else:
        payoffs = np.maximum(K - ST, 0)
    
    # Discount back to present value
    option_price = np.exp(-r * T) * np.mean(payoffs)
    
    # Calculate confidence interval
    std_error = np.std(payoffs) / np.sqrt(num_simulations)
    confidence_interval = 1.96 * std_error * np.exp(-r * T)
    
    return {
        'monte_carlo_price': option_price,
        'standard_error': std_error,
        'confidence_interval_95': confidence_interval,
        'lower_bound': option_price - confidence_interval,
        'upper_bound': option_price + confidence_interval
    }


if __name__ == "__main__":
    # Example usage
    print("Black-Scholes Option Pricing Model Demo")
    print("=" * 50)
    
    # Example parameters
    S = 100  # Current stock price
    K = 105  # Strike price
    T = 0.25  # 3 months to expiration
    r = 0.05  # 5% risk-free rate
    sigma = 0.2  # 20% volatility
    
    # Create model instance
    bs_model = BlackScholesModel(S, K, T, r, sigma)
    
    # Get complete analysis
    summary = bs_model.get_option_summary()
    
    print(f"Parameters:")
    for key, value in summary['parameters'].items():
        print(f"  {key}: {value}")
    
    print(f"\nOption Prices:")
    print(f"  Call Price: ${summary['prices']['call_price']:.4f}")
    print(f"  Put Price: ${summary['prices']['put_price']:.4f}")
    
    print(f"\nCall Option Greeks:")
    for greek, value in summary['call_greeks'].items():
        print(f"  {greek.capitalize()}: {value:.6f}")
    
    print(f"\nPut Option Greeks:")
    for greek, value in summary['put_greeks'].items():
        print(f"  {greek.capitalize()}: {value:.6f}")
    
    # Monte Carlo validation
    print(f"\nMonte Carlo Validation:")
    mc_call = monte_carlo_option_pricing(S, K, T, r, sigma, 'call')
    mc_put = monte_carlo_option_pricing(S, K, T, r, sigma, 'put')
    
    print(f"  Call - BS: ${summary['prices']['call_price']:.4f}, MC: ${mc_call['monte_carlo_price']:.4f}")
    print(f"  Put - BS: ${summary['prices']['put_price']:.4f}, MC: ${mc_put['monte_carlo_price']:.4f}")
