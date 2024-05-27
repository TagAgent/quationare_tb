import telebot
from quetions import QUETIONS
from local_settings import API_TOKEN
from local_settings import AUTHOR_CHATID

bot = telebot.TeleBot(API_TOKEN)

answers = []
last_answer = ""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"""
Здраствуйте, это бот-опросник 
Когда вы ответите на все вопросы все ваши ответы будут отправленны создателю этого бота 
{QUETIONS[0]}""")

@bot.message_handler(func=lambda message: True)
def ask_quetion(message):
    for index in range(1, len(QUETIONS)):
        send_quetion(message, index)
        last_answer = message.text

    print(answers)
    send_answers_to_author()

def send_quetion(message, index: int):
    if message.text != last_answer:
        msg = bot.send_message(message.chat.id, QUETIONS[index])
        bot.register_next_step_handler(msg, message.text)
        answers.append(message.text)

def send_answers_to_author():
    bot.send_message(AUTHOR_CHATID, str(answers))

bot.infinity_polling()
