from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core import Core
from core.elements.markups import Markups
from core.log import Log
from core.user import User

set_group_command = Router()
set_group_command.name = "set group"
log = Log()


@set_group_command.message(Command('set_group'))
async def set_group(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)

    log.message(call="/set_group", user=user, message=message)

    chat_id = message.chat.id
    core = Core()

    if chat_id > 0:
        await message.answer("Данная команда доступна только в группах, для подключения уведомлений в личных сообщениях"
                             "воспользуйтесь кнойпкой *\"поиск\"*", parse_mode="markdown", reply_markup=Markups.main())
    else:
        chat_exist_query = core.check_exist(
            table="config",
            condition=f"value = {chat_id}"
        )

        if chat_exist_query:
            await message.answer(f"чат №{chat_id} уже подключён к уведомлениям")
        else:
            core.add_chat(chat_id)
            await message.answer(f"чат №{chat_id} подключён к уведомлениям")
