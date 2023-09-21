import datetime
import requests
import csv

function = {
            1: "FX_DAILY",
            2: "FX_WEEKLY",
            3: "FX_MONTHLY"
            }
def base_currency_input():
    while True:
        print("See below for the top 10 traded currency in the market:")
        print(f"Code        Currency")
        print(f"--------------------")
        for code, currency in base_cx.items():
            print(f"{code}:        {currency}")

        cx1 = input("Please enter the base currency code: ")
        cx1 = cx1.upper()
        if cx1 in base_cx:
            return cx1

        else:
            print("No such currency code, please re-enter")

def quote_currency_input():
    while True:
        print("See below for the top 10 traded currency in the market:")
        print(f"Code        Currency")
        print(f"--------------------")
        for code,currency in base_cx.items():
            print(f"{code}:        {currency}")

        cx2 = input("Please enter the quote currency code: ")
        cx2 = cx2.upper()
        if cx2 in base_cx:

            return cx2

        else:
            print("No such currency code, please re-enter")

def main_menu():
    while True:
        print("Welcome to the Forex Analysis Platform")
        print("See below for the option")
        print("1. Check Daily Currency Rate")
        print("2. Check Weekly Currency Rate")
        print("3. Check Monthly Currency Rate")
        func_option = int(input("Please select your option as above:"))
        if func_option <= 0 or func_option > 3:
            print("Wrong Selection")
        else:
            final_func = function[func_option]
            print(final_func)
            return final_func


class AlphaVantageDataExporter:
    def __init__(self, api_key, mode, from_symbol, to_symbol, output_size='full'):
        self.api_key = api_key
        self.mode = mode
        self.from_symbol = from_symbol
        self.to_symbol = to_symbol
        self.output_size = output_size

    def fetch_exchange_rate_data(self):
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': self.mode,
            'from_symbol': self.from_symbol,
            'to_symbol': self.to_symbol,
            'outputsize': self.output_size,
            'apikey': self.api_key,
        }
        print(self.mode)
        if self.mode == "FX_WEEKLY":
            new_mode = "Time Series FX (Weekly)"
        elif self.mode == "FX_DAILY":
            new_mode = "Time Series FX (Daily)"
        elif self.mode == "FX_MONTHLY":
            new_mode = "Time Series FX (Monthly)"
        elif self.mode == "CURRENCY_EXCHANGE_RATE":
            new_mode = "Realtime Currency Exchange Rate"


        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if new_mode in data:
                show = data[new_mode]
                for date, info in show.items():
                    print(f"Date: {date}, Open Price:{info['1. open']},High Price:{info['2. high']},Low Price:{info['3. low']}, Close Price: {info['4. close']}")

                return data[new_mode]
            else:
                print("Historic data not found in the response.")
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    def export_to_csv(self, historic_data, csv_file_path):
        if not historic_data:
            return

        with open(csv_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write the header row
            csv_writer.writerow([base+"/"+quote])
            csv_writer.writerow(['Date', 'Open Price', 'High Price', 'Low Price', 'Close Price'])

            # Write the data rows
            for date, info in historic_data.items():
                csv_writer.writerow([date, info['1. open'], info['2. high'], info['3. low'], info['4. close']])

    def export_exchange_rate_data_to_csv(self, csv_file_path):
        historic_data = self.fetch_exchange_rate_data()
        if historic_data:
            self.export_to_csv(historic_data, csv_file_path)
            print(f"Data has been exported to {csv_file_path}")

base_cx = {"USD" : "US Dollars",
           "EUR" : "Euro",
           "GBP" : "Pound Sterling",
           "CHF" : "Swiss Franc",
           "AUS" : "Australian Dollars",
           "NZD" : "New Zealand Dollars",
           "JPY" : "Japanese Yen",
           "CAD" : "Canadian Dollars",
           "HKD" : "Hong Kong Dollars",
           "CNY" : "Chinese Renminbi"
           }



# Usage example:
if __name__ == "__main__":
    main = main_menu()
    base = base_currency_input()
    quote = quote_currency_input()
    api_key = 'Q7G4099PBI6QFAPV'
    #print(main)
    #print(base)
    #print(quote)
    exporter = AlphaVantageDataExporter(api_key,main, base, quote)
    csv_file_path = 'exchange_rates.csv'
    exporter.export_exchange_rate_data_to_csv(csv_file_path)
