import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

telegram = config['TELEGRAM']


token = telegram['token']
chat_id = telegram['chat_id']
