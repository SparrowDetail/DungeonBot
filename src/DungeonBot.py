from io import BytesIO
import discord
from discord.ext import commands
from DiceRollImageGenerator import BoundedImage
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

        generatedImage = BoundedImage(dieType=int(dieType), rollCount=int(numberOfDieRolled))
        imageByteArray: BytesIO = generatedImage.getByteArray()
        generatedImage.close()

        imageByteArray.seek(0)
        discordImageFile = discord.File(fp=imageByteArray, filename="rollImage.png")
        embed = discord.Embed(color=discord.Color.dark_green())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed.set_image(url="attachment://rollImage.png")
        await ctx.send(file=discordImageFile, embed=embed)

        imageByteArray.close()
    except (ValueError):
        await ctx.send(f"Roll must be entered in the form XdY, where X is the number of dice rolled and Y is a valid die type. You entered: {arg}")
    except (RollValueAndTypeError):
        await ctx.send(f'Sorry, I can only roll up to four dice right now. You tried to roll: {numberOfDieRolled}D{dieType}')
    except (OSError):
        #TODO: incorporate logger - advanced setup
        await ctx.send(f'Sorry, something went wrong...')

if __name__ == "__main__":
    token = ""

    with open("TOKEN.txt","r") as f:
        token = f.read()
    
    dungeonBot.run(token)