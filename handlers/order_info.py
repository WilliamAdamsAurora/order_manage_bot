from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram import Router, F

from core.elements.markups import Markups
from core.elements.templates import Templates
from core.order import Order

order_command = Router()
order_command.name = "order_command"


@order_command.message(Command("order"))
async def report(message: Message):
    order_id = int(message.text.split(" ")[1])

    order = Order(order_id)

    await message.answer(str(order), reply_markup=Markups.order_footer(order_id, order.point_a, order.point_b))
