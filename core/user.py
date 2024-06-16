from loguru import logger

from core.database import Database

logger.add("logs/users.log", format="\n{time} {level} \n{message}\n",
           level="DEBUG", rotation="10 MB", compression="zip")

# TODO log
# TODO var rename
# TODO refactor
# TODO optimization


class User(Database):
    def __init__(self, tg_id: int, username: str = None):
        logger.debug(f"__init__()\n"
                     f"└ tg_id: {tg_id}\n"
                     f"└ Username: {username}\n")
        super().__init__()

        user = self.ddl(f"SELECT * FROM users WHERE id = {tg_id}", fetchone=True)
        if user is None:
            self.ddl(f"INSERT INTO users (id, username) VALUES ({tg_id}, '{username}')")
            user = self.ddl(f"SELECT * FROM users WHERE id = {tg_id}", fetchone=True)

        if user[1] == "None" or user[1] == "":
            self.ddl(f"UPDATE `users` SET username='{username}' WHERE id={tg_id}")

        self._id = user[0]
        self.username = user[1]
        self.role = user[2]
        self._is_admin = user[3]
        self.action = user[4]
        self.position = user[5]

    @property
    def debug_info(self):
        return (f"{' user info '.center(30, '=')}\n"
                f"ID: {self._id}\n"
                f"Username: {self.username}\n"
                f"Role: {self.role}\n"
                f"Is admin: {True if self._is_admin == 1 else False}\n"
                f"Action: {self.action}\n"
                f"Position: {self.position}\n"
                f"{''.center(30, '=')}")

    @property
    def is_admin(self):
        return True if self._is_admin == 1 else False

    @property
    def get_id(self):
        return self._id

    def set_admin(self) -> None:
        self.ddl(f"UPDATE users SET is_admin=1 WHERE id = {self._id}")

    def set_action(self, new_action: str) -> None:
        self.ddl(f"UPDATE users SET action='{new_action}' WHERE id = {self._id}")

    def set_role(self, new_role: str) -> None:
        self.ddl(f"UPDATE users SET role = '{new_role}' WHERE id = {self._id}")

    @staticmethod
    def search_user(tg_id: int) -> tuple:
        return Database().ddl(f"SELECT * FROM users WHERE id = {tg_id}", fetchone=True)
