import telebot


def inline_keyboard(type: str, request: dict) -> telebot.types.InlineKeyboardMarkup:
    if type == "AcceptKeyboard":
        order_id = request["order_id"]

        inline = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton(text="Принять",
                                                  callback_data=f'accept {order_id}')
        inline.add(btn1)

        return inline
    elif type == "Empty":
        return telebot.types.InlineKeyboardMarkup()
    elif type == "ConfirmKeyboard":
        order_id = request["order_id"]

        inline = telebot.types.InlineKeyboardMarkup()
        btn1 = telebot.types.InlineKeyboardButton(text="Изменить",
                                                  callback_data=f'order_edit_keyboard {order_id}')
        btn2 = telebot.types.InlineKeyboardButton(text="Подтвердить",
                                                  callback_data=f'confirm {order_id}')
        inline.add(btn1, btn2)

        return inline
    elif type == "EditKeyboard":
        order_id = request["order_id"]

        inline = telebot.types.InlineKeyboardMarkup()

        btn1 = telebot.types.InlineKeyboardButton(text="тариф", callback_data=f'tariffs {order_id}')
        btn2 = telebot.types.InlineKeyboardButton(text="время", callback_data=f'edit_time {order_id}')
        btn3 = telebot.types.InlineKeyboardButton(text="стоимость", callback_data=f'edit_cost {order_id}')
        btn4 = telebot.types.InlineKeyboardButton(text="кол-во человек", callback_data=f'edit_amount {order_id}')
        btn5 = telebot.types.InlineKeyboardButton(text="пункт отправления", callback_data=f'edit_point1 {order_id}')
        btn6 = telebot.types.InlineKeyboardButton(text="пункт назначения", callback_data=f'edit_point2 {order_id}')
        btn7 = telebot.types.InlineKeyboardButton(text="Назад", callback_data=f'back {order_id}')

        inline.add(btn1, btn2)
        inline.add(btn3, btn4)
        inline.add(btn5, btn6)
        inline.add(btn7)

        return inline

