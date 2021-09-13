"""
*********************************************************************************
* |```|   /```|  |```|   |```|   /```````````\   |`````````\    |``````````\    *
* |   |  /   /   |   |   |   |   |   .___.   |   |   .__.   |   |   .___.   \   *
* |   | /   /    |   |   |   |   |   |   |   |   |   |  |   |   |   |   |    |  *
* |   |/   /     |   |___|   |   |   |   |   |   |   |__|   /   |   |   |    |  *
* |       /      |           |   |   |   |   |   |         /    |   |   |    |  *
* |       \      |    ___    |   |   |   |   |   |    __   \    |   |   |    |  *
* |        \     |   |   |   |   |   |   |   |   |   |  \   \   |   |   |    |  *
* |   |\    \    |   |   |   |   |   |   |   |   |   |  |   |   |   |___|    |  *
* |   | \    \   |   |   |   |   |   |___|   |   |   |  |   |   |           //  *
* |___|  \____\  |___|   |___|   \__________ /   |___|  |___|   |__________//   *
* |___|  |____|  |___|   |___|    \_________/    |___|  |___|   |__________/    *
*                                                                               *
*********************************************************************************
*                                                                               *
* Project Name: Khord Discord Bot                                               *
* Author: github.com/kirigaine                                                  *
* Description: My personal Discord bot. Provides a myriad of functions from     *
*   dice rolls to music playing. Personified as a deity, hence his lack of      *
*   social manners.                                                             *
* Requirements: discordpy, ffmpeg                                               *
*                                                                               *
*********************************************************************************
"""

from random import randint, choice, choices, shuffle
from enum import Enum
import re
import os

import discord
from discord.ext import commands

import phasmorpg

class RockPaperScissors(Enum):
    """Small class to handle rps game and emoji names"""
    ROCK = 1
    NEWSPAPER = 2
    SCISSORS = 3

ffmpeg_options = {
    'options': '-vn'
}

dnd_characters = ["Snorck", "Vikkus", "Nova'Norr", "Mateus", "Viktor", "Rilk"]

LOGO = """*********************************************************************************
* |```|   /```|  |```|   |```|   /```````````\   |`````````\    |``````````\    *
* |   |  /   /   |   |   |   |   |   .___.   |   |   .__.   |   |   .___.   \   *
* |   | /   /    |   |   |   |   |   |   |   |   |   |  |   |   |   |   |    |  *
* |   |/   /     |   |___|   |   |   |   |   |   |   |__|   /   |   |   |    |  *
* |       /      |           |   |   |   |   |   |         /    |   |   |    |  *
* |       \      |    ___    |   |   |   |   |   |    __   \    |   |   |    |  *
* |        \     |   |   |   |   |   |   |   |   |   |  \   \   |   |   |    |  *
* |   |\    \    |   |   |   |   |   |   |   |   |   |  |   |   |   |___|    |  *
* |   | \    \   |   |   |   |   |   |___|   |   |   |  |   |   |           //  *
* |___|  \____\  |___|   |___|   \__________ /   |___|  |___|   |__________//   *
* |___|  |____|  |___|   |___|    \_________/    |___|  |___|   |__________/    *
*                         Made By: github.com/kirigaine                         *
*********************************************************************************"""

print(LOGO)
bot = commands.Bot(command_prefix=';')
print("[CONSOLE] Attempting to log in to Discord")

@bot.command()
async def age(ctx):
    """Ask Khord for your age"""
    log_command(ctx,'age')
    await ctx.send(f"Mortal {ctx.author.mention} joined this realm on {str(ctx.author.joined_at)[:-7]}")

@bot.command()
async def dnd(ctx):
    """Khord picks a character from our D&D campaign"""
    log_command(ctx,'dnd')
    await ctx.send("**" + choice(dnd_characters) + "**, you have been chosen!")

@bot.command()
async def hello(ctx):
    """Greets Khord"""
    log_command(ctx,'hello')
    await ctx.send(f"Hello, mortal {ctx.author.display_name}.")

@bot.command()
async def leave(ctx):
    """Asks Khord to leave"""
    log_command(ctx,'leave')

    voice = ctx.voice_client

    if voice:
        await voice.disconnect()
        await ctx.send("Fine. I know when I'm not wanted.")
    else:
        await ctx.send("I'm not in your mortal channel, nor would I want to be.")

@bot.command()
async def paper(ctx):
    """Challenge Khord with paper"""
    log_command(ctx,'paper')

    result = rps_game(RockPaperScissors.NEWSPAPER)
    await ctx.send(result)

@bot.command()
async def pause(ctx):
    """Pauses Khord's serenading"""
    log_command(ctx,'pause')
    voice = ctx.voice_client
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Already paused / no audio playing")

@bot.command()
async def pgame(ctx, num_traits:str, num_players:str="4"):
    """Khord gives custom RPG traits for Phasmo"""
    log_command(ctx,f'pgame {num_traits} {num_players}')

    regex_passed_traits = regex_passed_players = None
    regex_passed_traits = re.search("^[1-9]{1}$", num_traits)
    regex_passed_players = re.search("^[1-4]{1}$", num_players)
    if not regex_passed_traits or not regex_passed_players:
        await ctx.send(f"Invalid input. Usage: ;pgame number_of_traits(1-9) [number_of_players](1-4)\n")
    else:
        num_traits = int(num_traits)
        num_players = int(num_players)


        items_copy = phasmorpg.items.copy()
        for i in range(0,num_players):

            message = f"```[PLAYER {i+1}]\n + Traits:\n"

            traits = get_traits(num_traits)

            for trait in traits:
                message += f"\t{trait[0]} --- {trait[1]}\n"

            if ["Forgetful","Lose two random items from the mission"] in traits:
                message += " + Items Lost:\n"
                items_lost = get_items(items_copy)
                message += f"\t{items_lost[0]}\n\t{items_lost[1]}\n"

            message += f" + (OPTIONAL) Personality: {get_personality()}\n"
            await ctx.send(f"{message}```")

@bot.command()
async def pick(ctx, *given_list):
    """Khord will pick for you"""
    log_command(ctx,f'pick {given_list}')
    if not given_list:
        raise commands.MissingRequiredArgument(given_list)
    await ctx.send(choice(given_list))

@pick.error
async def pick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: ;pick a1 a2 a3...")

@bot.command()
async def play(ctx, music_url:str):
    """Khord projects your music to all minds in your subrealm"""
    log_command(ctx,f'play {music_url}')

    if ctx.author.voice and not ctx.voice_client:
        await ctx.author.voice.channel.connect()
        # await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_mute=True, self_deaf=True)
        voice = ctx.voice_client

        # TO DO:
        for file in os.listdir("./"):
           if file.endswith(".mp3"):
                voice.play(discord.FFmpegPCMAudio('test.mp3',executable='./ffmpeg/bin/ffmpeg.exe'))
    else:
        await ctx.send("You're not even in the server")
        # raise commands.CommandError("User wasn't connected to a voice channel")

@bot.command()
async def pray(ctx):
    """Prays to Khord"""
    # TO DO: Turn this into slots/gambling
    log_command(ctx,'pray')
    await ctx.send(choices(["*nothing happens*","Sup","Have my blessing, Child of Khord"], weights=(5,3,1))[0])

@bot.command(alias='unpause')
async def resume(ctx):
    """Resumes Khord's serenading"""
    log_command(ctx,'resume')
    voice = ctx.voice_client
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.sent("Voice not paused")

@bot.command()
async def rock(ctx):
    """Challenge Khord with rock"""
    log_command(ctx,'rock')

    result = rps_game(RockPaperScissors.ROCK)
    await ctx.send(result)

@bot.command()
async def roll(ctx, dice:str):
    """Khord rolls dice for you"""
    log_command(ctx,f'roll {dice}')
    
    try:
        num_dice, die_max = map(int, dice.split('d'))
    except Exception:
        await ctx.send("Must be in XdX (e.g. 4d6)!")
        return

    rolls = ""
    total = 0
    for i in range(1, num_dice+1):
        roll_outcome = randint(1,int(die_max))
        total += roll_outcome
        rolls = f"{rolls} [{roll_outcome}]"
    await ctx.send(f"```{rolls} = {total}```")

@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: ;roll XdX")
    elif isinstance(error, ValueError):
        await ctx.send("Can't roll a die with 0 values")
    
@bot.command()
async def scissors(ctx):
    """Challenge Khord with scissors"""
    log_command(ctx,'scissors')

    result = rps_game(RockPaperScissors.SCISSORS)
    await ctx.send(result)

@bot.command()
async def stop(ctx):
    """Stops Khord's serenading"""
    log_command(ctx,'stop')

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

def rps_game(player_choice):
    player_victory = False
    npc_choice = RockPaperScissors(randint(1,3))

    # Determine if player won
    if ((player_choice == RockPaperScissors.ROCK and npc_choice == RockPaperScissors.SCISSORS) or
        (player_choice == RockPaperScissors.SCISSORS and npc_choice == RockPaperScissors.NEWSPAPER) or
        (player_choice == RockPaperScissors.NEWSPAPER and npc_choice == RockPaperScissors.ROCK)):
        player_victory = True

    # Add player and bot choices to output statement
    outcome_statement = f":{(player_choice.name).lower()}: ***vs*** :{(npc_choice.name).lower()}:\n"

    # Add victory/draw/loss result to output statement
    if player_victory:
        outcome_statement = outcome_statement + "Purely luck, mortal. :white_check_mark:"
    elif not player_victory and player_choice == npc_choice:
        outcome_statement += "Hmm. Interesting. :monkey:"
    else:
        outcome_statement += "As expected from a feeble mind. You lose. :x:"

    return (outcome_statement)

def log_command(ctx,user_command:str):
    """Logs user activity in console for debugging"""
    print(f"[COMMAND] - [{ctx.guild.name}] {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.display_name}) called: ';{user_command}'")

def get_traits(count):
    """Randomizes a copy of traits list, then pops desired amount for pgame"""
    traits = []
    c_copy = phasmorpg.traits.copy()
    shuffle(c_copy)
    for count in range(1, count+1):
        temp_index = randint(0,len(c_copy)-1)
        temp_trait = c_copy.pop(temp_index)
        traits.append(temp_trait)

    return traits

def get_personality():
    """Randomizes a personality for pgame"""
    return choice(phasmorpg.personalities)

def get_items(items_copy):
    """Randomizes 2 items for pgame"""
    items_gotten = []
    for item in range(0, 2):
        temp_index = randint(0,len(phasmorpg.items)-1)
        temp_item = items_copy.pop(temp_index)
        items_gotten.append(temp_item)
    return items_gotten


@bot.event
async def on_connect():
    print('[CONSOLE] Successfully logged in as {0.user}'.format(bot))


@bot.event
async def on_ready():
    print('[CONSOLE] {0.user}'.format(bot) + ' is now ready!')

@bot.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == bot.user:
        return
    elif "it is what it is" in message.content:
        await message.channel.send("IT IS WHAT IT IS")
    
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    print(error)


bot.run("token")
