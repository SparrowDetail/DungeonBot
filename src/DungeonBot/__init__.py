import logging
import logging.handlers

import discord
from discord.ext import commands
from DungeonBot.cogs import extensions

class DungeonBot(commands.Bot):
    def __init__(self, **options) -> None:
        intents = discord.Intents.all()
        super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=intents)
    
    async def on_ready(self):
        """
        Occurs when bot is finished setting up, indicates when the bot is ready
        """
        print(f'Logged in: {self.user}!\n')

    async def setup_hook(self) -> None:
        print("Seeking cogs...")

        for ext in extensions:
            await self.load_extension(f"DungeonBot.cogs.{ext}")

DungeonBot = DungeonBot()