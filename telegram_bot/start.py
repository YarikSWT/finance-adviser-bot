#!/usr/bin/env python
# pylint: disable=W0613, C0116, C0103
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.`
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from config import TELEGRAM_TOKEN, ENV, PUBLIC_ADDRESS, RUNNING_ADDRESS, PORT

from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from mongo_persistence import MongoPersistence
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import utils
from api.api import api

from modules import RegistrationModule, AddTransactionModule, HistoryModule, AdviserModule

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)


def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user = api.user.get(chat_id)
    if not user:
        reply_text = "Hi! My name is AI Bot. Please, /register"
        update.message.reply_text(reply_text)
    else:
        base_menu(update, context)


def ping(update: Update, context: CallbackContext) -> None:
    reply_text = "I am alive!!!!"
    update.message.reply_text(reply_text)

def test_ai(update: Update, context: CallbackContext) -> None:
    reply_text = "Excuse me. I just remind you, that you should not spend money on Food to achieve your goals!"
    update.message.reply_text(reply_text)

def base_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
        query.answer()
        chat_id = query.message.chat.id
    else:
        chat_id = update.message.chat_id
    user = api.user.get(chat_id)
    wallet = api.user(chat_id).money.get()
    reply_text = f"Hey, {user.name} \nYour balance: {wallet.balance}{wallet.currency} \nKeep going!"
    button_list = [
        InlineKeyboardButton("Add Transaction", callback_data='OPEN_ADD_TRANSACTION'),
        InlineKeyboardButton("History", callback_data='OPEN_HISTORY'),
        InlineKeyboardButton("Adviser", callback_data='OPEN_ADVISER'),
        InlineKeyboardButton("Settings", callback_data='OPEN_SETTINGS')
    ]
    reply_markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=2))
    if query:
        query.edit_message_text(text=reply_text, reply_markup=reply_markup)
    else:
        update.message.reply_text(text=reply_text, reply_markup=reply_markup)
    return -1


def main():
    # Create the Updater and pass it your bot's token.
    pp = MongoPersistence()
    updater = Updater(TELEGRAM_TOKEN,
                      persistence=pp,
                      use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    ping_handler = CommandHandler('ping', ping)
    dp.add_handler(ping_handler)

    test_ai_handler = CommandHandler('test_ai', test_ai)
    dp.add_handler(test_ai_handler)

    menu_handler = CallbackQueryHandler(base_menu, pattern='^' + 'OPEN_BASE_MENU' + '$')
    dp.add_handler(menu_handler)

    menu_command = CommandHandler('home', base_menu)
    dp.add_handler(menu_command)

    #   Connect modules

    RegistrationModule(dp, base_menu)
    AddTransactionModule(dp, base_menu)
    HistoryModule(dp, base_menu)
    AdviserModule(dp, base_menu)

    # Start the Bot
    if ENV != 'PROD':
        updater.start_polling()
        logger.info("Started in Polling mode...")
    else:
        webhook_address = PUBLIC_ADDRESS + "/" + TELEGRAM_TOKEN
        logger.info("Set Webhook on {} and PORT={}".format(webhook_address, PORT))
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TELEGRAM_TOKEN,
                              webhook_url=webhook_address)
        # updater.bot.setWebhook(webhook_address)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
