from datetime import datetime

import icecream
from loguru import logger

from core import utils
from core.database import Database
from core.elements.templates import Templates
from core.locator import Locator

logger.add("logs/orders.log", format="\n{time} {level} \n{message}\n",
           level="DEBUG", rotation="10 MB", compression="zip")

# TODO var rename
# TODO refactor
# TODO optimization


class Order(Database):
    _id: int                    # [protected] order ID
    tariff: str                 # Tariff
    cost: str                   # Cost of order
    date: str                   # Date and time of departure
    status: str                 # order status
    amount: int                 # amount of passenger
    comment: str                # comment for order [not longer 200 character]

    point_a: str                # Departure point
    point_b: str                # Point of destination
    distance: int               # Distance length [Locator.get_distance()]
    unit: str                   # unit of distance [km | m]
    delivery_time: int          # Needed time to deliver order [core.utils.get_delivery_time()]

    @logger.catch
    def __init__(self, order_id: int = None, data: list = None):
        # initialization of super-class: Database
        super().__init__()

        if data is not None:
            order_id = Order.create_order(data)

        # Getting order info from database
        # =================================
        # Format of data:
        # (0:id, 1:tariff, 2:cost, 3:date, 4:status, 5:people_amount, 6:pointA, 7:pointB, 8:register_date, 9:comment,)
        order = self.ddl(f"SELECT * FROM orders WHERE id = {order_id}")[0]
        icecream.ic(order)

        self._id = int(order[0])
        self.tariff = order[1]
        self.cost = order[2]
        self.date = order[3]
        self.status = order[4]
        self.amount = int(order[5])
        self.point_a = order[6]
        self.point_b = order[7]
        self.comment = order[9]

        raw_distance = Locator.get_distance(self.point_a, self.point_b)

        self.distance = raw_distance["value"]
        self.unit = raw_distance["unit"]
        self.delivery_time = utils.get_delivery_time(self.distance)

    @logger.catch
    def __str__(self):
        return Templates.ORDER_INFO.substitute(
            date=self.date,
            distance=self.distance,
            unit=self.unit,
            cost=self.cost,
            tariff=self.tariff,
            pointA=self.point_a,
            pointB=self.point_b,
            amount=self.amount,
            status=self.status,
            delivery_time=self.delivery_time
        )

    @logger.catch
    def __format__(self, format_spec) -> str:
        match format_spec:
            case "tariff":
                return self.tariff
            case "cost":
                return self.cost

    @logger.catch
    def get_id(self):
        return self._id

    @staticmethod
    @logger.catch
    def create_order(data: list) -> int:
        logger.debug(f"order.py:79\ncreate_order()\n└ data: {data}")


        # Generating ID
        order_id = utils.generate_order_id()

        logger.info("INSERT INTO orders (id, tariff, cost, date, people_amount, pointA, pointB, register_date)"
                    f"VALUES ({order_id}, '{data[0]}', '{data[1]}', '{data[2]}', {data[3]}, '{data[4]}', "
                    f"'{data[5]}', '{datetime.now()}')")

        Database().ddl("INSERT INTO orders (id, tariff, cost, date, people_amount, pointA, pointB, register_date)"
                       f"VALUES ({order_id}, '{data[0]}', '{data[1]}', '{data[2]}', {data[3]}, '{data[4]}', "
                       f"'{data[5]}', '{datetime.now()}')")
        logger.info(f"\nСоздан новый заказ №{order_id}")

        return order_id

    @logger.catch
    def update_parameter(self, parameter: str, value):
        logger.debug(f"order.py:109\nupdate_parameter()\n└ parameter: {parameter}\n└ value: {value}")

        self.ddl(f"UPDATE orders SET {parameter} = {value} WHERE id = {self._id}")

        logger.info(f"Параметр ${parameter} у заказа №{self._id} обновлён на {value}")

    @staticmethod
    @logger.catch
    def delete_order(order_id):
        Database().ddl(f"DELETE FROM `orders` WHERE id = {order_id}")
