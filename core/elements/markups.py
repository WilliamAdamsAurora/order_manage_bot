from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from core.locator import Locator

base_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Помощь"), KeyboardButton(text="Поиск")]
    ], resize_keyboard=True)


class Markups:
    @staticmethod
    def edit(order_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Изменить тариф", callback_data=f"edit_tariff {order_id}"),
                InlineKeyboardButton(text="Изменить Цену", callback_data=f"edit_cost {order_id}")
            ],
            [
                InlineKeyboardButton(text="Изменить дату", callback_data=f"edit_date {order_id}"),
                InlineKeyboardButton(text="Изменить кол-во человек", callback_data=f"edit_amount {order_id}")
            ],
            [
                InlineKeyboardButton(text="Изменить Пункт 1", callback_data=f"edit_point1 {order_id}"),
                InlineKeyboardButton(text="Изменить Пункт 2", callback_data=f"edit_point2 {order_id}")
            ],
            [
                InlineKeyboardButton(text="Добавить коментарий", callback_data=f"set_comment {order_id}")
            ],
            [
                InlineKeyboardButton(text="Подтвердить", callback_data=f"confirm {order_id}"),
                InlineKeyboardButton(text="Отменить заказ", callback_data=f"exit {order_id}")
            ],
        ])

    @staticmethod
    def tariffs(order_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Эконом", callback_data=f'set_tariff {order_id} Эконом'),
                InlineKeyboardButton(text="Комфорт", callback_data=f'set_tariff {order_id} Комфорт')
            ],
            [
                InlineKeyboardButton(text="Комфорт+", callback_data=f'set_tariff {order_id} Комфорт+'),
                InlineKeyboardButton(text="Минивэн", callback_data=f'set_tariff {order_id} Минивэн')
            ],
            [
                InlineKeyboardButton(text="Автобус", callback_data=f'set_tariff {order_id} Автобус')
            ],
            [
                InlineKeyboardButton(text="Другой", callback_data=f'set_custom_tariff {order_id}'),
                InlineKeyboardButton(text="Назад", callback_data=f'back {order_id}'),
            ]
        ])

    @staticmethod
    def cancel(order_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data=f"back {order_id}")],
        ])

    @staticmethod
    def exit() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text="Отмена")],
        ])

    @staticmethod
    def main() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text="Создать заказ"), KeyboardButton(text="Поиск")],
            [KeyboardButton(text="Помощь")]
        ])

    @staticmethod
    def location() -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
            [KeyboardButton(text='Отправить свою локацию 🗺️', request_location=True)],
            [KeyboardButton(text='Не отправлять')],
        ])

    @staticmethod
    def order_footer(order_id: int, point_a: str, point_b: str) -> InlineKeyboardMarkup:
        # Get coordinates -> list[float, float]
        raw_point_a = Locator.get_coordinates(point_a)
        raw_point_b = Locator.get_coordinates(point_b)

        # Format coordinates: list[float, float] -> $latitude,$longitude
        point1 = ",".join([str(raw_point_a[0]), str(raw_point_a[1])])
        point2 = ",".join([str(raw_point_b[0]), str(raw_point_b[1])])

        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Коментарий", callback_data=f"comment {order_id}"),
                InlineKeyboardButton(text="Принять", callback_data=f"accept {order_id}")],
            [
                InlineKeyboardButton(text="Маршрут", url=f"https://www.google.com/maps/dir/{point1}/{point2}")
            ]
        ])
