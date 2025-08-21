"""
Unit tests for Black-Scholes option pricing model.

This module contains comprehensive tests for the Black-Scholes implementation,
including pricing accuracy, Greeks calculation, and edge cases.

Author: Bowen
Date: 2024
Purpose: Risk Analyst Portfolio Project
"""

import unittest
import numpy as np
from src.black_scholes import BlackScholesModel, ImpliedVolatilityCalculator, monte_carlo_option_pricing


class TestBlackScholesModel(unittest.TestCase):
    """Test cases for Black-Scholes model implementation."""
    
    def setUp(self):
        """Set up test parameters."""
        self.S = 100  # Spot price
        self.K = 100  # Strike price
        self.T = 0.25  # Time to expiration (3 months)
        self.r = 0.05  # Risk-free rate
        self.sigma = 0.2  # Volatility
        
        self.bs_model = BlackScholesModel(self.S, self.K, self.T, self.r, self.sigma)
    
    def test_initialization(self):
        """Test model initialization."""
        self.assertEqual(self.bs_model.S, self.S)
        self.assertEqual(self.bs_model.K, self.K)
        self.assertEqual(self.bs_model.T, self.T)
        self.assertEqual(self.bs_model.r, self.r)
        self.assertEqual(self.bs_model.sigma, self.sigma)
    
    def test_d1_d2_calculation(self):
        """Test d1 and d2 parameter calculations."""
        # For ATM option with given parameters
        expected_d1 = (np.log(self.S/self.K) + (self.r + 0.5*self.sigma**2)*self.T) / (self.sigma*np.sqrt(self.T))
        expected_d2 = expected_d1 - self.sigma*np.sqrt(self.T)
        
        self.assertAlmostEqual(self.bs_model.d1, expected_d1, places=6)
        self.assertAlmostEqual(self.bs_model.d2, expected_d2, places=6)
    
    def test_call_option_pricing(self):
        """Test call option price calculation."""
        call_price = self.bs_model.call_price()
        
        # Call price should be positive
        self.assertGreater(call_price, 0)
        
        # For ATM option, call price should be reasonable
        self.assertGreater(call_price, 2)
        self.assertLess(call_price, 10)
    
    def test_put_option_pricing(self):
        """Test put option price calculation."""
        put_price = self.bs_model.put_price()
        
        # Put price should be positive
        self.assertGreater(put_price, 0)
        
        # For ATM option, put price should be reasonable
        self.assertGreater(put_price, 2)
        self.assertLess(put_price, 10)
    
    def test_put_call_parity(self):
        """Test put-call parity relationship."""
        call_price = self.bs_model.call_price()
        put_price = self.bs_model.put_price()
        
        # Put-call parity: C - P = S - K*e^(-r*T)
        parity_left = call_price - put_price
        parity_right = self.S - self.K * np.exp(-self.r * self.T)
        
        self.assertAlmostEqual(parity_left, parity_right, places=6)
    
    def test_delta_calculation(self):
        """Test delta calculation."""
        call_delta = self.bs_model.delta('call')
        put_delta = self.bs_model.delta('put')
        
        # Call delta should be between 0 and 1
        self.assertGreaterEqual(call_delta, 0)
        self.assertLessEqual(call_delta, 1)
        
        # Put delta should be between -1 and 0
        self.assertGreaterEqual(put_delta, -1)
        self.assertLessEqual(put_delta, 0)
        
        # Delta relationship: call_delta - put_delta = 1
        self.assertAlmostEqual(call_delta - put_delta, 1, places=6)
    
    def test_gamma_calculation(self):
        """Test gamma calculation."""
        gamma = self.bs_model.gamma()
        
        # Gamma should be positive
        self.assertGreater(gamma, 0)
        
        # For ATM option, gamma should be at maximum
        # Test with ITM and OTM options
        itm_model = BlackScholesModel(110, self.K, self.T, self.r, self.sigma)
        otm_model = BlackScholesModel(90, self.K, self.T, self.r, self.sigma)
        
        itm_gamma = itm_model.gamma()
        otm_gamma = otm_model.gamma()
        
        # ATM gamma should be higher than ITM and OTM
        self.assertGreater(gamma, itm_gamma)
        self.assertGreater(gamma, otm_gamma)
    
    def test_theta_calculation(self):
        """Test theta calculation."""
        call_theta = self.bs_model.theta('call')
        put_theta = self.bs_model.theta('put')
        
        # Theta should typically be negative (time decay)
        self.assertLess(call_theta, 0)
        
        # Theta values should be reasonable
        self.assertGreater(call_theta, -1)  # Not too negative
        self.assertGreater(put_theta, -1)
    
    def test_vega_calculation(self):
        """Test vega calculation."""
        vega = self.bs_model.vega()
        
        # Vega should be positive
        self.assertGreater(vega, 0)
        
        # Vega should be reasonable for given parameters
        self.assertLess(vega, 50)  # Reasonable upper bound
    
    def test_rho_calculation(self):
        """Test rho calculation."""
        call_rho = self.bs_model.rho('call')
        put_rho = self.bs_model.rho('put')
        
        # Call rho should be positive, put rho negative
        self.assertGreater(call_rho, 0)
        self.assertLess(put_rho, 0)
    
    def test_greeks_consistency(self):
        """Test Greeks consistency across option types."""
        call_greeks = self.bs_model.get_all_greeks('call')
        put_greeks = self.bs_model.get_all_greeks('put')
        
        # Gamma and Vega should be same for calls and puts
        self.assertAlmostEqual(call_greeks['gamma'], put_greeks['gamma'], places=6)
        self.assertAlmostEqual(call_greeks['vega'], put_greeks['vega'], places=6)
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Very short time to expiry
        short_model = BlackScholesModel(self.S, self.K, 0.001, self.r, self.sigma)
        short_call = short_model.call_price()
        short_put = short_model.put_price()
        
        # Prices should approach intrinsic value
        intrinsic_call = max(self.S - self.K, 0)
        intrinsic_put = max(self.K - self.S, 0)
        
        self.assertGreater(short_call, intrinsic_call * 0.9)  # Close to intrinsic
        self.assertGreater(short_put, intrinsic_put * 0.9)
        
        # Very low volatility
        low_vol_model = BlackScholesModel(self.S, self.K, self.T, self.r, 0.01)
        low_vol_call = low_vol_model.call_price()
        
        # Should be close to intrinsic value
        self.assertGreater(low_vol_call, 0)
        self.assertLess(low_vol_call, intrinsic_call + 2)  # Small time value
    
    def test_moneyness_effects(self):
        """Test option pricing across different moneyness levels."""
        strikes = [80, 90, 100, 110, 120]
        call_prices = []
        put_prices = []
        
        for K in strikes:
            model = BlackScholesModel(self.S, K, self.T, self.r, self.sigma)
            call_prices.append(model.call_price())
            put_prices.append(model.put_price())
        
        # Call prices should decrease with increasing strike
        for i in range(len(call_prices) - 1):
            self.assertGreater(call_prices[i], call_prices[i + 1])
        
        # Put prices should increase with increasing strike
        for i in range(len(put_prices) - 1):
            self.assertLess(put_prices[i], put_prices[i + 1])


class TestImpliedVolatilityCalculator(unittest.TestCase):
    """Test cases for implied volatility calculation."""
    
    def setUp(self):
        """Set up test parameters."""
        self.S = 100
        self.K = 100
        self.T = 0.25
        self.r = 0.05
        self.true_sigma = 0.2
        
        # Calculate theoretical price
        bs_model = BlackScholesModel(self.S, self.K, self.T, self.r, self.true_sigma)
        self.market_price = bs_model.call_price()
    
    def test_implied_volatility_calculation(self):
        """Test implied volatility calculation accuracy."""
        calculated_iv = ImpliedVolatilityCalculator.calculate_implied_volatility(
            self.market_price, self.S, self.K, self.T, self.r, 'call'
        )
        
        # Should recover the true volatility
        self.assertAlmostEqual(calculated_iv, self.true_sigma, places=4)
    
    def test_implied_volatility_put(self):
        """Test implied volatility for put options."""
        bs_model = BlackScholesModel(self.S, self.K, self.T, self.r, self.true_sigma)
        put_price = bs_model.put_price()
        
        calculated_iv = ImpliedVolatilityCalculator.calculate_implied_volatility(
            put_price, self.S, self.K, self.T, self.r, 'put'
        )
        
        # Should recover the true volatility
        self.assertAlmostEqual(calculated_iv, self.true_sigma, places=4)
    
    def test_implied_volatility_convergence(self):
        """Test convergence for different market prices."""
        test_sigmas = [0.1, 0.15, 0.25, 0.3, 0.4]
        
        for true_sigma in test_sigmas:
            bs_model = BlackScholesModel(self.S, self.K, self.T, self.r, true_sigma)
            market_price = bs_model.call_price()
            
            calculated_iv = ImpliedVolatilityCalculator.calculate_implied_volatility(
                market_price, self.S, self.K, self.T, self.r, 'call'
            )
            
            self.assertAlmostEqual(calculated_iv, true_sigma, places=3)


class TestMonteCarloValidation(unittest.TestCase):
    """Test cases for Monte Carlo option pricing validation."""
    
    def setUp(self):
        """Set up test parameters."""
        self.S = 100
        self.K = 100
        self.T = 0.25
        self.r = 0.05
        self.sigma = 0.2
        
        self.bs_model = BlackScholesModel(self.S, self.K, self.T, self.r, self.sigma)
    
    def test_monte_carlo_call_pricing(self):
        """Test Monte Carlo call option pricing."""
        mc_result = monte_carlo_option_pricing(
            self.S, self.K, self.T, self.r, self.sigma, 'call', 100000
        )
        
        bs_price = self.bs_model.call_price()
        mc_price = mc_result['monte_carlo_price']
        
        # Monte Carlo should be close to Black-Scholes (within 2 standard errors)
        error_bound = 2 * mc_result['standard_error'] * np.exp(-self.r * self.T)
        self.assertAlmostEqual(mc_price, bs_price, delta=error_bound)
    
    def test_monte_carlo_put_pricing(self):
        """Test Monte Carlo put option pricing."""
        mc_result = monte_carlo_option_pricing(
            self.S, self.K, self.T, self.r, self.sigma, 'put', 100000
        )
        
        bs_price = self.bs_model.put_price()
        mc_price = mc_result['monte_carlo_price']
        
        # Monte Carlo should be close to Black-Scholes
        error_bound = 2 * mc_result['standard_error'] * np.exp(-self.r * self.T)
        self.assertAlmostEqual(mc_price, bs_price, delta=error_bound)
    
    def test_monte_carlo_confidence_intervals(self):
        """Test Monte Carlo confidence interval calculation."""
        mc_result = monte_carlo_option_pricing(
            self.S, self.K, self.T, self.r, self.sigma, 'call', 50000
        )
        
        # Confidence interval should be reasonable
        self.assertGreater(mc_result['confidence_interval_95'], 0)
        self.assertLess(mc_result['confidence_interval_95'], mc_result['monte_carlo_price'])
        
        # Bounds should be properly calculated
        expected_lower = mc_result['monte_carlo_price'] - mc_result['confidence_interval_95']
        expected_upper = mc_result['monte_carlo_price'] + mc_result['confidence_interval_95']
        
        self.assertAlmostEqual(mc_result['lower_bound'], expected_lower, places=6)
        self.assertAlmostEqual(mc_result['upper_bound'], expected_upper, places=6)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
