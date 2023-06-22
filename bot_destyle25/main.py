import asyncio

from handler import run_handler
from bot import run_bot


async def main():
   await asyncio.gather(run_handler(), run_bot())


if __name__ == "__main__":
   asyncio.run(main())