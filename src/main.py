import asyncio
from DungeonBot import DungeonBot
import os

#Enter your Discord Bot Token here
#I use an environment variable, but a string literal or equivalent will function as well
TOKEN = os.getenv('DungeonBotToken')

async def main():
    await DungeonBot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())