import configparser

config = configparser.ConfigParser()
config.read('config.ini')
symbol_section = config['SYMBOL']
symbols = symbol_section['symbols']

symbol_data = {}

symbols = symbols.split(',')
for symbol in symbols:
    symbol = symbol.strip()
    max_cross = symbol_section[symbol]
    symbol_data[symbol] = max_cross


