from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
import utils
from api.api import api

def history(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query:
        chat_id = query.message.chat.id
    else:
        chat_id = update.message.chat_id

    transactions = api.user(chat_id).transactions.get()
    total = -sum([t.delta for t in transactions])
    historyStr = "\n".join(["{} - {} - {}".format(t.delta, t.category, t.description) for t in transactions])
    reply_text = "Total spending: {}  \n\n{}".format(total, historyStr)
    button_list = [
        InlineKeyboardButton("Done", callback_data='OPEN_BASE_MENU'),
    ]
    reply_markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=1))
    context.bot.send_message(chat_id=chat_id, text=reply_text, reply_markup=reply_markup)
    return -1


class HistoryModule:
    def __init__(self):
        conversation_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(history, pattern='^' + 'OPEN_HISTORY' + '$'),
                          CommandHandler('history', history)],
            states={
            },
            fallbacks=[],
            name="history_conversation",
            persistent=False,
        )

        self.conversation_handler = conversation_handler

    def get_handler(self):
        return self.conversation_handler
