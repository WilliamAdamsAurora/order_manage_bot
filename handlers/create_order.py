import aiogram.exceptions
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import Router, F, types
from icecream import ic

from core import utils, Core, Database
from core.elements.templates import Templates
from core.locator import Locator
from core.order import Order
from core.elements.markups import Markups
from core.user import User
from core.log import Log

creater = Router()
creater.name = "creater"
log = Log()


class OrderCreater(StatesGroup):
    raw_data = State()  # [string] Text data with parameters of order from message
    confirm = State()  # confirm step

    tariff = State()  # [string] Tariff
    cost = State()  # [string] Cost
    point1 = State()  # [string] Departure point
    point2 = State()  # [string] Point of destination
    date = State()  # [string] Date and time of departure
    amount = State()  # [integer] Person count
    comment = State()  # [string] Order comment
    order_id = State()  # [integer] ID


@creater.message(F.text == "Создать заказ", F.chat.type == "private")
async def start_creating_order(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)
    fsm = {
        "state": "__init__.OrderCreater -> OrderCreater.raw_data"
    }

    log.action(call=message.text, user=user, message=message, fsm=fsm)

    user.set_action("ORDER CREATING")

    await message.bot.send_photo(chat_id=message.from_user.id,
                                 photo=types.FSInputFile(path="./storage/img/create_order.png"),
                                 caption=Templates.ORDER_CREATE_HELP,
                                 reply_markup=Markups.exit())

    await state.set_state(OrderCreater.raw_data)


@creater.message(OrderCreater.raw_data, F.chat.type == "private")
async def get_order_raw_data(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)
    fsm = {
        "state": "OrderCreater.raw_data -> OrderCreater.confirm"
    }

    log.action(call=message.text, user=user, message=message, fsm=fsm)

    if message.text == "Отмена":
        await state.clear()
        await message.answer("Создание заказа отмененно", reply_markup=Markups.main())
    else:
        # Getting raw_data
        await state.update_data(raw_data=message.text)
        state_data: dict = await state.get_data()
        split_data: list = state_data['raw_data'].split("\n")

        if len(split_data) == 6:
            order = Order(data=split_data)
            await message.answer(str(order), reply_markup=Markups.edit(order.get_id()))
            await state.update_data(order_id=order.get_id())

            await state.set_state(OrderCreater.confirm)
        else:
            await message.answer("Неверный формат ввода")


@creater.message(OrderCreater.tariff, F.chat.type == "private")
async def edit_tariff(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)
    fsm = {
        "state": "OrderCreater.tariff"
    }

    log.action(call=message.text, user=user, message=message, fsm=fsm)

    state_data = await state.get_data()
    order_id: int = state_data['order_id']

    # Update tariff of order
    order = Order(order_id)
    order.update_parameter("tariff", f"'{message.text}'")
    order = Order(order_id)

    await message.answer(str(order), reply_markup=Markups.edit(order_id))


@creater.message(OrderCreater.cost, F.chat.type == "private")
async def edit_cost(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)
    fsm = {
        "state": "OrderCreater.cost"
    }

    log.action(call=message.text, user=user, message=message, fsm=fsm)

    state_data = await state.get_data()
    order_id: int = state_data['order_id']

    # Update cost of order
    order = Order(order_id)
    order.update_parameter("cost", f"'{message.text}'")
    order = Order(order_id)

    await message.answer(str(order), reply_markup=Markups.edit(order_id))


@creater.message(OrderCreater.amount, F.chat.type == "private")
async def edit_amount(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)
    fsm = {
        "state": "OrderCreater.amount"
    }

    log.action(call=message.text, user=user, message=message, fsm=fsm)

    state_data = await state.get_data()
    order_id = state_data['order_id']

    # Update amount of person
    order = Order(order_id)
    order.update_parameter("people_amount", f"'{message.text}'")
    order = Order(order_id)

    await message.answer(str(order), reply_markup=Markups.edit(order_id))


@creater.message(OrderCreater.comment, F.chat.type == "private")
async def edit_comment(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)
    fsm = {
        "state": "OrderCreater.comment"
    }

    log.action(call=message.text, user=user, message=message, fsm=fsm)

    state_data = await state.get_data()
    order_id: int = state_data['order_id']

    # Update order comment
    order = Order(order_id)
    order.update_parameter("comment", f"'{message.text}'")
    order = Order(order_id)

    await message.answer(str(order), reply_markup=Markups.edit(order_id))


@creater.message(OrderCreater.point1, F.chat.type == "private")
async def edit_point1(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)
    fsm = {
        "state": "OrderCreater.point1"
    }

    log.action(call=message.text, user=user, message=message, fsm=fsm)

    state_data = await state.get_data()
    order_id: int = state_data['order_id']

    # Update departure point
    order = Order(order_id)
    order.update_parameter("pointA", f"'{message.text}'")
    order = Order(order_id)

    await message.answer(str(order), reply_markup=Markups.edit(order_id))


@creater.message(OrderCreater.point2, F.chat.type == "private")
async def edit_point2(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)
    fsm = {
        "state": "OrderCreater.point2"
    }

    log.action(call=message.text, user=user, message=message, fsm=fsm)

    state_data = await state.get_data()
    order_id: int = state_data['order_id']

    # Update point of destination
    order = Order(order_id)
    order.update_parameter("pointB", f"'{message.text}'")
    order = Order(order_id)

    await message.answer(str(order), reply_markup=Markups.edit(order_id))


@creater.message(OrderCreater.date, F.chat.type == "private")
async def edit_date(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    user = User(user_id, username)
    fsm = {
        "state": "OrderCreater.date"
    }

    log.action(call=message.text, user=user, message=message, fsm=fsm)

    state_data = await state.get_data()
    order_id: int = state_data['order_id']

    # Update time of departure
    order = Order(order_id)
    order.update_parameter("date", f"'{message.text}'")
    order = Order(order_id)

    await message.answer(str(order), reply_markup=Markups.edit(order_id))


@creater.callback_query(F.data.split(" ")[0] == "edit_tariff")
async def get_tariffs_keys(call: types.CallbackQuery) -> None:
    order_id = int(call.data.split(" ")[1])  # Get order ID from CallBack data
    order = Order(order_id)

    await call.message.edit_text(text=str(order), reply_markup=Markups.tariffs(order_id))


@creater.callback_query(F.data.split(" ")[0] == "set_custom_tariff")
async def get_custom_tariff(call: types.CallbackQuery, state: FSMContext) -> None:
    order_id = int(call.data.split(" ")[1])  # Get order ID from CallBack data

    await call.message.edit_text(text="Введите тариф", reply_markup=Markups.cancel(order_id))
    await state.set_state(OrderCreater.tariff)


@creater.callback_query(F.data.split(" ")[0] == "set_tariff")
async def t1(call: types.CallbackQuery) -> None:
    new_tariff = call.data.split(" ")[2]  # Get tariff from CallBack data
    order_id = int(call.data.split(" ")[1])

    order = Order(order_id)
    order.update_parameter("tariff", f"'{new_tariff}'")
    order = Order(order_id)

    await call.message.edit_text(text=str(order), reply_markup=Markups.edit(order_id))


@creater.callback_query(F.data.split(" ")[0] == "edit_cost")
async def get_new_cost(call: types.CallbackQuery, state: FSMContext) -> None:
    order_id = int(call.data.split(" ")[1])  # Get order ID from CallBack data

    await call.message.edit_text(text="Введите Цену", reply_markup=Markups.cancel(order_id))
    await state.set_state(OrderCreater.cost)


@creater.callback_query(F.data.split(" ")[0] == "edit_amount")
async def het_new_amount(call: types.CallbackQuery, state: FSMContext) -> None:
    order_id = int(call.data.split(" ")[1])  # Get order ID from CallBack data

    await call.message.edit_text(text="Введите количество человек", reply_markup=Markups.cancel(order_id))
    await state.set_state(OrderCreater.amount)


@creater.callback_query(F.data.split(" ")[0] == "set_comment")
async def get_new_comment(call: types.CallbackQuery, state: FSMContext) -> None:
    order_id = int(call.data.split(" ")[1])  # Get order ID from CallBack data

    await call.message.edit_text(text="Введите коментарий", reply_markup=Markups.cancel(order_id))
    await state.set_state(OrderCreater.comment)


@creater.callback_query(F.data.split(" ")[0] == "edit_date")
async def get_new_date(call: types.CallbackQuery, state: FSMContext) -> None:
    order_id = int(call.data.split(" ")[1])  # Get order ID from CallBack data

    await call.message.edit_text(text="Введите новое время отправки", reply_markup=Markups.cancel(order_id))
    await state.set_state(OrderCreater.date)


@creater.callback_query(F.data.split(" ")[0] == "edit_point1")
async def get_new_point1(call: types.CallbackQuery, state: FSMContext) -> None:
    order_id = int(call.data.split(" ")[1])  # Get order ID from CallBack data

    await call.message.edit_text(text="Введите новый пункт отправления", reply_markup=Markups.cancel(order_id))
    await state.set_state(OrderCreater.point1)


@creater.callback_query(F.data.split(" ")[0] == "edit_point2")
async def get_new_point2(call: types.CallbackQuery, state: FSMContext) -> None:
    order_id = int(call.data.split(" ")[1])  # Get order ID from CallBack data

    await call.message.edit_text(text="Введите новый пункт назначения", reply_markup=Markups.cancel(order_id))
    await state.set_state(OrderCreater.point2)


@creater.callback_query(F.data.split(" ")[0] == "comment")
async def edit_comment(call: types.CallbackQuery):
    order = Order(int(call.data.split(" ")[1]))

    await call.answer(order.comment, show_alert=True)


@creater.callback_query(F.data.split(" ")[0] == "back")
async def q2(call: types.CallbackQuery):
    order_id = int(call.data.split(" ")[1])
    order = Order(order_id)

    await call.message.edit_text(text=str(order), reply_markup=Markups.edit(order_id))


@creater.callback_query(F.data.split(" ")[0] == "confirm")
async def complete(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    order_id: int = state_data['order_id']
    order = Order(order_id)
    core = Core()
    user = User(call.from_user.id)

    await call.message.delete()
    await call.message.answer(text=f"Заказ №{order.get_id()} сформирован", reply_markup=Markups.main())
    order.update_parameter(parameter="status", value="'сформирован'")
    await state.clear()

    user.set_action("MAIN")

    for chat in core.get_chats():
        message_text: str = Templates.order_info(order=order, mode="new order", to="chat")

        await call.message.bot.send_message(chat_id=chat, text=message_text,
                                            reply_markup=Markups.order_footer(order_id, order.point_a, order.point_b))

    for user_id in core.get_drivers():
        driver = User(user_id)

        if driver.position is None:
            message_text: str = Templates.order_info(order=order, mode="new order", to="no-geo user")
        else:
            raw_distance: dict = Locator.get_distance(driver.position, order.point_a)
            ic(raw_distance)
            if raw_distance is None:
                message_text: str = Templates.order_info(order=order, mode="new order", to="geo user",
                                                         distance=raw_distance['value'], unit=raw_distance['unit'])
            else:
                message_text: str = Templates.order_info(order=order, mode="new order", to="no-geo user")
        try:
            await call.message.bot.send_message(chat_id=user_id, text=message_text,
                                                reply_markup=Markups.order_footer(order_id, order.point_a,
                                                                                  order.point_b))
        except aiogram.exceptions.TelegramBadRequest:
            print(f"не удалось отправить уведомление пользователю @{driver.username}")


@creater.callback_query(F.data.split(" ")[0] == "accept")
async def acc(call: types.CallbackQuery):
    driver = User(call.from_user.id)
    order = Order(int(call.data.split(" ")[1]))
    core = Core()

    if driver.position == "":
        message_text = f"@{call.from_user.username} принял заказ №{order.get_id()}\n\n{str(order)}"
    else:
        raw_distance_to_order = Locator.get_distance(driver.position, order.point_a)
        distance_to_order = f"{raw_distance_to_order['value']} {raw_distance_to_order['unit']}"
        message_text = (f"@{driver.username} принял заказ №{order.get_id()}"
                        f"({distance_to_order} от пункта отправления)\n\n{str(order)}")

    await call.answer(text=f"Вы приняли заказ №{order.get_id()}", show_alert=True,
                      reply_markup=Markups.main())

    for admin in core.get_admins():
        try:
            await call.message.bot.send_message(chat_id=admin, text=message_text)
        except aiogram.exceptions.TelegramBadRequest:
            print(f"не удалось отправить данные пользователю {admin}")


@creater.callback_query(F.data.split(" ")[0] == "exit")
async def exit(call: types.CallbackQuery, state: FSMContext):
    user = User(call.from_user.id)
    Order.delete_order(call.data.split(" ")[1])
    await state.clear()
    user.set_action("MAIN")
    await call.message.answer("Создание заказа отмененно", reply_markup=Markups.main())
    await call.message.delete()
