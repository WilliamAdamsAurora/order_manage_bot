from aiogram import Router, F
from aiogram.types import Message

from core.elements.markups import Markups
from core.elements.templates import Templates
from core.log import Log
from core.user import User

msg_control = Router()
msg_control.name = "msg_control"
log = Log()


@msg_control.message(F.chat.type == "private")
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)

    log.message(call="msg", user=user, message=message)

    if user.action == "ORDER CREATING":
        await message.delete()
    else:
        await message.answer(Templates.START, reply_markup=Markups.main())


@msg_control.message(F.text.lower() == "назад", F.chat.type == "private")
async def start_creating_order(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)

    log.message(call=message.text, user=user, message=message)

    await message.answer(Templates.START, reply_markup=Markups.main())


@msg_control.message(F.text.lower() == "отмена", F.chat.type == "private")
async def start_creating_order(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)

    log.message(call=message.text, user=user, message=message)

    await message.answer(Templates.START, reply_markup=Markups.main())
