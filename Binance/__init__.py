import configparser
import json

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
    testnet = 'error'

# symbol_config = config['SYMBOL']
# symbol_busd = symbol_config['BUSD']
# symbol_busd = symbol_busd.split(',')
# symbol_busd = [symbol.strip() + 'BUSD' for symbol in symbol_busd]
#
# symbol_usdt = symbol_config['USDT']
# symbol_usdt = symbol_usdt.split(',')
# symbol_usdt = [symbol.strip() + 'USDT' for symbol in symbol_usdt]
#
# symbol_list = symbol_busd + symbol_usdt

symbol_file = open('symbol.json', mode='r')
symbol_size = json.load(symbol_file)
symbol_list = list(symbol_size.keys())
symbol_file.close()



