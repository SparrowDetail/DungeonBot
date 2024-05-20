# DungeonBot
A discord bot geared towards providing DnD utilities to a discord server

## Requirements
- Python 3.6 or above
- [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html) - designed using discord.py version 2.3.2
- [Pillow(Fork)](https://pillow.readthedocs.io/en/stable/installation.html) - used in roll image generation, designed using version 10.3.0

### Recommended
Pillow(Fork) recommends running within a [virtual environment(venv)](https://docs.python.org/3/library/venv.html)

## Running DungeonBot
You will first need to visit the [Discord Developer Portal](https://discord.com/login?redirect_to=%2Fdevelopers) and acquire a bot token by
creating a new application and generating a token within the Bot section on the dashboard. Using your bot will also require inviting it to
a discord server. This could simply be a test server you created if you desire. [This guide](https://discordpy.readthedocs.io/en/stable/discord.html) will
walk you through generating an invite link. I utilized the `Administrator` permission. With all this setup, you'll be ready to prepare the source code to
connect with and provide functionality to your bot application.

### Step 1: Download the source code
You can download the code manually as a zip file on the DungeonBot Github page or download the current working branch using:

`git clone https://github.com/SparrowDetail/DungeonBot.git`

### Step 2: Setup your virtual environment
It is recommended to run the bot within a (virtual environment)[https://docs.python.org/3/library/venv.html] to prevent Pillow(Fork) from interfering with any 
default versions of Pillow on your system.

Create your virtual environment by executing the following command within the `src/` directory of the DungeonBot project:

`python3 -m venv env/`

Now activate your venv:

```
//On Windows command line
C:\> <env PATH>\Scripts\activate.bat

//On a Bash shell
source <env PATH>/bin/activate
```

Within your venv you can install the required packages using pip. Run:

```
// Upgrade the current version of pip within your venv
python3 -m pip install --upgrade pip

//Install Pillow(Fork)
python3 -m pip install --upgrade Pillow

//Install Discord.py
python3 pip install -U discord.py
```

### Step 3: Enter your bot token and run
To enter your bot token, navigate to `src/main.py` and replace the TOKEN constant with your bot token (alternatively you can set your token as an environmental
variable with the name `DungeonBotToken` and the bot should run without this setup step):

```python
#Enter your Discord Bot Token here
#I use an environment variable, but a string literal or equivalent will function as well
TOKEN = os.getenv('DungeonBotToken')
```

With your venv active and the bot account invited to a Discord channel, your bot should be ready for testing. Run your bot from the src directory using the 
`main.py` script:

`python3 main.py`

**NOTE:** If the slash commands don't appear on Discord, try restarting the Discord application or refreshing the web browser. Discord "slashcommands" are
session based, so if you make changes to the applications command tree you will likely have to restart your current session on Discord.

# Cogs
All user commands utilize the discord.py app_command structure to register the bot commands as 'slashcommands.' Below is a sample use of the
`rng` command group `roll` command:

![slash_command](.readme/sample_command1.png)

![roll_command](.readme/sample_command2.png)

## RNG
Random number generation commands.

### `/rng roll`
Allows the user to roll up to four dice from an accepted list of available die assets (D2, D4, D6, D8, D10, D12, and D20)

### `/rng random`
Generates 1 to 10 random values with a specified head size. The head must be a positive integer greater than 0. For example, a head of 100
will generate a random value from 1 to 100.

## Initiative
Provides commands that allow users to create and manage initiative order tables. These are generated per-user based on their unique discord user
id.

### `/initiative private`
Sends a direct message (DM) to the user to allow the user to execute commands privately. Recommended for when several initiative rolls need to be added to
the table.

### `/initiative show`
Generate and display an embed containing the users initiative rolls

### `/initiative add`
Command used to add characters to the initiative order. Requires the user to enter a character name (string) and up to three optional values:
modifier, roll_value, and/or show. The modifier represents the value of the character's initiative modifier (typically DEX modifier), roll_value
allows the user to enter a specific roll for those that prefer real-world dice rolling, and show elects weather or not to display the initiative order
after adding (False by default).

### `/initiative remove`
Command used to remove characters from the initiative order. Requires the user to enter a character name (string) that they wish to remove and optionally 
show the initiative order afterwards (similar to the `add` command).

### `/initiative clear`
Removes all initiative roll entries for the user
