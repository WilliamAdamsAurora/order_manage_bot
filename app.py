from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand

from core import Core, Database
from core.log import Log
from handlers.create_order import creater
from handlers.ddl import ddl_command
from handlers.debug import debug_command
from handlers.help import help_command
from handlers.login import login_command
from handlers.msg import msg_control
from handlers.order_info import order_command
from handlers.remove_group import remove_group_command
from handlers.report import report_command
from handlers.search import search_command
from handlers.set_group import set_group_command
from handlers.start import start_command


class App:
    core = Core()
    db = Database()
    log = Log()

    dispatcher = Dispatcher()

    def __init__(self, *, mode: str):
        self.token = self.core.get_token(mode)
        self.bot = Bot(token=self.token)

        self.log.bot_logging(f"\n{' TOKEN '.center(65, '=')}\n"
                             f"Bot run with token {self.core.get_token(mode)}\n"
                             f"{''.center(65, '=')}\n")

    async def configurate(self):
        await self.set_commands()
        await self.register_handlers()

    async def set_commands(self):
        await self.bot.set_my_commands(commands=[
            BotCommand(command="/login", description="авторизоваться в системе"),
            BotCommand(command="/debug", description="получить логи"),
            BotCommand(command="/set_group", description="подключить уведомления к беседе"),
            BotCommand(command="/remove_group", description="отключить уведомления в беседе"),
            BotCommand(command="/start", description="Начать работу"),
            BotCommand(command="/report", description="Сообщить о проблеме"),
        ])

        self.log.bot_logging(f"\n{' COMMAND LIST '.center(24, '=')}\n"
                             f"Set commands success ✅\n"
                             f"{''.center(24, '=')}\n")

    async def register_handlers(self):
        handlers = (
            ddl_command,
            start_command,
            debug_command,
            login_command,
            remove_group_command,
            set_group_command,
            help_command,
            report_command,

            creater,
            search_command,
            order_command,

            msg_control,

        )

        log_message: str = f"\n{' ROUTERS '.center(48, '=')}\n"

        for index, router in enumerate(handlers):
            try:
                self.dispatcher.include_router(router)
                log_message += f"{router.name:<20}[{index+1}] initialized success ✅\n"
            except ValueError:
                log_message += f"{router.name:<15}[{index+1}] failed ❌\n"

        log_message += f"{''.center(48, '=')}\n"

        self.log.bot_logging(log_message)

    async def start(self):
        self.log.bot_logging(f"\n{' POLLING '.center(21, '=')}\n"
                             f"Bot polling starting\n"
                             f"{''.center(21, '=')}\n")
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dispatcher.start_polling(self.bot)
