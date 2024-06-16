from string import Template


class Templates:

    START = ("Добро пожаловать в бот для управления и принятие заказов\n\n Бот обновлён до новой версии, перед началом"
             " использования рекомендуется прочитать раздел помощь с помощью команды /help")

    REPORT = Template("Репорт от пользователя @$user\n\n$message")

    ORDER_INFO = Template("Выбор авто\n\n"
                          "$date\n"
                          "Расстояние ~$distance $unit\n"
                          "Цена: $cost\n"
                          "Тариф: $tariff\n"
                          "\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                          "Пункт отправления: $pointA\n\n"
                          "Пункт назначения: $pointB"
                          "\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
                          "$amount человек\n"
                          "Статус заказа: $status\n"
                          "время доставки: $delivery_time\n")

    ORDER_INFO_HEADERS = {
        "common": Template("Новый заказ №$order_id"),
        "geo user": Template("Новый заказ №$order_id ($distance $unit от вас)")
    }

    ORDER_CREATE_HELP = "Введите данные заказа как показано на фото, каждое значение должно быть на новой строке"

    HELP_COMMAND = ("Для создания заказа необходимо написать *\"Создать заказ\"* после чего следовать инструкции,"
                    "после подтверждения создания уведомление придёт во все подключенные беседы и всем водителлям"
                    "включившим *Поиск*.\n\nЧтобы принять заказ необходимо нажать кнопку *принят* под сообщением о "
                    "заказе, после чего администраторы получат уведомление об этом с ссылкой на ваш профиль.\n\n"
                    "Чтобы получать уведомления о новых заказах необходимо написать боту *\"Поиск\"*, после чего "
                    "отправить своё местоположение(это необходимо для того чтобы можно было расчитать расстояние "
                    "от вас до пункта отправки).\n\n Если возникли какие-либо неполадки в ходе работы бота "
                    "необходимо отправить запрос в данном формате:\n/report [проблема]\n\nТак же вы можете ознакомится"
                    "с более подробной информацией по данной [ссылке](https://williamadamsaurora.github.io/order_bot"
                    "/main.html)")

    LOG_MESSAGE = Template(f"Message ->\n"
                           f"@$username (chat $chat)\n"
                           f"$text\n\n"
                           f"$user_info\n")

    LOG_ACTION = Template(f"Message ->\n"
                          f"@$username (chat $chat)\n"
                          f"$text\n\n"
                          f"$user_info\n"
                          f"$fsm_info\n")

    LOG_DB_INIT = Template(f"{' DATABASE '.center(30, '=')}\n"
                           f"DB name: $name\n"
                           f"Host: $host\n"
                           f"User: $user\n"
                           f"{''.center(30, '=')}\n\n")

    @staticmethod
    def order_info(order, **kwargs) -> str:
        default_result = Templates.ORDER_INFO.substitute(date=order.date,
                                                         distance=order.distance,
                                                         unit=order.unit,
                                                         cost=order.cost,
                                                         tariff=order.tariff,
                                                         pointA=order.point_a,
                                                         pointB=order.point_b,
                                                         amount=order.amount,
                                                         status=order.status,
                                                         delivery_time=order.delivery_time)
        if kwargs['mode'] == "default":
            return default_result
        elif kwargs['mode'] == "new order":
            if kwargs['to'] in ["chat", "no-geo user"]:
                order_header = Templates.ORDER_INFO_HEADERS['common'].substitute(
                    order_id=order.get_id()
                )
            else:
                order_header = Templates.ORDER_INFO_HEADERS['geo user'].substitute(
                    order_id=order.get_id(),
                    distance=kwargs['distance'],
                    unit=kwargs['unit']
                )

            return f"{order_header}\n\n{default_result}"
