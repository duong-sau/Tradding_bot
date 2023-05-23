import json

symbol_file = open('symbol.json', mode='r')
symbol_size = json.load(symbol_file)
symbol_list = list(symbol_size.keys())
symbol_file.close()
