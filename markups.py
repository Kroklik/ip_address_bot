from telebot.types import KeyboardButton, ReplyKeyboardMarkup


# Главное меню с кнопкой для запроса IP
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text='Узнать об IP')
    markup.add(btn)
    return markup
