from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from core.elements.templates import Templates
from core.log import Log
from core.user import User

help_command = Router()
help_command.name = "help"
log = Log()


@help_command.message(Command("help"), F.message.chat.type == "private")
async def help_tg_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)

    log.message(call="/help", user=user, message=message)

    await message.answer(Templates.HELP_COMMAND, parse_mode="markdown")


@help_command.message(F.text.lower() == "помощь", F.message.chat.type == "private")
async def help_text_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)

    log.message(call="text-command \"помощь\"", user=user, message=message)

    await message.answer(Templates.HELP_COMMAND, parse_mode="markdown")
