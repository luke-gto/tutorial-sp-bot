from __future__ import print_function
import logging
from typing import Dict
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext)
from wh_img import custom_title, random_title, title_from_keyword, print_tutorial
import telegram
import os
import os.path
from dotenv import load_dotenv
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

if os.path.isfile(".env"):
    load_dotenv()
    TOKEN = os.getenv("API_TOKEN")
    
else:
    TOKEN = os.getenv('API_TOKEN')
    
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ['Keyword'],
    ['Custom title'],
    ['Random title'],
    ['Restart']
    ]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Hi! I can make random tutorials. How? Tap on the buttons below to:\n\n1) Give me a keyword and let me choose the title of the tutorial\n2) Send me the title of the tutorial\n3) Let me pick a random title.",
        reply_markup=markup,
    )

    return CHOOSING

def restart(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "/start",
        reply_markup=markup,
    )

    return CHOOSING


def regular_choice(update: Update, context: CallbackContext) -> int:
    text = update.message.text        
    context.user_data['choice'] = text
    update.message.reply_text(f'{text.lower()}? Okay!')

    if "Random title" in text:
        update.message.reply_text("No fantasy, then. Let me handle it.")
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
        image = print_tutorial(random_title())        
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=image)
        return CHOOSING

    return TYPING_REPLY


def received_information(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(        
        f"You chose: {facts_to_str(user_data)}", reply_markup=markup,)
    title = (facts_to_str(user_data))
    user_data.clear()
    if "Keyword" in title:
        keyword = title[11:]
        title_tutorial = title_from_keyword(keyword)
        if title_tutorial == -1:
            update.message.reply_text("No matching keyword, retry.")
            return CHOOSING
        else:    
            update.message.reply_text("I'm generating the tutorial:\n\n{}\n\nWait please, I'm doing it, I promise.".format(title_tutorial.replace("\n", "")))
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
            image = print_tutorial(title_tutorial)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=image)
            return CHOOSING

    if "Custom title" in title:
        custom_title_input = title[16:]
        custom_title_ok = custom_title(custom_title_input)
        update.message.reply_text("I'm generating the tutorial:\n\n{}\n\nWait please, I'm doing it, I promise.".format(custom_title_ok.replace("\n", "")))
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.UPLOAD_PHOTO)
        image = print_tutorial(custom_title_ok)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=image)    
        return CHOOSING

def main() -> None:

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Keyword|Custom title|Random title)$'), regular_choice
                ),
                            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^(Keyword|Custom title|Random title)$')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^(Keyword|Custom title|Random title)$')),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Restart$'), restart)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
