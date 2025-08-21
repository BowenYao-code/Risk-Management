# Risk Management Platform 📊

A professional Black-Scholes option pricing and risk management web application showcasing quantitative finance expertise.

🌐 **Live Demo**: [https://yourusername.github.io/risk-management-website/](https://yourusername.github.io/risk-management-website/)

## 📁 Project Structure for GitHub Pages

```
risk-management-website/
├── docs/                    # GitHub Pages deployment folder
│   ├── index.html          # Main single-page application
│   ├── css/               
│   │   └── style.css       # Custom styles
│   └── js/
│       ├── black-scholes.js  # Option pricing calculations
│       └── main.js           # Main application logic
├── src/                     # Python source (for Flask version)
│   ├── black_scholes.py
│   └── visualizations.py
├── templates/               # Flask templates (for local version)
├── static/                  # Flask static files (for local version)
├── app.py                   # Flask application (for local/Heroku)
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Deployment Options

### Option 1: GitHub Pages (Static Version) ✅
This is the easiest way to deploy your portfolio project:

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/risk-management-website.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under "Source", select **Deploy from a branch**
   - Choose **main** branch and **/docs** folder
   - Click **Save**
   - Your site will be live at `https://yourusername.github.io/risk-management-website/`

### Option 2: Vercel/Netlify (Flask Version)
For the full Flask application with backend calculations:

**Vercel Deployment**:
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
   ```json
   {
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```
3. Run `vercel` and follow prompts

**Netlify Deployment**:
- Use Netlify Functions for serverless backend
- Or deploy only the static version from `/docs`

### Option 3: Heroku (Flask Version)
1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## 📋 Features

### Core Functionality
- ✅ Black-Scholes Option Pricing
- ✅ Greeks Calculation (Delta, Gamma, Theta, Vega, Rho)
- ✅ Monte Carlo Simulation
- ✅ Implied Volatility Calculator
- ✅ P&L Analysis
- ✅ Put-Call Parity Verification
- ✅ Interactive Charts with Plotly.js

### Technical Stack
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5, Custom CSS with gradients
- **Charts**: Plotly.js for interactive visualizations
- **Backend (Flask version)**: Python, Flask, NumPy, SciPy
- **Deployment**: GitHub Pages / Vercel / Netlify / Heroku

## 🔧 Local Development

### Static Version (GitHub Pages)
Simply open `docs/index.html` in your browser or use a local server:
```bash
# Python 3
python -m http.server 8000 --directory docs

# Node.js
npx http-server docs
```

### Flask Version
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## 📈 Mathematical Models

### Black-Scholes Formula
```
Call = S₀ × N(d₁) - K × e^(-rT) × N(d₂)
Put = K × e^(-rT) × N(-d₂) - S₀ × N(-d₁)

where:
d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)
d₂ = d₁ - σ√T
```

### Greeks
- **Delta (Δ)**: Rate of change in option price with respect to underlying price
- **Gamma (Γ)**: Rate of change in delta with respect to underlying price
- **Theta (Θ)**: Rate of change in option price with respect to time
- **Vega (ν)**: Rate of change in option price with respect to volatility
- **Rho (ρ)**: Rate of change in option price with respect to interest rate

## 🎨 Design Features
- Modern dark theme with gradient accents
- Responsive design for all devices
- Interactive real-time calculations
- Professional financial dashboard layout
- Smooth animations and transitions

## 👤 Author
**Bowen Yao**
- Portfolio Project for Risk Analyst Position
- Demonstrating expertise in quantitative finance and web development

## 📄 License
MIT License - Feel free to use this project as a template for your own portfolio

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## ⭐ Show your support
Give a ⭐️ if this project helped you!

---
*This project is part of my portfolio demonstrating skills in quantitative finance, risk management, and full-stack development.*
