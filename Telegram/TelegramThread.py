import telebot
from telebot.apihelper import ApiTelegramException

from Telegram import token, chat_id


def tele_notification(content):
    try:
        bot = telebot.TeleBot(token)
        bot.send_message(chat_id, content)
    except ApiTelegramException:
        print('API exception')


def take_1_notification(control_id, position_num):
    tele_notification(f"Take profit 1 thành công {position_num}/{control_id}")


def take_2_notification(control_id, position_num):
    tele_notification(f'Take profit 2 thành công {position_num}/{control_id}')


def stop_notification(control_id, position_num):
    tele_notification(f'Stop loss    thành công {position_num}/{control_id}')


def limit_notification(control_id, position_num):
    tele_notification(f'Khớp limit thành công  {position_num}/{control_id}')


def start_notification(control_id):
    tele_notification(f'Băt đầu    DCA {control_id}')


def end_notification(control_id):
    tele_notification(f'Đã cắt hết các lệnh    DCA {control_id}')


def error_notification(message):
    tele_notification(f'Lỗi    {message}')
