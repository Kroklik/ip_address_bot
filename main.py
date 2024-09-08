from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN, IP_TOKEN
from markups import main_menu
import requests

bot = TeleBot(TOKEN)


# Команда /start
@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.from_user.id
    bot.send_message(chat_id,
                     f'Привет, {message.from_user.username}! '
                     'Этот бот поможет вам узнать информацию о любом IP-адресе. '
                     'Нажмите кнопку ниже, чтобы начать!',
                     reply_markup=main_menu())


# Обработка кнопки "Узнать об IP"
@bot.message_handler(regexp='Узнать об IP')
def ask_for_ip(message: Message):
    chat_id = message.from_user.id
    msg = bot.send_message(chat_id, 'Пожалуйста, введите IP-адрес. Пример: 84.54.78.12',
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_ip)


# Обработка введённого IP
def process_ip(message: Message):
    chat_id = message.from_user.id
    ip = message.text.strip()

    if not validate_ip(ip):
        bot.send_message(chat_id, '❌ Некорректный формат IP-адреса. Попробуйте ещё раз.', reply_markup=main_menu())
        return

    send_ip = f'https://ipinfo.io/{ip}?token={IP_TOKEN}'

    try:
        response = requests.get(send_ip)
        response.raise_for_status()
        data = response.json()

        loc = data['loc'].split(',')
        longitude = loc[1]
        latitude = loc[0]

        result = f'''
🌐 <b>IP-адрес:</b> {data['ip']}
🏙️ <b>Город:</b> {data['city']}
🌍 <b>Регион:</b> {data['region']}
🏳️ <b>Страна:</b> {data['country']}

📍 <b>Координаты:</b>
  • <b>Широта:</b> {latitude}
  • <b>Долгота:</b> {longitude}

🕰️ <b>Часовой пояс:</b> {data['timezone']}
        '''

        bot.send_message(chat_id, result, parse_mode='HTML')
        ask_for_ip(message)

    except requests.RequestException:
        bot.send_message(chat_id, '❌ Произошла ошибка при запросе информации. Попробуйте снова.')
        ask_for_ip(message)


# Проверка корректности IP-адреса
def validate_ip(ip: str) -> bool:
    import re
    pattern = re.compile(r'^\d{1,3}(\.\d{1,3}){3}$')
    return bool(pattern.match(ip))


bot.polling(none_stop=True)
