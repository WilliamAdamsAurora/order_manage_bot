from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.elements.markups import base_markup, Markups
from core.elements.templates import Templates
from core.log import Log
from core.user import User

start_command = Router()
start_command.name = "start"
log = Log()


@start_command.message(CommandStart(), F.message.chat.type == "private")
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)
    markup = Markups.main() if user.is_admin else base_markup

    log.message(call="/start", user=user, message=message)

    await message.answer(Templates.START,
                         reply_markup=markup, parse_mode="markdown")



