from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from core import Core
from core.elements.markups import base_markup
from core.log import Log
from core.user import User

login_command = Router()
login_command.name = "login"
log = Log()


class Login(StatesGroup):
    login_key = State()
    confirm = State()


@login_command.message(Command("login"), F.message.chat.type == "private")
async def login(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(tg_id=user_id, username=username)

    log.message(call="/login", user=user, message=message)

    if user.is_admin:
        await message.answer("Вы уже авторизованны")
    else:
        await state.set_state(Login.login_key)
        await message.answer("Введите ключ авторизации")


@login_command.message(Login.login_key, F.message.chat.type == "private")
async def login2(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username

    fsm = {
        "state": "Login.login_key"
    }
    user = User(tg_id=user_id, username=username)
    core = Core()

    log.action(call=f"login enter {message.text}", user=user, message=message, fsm=fsm)

    if message.text == "Отмена":
        await message.answer("Авторизация прервана", reply_markup=base_markup)
        await state.clear()
    else:
        if core.check_login_key(message.text):
            await message.answer("Вы успешно авторизованы")
            user.set_admin()
            await state.clear()
        else:
            await state.set_state(Login.login_key)
            await message.answer("Неверный ключ, попробуйте ещё")

