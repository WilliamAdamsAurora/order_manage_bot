from aiogram import Router, F
from aiogram.types import Message, Location
from loguru import logger

from core.elements.markups import Markups
from core.locator import Locator
from core.user import User

search_command = Router()
search_command.name = "search"
logger.add("logs/handlers.log", format="\n{time} {level} \n{message}\n",
           level="DEBUG", rotation="10 MB", compression="zip")


@search_command.message(F.location)
@logger.catch
async def geo(message: Location):
    loc = Locator()
    user = User(message.from_user.id)

    new_city = loc.get_point_name((message.location.latitude, message.location.longitude))

    if new_city['type'] == "state":
        await message.bot.send_message(message.from_user.id, "К сожалению не удалось обработать данные",
                                       reply_markup=Markups.main())
    else:
        user.ddl("UPDATE users SET position = '{new_city}' WHERE id = {id}".format(
            new_city=new_city['name'], id=user.get_id)
        )

        await message.bot.send_message(message.from_user.id, "Геоданные сохранены", reply_markup=Markups.main())


@search_command.message(F.text == "Не отправлять", F.chat.type == "private")
@logger.catch
async def set_group1(message: Message) -> None:
    await message.bot.send_message(message.from_user.id, "Подключение и настройка завершены", reply_markup=Markups.main())


@search_command.message(F.text == "Поиск", F.chat.type == "private")
@logger.catch
async def set_group(message: Message) -> None:
    user = User(message.from_user.id)

    if user.role == "driver":
        user.set_role("user")
        await message.answer(f"Уведомления отключены", reply_markup=Markups.main())
    else:
        user.set_role("driver")
        await message.answer(f"Уведомления подключены, пожалуйста предоставте ваши геоданные для более удобной работы",
                             reply_markup=Markups.location())
