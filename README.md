# Black-Scholes Option Pricing Platform 📈

A professional quantitative finance web application for derivatives pricing and risk management.

🌐 **Live Demo**: [https://bowenyao-code.github.io/Risk-Management/](https://bowenyao-code.github.io/Risk-Management/)

## 🚀 Features

- **Black-Scholes Option Pricing**: Real-time calculation of European call and put options
- **Greeks Analysis**: Complete Greeks (Delta, Gamma, Theta, Vega, Rho) calculation
- **Monte Carlo Simulation**: Advanced path simulation for option pricing
- **Risk Metrics**: VaR, CVaR, stress testing and comprehensive risk analysis
- **Interactive Visualizations**: 3D price surfaces and dynamic charts using Plotly
- **Modern UI/UX**: Responsive design with gradient effects and animations

## 💻 Technology Stack

- **Backend**: Python, Flask, NumPy, SciPy, Pandas
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Visualization**: Plotly.js, Chart.js
- **Deployment**: GitHub Pages (static demo), Flask (full version)

## 📁 Project Structure

```
├── index.html           # Main static demo page for GitHub Pages
├── app.py              # Flask application (full version)
├── black_scholes.py    # Black-Scholes model implementation
├── visualizations.py   # Visualization utilities
├── style.css          # Custom styles
├── main.js            # Main JavaScript
├── black-scholes.js   # Client-side Black-Scholes calculator
└── *.html             # Various page templates
```

## 🎯 Usage

### Static Demo (GitHub Pages)
Visit the live demo at the link above to use the basic Black-Scholes calculator.

### Full Version (Local)
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Flask app: `python app.py`
4. Open browser to `http://localhost:5001`

## 📊 Mathematical Models

This application implements:
- **Black-Scholes-Merton Model** for European option pricing
- **Greeks Calculation** using analytical formulas
- **Monte Carlo Simulation** with variance reduction techniques
- **Implied Volatility** using Newton-Raphson method

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Bowen Yao**
- GitHub: [@BowenYao-code](https://github.com/BowenYao-code)
- LinkedIn: [Bowen Yao](https://linkedin.com/in/bowen-yao)

## 🙏 Acknowledgments

- Black-Scholes model by Fischer Black and Myron Scholes
- Bootstrap for the UI framework
- Plotly for interactive visualizations

---

⭐ If you find this project useful, please consider giving it a star on GitHub!
