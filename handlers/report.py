from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from core.elements.templates import Templates

report_command = Router()
report_command.name = "report"


@report_command.message(Command("report"))
async def report(message: Message):
    await message.bot.send_message(chat_id=5147993400, text=Templates.REPORT.substitute(
        user=message.from_user.username,
        message=message.text
    ))
