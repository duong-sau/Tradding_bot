from google.oauth2 import service_account
import google.auth
from googleapiclient.discovery import build

# Đặt thông tin của file json credential của bạn ở đây
SERVICE_ACCOUNT_FILE = r'C:\Users\Sau\Downloads\Tradding_bot\Logic\traddingbot-18675fbbd1d6.json'
# Đặt ID của bảng tính của bạn ở đây
SPREADSHEET_ID = '1qrSDPFVZYW2k1oJGgrTqbPlfzp17wbM2q6Nua8aFUP4'

# Tạo credentials object từ file json
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])

# Tạo một service object để tương tác với Google Sheets API
service = build('sheets', 'v4', credentials=creds)

# Lấy dữ liệu từ bảng tính
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='Trang tính1!A1:B2').execute()
data = result.get('values', [])

# In ra dữ liệu
if not data:
    print('Không tìm thấy dữ liệu.')
else:
    print('Dữ liệu:')
    for row in data:
        print(f'{row[0]}, {row[1]}')
