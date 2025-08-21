/**
 * Black-Scholes Option Pricing Model - JavaScript Implementation
 * Author: Bowen Yao
 * Purpose: Client-side option pricing calculations for GitHub Pages deployment
 */

class BlackScholesModel {
    constructor(S, K, T, r, sigma) {
        this.S = S;         // Current stock price
        this.K = K;         // Strike price
        this.T = T;         // Time to expiration in years
        this.r = r;         // Risk-free rate
        this.sigma = sigma; // Volatility
    }

    // Standard normal cumulative distribution function
    normalCDF(x) {
        const a1 =  0.254829592;
        const a2 = -0.284496736;
        const a3 =  1.421413741;
        const a4 = -1.453152027;
        const a5 =  1.061405429;
        const p  =  0.3275911;

        // Save the sign of x
        const sign = x < 0 ? -1 : 1;
        x = Math.abs(x) / Math.sqrt(2.0);

        // A&S formula 7.1.26
        const t = 1.0 / (1.0 + p * x);
        const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

        return 0.5 * (1.0 + sign * y);
    }

    // Standard normal probability density function
    normalPDF(x) {
        return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI);
    }

    // Calculate d1 and d2
    calculateD1D2() {
        const d1 = (Math.log(this.S / this.K) + (this.r + 0.5 * this.sigma * this.sigma) * this.T) / 
                   (this.sigma * Math.sqrt(this.T));
        const d2 = d1 - this.sigma * Math.sqrt(this.T);
        return { d1, d2 };
    }

    // Calculate call option price
    callPrice() {
        const { d1, d2 } = this.calculateD1D2();
        return this.S * this.normalCDF(d1) - this.K * Math.exp(-this.r * this.T) * this.normalCDF(d2);
    }

    // Calculate put option price
    putPrice() {
        const { d1, d2 } = this.calculateD1D2();
        return this.K * Math.exp(-this.r * this.T) * this.normalCDF(-d2) - this.S * this.normalCDF(-d1);
    }

    // Calculate Delta
    delta(optionType = 'call') {
        const { d1 } = this.calculateD1D2();
        return optionType === 'call' ? this.normalCDF(d1) : -this.normalCDF(-d1);
    }

    // Calculate Gamma
    gamma() {
        const { d1 } = this.calculateD1D2();
        return this.normalPDF(d1) / (this.S * this.sigma * Math.sqrt(this.T));
    }

    // Calculate Theta
    theta(optionType = 'call') {
        const { d1, d2 } = this.calculateD1D2();
        const term1 = -(this.S * this.normalPDF(d1) * this.sigma) / (2 * Math.sqrt(this.T));
        
        if (optionType === 'call') {
            const term2 = -this.r * this.K * Math.exp(-this.r * this.T) * this.normalCDF(d2);
            return (term1 + term2) / 365; // Convert to daily theta
        } else {
            const term2 = this.r * this.K * Math.exp(-this.r * this.T) * this.normalCDF(-d2);
            return (term1 + term2) / 365; // Convert to daily theta
        }
    }

    // Calculate Vega
    vega() {
        const { d1 } = this.calculateD1D2();
        return this.S * this.normalPDF(d1) * Math.sqrt(this.T) / 100; // Divide by 100 for 1% change
    }

    // Calculate Rho
    rho(optionType = 'call') {
        const { d2 } = this.calculateD1D2();
        const value = this.K * this.T * Math.exp(-this.r * this.T);
        
        if (optionType === 'call') {
            return value * this.normalCDF(d2) / 100; // Divide by 100 for 1% change
        } else {
            return -value * this.normalCDF(-d2) / 100; // Divide by 100 for 1% change
        }
    }

    // Get all Greeks
    getAllGreeks(optionType = 'call') {
        return {
            delta: this.delta(optionType),
            gamma: this.gamma(),
            theta: this.theta(optionType),
            vega: this.vega(),
            rho: this.rho(optionType)
        };
    }

    // Check put-call parity
    putCallParity() {
        const callPrice = this.callPrice();
        const putPrice = this.putPrice();
        const parityCall = callPrice - putPrice;
        const parityTheoretical = this.S - this.K * Math.exp(-this.r * this.T);
        return {
            holds: Math.abs(parityCall - parityTheoretical) < 0.0001,
            difference: Math.abs(parityCall - parityTheoretical)
        };
    }

    // Determine moneyness
    moneyness() {
        const ratio = this.S / this.K;
        if (ratio > 1.05) return 'In the Money';
        if (ratio < 0.95) return 'Out of the Money';
        return 'At the Money';
    }
}

// Monte Carlo Simulation for option pricing
function monteCarloSimulation(S, K, T, r, sigma, numSimulations = 10000) {
    let callPayoffSum = 0;
    let putPayoffSum = 0;

    for (let i = 0; i < numSimulations; i++) {
        // Generate random normal variable using Box-Muller transform
        const u1 = Math.random();
        const u2 = Math.random();
        const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        
        // Calculate terminal stock price
        const ST = S * Math.exp((r - 0.5 * sigma * sigma) * T + sigma * Math.sqrt(T) * z);
        
        // Calculate payoffs
        callPayoffSum += Math.max(ST - K, 0);
        putPayoffSum += Math.max(K - ST, 0);
    }

    // Discount average payoffs to present value
    const discountFactor = Math.exp(-r * T);
    const callPrice = (callPayoffSum / numSimulations) * discountFactor;
    const putPrice = (putPayoffSum / numSimulations) * discountFactor;

    return { callPrice, putPrice };
}

// Implied Volatility Calculator using Newton-Raphson method
function calculateImpliedVolatility(marketPrice, S, K, T, r, optionType = 'call', maxIterations = 100) {
    let sigma = 0.3; // Initial guess
    const tolerance = 0.0001;

    for (let i = 0; i < maxIterations; i++) {
        const bs = new BlackScholesModel(S, K, T, r, sigma);
        const price = optionType === 'call' ? bs.callPrice() : bs.putPrice();
        const vega = bs.vega() * 100; // Multiply by 100 because vega is per 1% change

        const diff = price - marketPrice;
        
        if (Math.abs(diff) < tolerance) {
            return sigma;
        }

        // Newton-Raphson update
        sigma = sigma - diff / vega;
        
        // Ensure sigma stays positive
        if (sigma <= 0) {
            sigma = 0.01;
        }
    }

    return sigma; // Return best estimate even if not fully converged
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        BlackScholesModel,
        monteCarloSimulation,
        calculateImpliedVolatility
    };
}
