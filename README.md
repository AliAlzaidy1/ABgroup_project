# ABgroup_project - FOREX

## Project Confluence space:
**https://apedroni.atlassian.net/l/cp/nbRNdj1F**

## Files description:
### BoE_ECB_rates.csv
File with the data about the interest rates. Columns are:
  
- Date: in the AAA-MM-DD format
     
- BoE_base_rate: it is the interest rate set by the Bank of England that influences the other bank rates (for deposits, lenders, etc)
      
- ECB_deposit_facility_rate
- ECB_fixed_rate_tenders
- ECB_marginal_lending_facility_rate
       
These last three are the 3 key rates of the European Central Bank (there is not one easy "base one").

Note: BoE data start in 2010, ECB data start in 2011.

### get_BoE_ECB_rates.py
Python script to download the above data.
