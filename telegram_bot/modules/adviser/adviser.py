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

MenuController, SetupDailyExpenseLimit, EnableDailyExpenseLimit, AdviserHome = range(1, 5)

def open_adviser(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    reply_text = 'Hey! This is Advising part of my functionality. What is you interest?'
    button_list = [
        InlineKeyboardButton("Prevent Buying (AI)", callback_data='PREVENT_BUYING'),
        InlineKeyboardButton("Reduce Daily Expenses", callback_data='DAILY_EXPENSE_LIMIT'),
        InlineKeyboardButton("Back to Menu", callback_data='END_ADVISER'),
    ]
    markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=2))
    if query:
        query.edit_message_text(text=reply_text, reply_markup=markup)
    else:
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=reply_text, reply_markup=markup)
    return MenuController

def daily_expense_menu(update: Update, context: CallbackContext) -> None:
    chat_id = utils.get_chat_id(update)
    limit = api.user(chat_id).daily_expense_limit.get()
    if not limit:
        reply_text = 'This feature will help you to reduce your daily expense limit. Enable it!'
        button_list = [
            InlineKeyboardButton("Enable", callback_data='START_ENABLING_DAILY_EXPENSE_LIMIT'),
            InlineKeyboardButton("Back", callback_data='OPEN_ADVISER'),
        ]
    else:
        reply_text = 'Your daily limit is: {}'.format(limit.limit)
        button_list = [
            InlineKeyboardButton("Disable", callback_data='DISABLE_DAILY_EXPENSE_LIMIT'),
            InlineKeyboardButton("Back", callback_data='OPEN_ADVISER'),
        ]
    markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=2))
    query = update.callback_query
    if query:
        query.edit_message_text(text=reply_text, reply_markup=markup)
    else:
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text=reply_text, reply_markup=markup)
    return SetupDailyExpenseLimit

def prevent_unexpected_menu(update: Update, context: CallbackContext) -> None:
    return

def start_enabling_daily_expense_limit(update: Update, context: CallbackContext):
    reply_text = 'Enter daily expense limit:'
    chat_id = utils.get_chat_id(update)
    context.bot.send_message(chat_id=chat_id, text=reply_text)
    return EnableDailyExpenseLimit

def enable_daily_expense_limit(update: Update, context: CallbackContext):
    input_limit = int(update.message.text)
    chat_id = utils.get_chat_id(update)
    user = api.user.get(chat_id)
    limit = api.daily_expense_limit.post(data={"limit": input_limit, "user": user["_id"]["$oid"]})
    button_list = [
        InlineKeyboardButton("Done", callback_data='DAILY_EXPENSE_LIMIT'),
    ]
    reply_text = 'Daily Expense limit successfully set!'
    markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=1))
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=reply_text, reply_markup=markup)
    return MenuController

def disable_daily_expense_limit(update: Update, context: CallbackContext):
    chat_id = utils.get_chat_id(update)
    limit = api.user(chat_id).daily_expense_limit.get()
    api.daily_expense_limit.delete(limit["_id"]["$oid"])
    reply_text = 'Daily Expense limit successfully disabled'
    button_list = [
        InlineKeyboardButton("Done", callback_data='DAILY_EXPENSE_LIMIT'),
    ]
    markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=1))
    context.bot.send_message(chat_id=chat_id, text=reply_text, reply_markup=markup)
    return MenuController

class AdviserModule:
    def __init__(self, dispatcher, base_menu):
        conversation_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(open_adviser, pattern='^' + 'OPEN_ADVISER' + '$'),
                          CommandHandler('adviser', open_adviser)],
            states={
                AdviserHome: [CallbackQueryHandler(open_adviser, pattern='^' + 'OPEN_ADVISER' + '$')],
                MenuController: [CallbackQueryHandler(daily_expense_menu, pattern='^' + 'DAILY_EXPENSE_LIMIT' + '$'),
                                 CallbackQueryHandler(prevent_unexpected_menu, pattern='^' + 'PREVENT_BUYING' + '$')],
                SetupDailyExpenseLimit: [CallbackQueryHandler(start_enabling_daily_expense_limit, pattern='^' + 'START_ENABLING_DAILY_EXPENSE_LIMIT' + '$'),
                                         CallbackQueryHandler(disable_daily_expense_limit, pattern='^' + 'DISABLE_DAILY_EXPENSE_LIMIT' + '$'),
                                         CallbackQueryHandler(open_adviser, pattern='^' + 'OPEN_ADVISER' + '$')],
                EnableDailyExpenseLimit: [MessageHandler(Filters.text, enable_daily_expense_limit)]
            },
            fallbacks=[CallbackQueryHandler(base_menu, pattern='^' + 'END_ADVISER' + '$')],
            name="add_transaction_conversation",
            persistent=False,
        )
        self.conversation_handler = conversation_handler
        dispatcher.add_handler(conversation_handler)

    def get_handler(self):
        return self.conversation_handler
