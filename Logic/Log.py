import pygsheets
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = r'C:\Users\Sau\Downloads\Tradding_bot\Logic\traddingbot-18675fbbd1d6.json'
SPREADSHEET_ID = '1qrSDPFVZYW2k1oJGgrTqbPlfzp17wbM2q6Nua8aFUP4'

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)



client = pygsheets.authorize(client_secret=creds)

# Open the spreadsheet and the first sheet.
sh = client.open('Tradding bot loging')
wks = sh.sheet1

# Update a single cell.
wks.update_value('A1', "Numbers on Stuff")

# Update the worksheet with the numpy array values. Beginning at cell 'A2'.
wks.update_values('A2', 'A')

# Share the sheet with your friend. (read access only)
sh.share('friend@gmail.com')
# sharing with write access
sh.share('friend@gmail.com', role='writer')


def log_request(data):
    for row in data:
        print(row)


def order_log(symbol, quantity, price, stop_price):
    print(symbol, quantity, price, stop_price)
