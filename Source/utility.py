import win32api
import win32con


def MessageBox(message, title="Notification"):
    win32api.MessageBox(win32con.NULL, str(message), title, win32con.MB_OK)
