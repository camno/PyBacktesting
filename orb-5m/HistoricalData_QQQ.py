from ib_insync import *
import pandas as pd

# IB connection 
HOST = "127.0.0.1"  # defined in the IB Trader Workstation
PORT = 7496         # defined in the IB Trader Workstation
CLIENT_ID = 1       # defined in the IB Trader Workstation

util.startLoop() # Starts loop that allows us to work with the API in Jupyter notebooks – this is not necessary in a script
ib_client = IB() # Creates an instance of the IB client class
ib_client.connect(HOST, PORT, CLIENT_ID) # Connects to TWS

# Retrieve account summary for currently signed in user

accounts = ib_client.accountSummary()
print(f"Account currently signed in to TWS is: {accounts[0]}")

# Request details for TQQQ and SQQQ contracts
tqqq_contract = Stock("TQQQ", exchange = "ISLAND")
sqqq_contract = Stock("SQQQ", exchange = "ISLAND")

full_tqqq_contract_details = ib_client.reqContractDetails(tqqq_contract)
full_sqqq_contract_details = ib_client.reqContractDetails(sqqq_contract)

print(f"Full contract details for TQQQ: {full_tqqq_contract_details}", end = "\n\n")
print(f"Full contract details for SQQQ stock: {full_sqqq_contract_details}")

tqqq_head_timestamp = ib_client.reqHeadTimeStamp(tqqq_contract, "MIDPOINT", useRTH = True)
print(f"Head timestamp for TQQQ: {tqqq_head_timestamp}")

sqqq_head_timestamp = ib_client.reqHeadTimeStamp(sqqq_contract, "MIDPOINT", useRTH = True)
print(f"Head timestamp for SQQQ: {sqqq_head_timestamp}")


# Request historical bars for the 3 Months with bar size of 5 mins, longer than 3 M may be time out
# in order to obtain the 1 year data, need to concatenate the data first.

# endDateTimes = ["20221120-23:59:59", "20230220-23:59:59", "20230521-23:59:59", "20230817-23:59:59"]
# 10 years' data, UTC format yyyymmddd-hh:mm:ss, or 
# endDateTimes = ["20131206-23:59:59", "20140306-23:59:59", "20140606-23:59:59", "20140906-23:59:59",
#     "20141206-23:59:59", "20150306-23:59:59", "20150606-23:59:59", "20150906-23:59:59",
#     "20151206-23:59:59", "20160306-23:59:59", "20160606-23:59:59", "20160906-23:59:59",
#     "20161206-23:59:59", "20170306-23:59:59", "20170606-23:59:59", "20170906-23:59:59",
#     "20171206-23:59:59", "20180306-23:59:59", "20180606-23:59:59", "20180906-23:59:59",
#     "20181206-23:59:59", "20190306-23:59:59", "20190606-23:59:59", "20190906-23:59:59",
#     "20191206-23:59:59", "20200306-23:59:59", "20200606-23:59:59", "20200906-23:59:59",
#     "20201206-23:59:59", "20210306-23:59:59", "20210606-23:59:59", "20210906-23:59:59",
#     "20211206-23:59:59", "20220306-23:59:59", "20220606-23:59:59", "20220906-23:59:59",
#     "20221206-23:59:59", "20230306-23:59:59", "20230606-23:59:59", "20230906-23:59:59"]

# 20031126 15:59:00 US/Eastern
endDateTimes = [  
    "20131206 23:59:59 US/Eastern", "20140306 23:59:59 US/Eastern", "20140606 23:59:59 US/Eastern", "20140906 23:59:59 US/Eastern",
    "20141206 23:59:59 US/Eastern", "20150306 23:59:59 US/Eastern", "20150606 23:59:59 US/Eastern", "20150906 23:59:59 US/Eastern",
    "20151206 23:59:59 US/Eastern", "20160306 23:59:59 US/Eastern", "20160606 23:59:59 US/Eastern", "20160906 23:59:59 US/Eastern",
    "20161206 23:59:59 US/Eastern", "20170306 23:59:59 US/Eastern", "20170606 23:59:59 US/Eastern", "20170906 23:59:59 US/Eastern",
    "20171206 23:59:59 US/Eastern", "20180306 23:59:59 US/Eastern", "20180606 23:59:59 US/Eastern", "20180906 23:59:59 US/Eastern",
    "20181206 23:59:59 US/Eastern", "20190306 23:59:59 US/Eastern", "20190606 23:59:59 US/Eastern", "20190906 23:59:59 US/Eastern",
    "20191206 23:59:59 US/Eastern", "20200306 23:59:59 US/Eastern", "20200606 23:59:59 US/Eastern", "20200906 23:59:59 US/Eastern",
    "20201206 23:59:59 US/Eastern", "20210306 23:59:59 US/Eastern", "20210606 23:59:59 US/Eastern", "20210906 23:59:59 US/Eastern",
    "20211206 23:59:59 US/Eastern", "20220306 23:59:59 US/Eastern", "20220606 23:59:59 US/Eastern", "20220906 23:59:59 US/Eastern",
    "20221206 23:59:59 US/Eastern", "20230306 23:59:59 US/Eastern", "20230606 23:59:59 US/Eastern", "20230906 23:59:59 US/Eastern"]

frames = []
for i in range(40):
    tqqq_historical_bars = ib_client.reqHistoricalData(
        tqqq_contract,
        endDateTime = endDateTimes[i],
        durationStr = "3 M",
        barSizeSetting = "5 mins",
        whatToShow = "TRADES", # https://interactivebrokers.github.io/tws-api/historical_bars.html#hd_what_to_show
        useRTH = True, # if true, only showing regular trading hours
        formatDate = 1 # uni time stamp
    )

    df = util.df(tqqq_historical_bars)
    frames.append(df)

tqqq_one_year_df = pd.concat(frames)

# save to csv file for later use
tqqq_one_year_df.to_csv('data/tqqq_5m_10y.csv', index = False)

# Similarly, Request historical bars for SQQQ

frames = []
for i in range(40):
    sqqq_historical_bars = ib_client.reqHistoricalData(
        sqqq_contract,
        endDateTime = endDateTimes[i],
        durationStr = "3 M",
        barSizeSetting = "5 mins",
        whatToShow = "TRADES",# https://interactivebrokers.github.io/tws-api/historical_bars.html#hd_what_to_show
        useRTH = True,# if true, only showing regular trading hours
        formatDate = 1
    )

    df = util.df(sqqq_historical_bars)
    frames.append(df)

sqqq_one_year_df = pd.concat(frames)

# save to csv file for later use
sqqq_one_year_df.to_csv('data/sqqq_5m_10y.csv', index = False)

ib_client.disconnect()