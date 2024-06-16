from datetime import datetime

from loguru import logger

from core import Database

logger.add("logs/core.log", format="\n{time} {level} \n{message}\n", level="DEBUG", rotation="3:00", compression="zip")

# TODO log
# TODO var rename
# TODO refactor
# TODO optimization


@logger.catch
def generate_order_id() -> int:
    """
    <= GENERATING ID =>

        The algorithm requests the time, then takes the number of microseconds for the current time,
    if there is no such ID in the database, the new order is assigned this number, and if such ID
    exists, the cycle is repeated.
    """

    while True:
        time = datetime.now()
        microseconds = time.microsecond

        order = Database().ddl(f"SELECT * FROM orders WHERE id = '{microseconds}'")
        if not order:
            logger.debug(f"utils.py:31\ngenerate_order_id()\n└ return: {microseconds}")
            return microseconds
        else:
            pass


@logger.catch
def get_delivery_time(distance: int):
    """
    Get the approximate time in which the distance will be passed

    :param distance: distance between two points
    :return: formated string with numbers of hours ,
    """
    logger.debug(f"utils.py:45\nget_delivery_time()\n└ distance: {distance}")

    hours = (distance / 100) * 2  # average speed is 50km/h
    if round(hours) == 0:
        return "<1 часа"
    elif round(hours) == 1:
        return "1 час"
    elif 1 < round(hours) < 5:
        return f"{round(hours)} часа"
    else:
        return f"{round(hours)} часов"
