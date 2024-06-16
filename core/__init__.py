from core.database import Database


class Core(Database):
    DEBUG = "debug"
    RELEASE = "release"

    def __init__(self):
        super().__init__()

    def get_token(self, mode: str) -> str:
        match mode:
            case "release":
                return self.ddl("SELECT value FROM config WHERE parameter = 'BOT_TOKEN'", fetchone_item=True)
            case "debug":
                return self.ddl("SELECT value FROM config WHERE parameter = 'DEBUG_TOKEN'", fetchone_item=True)

    def check_login_key(self, key: str) -> bool:
        """
        Login-key validation

        :param key: user input
        :return: True/False
        """
        login_key = self.ddl("SELECT value FROM config WHERE parameter = 'LOGIN_KEY'", fetchone_item=True)

        return True if key == login_key else False

    def get_chats(self):
        data = self.ddl("SELECT value FROM config WHERE parameter = 'CHAT_ID'")
        return [int(chat[0]) for chat in data]

    def get_drivers(self):
        data = self.ddl("SELECT id FROM users WHERE role = 'driver'")
        return [int(driver[0]) for driver in data]

    def get_admins(self):
        data = self.ddl("SELECT id FROM users WHERE is_admin = 1")
        return [int(admin[0]) for admin in data]

    def add_chat(self, chat_id: int):
        self.ddl(f"INSERT INTO config (parameter, value) VALUES ('CHAT_ID', {chat_id})")

    def delete_group(self, chat_id: int) -> None:
        self.ddl(f"DELETE FROM config WHERE value = {chat_id}")
