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

ChooseSpendCategory, SpendAmount, Description, TransactionAdded, ChooseType, ChooseIncomeCategory, IncomeAmount = range(
    7, 14)

def add_transaction(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    reply_text = 'Hey! Choose transaction type:'
    button_list = [
        InlineKeyboardButton("Income", callback_data='INCOME_TRANSACTION'),
        InlineKeyboardButton("Outcome", callback_data='OUTCOME_TRANSACTION'),
    ]
    markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=2))
    if query:
        chat_id = query.message.chat.id
    else:
        chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=reply_text, reply_markup=markup)
    return ChooseType


def choose_type_outcome(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    reply_text = 'Hey! Enter category of spending:'
    reply_keyboard = [
        ['Food', 'Pharmacy', 'Relations', 'Clothes']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    if query:
        context.bot.send_message(chat_id=query.message.chat.id, text=reply_text, reply_markup=markup)
    else:
        update.message.reply_text(reply_markup=markup, text=reply_text)
    return ChooseSpendCategory


def choose_type_income(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    reply_text = 'Hey! Enter category of Income:'
    reply_keyboard = [
        ['Salary', 'Random', 'Debt']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    if query:
        context.bot.send_message(chat_id=query.message.chat.id, text=reply_text, reply_markup=markup)
    else:
        update.message.reply_text(reply_markup=markup, text=reply_text)
    return ChooseIncomeCategory


def enter_spend_amount(update: Update, context: CallbackContext) -> None:
    amount = update.message.text
    context.user_data['amount'] = - int(amount)
    reply_text = 'Okay! Enter description or skip'
    button_list = [
        InlineKeyboardButton("Skip", callback_data='SKIP_ENTER_DESCRIPTION'),
    ]
    reply_markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=1))
    update.message.reply_text(text=reply_text, reply_markup=reply_markup)
    return Description


def enter_income_amount(update: Update, context: CallbackContext) -> None:
    amount = update.message.text
    context.user_data['amount'] = int(amount)
    reply_text = 'Okay! Enter description or skip'
    button_list = [
        InlineKeyboardButton("Skip", callback_data='SKIP_ENTER_DESCRIPTION'),
    ]
    reply_markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=1))
    update.message.reply_text(text=reply_text, reply_markup=reply_markup)
    return Description


def choose_spend_category(update: Update, context: CallbackContext) -> None:
    category = update.message.text
    context.user_data['category'] = category
    reply_text = 'Okay! Enter amount of money you spent:'
    update.message.reply_text(text=reply_text)
    return SpendAmount


def choose_income_category(update: Update, context: CallbackContext) -> None:
    category = update.message.text
    context.user_data['category'] = category
    reply_text = 'Okay! Enter amount of money you Got:'
    update.message.reply_text(text=reply_text)
    return IncomeAmount


def enter_description(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
        description = ''
    else:
        description = update.message.text
    context.user_data['description'] = description
    category = context.user_data['category']
    amount = context.user_data['amount']
    reply_text = f"New Transaction:\nCategory: {category} \nAmount: {amount} \nDescription: {description}\n"
    button_list = [
        InlineKeyboardButton("Done", callback_data='OPEN_BASE_MENU'),
    ]
    reply_markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=1))
    if query:
        chat_id = query.message.chat.id
    else:
        chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text=reply_text, reply_markup=reply_markup)
    api.user(chat_id).transactions.post(
        data={"category": category, "delta": amount, "time": 0, "description": description})
    return -1


class AddTransactionModule:
    def __init__(self):
        conversation_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(add_transaction, pattern='^' + 'OPEN_ADD_TRANSACTION' + '$'),
                          CommandHandler('add_transaction', add_transaction)],
            states={
                ChooseType: [CallbackQueryHandler(choose_type_income, pattern='^' + 'INCOME_TRANSACTION' + '$'),
                             CallbackQueryHandler(choose_type_outcome, pattern='^' + 'OUTCOME_TRANSACTION' + '$')],
                ChooseSpendCategory: [MessageHandler(Filters.text, choose_spend_category)],
                ChooseIncomeCategory: [MessageHandler(Filters.text, choose_income_category)],
                SpendAmount: [MessageHandler(Filters.text, enter_spend_amount)],
                IncomeAmount: [MessageHandler(Filters.text, enter_income_amount)],
                Description: [CallbackQueryHandler(enter_description, pattern='^' + 'SKIP_ENTER_DESCRIPTION' + '$'),
                              MessageHandler(Filters.text, enter_description)]
            },
            fallbacks=[],
            name="add_transaction_conversation",
            persistent=False,
        )

        self.conversation_handler = conversation_handler

    def get_handler(self):
        return self.conversation_handler
