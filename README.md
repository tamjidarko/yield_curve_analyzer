# Yield Curve Analysis Project

A Python-based tool for analyzing US Treasury yield curves and tracking key fixed income indicators. This project demonstrates fundamental concepts in fixed income analysis including yield curve dynamics, spread calculations, and recession indicators.

## Project Overview

This analysis tool helps understand:

- **Term Structure of Interest Rates** - How yields vary by maturity
- **2s10s Spread Tracking** - The key recession indicator (10Y - 2Y yields)
- **Yield Curve Shape Analysis** - Normal vs. inverted curves
- **Historical Trend Analysis** - Curve evolution over time

## Key Features

- **Real-time Treasury Data** - Fetches current US Treasury yields via Yahoo Finance
- **Yield Curve Visualization** - Dynamic plots showing curve evolution
- **Inversion Detection** - Automatically identifies recession warning periods
- **Spread Analysis** - Calculates and tracks key yield spreads
- **Statistical Summary** - Comprehensive analysis reports
- **Error Handling** - Fallback to simulated data for learning

## Quick Start

### Prerequisites

```bash
pip install pandas numpy matplotlib yfinance
```

### Running the Analysis

```bash
python yield_curve_analyzer.py
```

### Sample Output

```
CURRENT YIELD LEVELS:
  2Y: 4.21%
  5Y: 4.54%
  10Y: 4.75%
  30Y: 4.80%

SPREAD ANALYSIS:
  Current 2s10s spread: 0.55 bp
  Status: Normal yield curve (positive spread)
```

## Project Structure

```
yield_curve_analyzer/
├── yield_curve_analyzer.py    # Main analysis script
├── visualizations/            # Generated charts and plots
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

## What You'll Learn

### Fixed Income Concepts

- **Yield Curve Fundamentals** - Relationship between yields and maturities
- **Term Structure Theory** - Why long-term rates differ from short-term
- **Recession Indicators** - How inverted curves predict economic downturns
- **Spread Analysis** - Key metrics tracked by bond traders

### Python Skills

- Financial data fetching with `yfinance`
- Time series analysis with `pandas`
- Data visualization with `matplotlib`
- Object-oriented programming for financial analysis

## Understanding the Output

### Normal vs. Inverted Curves

- **Normal Curve** (2s10s > 0): Healthy economy, longer-term rates higher
- **Inverted Curve** (2s10s < 0): Recession warning, short-term rates higher
- **Flat Curve**: Transition period, economic uncertainty

### Key Indicators

- **2s10s Spread**: Most watched recession predictor
- **5s30s Spread**: Term premium indicator
- **Curve Volatility**: Market stress indicator

## Current Analysis Results

Based on recent data analysis:

- **No recession signal** - Positive 2s10s spread maintained
- **Relatively flat curve** - Modest growth expectations
- **Stable conditions** - Low spread volatility

## Technical Implementation

### Data Sources

- **Primary**: Yahoo Finance Treasury data (^TNX, ^FVX, ^TYX, ^IRX)
- **Fallback**: Realistic simulated data for learning environments
- **Frequency**: Daily business day observations

### Key Calculations

```python
# 2s10s Spread Calculation
spread_2s10s = yield_10y - yield_2y

# Inversion Detection
is_inverted = spread_2s10s < 0
```

### Visualization Features

- Multi-period yield curve overlays
- Historical spread tracking
- Inversion period highlighting
- Professional financial charting

## Educational Value

This project is designed for:

- **Finance Students** learning fixed income fundamentals
- **Python Beginners** interested in financial applications
- **Analysts** wanting to understand yield curve mechanics
- **Traders** seeking recession indicator tools

## Known Limitations

- Uses 3-month Treasury as 2Y proxy (estimated from curve)
- Limited to 4 maturity points (2Y, 5Y, 10Y, 30Y)
- No Federal Reserve rate integration
- Weekend/holiday data limitations

## Future Enhancements

### Planned Improvements

- [ ] **FRED API Integration** - Official Federal Reserve data
- [ ] **Extended Maturity Range** - 1M, 3M, 6M, 1Y, 3Y, 7Y points
- [ ] **Fed Funds Rate Analysis** - Policy rate impact studies
- [ ] **International Comparisons** - Multi-country yield analysis
- [ ] **Forward Rate Calculations** - Implied future rate expectations

### Advanced Features

- [ ] **Principal Component Analysis** - Yield curve factor decomposition
- [ ] **Nelson-Siegel Modeling** - Professional curve fitting
- [ ] **Real-time Data Streaming** - Live market updates
- [ ] **Economic Indicator Integration** - GDP, employment, inflation overlays

## Learning Resources

### Fixed Income Fundamentals

- [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/)
- [Treasury.gov Yield Curve Data](https://www.treasury.gov/resource-center/data-chart-center/interest-rates/)
- "Fixed Income Analysis" by Frank J. Fabozzi

### Python for Finance

- `yfinance` documentation for market data
- `pandas` for time series analysis
- `matplotlib` for financial visualization

## Contributing

This is a learning project! Suggestions and improvements welcome:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with improvements

## License

This project is for educational purposes. Data is sourced from publicly available financial APIs.

## About

Created as part of a fixed income analysis learning project. Demonstrates fundamental yield curve concepts and Python implementation for financial analysis.

**Author**: [Your Name]  
**Date**: August 2025  
**Purpose**: Educational - Fixed Income & Python Learning

---

**Disclaimer**: This tool is for educational purposes only. Not intended for investment decisions.