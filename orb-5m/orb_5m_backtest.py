import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from strategy_measures import *

# import data from csv files
tqqq = pd.read_csv("data/tqqq_5m_10y.csv")
sqqq = pd.read_csv("data/sqqq_5m_10y.csv")

# Define the backtesting function, given certain parameter, such as
# Initial Capital C,
# Risk factor, r, for example, 1%
# Single exit R-multiples G, i.e., GR (we could do multi-step exit later if possible)
# Entry price floats x, i.e., high + x cents 
# Stop loss floats y, i.e., low - y cents
# initial day: init_day
def orb_5m_single_exit( tqqq, sqqq, C = 5000, r = 0.01, G = 10, x = 0, y = 0, init_day = "2013-09-09"):
    
    commission = 0.00124 # per share 
    
    today = pd.Timestamp(init_day).date()
    i = 0 # bar index, i.e., row number of the dataframe 
    d = 0 # the number of the days has passed
    
    entered, exited = False, False
    t, s = False, False
    capitals = [C]
    
    print(today, pd.Timestamp(tqqq.loc[i].date).date())
    
    s_trades = 0
    t_trades = 0
    while pd.Timestamp(tqqq.loc[i].date).date() == today:# in a trading day
        
        
#         print(f"i = {i}, d = {d}")
#         print(f"Today is {today}")
#         print(f"The time is {pd.Timestamp(tqqq.loc[i].date).time()}")
            
        
        # if this time slot is the first 5 min opening range
        # set up today's trading parameters, market open at 9:30 us/eastern
        if ( pd.Timestamp(tqqq.loc[i].date).time() == pd.Timestamp('09:30:00').time() ):
            # (pd.Timestamp(tqqq.loc[i - 1].date).date() != today and pd.Timestamp(tqqq.loc[i].date).time() == pd.Timestamp('14:30:00').time())):
             
            print(f"The date is {pd.Timestamp(tqqq.loc[i].date).date()}")
            print(f"The time is {pd.Timestamp(tqqq.loc[i].date).time()}")
            
            # retreive previous day balance
            capital = capitals[d]
            
            # amount of risk willing to take to find out the result
            R = r * capital

            
            # if tqqq's close > open and not a doji, long tqqq, 
            # if tqqq's close < open and not a doji, long sqqq
            if tqqq.loc[i].close - tqqq.loc[i].open > 0.02:
                
                high = tqqq.loc[i].high 
                low = tqqq.loc[i].low
                open_ = tqqq.loc[i].open
                close_ = tqqq.loc[i].close
                
                t = True 
                print("Pick TQQQ")

            # ensuring sqqq is not doji
            elif sqqq.loc[i].close - sqqq.loc[i].open >= 0.01:
                
                high = sqqq.loc[i].high
                low = sqqq.loc[i].low
                open_ = sqqq.loc[i].open
                close_ = sqqq.loc[i].close
                
                s = True 
                print("Pick SQQQ")
            else: # doji case
                
                # not trading today 
                
                
                # record today's balance
                capitals.append(capital)
                
                # increase the day passed
                d += 1
                print("I don't trade")
                print(f"SQQQ open {sqqq.loc[i].open}, close {sqqq.loc[i].close}")
                print(f"TQQQ open {tqqq.loc[i].open}, close {tqqq.loc[i].close}")
                
            if s or t:
                # method 1: using open and high as the range
                entry = high + x 
                stop_loss = open_ - y

                # method 2: using high and low as the range
#                 entry = high + x 
#                 stop_loss = low - y
            
                # decide the number of shares to buy 
                shares = min( 4 * capital // entry, R // (entry - stop_loss))
            
            
#         # checking the follow up bars, deciding whether entering the trade     
#         # if it is doji case, increase the timestamp until skipping the day    
#         if (not s and not t) == True:
#             i += 1 
#             continue
        
        
        # check whether exit the trade base on the multiple risk condition:
        if entered == True and exited == False :
            if t == True: 
                if tqqq.loc[i].high >= entry + G * (entry - stop_loss):
                    exited = True
                    capital += (entry + G * (entry - stop_loss) - commission ) * shares
                elif tqqq.loc[i].low <= stop_loss:
                    exited = True 
                    capital += (stop_loss - commission) * shares
                
            if s == True:
                if sqqq.loc[i].high >= entry + G * (entry - stop_loss):
                    exited = True
                    capital += (entry + G * (entry - stop_loss) - commission ) * shares
                elif sqqq.loc[i].low <= stop_loss:
                    exited = True
                    capital += (stop_loss - commission) * shares
            
                
        elif entered == False:
            
            if t == True and tqqq.loc[i].high > entry: # trading tqqq 
                    entered =  True 
                    capital -= entry * shares
                    t_trades += 1
                    print(f"Time is {pd.Timestamp(tqqq.loc[i].date).time()}")
                    print(f"Entering a TQQQ trade, entry price {entry}, stop loss {stop_loss}, shares {shares}")
            
            elif s == True and sqqq.loc[i].high > entry: # trading sqqq
                    entered = True
                    capital -= entry * shares
                    s_trades += 1
                    print(f"Time is {pd.Timestamp(tqqq.loc[i].date).time()}")
                    print(f"Entering a SQQQ trade, entry price {entry}, stop loss {stop_loss}, shares {shares}")
            
            else:                
                print("Not enter any trade yet")
                print(f"s is {s}")
                print(f"t is {t}")
        
        # move on the next 5m bar
        i += 1
        
        # this bar is today's last bar 
        # then, close the trade and update today to be the next day 
        
#         print(pd.Timestamp(tqqq.loc[i].date).date())
#         print(today + pd.DateOffset(1))
        
        if i < len(tqqq): # the header is not considered
            if pd.Timestamp(tqqq.loc[i].date).date() != today:
                print(f"end of the day {today}")
                print(f"i = {i}, d = {d}")
            # update today, since we are marching the next day
                d += 1
                today = pd.Timestamp(tqqq.loc[i].date).date()
            
                if t == True:
                    close = tqqq.loc[i - 1].close
                elif s == True:
                    close = sqqq.loc[i - 1].close
            
            # eixt the trade if not yet exited 
                if exited == False and entered == True:
                    capital += (close - commission) * shares
                    capitals.append(capital)
            # if exitted or not enterred the trade
                else:
                    capitals.append(capital)
                
            # update status 
                entered, exited = False, False
                t, s = False, False
                
        else: # end of the data
            print(f"end of the day {today}")
            print(f"i = {i}, d = {d}")
            
            if t == True:
                close = tqqq.loc[i - 1].close
            elif s == True:
                close = sqqq.loc[i - 1].close
            
            # eixt the trade if not yet exited 
            if exited == False and entered == True:
                capital += (close - commission) * shares
                capitals.append(capital)
            # if exitted or not enterred the trade
            else:
                capitals.append(capital)
                
            break 
            
            
        
          
    return capitals, d, s_trades, t_trades
        
balances, d, s_trades, t_trades = orb_5m_single_exit(tqqq, sqqq,
                   C = 25000,
                   r = 0.01,
                   G = 4, 
                   x = 0, 
                   y = 0, 
                   init_day = "2013-09-09")

print(f'The Sharpie Ratio is {sharpieRatio(balances, 0)}')

maxDD, maxDDD, i = calculateMaxDD(balances)
print(f"The maximum drawdown is {maxDD}, the maximum drawdown duration is {maxDDD}")
plt.plot(balances)
plt.show()