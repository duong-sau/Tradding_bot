import inspect
import sys
from datetime import datetime

import telebot

from Telegram import token, chat_id


def tele_notification(content):
    try:
        bot = telebot.TeleBot(token)
        bot.send_message(chat_id, content)
    except:
        all_log()


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


def log_error():
    previous_frame = inspect.currentframe().f_back
    calling_function_name = previous_frame.f_code.co_name
    calling_file_name = previous_frame.f_code.co_filename
    last_error = sys.exc_info()[1]
    tele_notification(f'Lỗi    {calling_function_name} |||  last error {last_error} ||| {calling_file_name}')


def all_log():
    file = open('log.txt', mode='a')
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    last_error = sys.exc_info()[1]
    previous_frame = inspect.currentframe().f_back
    calling_function_name = previous_frame.f_code.co_name
    file.write(f"{formatted_time} || {last_error} || {calling_function_name} \n")
    file.close()
