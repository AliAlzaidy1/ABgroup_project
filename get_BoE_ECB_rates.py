import pandas as pd
import requests
from requests import HTTPError
import io
import matplotlib.pyplot as plt

# ---------- Bank of England -------------------

# info on CSV downloads from the Bank of England database at:
# https://www.bankofengland.co.uk/boeapps/database/help.asp?Back=Y&Highlight=CSV#CSV

# tutorial by PythonSherpa at:
# https://www.pythonsherpa.com/tutorials/5/

# tutorial about the requests package at:
# https://www.dataquest.io/blog/tutorial-an-introduction-to-python-requests-library/

# I'm downloading the OFFICIAL BANK RATE aka BASE RATE AKA INTEREST RATE
# info: https://www.bankofengland.co.uk/explainers/why-are-interest-rates-in-the-uk-going-up

# the SeriesCode: IUDBEDR

BoE_url_endpoint = 'https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes'

# parameters to append
BoE_payload = {
    'Datefrom'   : '01/Jan/2010',
    'Dateto'     : 'now',
    'SeriesCodes': 'IUDBEDR',
    'CSVF'       : 'TN', # tabular data without titles
    'UsingCodes' : 'Y',
    'VPD'        : 'Y',
    'VFD'        : 'N'
}

# ATTENTION: add headers to make it look like the request comes from a browser, otherwise it won't work
# https://stackoverflow.com/questions/41946166/requests-get-returns-403-while-the-same-url-works-in-browser
# without headers:
# 500 Server Error: Internal Server Error for url: https://www.bankofengland.co.uk/...

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/54.0.2840.90 '
                  'Safari/537.36'
}


# create the full link and send a get request
try:
    BoE_response = requests.get(BoE_url_endpoint, params=BoE_payload, headers=headers)
    BoE_response.raise_for_status()
    # Check if the response was successful, it should return '200'
    print('Response Code:', BoE_response.status_code)
    
except HTTPError as err:
    print(err)
else:
    # print(BoE_response.url)
    
    
    BoE_df = pd.read_csv(io.BytesIO(BoE_response.content))
    BoE_df['DATE'] = pd.to_datetime(BoE_df['DATE'])
    BoE_df.rename(columns={'DATE' : 'Date', 'IUDBEDR': 'BoE_base_rate'}, inplace=True)
    print(BoE_df.head())
    print(BoE_df.info())
    
    # fill the gaps
    full_date_range = pd.date_range(start=BoE_df['Date'].min(), end=BoE_df['Date'].max())
    missing_dates = full_date_range.difference(BoE_df['Date'])
    BoE_df.set_index('Date', inplace=True)
    BoE_df = BoE_df.reindex(full_date_range, method='ffill')
    
    BoE_df['Date'] = BoE_df.index
    BoE_df = BoE_df[['Date', 'BoE_base_rate']]
    
    print(BoE_df.head())
    print(BoE_df.info())
    
    BoE_df.to_csv('BoE_base_rate.csv', index=False, encoding='utf-8')
    
    



BoE_ECB_rates = BoE_df.copy()


# ---------- European Central Bank -------------

# NB:
# ECB does not have a single base rate like BoE.
# ********************************
# ECB has 3 key ECB interest rates:
# Deposit Facility - Fixed Rate Tender - Marginal Lending
# https://data.ecb.europa.eu/main-figures/ecb-interest-rates-and-exchange-rates/key-ecb-interest-rates
# ********************************
# https://www.ecb.europa.eu/services/glossary/html/glossk.en.html

# find the time series dimensions for the request link here:
# https://data.ecb.europa.eu/data/data-categories/ecbeurosystem-policy-and-exchange-rates/official-interest-rates?searchTerm=&filterSequence=frequency&sort=t_ecb_last_update&filterType=basic&showDatasetModal=false&filtersReset=false&resetAll=false&frequency%5B%5D=B

'''
DEPOSIT FACILITY : FM.B.U2.EUR.4F.KR.DFR.LEV
Frequency: Daily - businessweek [B]
Reference area: Euro area (changing composition) [U2]
Currency: Euro [EUR]
Financial market provider: ECB [4F]
Financial market instrument: Key interest rate [KR]
Financial market provider identifier: ECB Deposit facility - date of changes (raw data) [DFR]
Financial market data type: Level [LEV]

FIXED RATE TENDER : FM.B.U2.EUR.4F.KR.MRR_FR.LEV
Frequency: Daily - businessweek [B]
Reference area: Euro area (changing composition) [U2]
Currency: Euro [EUR]
Financial market provider: ECB [4F]
Financial market instrument: Key interest rate [KR]
Financial market provider identifier: ECB Main refinancing operations - fixed rate tenders (fixed rate) (date of changes) [MRR_FR]
Financial market data type: Level [LEV]

MARGINAL LENDING : FM.B.U2.EUR.4F.KR.MLFR.LEV
Frequency: Daily - businessweek [B]
Reference area: Euro area (changing composition) [U2]
Currency: Euro [EUR]
Financial market provider: ECB [4F]
Financial market instrument: Key interest rate [KR]
Financial market provider identifier: ECB Marginal lending facility - date of changes (raw data) [MLFR]
Financial market data type: Level [LEV]
'''
    
ECB_entrypoint = 'https://data-api.ecb.europa.eu/service/'
# Building blocks for the URL

resource = 'data'           # The resource for data queries is always'data'
flowRef ='FM'              # Dataflow describing the data that needs to be returned
rates = ['ECB_deposit_facility_rate', 'ECB_fixed_rate_tenders', 'ECB_marginal_lending_facility_rate'] # ECB key interest rates names
keys = ['B.U2.EUR.4F.KR.DFR.LEV', 'B.U2.EUR.4F.KR.MRR_FR.LEV', 'B.U2.EUR.4F.KR.MLFR.LEV']    # unique dimension values

# Define the parameters
ECB_payload = {
    'startPeriod': '2010-01-01',  # Start date of the time series
    'endPeriod': '2023-09-30',    # End of the time series
    'format': 'csvdata'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/54.0.2840.90 '
                  'Safari/537.36'
}

ECB_df = pd.DataFrame()

for rate, key in zip(rates, keys):

    ECB_url_endpoint = ECB_entrypoint + resource + '/'+ flowRef + '/' + key

    # create the full link and send a get request
    try:
        ECB_response = requests.get(ECB_url_endpoint, params=ECB_payload, headers=headers)
        ECB_response.raise_for_status()
        # Check if the response was successful, it should return '200'
        print('Response Code:', ECB_response.status_code)
        
    except HTTPError as err:
        print(err)
    else:
        # print(ECB_response.url)
        
        df = pd.read_csv(io.BytesIO(ECB_response.content))
        df = df[['TIME_PERIOD', 'OBS_VALUE']]
        df.rename(columns={'TIME_PERIOD' : 'Date', 'OBS_VALUE': rate}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        
        print(df.head())
        print(df.info())
        
        # fill the gaps
        full_date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max())
        missing_dates = full_date_range.difference(df['Date'])
        df.set_index('Date', inplace=True)
        df = df.reindex(full_date_range, method='ffill')
        
        print(df.head())
        print(df.info())
        # outer join the different rates
        ECB_df = pd.concat([ECB_df, df], axis=1).reindex(df.index)
        
        
# give a name to the date column
ECB_df['Date'] = ECB_df.index
# reorder the columns
ECB_df = ECB_df[['Date', rates[0], rates[1], rates[2]]]
# save to csv
ECB_df.to_csv('ECB_base_rate.csv', index=False, encoding='utf-8')


BoE_ECB_rates = pd.merge(BoE_df, ECB_df, on='Date', how='outer')
BoE_ECB_rates.to_csv('BoE_ECB_rates.csv', index=False, encoding='utf-8')

plt.plot(BoE_df.Date, BoE_df.BoE_base_rate)
plt.plot(ECB_df.index, ECB_df.ECB_deposit_facility_rate, label = rates[0])
plt.plot(ECB_df.index, ECB_df.ECB_fixed_rate_tenders, label = rates[1])
plt.plot(ECB_df.index, ECB_df.ECB_marginal_lending_facility_rate, label = rates[2])
plt.legend()
plt.show()