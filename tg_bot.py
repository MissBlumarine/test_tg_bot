import telebot

import config

# создаем бот и передаем ему токен
bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=['donation'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)

    btn1 = telebot.types.KeyboardButton('RUB')
    btn2 = telebot.types.KeyboardButton('USD')

    markup.add(btn1, btn2)

    text = f'Привет, {message.from_user.full_name}! \n' \
           f'Я твой бот-помощник. Я помогу тебе скинуться на День рождения коллеги.\n' \
           f'Выбери валюту платежа'

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markup
                     )


@bot.message_handler(regexp='RUB')
def send_rubles(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton('50')
    btn2 = telebot.types.KeyboardButton('200')
    btn3 = telebot.types.KeyboardButton('500')
    btn4 = telebot.types.KeyboardButton('1000')
    btn5 = telebot.types.KeyboardButton('закрыть')

    markup.add(btn1, btn2, btn3, btn4, btn5)
    text = 'Выберите сумму'

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='USD')
def send_dollars(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton('1')
    btn2 = telebot.types.KeyboardButton('10')
    btn3 = telebot.types.KeyboardButton('15')
    btn4 = telebot.types.KeyboardButton('20')
    btn5 = telebot.types.KeyboardButton('RUB')

    markup.add(btn1, btn2, btn3, btn4, btn5)
    text = 'Выберите сумму'

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='закрыть')
def get_back_button(message):
    # markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    #
    # btn1 = telebot.types.KeyboardButton('RUB')
    # btn2 = telebot.types.KeyboardButton('USD')
    #
    # markup.add(btn1, btn2)

    text = f'Спасибо, что зашли к нам, {message.from_user.full_name}!\n' \
           f'Ждем Вас снова'

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=telebot.types.ReplyKeyboardRemove()
                     )


# команда для запуска бота
bot.infinity_polling()
