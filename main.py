import telebot
from quetions import QUETIONS
from local_settings import API_TOKEN
from local_settings import AUTHOR_CHATID

bot = telebot.TeleBot(API_TOKEN)

answers = {}
chats = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """
Здраствуйте, это бот-опросник 
Когда вы ответите на все вопросы все ваши ответы будут отправленны создателю этого бота """)
    send_quetion(message)

def send_quetion(message):
    if message.chat.id not in chats:
        chats[message.chat.id] = 0
        answers[message.chat.id] = []

    if chats[message.chat.id] == len(QUETIONS):
        bot.send_message(message.chat.id, """Вы ответили на все вопросы! Ваши ответы отправленны автору этого бота!
        """)
        send_to_author(message)
        answers[message.chat.id] = []
        chats[message.chat.id] = 0
    else:
        bot_message = bot.send_message(message.chat.id, QUETIONS[chats[message.chat.id]])
        chats[message.chat.id] += 1
        bot.register_next_step_handler(bot_message, add_answer)

def add_answer(message):
    answers[message.chat.id].append(message.text)
    print(answers)
    send_quetion(message)

def send_to_author(message):
    answers_text = str(answers[message.chat.id])
    print(answers)
    bot.send_message(AUTHOR_CHATID, f"Ответы на вопросы от пользователя {message.from_user.first_name}: {answers_text[1:len(answers_text) - 1]}")

bot.infinity_polling()
