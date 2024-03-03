import numpy as np
import pandas as pd

def sharpieRatio(daily_balances, risk_free_rate = 0.0):
   
   # from the balance to 
   daily_return = np.diff(daily_balances) / daily_balances[1:]

   # excess daily returns given the risk-free rate, with 252 trading days per year
   excess_return = daily_return - risk_free_rate / 252

   # return the sharpie ratio 
   return np.sqrt(252) * np.mean(excess_return) / np.std(excess_return)



def calculateMaxDD(daily_balances):
   # calculation of maximum drawdown and maximum drawdown duration based on
   # cumulative COMPOUNDED returns. cumret must be a compounded cumulative return.
   # i is the index of the day with maxDD
   
   # translate the equity curve to cumulative returns 
   cumulative_return = np.array(daily_balances) / daily_balances[0] - 1

   high_watermark = np.zeros(len(cumulative_return))

   drawdown = np.zeros(len(cumulative_return))
   
   drawdown_duration = np.zeros(len(cumulative_return))
   for t in range(1, len(cumulative_return)):          # check the current cumumlative return is higher if it's greater than the high watermark\
      
      high_watermark[t] = max(high_watermark[t - 1], cumulative_return[t])  
      drawdown[t] = (1 + cumulative_return[t]) / (1 + high_watermark[t]) - 1
      if drawdown[t] >= 0:
        drawdown_duration[t] = 0
      else:
        drawdown_duration[t] = drawdown_duration[t - 1] + 1
    
   maxDD, i = np.min(drawdown), np.argmin(drawdown)
    # drawdown < 0 always
   maxDDD = np.max(drawdown_duration)
    # return the max drawdown, maximum drawdown duration, and the index of the day with max drawdown
   return maxDD, maxDDD, i
   


