from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import utils
from api.api import api

RegName, RegCurrency, RegBalance = range(3, 6)


def register(update: Update, context: CallbackContext) -> None:
    print('register....')
    reply_text = 'Enter you Name:'
    update.message.reply_text(reply_text)
    return RegName


def enter_name(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    context.user_data['name'] = text
    reply_text = 'Your name is ' + text
    update.message.reply_text(reply_text)
    chat_id = update.message.chat_id
    created_user = api.user.post(data={"chat_id": chat_id, "name": text})
    context.user_data["bd_id"] = created_user.id
    reply_text = 'Enter currency of you wallet:'
    reply_keyboard = [
        ['$', '€', '₽']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text(reply_markup=markup, text=reply_text)
    return RegCurrency


def enter_currency(update: Update, context: CallbackContext) -> None:
    currency = update.message.text
    context.user_data['currency'] = currency
    reply_text = 'Your currency is "{}"'.format(currency)
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(text=reply_text, reply_markup=reply_markup)
    update.message.reply_text('Enter you current balance: ')
    return RegBalance


def enter_balance(update: Update, context: CallbackContext):
    balance = update.message.text
    context.user_data['balance'] = balance
    reply_text = 'Your balance is "{}{}" '.format(balance, context.user_data['currency'])
    update.message.reply_text(reply_text)

    balance = context.user_data['balance']
    currency = context.user_data['currency']
    chat_id = update.message.chat_id
    api.user(chat_id).money.post(data={"balance": balance, "currency": currency})
    name = context.user_data['name']
    reply_text = f"Your data:, \n {name} \n balance: {balance}{currency}\n"
    button_list = [
        InlineKeyboardButton("Done", callback_data='OPEN_BASE_MENU'),
    ]
    reply_markup = InlineKeyboardMarkup(utils.build_menu(button_list, n_cols=1))
    update.message.reply_text(text=reply_text, reply_markup=reply_markup)
    return -1


class RegistrationModule:

    def __init__(self, dispatcher, base_menu):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('register', register)],
            states={
                RegName: [
                    MessageHandler(Filters.text, enter_name),
                ],
                RegCurrency: [
                    MessageHandler(
                        Filters.regex('^($|€|₽)$'), enter_currency
                    )
                ],
                RegBalance: [
                    MessageHandler(Filters.text, enter_balance)
                ],
            },
            fallbacks=[],
            name="registration_conversation",
            persistent=False,
        )

        self.conversation_handler = conversation_handler
        dispatcher.add_handler(conversation_handler)

    def get_handler(self):
        return self.conversation_handler
