import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import yfinance as yf
import requests
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (12, 8)

class YieldCurveAnalyzer:
    """
    A class to analyze US Treasury yield curves and track key metrics.
    
    This tool helps you understand:
    - How yield curves change over time
    - The relationship between different treasury maturities
    - Key spreads like the 2s10s (2yr vs 10yr)
    - When yield curves invert (recession indicator)
    """
    
    def __init__(self):
        self.data = None
        self.fed_funds_rate = None
        
    def fetch_treasury_data(self, start_date=None, end_date=None):
        """
        Fetch US Treasury yield data using Yahoo Finance
        
        We'll get:
        - 2 Year Treasury 
        - 5 Year Treasury 
        - 10 Year Treasury
        - 30 Year Treasury
        """
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        print("Fetching Treasury yield data...")
        print(f"Date range: {start_date} to {end_date}")
        
        # Treasury yield tickers (Yahoo Finance)
        tickers = {
            '2Y': '^IRX',     # 13 Week Treasury Bill (we'll adjust this)
            '5Y': '^FVX',     # 5 Year Treasury
            '10Y': '^TNX',    # 10 Year Treasury  
            '30Y': '^TYX'     # 30 Year Treasury
        }
        
        treasury_data = {}
        successful_fetches = []
        
        for maturity, ticker in tickers.items():
            try:
                print(f"Attempting to fetch {maturity} ({ticker})...")
                data = yf.download(ticker, start=start_date, end=end_date, progress=False)
                
                if not data.empty and 'Close' in data.columns:
                    # Convert to Series and ensure we have valid data
                    close_data = data['Close'].dropna()
                    if len(close_data) > 0:
                        # Ensure it's a proper Series with DatetimeIndex
                        if not isinstance(close_data.index, pd.DatetimeIndex):
                            close_data.index = pd.to_datetime(close_data.index)
                        treasury_data[maturity] = close_data
                        successful_fetches.append(maturity)
                        print(f"✓ Successfully fetched {maturity} data ({len(close_data)} points)")
                    else:
                        print(f"✗ No valid close data for {maturity}")
                else:
                    print(f"✗ Empty or invalid data for {maturity}")
                    
            except Exception as e:
                print(f"✗ Error fetching {maturity}: {str(e)}")
        
        print(f"\nSuccessfully fetched data for: {successful_fetches}")
        
        # Only proceed if we have at least 2 series with data
        if len(treasury_data) >= 2:
            try:
                print("Processing fetched data...")
                
                # Debug: Check what we actually have
                for key, series in treasury_data.items():
                    print(f"  {key}: {len(series)} points, index type: {type(series.index)}")
                    print(f"    First few dates: {series.index[:3].tolist()}")
                    print(f"    First few values: {series.head(3).values.flatten().tolist()}")
                    print(f"    Data type: {type(series)}")
                
                # Ensure all series have datetime index
                processed_data = {}
                for maturity, series in treasury_data.items():
                    # Convert index to datetime if it isn't already
                    if not isinstance(series.index, pd.DatetimeIndex):
                        series.index = pd.to_datetime(series.index)
                    processed_data[maturity] = series
                
                # Create DataFrame using outer join to handle different date ranges
                print("Creating DataFrame from fetched series...")
                
                # Method 1: Try direct DataFrame creation
                try:
                    self.data = pd.DataFrame(processed_data)
                    print("✓ DataFrame created successfully with direct method")
                except Exception as e1:
                    print(f"✗ Direct method failed: {e1}")
                    
                    # Method 2: Try creating empty DataFrame and adding columns
                    try:
                        # Get all unique dates
                        all_dates = set()
                        for series in processed_data.values():
                            all_dates.update(series.index)
                        all_dates = sorted(all_dates)
                        
                        # Create empty DataFrame with the date index
                        self.data = pd.DataFrame(index=all_dates)
                        
                        # Add each series as a column
                        for maturity, series in processed_data.items():
                            self.data[maturity] = series
                            
                        print("✓ DataFrame created successfully with manual method")
                    except Exception as e2:
                        print(f"✗ Manual method also failed: {e2}")
                        raise e2
                
                print(f"Initial data shape: {self.data.shape}")
                print(f"Index type: {type(self.data.index)}")
                
                # Ensure index is datetime
                if not isinstance(self.data.index, pd.DatetimeIndex):
                    self.data.index = pd.to_datetime(self.data.index)
                
                # Clean the data - remove rows with all NaN values
                initial_rows = len(self.data)
                self.data = self.data.dropna(how='all')
                print(f"Removed {initial_rows - len(self.data)} rows with all NaN values")
                
                print(f"After cleaning: {self.data.shape}")
                
                # Fill forward any missing values (common in financial data)
                self.data = self.data.fillna(method='ffill').fillna(method='bfill')
                
                # Create a better 2Y estimate if we don't have good 2Y data
                # Note: ^IRX is actually 3-month Treasury, so we need to adjust
                if '2Y' in self.data.columns:
                    # The ^IRX (labeled as '2Y') is actually 3-month rate
                    # Let's create a proper 2Y estimate from the curve
                    if '5Y' in self.data.columns and '10Y' in self.data.columns:
                        # Estimate 2Y using typical yield curve relationships
                        # 2Y is usually between 3-month and 5Y, closer to 5Y
                        three_month = self.data['2Y']  # This is actually 3-month
                        five_year = self.data['5Y']
                        
                        # Linear interpolation: 2Y ≈ 3M + 0.7 * (5Y - 3M)
                        self.data['2Y_estimated'] = three_month + 0.7 * (five_year - three_month)
                        print("✓ Created estimated 2Y yields from 3-month and 5Y data")
                    else:
                        # Fallback: just use the 3-month as proxy
                        self.data['2Y_estimated'] = self.data['2Y']
                        print("⚠️  Using 3-month rate as 2Y proxy")
                elif '5Y' in self.data.columns:
                    # If no 2Y data, estimate from 5Y
                    self.data['2Y_estimated'] = self.data['5Y'] - 0.5
                    print("✓ Estimated 2Y yields from 5Y data")
                
                if not self.data.empty:
                    print(f"✓ Final data shape: {self.data.shape}")
                    print(f"✓ Date range: {self.data.index.min()} to {self.data.index.max()}")
                    print(f"✓ Available columns: {list(self.data.columns)}")
                    
                    # Show some sample data
                    print(f"✓ Sample data (last 3 rows):")
                    print(self.data.tail(3))
                    
                    return True
                else:
                    print("✗ Data is empty after processing")
                    return False
                    
            except Exception as e:
                print(f"✗ Error processing data: {str(e)}")
                print("Full error details:")
                import traceback
                traceback.print_exc()
                
                # Try the fallback approach
                print("\n🔄 Trying alternative data processing approach...")
                return self.create_sample_data()
        else:
            print(f"✗ Insufficient data: only {len(treasury_data)} series fetched (need at least 2)")
            
            # Try alternative approach with simulated data for learning
            print("\n🔄 Creating simulated data for learning purposes...")
            return self.create_sample_data()
    
    def create_sample_data(self):
        """
        Create sample treasury data for learning when real data isn't available
        """
        try:
            # Create date range for past year
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            date_range = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days
            
            # Create realistic treasury yields with some randomness
            np.random.seed(42)  # For reproducible results
            base_10y = 4.5  # Starting 10Y yield around current levels
            
            # Generate yields with realistic relationships and some time-series behavior
            yields_10y = []
            yields_5y = []
            yields_2y = []
            yields_30y = []
            
            current_10y = base_10y
            
            for i in range(len(date_range)):
                # Add some random walk behavior
                change = np.random.normal(0, 0.05)  # Small daily changes
                current_10y += change
                current_10y = max(1.0, min(7.0, current_10y))  # Keep in reasonable range
                
                # Create yield curve relationships
                y_10 = current_10y
                y_5 = y_10 - 0.3 + np.random.normal(0, 0.1)  # 5Y typically lower
                y_2 = y_5 - 0.4 + np.random.normal(0, 0.1)   # 2Y typically lower still
                y_30 = y_10 + 0.2 + np.random.normal(0, 0.1)  # 30Y typically higher
                
                yields_10y.append(y_10)
                yields_5y.append(y_5)
                yields_2y.append(y_2)
                yields_30y.append(y_30)
            
            # Create DataFrame
            self.data = pd.DataFrame({
                '2Y_estimated': yields_2y,
                '5Y': yields_5y,
                '10Y': yields_10y,
                '30Y': yields_30y
            }, index=date_range)
            
            print(f"✓ Created sample data with shape: {self.data.shape}")
            print("📝 Note: This is simulated data for learning purposes")
            return True
            
        except Exception as e:
            print(f"✗ Error creating sample data: {str(e)}")
            return False
    
    def fetch_fed_funds_rate(self):
        """
        Fetch Federal Funds Rate data
        We'll use a simple approach with available data
        """
        try:
            # Using FRED data via a simple API call
            print("Fetching Fed Funds Rate data...")
            
            # For now, we'll create a simple proxy
            # In production, you'd use FRED API
            dates = pd.date_range(start=self.data.index.min(), 
                                end=self.data.index.max(), freq='D')
            
            # Create a simplified fed funds rate (this is just for demonstration)
            # In reality, you'd fetch this from FRED
            fed_rate_values = np.random.uniform(4.5, 5.5, len(dates))  # Current range
            
            self.fed_funds_rate = pd.Series(fed_rate_values, index=dates)
            print("✓ Fed Funds Rate data created (demo version)")
            
        except Exception as e:
            print(f"✗ Error creating fed funds data: {str(e)}")
    
    def calculate_spreads(self):
        """
        Calculate key yield curve spreads
        
        The 2s10s spread is the most watched indicator:
        - Positive spread = normal curve (long-term rates > short-term)
        - Negative spread = inverted curve (recession warning!)
        """
        if self.data is None:
            print("No data available. Fetch data first!")
            return
        
        # Calculate 2s10s spread (10-year minus 2-year)
        if '10Y' in self.data.columns and '2Y_estimated' in self.data.columns:
            self.data['2s10s_spread'] = self.data['10Y'] - self.data['2Y_estimated']
        
        # Calculate 5s30s spread  
        if '30Y' in self.data.columns and '5Y' in self.data.columns:
            self.data['5s30s_spread'] = self.data['30Y'] - self.data['5Y']
            
        print("✓ Spreads calculated successfully!")
        
    def plot_yield_curve_evolution(self, num_dates=5):
        """
        Plot how the yield curve has evolved over time
        """
        if self.data is None:
            print("No data to plot!")
            return
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Plot 1: Recent yield curves
        maturities = [2, 5, 10, 30]  # years
        maturity_labels = ['2Y_estimated', '5Y', '10Y', '30Y']
        
        # Select dates to show
        recent_dates = self.data.index[-num_dates*20::20]  # Every 20th day for last num_dates
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(recent_dates)))
        
        for i, date in enumerate(recent_dates):
            if date in self.data.index:
                yields = []
                for label in maturity_labels:
                    if label in self.data.columns:
                        yields.append(self.data.loc[date, label])
                    else:
                        yields.append(np.nan)
                
                ax1.plot(maturities, yields, 'o-', color=colors[i], 
                        label=f"{date.strftime('%Y-%m-%d')}", linewidth=2, markersize=6)
        
        ax1.set_xlabel('Maturity (Years)')
        ax1.set_ylabel('Yield (%)')
        ax1.set_title('US Treasury Yield Curve Evolution')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: 2s10s spread over time
        if '2s10s_spread' in self.data.columns:
            ax2.plot(self.data.index, self.data['2s10s_spread'], 
                    linewidth=2, color='darkblue', label='2s10s Spread')
            ax2.axhline(y=0, color='red', linestyle='--', alpha=0.7, label='Inversion Line')
            ax2.fill_between(self.data.index, 
                           self.data['2s10s_spread'], 
                           0, 
                           where=(self.data['2s10s_spread'] < 0),
                           alpha=0.3, color='red', label='Inversion Periods')
            
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Spread (basis points)')
            ax2.set_title('2s10s Yield Spread Over Time (Negative = Inverted)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Format x-axis
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        plt.show()
        
    def analyze_inversions(self):
        """
        Identify and analyze yield curve inversions
        """
        if '2s10s_spread' not in self.data.columns:
            print("2s10s spread not calculated!")
            return
            
        # Find inversion periods
        inversions = self.data['2s10s_spread'] < 0
        inversion_periods = []
        
        in_inversion = False
        start_date = None
        
        for date, is_inverted in inversions.items():
            if is_inverted and not in_inversion:
                # Start of inversion
                in_inversion = True
                start_date = date
            elif not is_inverted and in_inversion:
                # End of inversion
                in_inversion = False
                inversion_periods.append((start_date, date))
        
        # Handle case where we're still in inversion
        if in_inversion:
            inversion_periods.append((start_date, self.data.index[-1]))
        
        print("\n" + "="*50)
        print("YIELD CURVE INVERSION ANALYSIS")
        print("="*50)
        
        if inversion_periods:
            print(f"Number of inversion periods: {len(inversion_periods)}")
            for i, (start, end) in enumerate(inversion_periods):
                duration = (end - start).days
                print(f"\nInversion {i+1}:")
                print(f"  Start: {start.strftime('%Y-%m-%d')}")
                print(f"  End: {end.strftime('%Y-%m-%d')}")
                print(f"  Duration: {duration} days")
        else:
            print("No yield curve inversions detected in this period.")
            
        # Current status
        current_spread = self.data['2s10s_spread'].iloc[-1]
        print(f"\nCurrent 2s10s spread: {current_spread:.2f} basis points")
        
        if current_spread < 0:
            print("⚠️  YIELD CURVE IS CURRENTLY INVERTED!")
        else:
            print("✅ Yield curve is currently normal (positive spread)")
            
    def generate_summary_report(self):
        """
        Generate a comprehensive summary report
        """
        if self.data is None:
            print("No data available!")
            return
            
        print("\n" + "="*60)
        print("YIELD CURVE ANALYSIS SUMMARY REPORT")
        print("="*60)
        
        print(f"Analysis Period: {self.data.index.min().strftime('%Y-%m-%d')} to {self.data.index.max().strftime('%Y-%m-%d')}")
        print(f"Total observations: {len(self.data)}")
        
        # Current yields
        print("\n📊 CURRENT YIELD LEVELS:")
        latest_date = self.data.index[-1]
        for col in ['2Y_estimated', '5Y', '10Y', '30Y']:
            if col in self.data.columns:
                yield_value = self.data[col].iloc[-1]
                print(f"  {col.replace('_estimated', '')}: {yield_value:.2f}%")
        
        # Spread analysis
        if '2s10s_spread' in self.data.columns:
            print("\n📈 SPREAD ANALYSIS:")
            current_spread = self.data['2s10s_spread'].iloc[-1]
            max_spread = self.data['2s10s_spread'].max()
            min_spread = self.data['2s10s_spread'].min()
            avg_spread = self.data['2s10s_spread'].mean()
            
            print(f"  Current 2s10s spread: {current_spread:.2f} bp")
            print(f"  Average spread: {avg_spread:.2f} bp")
            print(f"  Maximum spread: {max_spread:.2f} bp")
            print(f"  Minimum spread: {min_spread:.2f} bp")
            
            # Volatility
            spread_std = self.data['2s10s_spread'].std()
            print(f"  Spread volatility (std dev): {spread_std:.2f} bp")

def main():
    """
    Main function to run the yield curve analysis
    """
    print("🏦 Welcome to the Yield Curve Analyzer!")
    print("This tool will help you understand Treasury yield curves and spreads.\n")
    
    # Create analyzer instance
    analyzer = YieldCurveAnalyzer()
    
    # Fetch data
    print("Attempting to fetch Treasury data from Yahoo Finance...")
    success = analyzer.fetch_treasury_data()
    
    if not success:
        print("\n❌ Unable to fetch or create treasury data.")
        print("This could be due to:")
        print("- Internet connectivity issues")
        print("- Yahoo Finance API limitations")
        print("- Weekend/holiday data availability")
        print("\nPlease try again later or check your internet connection.")
        return
    
    # Calculate spreads
    print("\n🔢 Calculating yield spreads...")
    analyzer.calculate_spreads()
    
    # Generate visualizations
    print("\n📊 Generating yield curve plots...")
    try:
        analyzer.plot_yield_curve_evolution()
        print("✓ Charts displayed successfully!")
    except Exception as e:
        print(f"⚠️  Chart display issue: {str(e)}")
        print("Charts may not display in some environments.")
    
    # Analyze inversions
    print("\n🔍 Analyzing yield curve inversions...")
    analyzer.analyze_inversions()
    
    # Generate summary report
    print("\n📋 Generating summary report...")
    analyzer.generate_summary_report()
    
    print("\n✅ Analysis complete!")
if __name__ == "__main__":
    main()
