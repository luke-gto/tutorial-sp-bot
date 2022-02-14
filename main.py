
import telebot
import os
from src.wh_img import custom_title, random_title, title_from_keyword, print_tutorial
from telebot import types
from dotenv import load_dotenv


if os.path.isfile("src/.env"):
    load_dotenv('src/.env')    
    TOKEN = os.getenv("API_TOKEN")
    
else:
    TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup()
markup.row_width = 1
keyword_mkup = types.KeyboardButton('Keyword')
custom_title_mkup = types.KeyboardButton('Custom title')
random_title_mkup = types.KeyboardButton('Random title')
help_mkup = types.KeyboardButton("Help")

markup.add(keyword_mkup, custom_title_mkup, random_title_mkup, help_mkup)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, 'Hi! I can make random tutorials. How? Tap on the buttons below to:\n\n1) Give me a keyword and let me choose the title of the tutorial\n2) Send me the title of the tutorial\n3) Let me pick a random title.', reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def get_choice(message):

    if message.text == 'Help':
        send_welcome(message)

    if message.text == 'Keyword' or 'Custom title' or 'Random title':
        choice = message.text

        if choice == 'Custom title':
            message = bot.send_message(message.chat.id, 'Type your title:')
            bot.register_next_step_handler(message, get_user_title)

        if choice == 'Keyword':
            message = bot.send_message(message.chat.id, 'Type your keyword:')
            bot.register_next_step_handler(message, get_user_keyword)
            

        if choice == 'Random title':
            bot.send_chat_action(message.chat.id, 'upload_photo')
            image = print_tutorial(random_title())
            bot.send_photo(message.chat.id, image)
            return

    else:        

        bot.send_message(message.chat.id, 'Bro you have to tap on the buttons below!')

def get_user_title(message):
    input = message.text
    custom_title_ok = custom_title(input)
    bot.reply_to(message, "Gotcha! I'm working on it")
    image = print_tutorial(custom_title_ok)
    bot.send_chat_action(message.chat.id, 'upload_photo')
    bot.send_photo(message.chat.id, image)
    return


def get_user_keyword(message):
    input = message.text
    title_tutorial = title_from_keyword(input)
    bot.reply_to(message, "Gotcha! I'm working on it")
    if title_tutorial == -1:
        bot.send_message(message.chat.id, 'No matching keyword, please retry!')
    else:
        image = print_tutorial(title_tutorial)
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, image)
        return

def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()
