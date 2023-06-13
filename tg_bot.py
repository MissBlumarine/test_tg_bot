import telebot
from telebot.types import LabeledPrice, ShippingOption

import config

# создаем бот и передаем ему токен
bot = telebot.TeleBot(config.bot_token)


#информация о параметрах платежа
# "RUB":{"code":"RUB","title":"Russian Ruble","symbol":"RUB","native":"₽",
# "thousands_sep":" ","decimal_sep":",","symbol_left":false,"space_between":true,"exp":2,
# "min_amount":"8653","max_amount":"86530475"}

# список с ценами для осуществления платежа
prices = [[LabeledPrice(label='Перевод 90 рублей', amount=9000)],
          [LabeledPrice(label='Перевод 200 рублей', amount=20000)],
          [LabeledPrice(label='Перевод 500 рублей', amount=50000)],
          [LabeledPrice(label='Перевод 1000 рублей', amount=100000)]]


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    """
    Функция, которая выводит на экран приветственное сообщение
    :param message:
    :return:
    """
    bot.reply_to(message, """\
Привет, дружище!
Я помогу тебе порадовать коллегу на День Рождения!\
Чтобы начать введи /donation
""")


@bot.message_handler(commands=['donation'])
def start_message(message):
    """
        Функция, которая выводит на экран кнопки для выбора валюты платежа
        :param message:
        :return:
        """

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)

    # создаем кнопки "RUB" и "USD"
    btn1 = telebot.types.KeyboardButton('RUB')
    btn2 = telebot.types.KeyboardButton('USD')

    markup.add(btn1, btn2)

    text = f'Привет еще раз, {message.from_user.full_name}! \n' \
           f'Я твой бот-помощник. Я помогу тебе скинуться на День рождения коллеги.\n' \
           f'Выбери валюту платежа'

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markup
                     )


@bot.message_handler(regexp='RUB')
def send_rubles(message):
    """
            Функция, которая выводит на экран кнопки для выбора валюты платежа
            :param message:
            :return:
            """

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn1 = telebot.types.KeyboardButton('90')
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

    text = f'Спасибо, что зашли к нам, {message.from_user.full_name}!\n' \
           f'Ждем Вас снова'

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=telebot.types.ReplyKeyboardRemove()
                     )


@bot.message_handler(regexp='100')
def command_pay_100(message):
    bot.send_message(message.chat.id,
                     'Тариф "Неприятный коллега')

    bot.send_invoice(
        message.chat.id,
        title='100 рублей',
        invoice_payload='Неприятный коллега',
        description='Перевод 100 рублей',
        provider_token=config.payments_token,
        currency='rub',
        prices=prices[0],
        is_flexible=False
    )


@bot.message_handler(regexp='200')
def command_pay_200(message):
    bot.send_message(message.chat.id,
                     'Тариф "Неплохой коллега')

    bot.send_invoice(
        message.chat.id,
        title='200 рублей',
        invoice_payload='Неплохой коллега',
        description='Перевод 200 рублей',
        provider_token=config.payments_token,
        currency='rub',
        prices=prices[1],
        is_flexible=False
    )


@bot.message_handler(regexp='500')
def command_pay_500(message):
    bot.send_message(message.chat.id,
                     'Тариф "Классный коллега')

    bot.send_invoice(
        message.chat.id,
        title='500 рублей',
        invoice_payload='Классный коллега',
        description='Перевод 500 рублей',
        provider_token=config.payments_token,
        currency='rub',
        prices=prices[2],
        is_flexible=False
    )


@bot.message_handler(regexp='1300')
def command_pay_1300(message):
    bot.send_message(message.chat.id,
                     'Тариф "Кореш')

    bot.send_invoice(
        message.chat.id,
        title='1500 рублей',
        invoice_payload='Кореш',
        description='Перевод 1300 рублей',
        provider_token=config.payments_token,
        currency='rub',
        prices=prices[3],
        is_flexible=False
    )




@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):

    if message.successful_payment.total_amount == 10000 or message.successful_payment.total_amount == 20000:
        bot.send_message(message.chat.id,
                         'Спасибо!\n'\
                         'Ваш платеж на сумму {} {} отправлен'.format(
                             message.successful_payment.total_amount / 100, message.successful_payment.currency),
                         parse_mode='Markdown')

    if message.successful_payment.total_amount == 50000 or message.successful_payment.total_amount == 100000:
        bot.send_message(message.chat.id,
                         'СУПЕРСПАСИБО!!\n' \
                         'Ваш платеж на сумму {} {} отправлен'.format(
                             message.successful_payment.total_amount / 100, message.successful_payment.currency),
                         parse_mode='Markdown')


# команда для запуска бота
bot.infinity_polling()
