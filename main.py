import asyncio

from app import App
from core import Core


async def main() -> None:
    app = App(mode=Core.RELEASE)
    await app.configurate()
    await app.start()


if __name__ == "__main__":

    asyncio.run(main())



