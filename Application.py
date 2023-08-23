import telebot
from Configuration import keys, TOKEN
from Extensions import APIException, CurrencyConverter
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Я бот который может конвертировать валюты.\n" \
           "Отправь команду /help чтобы узнать больше."
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Чтобы конвертировать валюты,\nвведи три последовательных параметра через пробел,\nв виде:\n\
 <валюта цену которой хочешь узнать>\n <валюта в которой надо узнать цену первой валюты>\n \
<количество первой валюты>.\n\
Используй команду /values чтобы узнать информацию о  доступных валютах."
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество параметров:\n Необходимо 3 параметра!')

        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя!\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {round(total_base, 4)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)