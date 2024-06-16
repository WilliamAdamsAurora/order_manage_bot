from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.elements.markups import Markups
from core.order import Order

order_command = Router()
order_command.name = "order_command"


@order_command.message(Command("order"))
async def report(message: Message):
    order_id = int(message.text.split(" ")[1])

    order = Order(order_id)

    await message.answer(str(order), reply_markup=Markups.order_footer(order_id, order.point_a, order.point_b))
