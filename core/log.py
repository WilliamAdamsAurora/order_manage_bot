from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from core.elements.templates import Templates

logger.add("logs/messages.log",
           format="\n{level.icon}{time:DD.MM HH:mm:ss}\n{message}\n",
           level="DEBUG",
           filter=lambda record: record['extra'].get('name') == f'message')
logger.add("../logs/db.log",
           format="\n{level.icon}{time:DD.MM HH:mm:ss}\n{message}\n",
           level="DEBUG",
           filter=lambda record: record['extra'].get('name') == f'db')
logger.add("logs/bot.log",
           format="\n{level.icon}{time:DD.MM HH:mm:ss}\n{message}\n",
           level="DEBUG",
           filter=lambda record: record['extra'].get('name') == f'bot')


class Log:
    message_log = logger.bind(name="message")
    db_log = logger.bind(name="db")
    bot_log = logger.bind(name="bot")

    def __init__(self):
        ...

    def bot_logging(self, text: str):
        self.bot_log.info(text)

    def module_start(self, text: str):
        self.db_log.info(text)

    def message(self, *, call: str, user, message: Message):
        user_id = message.from_user.id
        username = message.from_user.username
        chat_id = message.chat.id

        self.message_log.info(Templates.LOG_MESSAGE.substitute(
            username=username,
            chat=chat_id,
            text=message.text,
            user_info=user.debug_info
        ))

    def action(self, *, call: str, user, message: Message, fsm: dict):
        user_id = message.from_user.id
        username = message.from_user.username
        chat_id = message.chat.id

        self.message_log.info(f"{call} from @{username} | {user_id}\n"
                              f"Chat: {chat_id}\n\n"
                              f"{user.debug_info}\n\n"
                              f"{' FSM '.center(30, '=')}\n"
                              f"State: {fsm['state']}\n"
                              f"{''.center(30, '=')}\n")
