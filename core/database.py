import pymysql
import yaml
from icecream import ic
from loguru import logger

from core.elements.templates import Templates
from core.log import Log

log = Log()

# TODO log
# TODO var rename
# TODO refactor
# TODO optimization


class Database:
    def __init__(self):
        with open("./storage/settings.yaml") as settings:
            database_keys = yaml.safe_load(settings)['database']

        log.module_start(Templates.LOG_DB_INIT.substitute(
            host=database_keys['host'],
            name=database_keys['name'],
            user=database_keys['username']
        ))

        self.database = pymysql.connect(user=database_keys['username'], password=database_keys['password'],
                                        host=database_keys['host'], db=database_keys['name'])
        self.cursor = self.database.cursor()

    @logger.catch
    def ddl(self, query: str, **options):
        logger.debug(f"ddl()\n└ query: {query}\n└ options: {options}")

        self.cursor.execute(query)
        self.database.commit()

        if "fetchone" in options and options["fetchone"]:
            return list(self.cursor.fetchone())
        elif "fetchone_item" in options and options["fetchone_item"]:
            return list(self.cursor.fetchone())[0]

        return list(self.cursor.fetchall())

    @logger.catch
    def check_exist(self, *, table: str, condition: str):
        logger.debug(f"check_exist()\n└ table: {table}\n└ condition: {condition}")

        result = self.ddl(f"SELECT * FROM {table} WHERE {condition}")
        ic(result)

        return False if result == [] else True


if __name__ == "__main__":
    d = Database()
    d.ddl()
