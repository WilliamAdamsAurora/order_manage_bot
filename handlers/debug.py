from aiogram.types import Message, InputMediaDocument, FSInputFile
from aiogram.filters import Command
from aiogram import Router, F

debug_command = Router()
debug_command.name = "debug"


@debug_command.message(Command("debug"), F.message.chat.type == "private")
async def command_debug_handler(message: Message):
    await message.answer_media_group([
        InputMediaDocument(type="document", media=FSInputFile(path="./logs/core.log")),
        InputMediaDocument(type="document", media=FSInputFile(path="./logs/db.log")),
        InputMediaDocument(type="document", media=FSInputFile(path="./logs/locator.log")),
        InputMediaDocument(type="document", media=FSInputFile(path="./logs/orders.log")),
        InputMediaDocument(type="document", media=FSInputFile(path="./logs/handlers.log")),
        InputMediaDocument(type="document", media=FSInputFile(path="./logs/users.log")),
        InputMediaDocument(type="document", media=FSInputFile(path="./logs/messages.log")),
    ])
