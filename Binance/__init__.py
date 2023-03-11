import configparser
time_step = 1

config = configparser.ConfigParser()
config.read('config.ini')

mode = config['APP']['mode']
data = config[mode]

api_key = data['api_key']
api_secret = data['api_secret']



