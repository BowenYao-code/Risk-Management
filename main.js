/**
 * Black-Scholes Option Pricing - Main JavaScript
 * 
 * This file contains utility functions and common functionality
 * used across the web application.
 * 
 * Author: Bowen
 * Date: 2024
 */

// Global configuration
const CONFIG = {
    API_BASE_URL: '',
    DEFAULT_PRECISION: 6,
    CHART_COLORS: {
        primary: '#007bff',
        secondary: '#6c757d',
        success: '#28a745',
        info: '#17a2b8',
        warning: '#ffc107',
        danger: '#dc3545'
    }
};

// Utility Functions
const Utils = {
    /**
     * Format number for display
     */
    formatNumber: function(num, precision = CONFIG.DEFAULT_PRECISION) {
        if (typeof num !== 'number' || isNaN(num)) {
            return 'N/A';
        }
        return num.toFixed(precision);
    },

    /**
     * Format currency
     */
    formatCurrency: function(num, precision = 2) {
        if (typeof num !== 'number' || isNaN(num)) {
            return '$N/A';
        }
        return '$' + num.toFixed(precision);
    },

    /**
     * Format percentage
     */
    formatPercentage: function(num, precision = 2) {
        if (typeof num !== 'number' || isNaN(num)) {
            return 'N/A%';
        }
        return (num * 100).toFixed(precision) + '%';
    },

    /**
     * Validate input parameters
     */
    validateParameters: function(params) {
        const errors = [];
        
        if (!params.spot_price || params.spot_price <= 0) {
            errors.push('Spot price must be positive');
        }
        
        if (!params.strike_price || params.strike_price <= 0) {
            errors.push('Strike price must be positive');
        }
        
        if (!params.time_to_expiry || params.time_to_expiry <= 0) {
            errors.push('Time to expiry must be positive');
        }
        
        if (params.risk_free_rate < 0 || params.risk_free_rate > 1) {
            errors.push('Risk-free rate must be between 0 and 100%');
        }
        
        if (!params.volatility || params.volatility <= 0) {
            errors.push('Volatility must be positive');
        }
        
        return errors;
    },

    /**
     * Show loading state
     */
    showLoading: function(elementId, message = 'Loading...') {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="text-center py-4">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-2">${message}</p>
                </div>
            `;
        }
    },

    /**
     * Show error message
     */
    showError: function(elementId, message) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    ${message}
                </div>
            `;
        }
    },

    /**
     * Show success message
     */
    showSuccess: function(elementId, message) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="alert alert-success" role="alert">
                    <i class="fas fa-check-circle me-2"></i>
                    ${message}
                </div>
            `;
        }
    },

    /**
     * Debounce function
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Get moneyness description
     */
    getMoneynessDescription: function(moneyness) {
        if (moneyness < 0.95) {
            return { text: 'Out-of-the-Money', class: 'text-danger' };
        } else if (moneyness > 1.05) {
            return { text: 'In-the-Money', class: 'text-success' };
        } else {
            return { text: 'At-the-Money', class: 'text-warning' };
        }
    },

    /**
     * Calculate time to expiry in different units
     */
    getTimeToExpiryBreakdown: function(years) {
        const days = Math.round(years * 365);
        const months = Math.round(years * 12);
        const weeks = Math.round(years * 52);
        
        return {
            years: years,
            months: months,
            weeks: weeks,
            days: days
        };
    }
};

// API Helper Functions
const API = {
    /**
     * Make API request
     */
    request: async function(endpoint, data = null, method = 'GET') {
        const url = CONFIG.API_BASE_URL + endpoint;
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, options);
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'API request failed');
            }
            
            return result;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    /**
     * Calculate option prices
     */
    calculateOption: function(params) {
        return this.request('/api/calculate-option', params, 'POST');
    },

    /**
     * Calculate implied volatility
     */
    calculateImpliedVolatility: function(params) {
        return this.request('/api/implied-volatility', params, 'POST');
    },

    /**
     * Generate Greeks chart
     */
    generateGreeksChart: function(params) {
        return this.request('/api/greeks-chart', params, 'POST');
    },

    /**
     * Generate price surface
     */
    generatePriceSurface: function(params) {
        return this.request('/api/price-surface', params, 'POST');
    },

    /**
     * Generate P&L analysis
     */
    generatePnLAnalysis: function(params) {
        return this.request('/api/pnl-analysis', params, 'POST');
    },

    /**
     * Perform sensitivity analysis
     */
    sensitivityAnalysis: function(params) {
        return this.request('/api/sensitivity-analysis', params, 'POST');
    }
};

// Chart Helper Functions
const ChartUtils = {
    /**
     * Default Plotly configuration
     */
    getDefaultConfig: function() {
        return {
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
            responsive: true
        };
    },

    /**
     * Default layout settings
     */
    getDefaultLayout: function() {
        return {
            font: {
                family: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
                size: 12
            },
            margin: {
                l: 60,
                r: 30,
                t: 80,
                b: 60
            },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            showlegend: true
        };
    },

    /**
     * Render Plotly chart
     */
    renderChart: function(elementId, chartData, config = null) {
        const element = document.getElementById(elementId);
        if (!element) {
            console.error('Chart element not found:', elementId);
            return;
        }

        const plotConfig = config || this.getDefaultConfig();
        
        try {
            if (typeof chartData === 'string') {
                chartData = JSON.parse(chartData);
            }
            
            Plotly.newPlot(elementId, chartData.data, chartData.layout, plotConfig);
        } catch (error) {
            console.error('Error rendering chart:', error);
            Utils.showError(elementId, 'Error rendering chart: ' + error.message);
        }
    }
};

// Form Helper Functions
const FormUtils = {
    /**
     * Get form data as object
     */
    getFormData: function(formId) {
        const form = document.getElementById(formId);
        if (!form) {
            console.error('Form not found:', formId);
            return null;
        }
        
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    },

    /**
     * Set form values
     */
    setFormValues: function(formId, values) {
        const form = document.getElementById(formId);
        if (!form) {
            console.error('Form not found:', formId);
            return;
        }
        
        for (let [key, value] of Object.entries(values)) {
            const element = form.querySelector(`[name="${key}"]`);
            if (element) {
                element.value = value;
            }
        }
    },

    /**
     * Reset form to default values
     */
    resetForm: function(formId, defaults = {}) {
        const form = document.getElementById(formId);
        if (!form) {
            console.error('Form not found:', formId);
            return;
        }
        
        form.reset();
        
        if (Object.keys(defaults).length > 0) {
            this.setFormValues(formId, defaults);
        }
    }
};

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });

    cards.forEach(card => {
        observer.observe(card);
    });
});

// Error handling
window.addEventListener('error', function(event) {
    console.error('JavaScript Error:', event.error);
});

window.addEventListener('unhandledrejection', function(event) {
    console.error('Unhandled Promise Rejection:', event.reason);
});

// Export to global scope
window.Utils = Utils;
window.API = API;
window.ChartUtils = ChartUtils;
window.FormUtils = FormUtils;
