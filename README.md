# US Treasury Yield Curve Analysis

A Python tool for analyzing US Treasury yield curves and detecting recession indicators through the 2s10s spread. This project demonstrates fundamental fixed income analysis using real market data from Yahoo Finance.

## Key Findings (August 2024 - August 2025)

**Recession Signals Detected:**
- **2 Yield Curve Inversions**: 42-day period (Aug-Oct 2024) and 2-day period (Oct 2024)
- **Current Status**: Curve normalized but remains very flat (2s10s spread: 0.42 bp)
- **Fed Policy Signal**: 5Y yield below 2Y yield indicates expected rate cuts

**Current Market Conditions:**
- 2Y: 3.80% | 5Y: 3.70% | 10Y: 4.23% | 30Y: 4.92%
- Partial inversion persists (5Y < 2Y), suggesting continued economic uncertainty

## Methodology

### Data Collection
- **Source**: Yahoo Finance Treasury data (daily frequency)
- **Instruments**: 3-month (^IRX), 5Y (^FVX), 10Y (^TNX), 30Y (^TYX) Treasury yields
- **Period**: 1-year rolling analysis
- **2Y Estimation**: Interpolated from 3-month and 5Y yields using typical curve relationships

### Key Calculations
```python
# 2s10s Spread (primary recession indicator)
spread_2s10s = yield_10y - yield_2y_estimated

# Inversion Detection
is_inverted = spread_2s10s < 0
```

### Analysis Components
1. **Yield Curve Visualization**: Multi-period overlay charts showing curve evolution
2. **Spread Tracking**: Historical 2s10s spread with inversion period highlighting
3. **Inversion Analysis**: Automated detection and duration measurement of negative spreads
4. **Statistical Summary**: Current levels, historical ranges, and volatility metrics

## Installation and Usage

### Prerequisites
```bash
pip install pandas numpy matplotlib yfinance
```

### Run Analysis
```bash
python yield_curve_analyzer.py
```

### Expected Output
```
YIELD CURVE INVERSION ANALYSIS
Number of inversion periods: 2
Current 2s10s spread: 0.42 basis points
Status: Normal yield curve (positive spread)
```

## Project Structure
```
yield_curve_analyzer/
├── yield_curve_analyzer.py    # Main analysis script
├── visualizations/            # Generated charts
├── README.md                  # Documentation
└── requirements.txt           # Dependencies
```

## Technical Implementation

**Data Processing:**
- Handles missing data through forward/backward filling
- Manages misaligned date indexes across different Treasury maturities
- Implements fallback to simulated data for learning environments

**Visualization:**
- Professional financial charting with matplotlib
- Inversion period highlighting in red
- Multi-maturity yield curve overlays
- Time series analysis with proper date formatting

## Strengths

1. **Real Market Data**: Uses actual Treasury yields, not simulated data
2. **Automated Detection**: Systematically identifies inversion periods
3. **Professional Visualization**: Charts suitable for financial analysis
4. **Robust Error Handling**: Continues analysis even with data issues
5. **Educational Value**: Clear explanations of fixed income concepts

## Known Limitations

### Data Quality Issues
- **2Y Proxy**: Uses 3-month Treasury (^IRX) to estimate 2Y yields, creating potential inaccuracy
- **Limited Maturity Points**: Only 4 points (2Y, 5Y, 10Y, 30Y) vs. professional 11+ point curves
- **Data Source**: Yahoo Finance may have gaps or delays vs. official sources

### Methodology Gaps
- **No Fed Funds Integration**: Missing Federal Reserve policy rate analysis
- **Missing Economic Context**: No overlay of employment, inflation, or GDP data
- **Static Analysis**: No real-time updates or intraday analysis
- **Limited International Scope**: US-only analysis, no global yield comparisons

### Statistical Limitations
- **No Forward Rates**: Missing implied future rate calculations
- **No Term Premium Decomposition**: Cannot separate risk premium from expectations
- **Simple Curve Fitting**: No Nelson-Siegel or advanced term structure modeling
- **No Principal Component Analysis**: Missing factor-based yield curve analysis

## Future Improvements

### High Priority
- [ ] **FRED API Integration**: Replace Yahoo Finance with official Federal Reserve data
- [ ] **True 2Y Data**: Obtain actual 2-year Treasury yields vs. estimated
- [ ] **Extended Maturity Range**: Add 1M, 3M, 6M, 1Y, 3Y, 7Y points for complete curve
- [ ] **Fed Funds Overlay**: Compare yield curve changes to Federal Reserve policy actions


**Key Concepts Demonstrated:**
- Term structure of interest rates
- Yield curve inversion as recession indicator
- Federal Reserve policy impact on curves
- Financial time series analysis in Python

## Disclaimer

This tool is for educational and analytical purposes only. Historical yield curve inversions have preceded recessions, but timing and severity vary. Not intended for investment decisions.

## About

**Purpose**: Educational demonstration of fixed income analysis concepts  
**Data Period**: August 2024 - August 2025  
**Last Updated**: August 2025  

*Created as part of a fixed income learning project to understand Treasury yield curve dynamics and recession indicators.*
