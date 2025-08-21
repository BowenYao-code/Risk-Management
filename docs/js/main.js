/**
 * Main JavaScript for Risk Management Platform
 * Author: Bowen Yao
 */

// Global variables for current calculations
let currentModel = null;
let chartData = {};

// Calculate option prices and Greeks
function calculateOption() {
    // Get input values
    const S = parseFloat(document.getElementById('spotPrice').value);
    const K = parseFloat(document.getElementById('strikePrice').value);
    const T = parseFloat(document.getElementById('timeToExpiry').value);
    const r = parseFloat(document.getElementById('riskFreeRate').value) / 100;
    const sigma = parseFloat(document.getElementById('volatility').value) / 100;

    // Validate inputs
    if (isNaN(S) || isNaN(K) || isNaN(T) || isNaN(r) || isNaN(sigma)) {
        alert('Please enter valid numerical values for all parameters.');
        return;
    }

    // Create Black-Scholes model
    currentModel = new BlackScholesModel(S, K, T, r, sigma);

    // Calculate prices
    const callPrice = currentModel.callPrice();
    const putPrice = currentModel.putPrice();

    // Calculate Greeks
    const callGreeks = currentModel.getAllGreeks('call');
    const putGreeks = currentModel.getAllGreeks('put');

    // Monte Carlo validation
    const mcResults = monteCarloSimulation(S, K, T, r, sigma, 10000);

    // Check put-call parity
    const parity = currentModel.putCallParity();

    // Determine moneyness
    const moneyness = currentModel.moneyness();

    // Display results
    displayPricingResults(callPrice, putPrice, mcResults, parity, moneyness);
    displayGreeks(callGreeks, putGreeks);
    updateGreeksChart(S, K, T, r, sigma);
    updatePnLChart(S, K, T, r, sigma, callPrice, putPrice);
    updateVolatilitySurface(K, T, r);
}

// Display pricing results
function displayPricingResults(callPrice, putPrice, mcResults, parity, moneyness) {
    const resultsHTML = `
        <div class="row">
            <div class="col-md-6">
                <h5>Black-Scholes Prices</h5>
                <div class="result-item">
                    <span>Call Option:</span>
                    <span class="result-value">$${callPrice.toFixed(4)}</span>
                </div>
                <div class="result-item">
                    <span>Put Option:</span>
                    <span class="result-value">$${putPrice.toFixed(4)}</span>
                </div>
            </div>
            <div class="col-md-6">
                <h5>Monte Carlo Validation</h5>
                <div class="result-item">
                    <span>Call (MC):</span>
                    <span class="result-value">$${mcResults.callPrice.toFixed(4)}</span>
                </div>
                <div class="result-item">
                    <span>Put (MC):</span>
                    <span class="result-value">$${mcResults.putPrice.toFixed(4)}</span>
                </div>
            </div>
        </div>
        <div class="row mt-3">
            <div class="col-12">
                <div class="alert ${parity.holds ? 'alert-success' : 'alert-warning'}">
                    <i class="fas ${parity.holds ? 'fa-check-circle' : 'fa-exclamation-triangle'}"></i>
                    Put-Call Parity: ${parity.holds ? 'Holds' : 'Violation detected'} 
                    (Difference: $${parity.difference.toFixed(6)})
                </div>
                <div class="badge bg-primary">Moneyness: ${moneyness}</div>
            </div>
        </div>
    `;
    
    document.getElementById('pricingResults').innerHTML = resultsHTML;
}

// Display Greeks values
function displayGreeks(callGreeks, putGreeks) {
    document.getElementById('deltaValue').textContent = callGreeks.delta.toFixed(4);
    document.getElementById('gammaValue').textContent = callGreeks.gamma.toFixed(4);
    document.getElementById('thetaValue').textContent = callGreeks.theta.toFixed(4);
    document.getElementById('vegaValue').textContent = callGreeks.vega.toFixed(4);
    document.getElementById('rhoValue').textContent = callGreeks.rho.toFixed(4);
}

// Update Greeks chart
function updateGreeksChart(S, K, T, r, sigma) {
    const spotRange = [];
    const deltas = [];
    const gammas = [];
    
    for (let spot = S * 0.5; spot <= S * 1.5; spot += S * 0.01) {
        spotRange.push(spot);
        const model = new BlackScholesModel(spot, K, T, r, sigma);
        deltas.push(model.delta('call'));
        gammas.push(model.gamma());
    }

    const trace1 = {
        x: spotRange,
        y: deltas,
        type: 'scatter',
        name: 'Delta',
        line: { color: '#64c8ff', width: 3 }
    };

    const trace2 = {
        x: spotRange,
        y: gammas,
        type: 'scatter',
        name: 'Gamma',
        yaxis: 'y2',
        line: { color: '#00ff88', width: 3 }
    };

    const layout = {
        title: 'Greeks vs Spot Price',
        xaxis: { 
            title: 'Spot Price ($)',
            gridcolor: 'rgba(255,255,255,0.1)'
        },
        yaxis: { 
            title: 'Delta',
            titlefont: { color: '#64c8ff' },
            tickfont: { color: '#64c8ff' },
            gridcolor: 'rgba(255,255,255,0.1)'
        },
        yaxis2: {
            title: 'Gamma',
            titlefont: { color: '#00ff88' },
            tickfont: { color: '#00ff88' },
            overlaying: 'y',
            side: 'right'
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: 'white' },
        shapes: [{
            type: 'line',
            x0: S, x1: S,
            y0: 0, y1: 1,
            line: {
                color: 'rgba(255,255,255,0.3)',
                width: 2,
                dash: 'dash'
            }
        }]
    };

    Plotly.newPlot('greeksChart', [trace1, trace2], layout);
}

// Update P&L chart
function updatePnLChart(S, K, T, r, sigma, callPremium, putPremium) {
    const spotRange = [];
    const callPnL = [];
    const putPnL = [];
    
    for (let spot = S * 0.5; spot <= S * 1.5; spot += S * 0.01) {
        spotRange.push(spot);
        // P&L at expiration
        callPnL.push(Math.max(spot - K, 0) - callPremium);
        putPnL.push(Math.max(K - spot, 0) - putPremium);
    }

    const trace1 = {
        x: spotRange,
        y: callPnL,
        type: 'scatter',
        name: 'Call P&L',
        line: { color: '#64c8ff', width: 3 }
    };

    const trace2 = {
        x: spotRange,
        y: putPnL,
        type: 'scatter',
        name: 'Put P&L',
        line: { color: '#ff6b6b', width: 3 }
    };

    const layout = {
        title: 'Profit/Loss at Expiration',
        xaxis: { 
            title: 'Spot Price at Expiration ($)',
            gridcolor: 'rgba(255,255,255,0.1)'
        },
        yaxis: { 
            title: 'Profit/Loss ($)',
            gridcolor: 'rgba(255,255,255,0.1)',
            zerolinecolor: 'rgba(255,255,255,0.3)',
            zerolinewidth: 2
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: 'white' },
        shapes: [
            {
                type: 'line',
                x0: S, x1: S,
                y0: Math.min(...callPnL, ...putPnL),
                y1: Math.max(...callPnL, ...putPnL),
                line: {
                    color: 'rgba(255,255,255,0.3)',
                    width: 2,
                    dash: 'dash'
                }
            },
            {
                type: 'line',
                x0: K, x1: K,
                y0: Math.min(...callPnL, ...putPnL),
                y1: Math.max(...callPnL, ...putPnL),
                line: {
                    color: 'rgba(255,107,107,0.3)',
                    width: 2,
                    dash: 'dash'
                }
            }
        ]
    };

    Plotly.newPlot('pnlChart', [trace1, trace2], layout);
}

// Update Volatility Surface (simplified 2D version for demo)
function updateVolatilitySurface(K, T, r) {
    const strikes = [];
    const volatilities = [];
    
    // Generate sample implied volatility smile
    for (let strike = K * 0.8; strike <= K * 1.2; strike += K * 0.01) {
        strikes.push(strike);
        // Simple volatility smile model
        const moneyness = strike / K;
        const vol = 0.2 + 0.1 * Math.pow(moneyness - 1, 2);
        volatilities.push(vol * 100);
    }

    const trace = {
        x: strikes,
        y: volatilities,
        type: 'scatter',
        name: 'Implied Volatility',
        mode: 'lines',
        line: { 
            color: '#667eea', 
            width: 3,
            shape: 'spline'
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(102, 126, 234, 0.1)'
    };

    const layout = {
        title: 'Implied Volatility Smile',
        xaxis: { 
            title: 'Strike Price ($)',
            gridcolor: 'rgba(255,255,255,0.1)'
        },
        yaxis: { 
            title: 'Implied Volatility (%)',
            gridcolor: 'rgba(255,255,255,0.1)'
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { color: 'white' },
        shapes: [{
            type: 'line',
            x0: K, x1: K,
            y0: Math.min(...volatilities),
            y1: Math.max(...volatilities),
            line: {
                color: 'rgba(255,255,255,0.3)',
                width: 2,
                dash: 'dash'
            }
        }]
    };

    Plotly.newPlot('volSurfaceChart', [trace], layout);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Set default values and calculate
    if (document.getElementById('spotPrice')) {
        calculateOption();
    }
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add input event listeners for real-time updates
    const inputs = ['spotPrice', 'strikePrice', 'timeToExpiry', 'riskFreeRate', 'volatility'];
    inputs.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', function() {
                // Debounce calculations
                clearTimeout(window.calculateTimeout);
                window.calculateTimeout = setTimeout(calculateOption, 300);
            });
        }
    });
});

// Style helper for result items
const style = document.createElement('style');
style.textContent = `
    .result-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .result-value {
        font-weight: 700;
        color: #64c8ff;
    }
    .alert {
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .alert-success {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
        color: #00ff88;
    }
    .alert-warning {
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid rgba(255, 107, 107, 0.3);
        color: #ff6b6b;
    }
`;
document.head.appendChild(style);
