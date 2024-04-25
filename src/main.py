import asyncio
from DungeonBot import DungeonBot
import os

TOKEN = os.getenv('DungeonBotToken')

async def main():
    await DungeonBot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())