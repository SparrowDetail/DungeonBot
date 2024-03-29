from io import BytesIO
import discord
from discord.ext import commands
from random import randint
import DiceRollImageGenerator as genImg
from DiceRollImageGenerator import RollValueAndTypeError

intents = discord.Intents.default()
intents.message_content = True

dungeonBot = commands.Bot(command_prefix="!", intents=intents)

@dungeonBot.event
async def on_ready():
    """
    Execute when connection is established
    """
    print(f'Logged in as: {dungeonBot.user}')

@dungeonBot.command()
async def roll(ctx, arg):
    """
    Bot command that accepts input in the form XdY, where X represents a number of dice the user wishes to roll and Y represents a
    die type present in a typical DnD die set (2, 4, 6, 8, 10, 12, 20). Currently, only up to four die may be generated.

    :param ctx: Discord context that command is being executed within
    :param arg: Command passed within the discord context, expected to be in the form XdY
    """
    try:
        numberOfDieRolled, dieType = str(arg).upper().split('D')
        print(f"Rolls: {numberOfDieRolled}\nDie Type: {dieType}")

        rollValues = __createRollValues__(int(dieType), int(numberOfDieRolled))
        rollImageByteArray: BytesIO = genImg.generateDieByteArray(rollValues, int(dieType))
        rollImageByteArray.seek(0)

        discordImageFile = discord.File(fp=rollImageByteArray, filename="rollImage.png")
        embed = discord.Embed(color=discord.Color.dark_green())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed.set_image(url="attachment://rollImage.png")
        await ctx.send(file=discordImageFile, embed=embed)

        rollImageByteArray.close()
    except (ValueError):
        await ctx.send(f"Roll must be entered in the form XdY, where X is the number of dice rolled and Y is a valid die type. You entered: {arg}")
    except (RollValueAndTypeError):
        await ctx.send(f'Sorry, I can only roll up to four dice right now. You tried to roll: {numberOfDieRolled}D{dieType}')

def __createRollValues__(sidesOnDie:int, amountRolled:int) -> list:
    """
    Generates a list of int values representing the values resulting from a die rolled a specified number of times with a specified number of faces.

    :param sidesOnDie: int representing the number of sides on a die
    :param amountRolled: int representing the number of times a die is rolled
    """
    rolls:list = []

    for i in range(0,amountRolled):
        rolls.append(randint(1,sidesOnDie))

    return rolls

if __name__ == "__main__":
    token = ""

    with open("TOKEN.txt","r") as f:
        token = f.read()
    
    dungeonBot.run(token)