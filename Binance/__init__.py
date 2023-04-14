import configparser
import ctypes
import sys

time_step = 1

config = configparser.ConfigParser()
config.read('config.ini')

mode = config['APP']['mode']
data = config[mode]

api_key = data['api_key']
api_secret = data['api_secret']

testnet = data['testnet']

if testnet == 'True':
    testnet = True
elif testnet == 'False':
    testnet = False
else:
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, 'Chưa cài đặt testnet', 'Lỗi', 0)
    sys.exit(0)
