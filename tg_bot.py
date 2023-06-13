import telebot

import config


# создаем бот и передаем ему токен
bot = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.full_name}! \n'
                     f'Я твой бот-помощник. Я помогу тебе скинуться на День рождения коллеги.'
                     )

# команда для запуска бота
bot.infinity_polling()