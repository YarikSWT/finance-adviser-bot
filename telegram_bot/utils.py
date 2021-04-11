
def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def get_chat_id(update):
    query = update.callback_query
    if query:
        chat_id = query.message.chat.id
    else:
        chat_id = update.message.chat_id
    return chat_id