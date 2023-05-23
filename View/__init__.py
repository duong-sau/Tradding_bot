import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')

mode = config['APP']['mode']
data = config[mode]
testnet = data['testnet']

if testnet == 'True':
    testnet = True
elif testnet == 'False':
    testnet = False
else:
    testnet = 'error'


symbol_file = open('symbol.json', mode='r')
symbol_size = json.load(symbol_file)
symbol_list = list(symbol_size.keys())
symbol_file.close()


def get_tick_price(symbol):
    symbol_data = symbol_size
    con = symbol_data[symbol]
    return con[0], con[1]
