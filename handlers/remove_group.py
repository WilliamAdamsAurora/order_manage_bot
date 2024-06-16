from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from core import Core
from core.elements.markups import Markups
from core.user import User
from core.log import Log

remove_group_command = Router()
remove_group_command.name = "remove group"
log = Log()


@remove_group_command.message(Command('remove_group'))
async def remove_group(message: Message) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)

    log.message(call="/remove_group", user=user, message=message)

    chat_id = message.chat.id
    core = Core()

    if chat_id > 0:
        await message.answer("Данная команда доступна только в группах, для отключения уведомлений в личных сообщениях"
                             "воспользуйтесь кнойпкой *\"поиск\"*", parse_mode="markdown", reply_markup=Markups.main())
    else:
        chat_exist_query = core.check_exist(
            table="config",
            condition=f"value = {chat_id}"
        )

        if chat_exist_query:
            core.delete_group(chat_id)
            await message.answer(f"чат №{chat_id} отключён от уведомлений")
        else:
            await message.answer(f"чат №{chat_id} не подключен к уведомлениям")
