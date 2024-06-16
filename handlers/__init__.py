from aiogram import Dispatcher

from handlers.msg import msg_control
from handlers.start import start_command
from handlers.debug import debug_command
from handlers.login import login_command
from handlers.set_group import set_group_command
from handlers.remove_group import remove_group_command
from handlers.create_order import creater
from handlers.search import search_command
from handlers.help import help_command
from handlers.report import report_command
from handlers.ddl import ddl_command


def register(dp: Dispatcher) -> None:
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

        msg_control,
    )

    for handler in handlers:
        dp.include_router(handler)
