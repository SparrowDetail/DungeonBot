# DungeonBot
A discord bot geared towards providing DnD utilities to a discord server

## Requirements
- [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html) - designed using discord.py version 2.3.2
- [Pillow(Fork)](https://pillow.readthedocs.io/en/stable/installation.html) - used in roll image generation, designed using version 10.3.0

### Recommended
Pillow(Fork) recommends running within a [virtual environment(venv)](https://docs.python.org/3/library/venv.html)

## Cogs
All commands currently utilize a "!" prefix, but the project is slated to move towards 'slashcommands'

### Roll
Generate a set of rolls from a traditional DnD die (D2, D4, D6, D8, D10, D12, D20). Currently, you can only roll up to four dice.
All arguments must be in the form 'XdY', where 'X' is the number of die you wish to roll and 'Y' is the type of die you wish to roll, example:

![RollImage](.readme/roll_sample.png)

### Initiative
Provides commands that allow users to create and manage initiative order tables. These are generated per-user based on their unique discord user
id.

#### `/initiative private`
Sends a direct message (DM) to the user to allow the user to execute commands privately. Recommended for when several initiative rolls need to be added to
the table.

#### `/initiative show`
Generate and display an embed containing the users initiative rolls

#### `/initiative add` and `/initiative add_show`
Commands used to add characters to the initiative order. Requires the user to enter a character name (string) and a roll modifier (integer). The `add`
command will simply add the data to the table, while the `add_show` command will add the data and generate a new embed to display to the users.

#### `/initiative remove` and `/initiative remove_show`
Commands used to remove characters from the initiative order. Requires the user to enter a character name (string) that they wish to remove. The `remove`
command will simply remove the data from the table, while the `remove_show` command will remove the data and generate a new embed to display to the users.

#### `/initiative clear`
Removes all initiative roll entries for the user
