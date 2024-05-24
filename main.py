import telebot
from quetions import QUETIONS
from local_settings import API_TOKEN
from local_settings import AUTHOR_CHATID

bot = telebot.TeleBot(API_TOKEN)

answers = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"""
Здраствуйте, это бот-опросник 
Когда вы ответите на все вопросы все ваши ответы будут отправленны создателю этого бота 
{QUETIONS[0]}""")

@bot.message_handler(func=lambda message: True)
def ask_quetion(message):
    for item in range(1, len(QUETIONS)):
        bot.send_message(message.chat.id, QUETIONS[item])
        answers.append(message.text)
        print(answers)

bot.infinity_polling()
