import asyncio
from DungeonBot import DungeonBot
import os

TOKEN = os.getenv('DungeonBotToken')

async def load_cogs():
    print("Loading cogs...")
    await DungeonBot.load_extension('DungeonBot.cogs.Roll')
    print("Finished")

async def main():
    await DungeonBot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())