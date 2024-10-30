from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
   
    def __init__(self):
        # Define the ticker of interest
        self.ticker = "AAPL"
    
    @property
    def assets(self):
        # The asset we are interested in trading - AAPL.
        return [self.ticker]

    @property
    def interval(self):
        # Using daily data for analysis.
        return "1day"
    
    def run(self, data):
        # Run the strategy logic for each trading interval.
        
        # We calculate the 5-day and 10-day simple moving averages (SMA)
        sma_5 = SMA(self.ticker, data["ohlcv"], 5)
        sma_10 = SMA(self.ticker, data["ohlcv"], 10)
        
        # Check to make sure we have enough data for both SMAs before proceeding
        if sma_5 is not None and sma_10 is not None:
            # If the latest 5-day SMA is above the 10-day SMA, suggest buying or holding AAPL
            if sma_5[-1] > sma_10[-1]:
                log(f"Upward trend detected. Allocating to {self.ticker}")
                allocation = {self.ticker: 1.0}  # Allocate 100% of the portfolio to AAPL
            else:
                # If the 5-day SMA is below the 10-day SMA, suggest it's better not to hold AAPL
                log(f"Downward trend or no clear trend detected. No allocation to {self.ticker}")
                allocation = {self.ticker: 0.0}  # Allocate 0% of the portfolio to AAPL
        else:
            # In case of insufficient data for either SMA calculation, no allocation is made.
            log("Insufficient data for SMA calculation. No allocation made.")
            allocation = {self.ticker: 0.0}
        
        # Return the target allocation
        return TargetAllocation(allocation)