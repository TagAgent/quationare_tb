import telebot
from quetions import QUETIONS
from local_settings import API_TOKEN
from local_settings import AUTHOR_CHATID

bot = telebot.TeleBot(API_TOKEN)

answers = []
chats = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"""
Здраствуйте, это бот-опросник 
Когда вы ответите на все вопросы все ваши ответы будут отправленны создателю этого бота """)
    send_quetion(message)

@bot.message_handler(func=lambda message: True)
def send_quetion(message):
    if message.chat.id not in chats:
        chats[message.chat.id] = 0

    for item in chats:
        if chats[item] >= len(QUETIONS):
            bot.send_message(message.chat.id, "Вы ответили на все вопросы! Ваши ответы отправленны автору этого бота!")
            send_to_author(message)
            break

        if message.chat.id == item:
            bot_message = bot.send_message(message.chat.id, QUETIONS[chats[item]])
            chats[item] += 1
            bot.register_next_step_handler(bot_message, add_answer)
            break


def add_answer(message):
    answers.append(message.text)
    send_quetion(message)

def send_to_author(message):
    answers_text = str(answers)
    bot.send_message(AUTHOR_CHATID, f"Ответы на вопросы от пользователя {message.from_user.first_name}: {answers_text[1:len(answers_text)-1]}")

bot.infinity_polling()
