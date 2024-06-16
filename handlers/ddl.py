from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from core import Database

ddl_command = Router()
ddl_command.name = "ddl"


@ddl_command.message(Command('ddl'), F.message.chat.type == "private")
async def ddl_command_handler(message: Message) -> None:
    d = Database()
    await message.answer(f">>> {d.ddl(message.text.split(' ', maxsplit=1)[1])}")
