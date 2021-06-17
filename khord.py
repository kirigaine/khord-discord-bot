from random import randint, choice
from enum import Enum
import re

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=';')
class rps(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

dnd_characters = ["Snorck", "Vikkus", "Nova'Norr", "Mateus", "Viktor", "Rilk"]

@bot.command()
async def hello(ctx):
    """Respond to user with a simple 'hello'"""
    await ctx.send("Hello, mortal.")

@bot.command()
async def roll(ctx, arg1, arg2=1):
    regex_passed1 = re.search("^[0-9]{1,3}$", str(arg1))
    regex_passed2 = re.search("^[0-9]{1,3}$", str(arg2))
    print(f"{regex_passed1} {regex_passed2}")
    if regex_passed1 and regex_passed2:
        rolls = ""
        for i in range(1, arg2+1):
            roll_outcome = randint(1,int(arg1))
            rolls = f"{rolls} {roll_outcome}"
        await ctx.send(f"Roll: {rolls} | arg1: {arg1} arg2: {arg2}")
    else:
        await ctx.send("fail")
        
@bot.command()
async def rock(ctx):
    """';rock' calls for Rock Paper Scissors with rock"""
    result = rps_game(rps.ROCK)
    await ctx.send(result)

@bot.command()
async def paper(ctx):
    """';paper' calls for Rock Paper Scissors with paper"""
    result = rps_game(rps.PAPER)
    await ctx.send(result)

@bot.command()
async def scissors(ctx):
    """';scissors' calls for Rock Paper Scissors with scissors"""
    result = rps_game(rps.SCISSORS)
    await ctx.send(result)

@bot.command()
async def randchar(ctx):
    await ctx.send("**" + choice(dnd_characters) + "**, you have been chosen!")

def rps_game(player_choice):
    bool_victory = False
    npc_choice = rps(randint(1,3))

    if ((player_choice == rps.ROCK and npc_choice == rps.SCISSORS) or
        (player_choice == rps.SCISSORS and npc_choice == rps.PAPER) or
        (player_choice == rps.PAPER and npc_choice == rps.PAPER)):
            bool_victory = True

    outcome_statement = f":{player_choice}: ***vs.*** :{npc_choice}:\n"

    if bool_victory:
        outcome_statement = outcome_statement + "Purely luck, mortal. :white_check_mark:"
    elif not bool_victory and player_choice == npc_choice:
        outcome_statement += "Hmm. Interesting."
    else:
        outcome_statement += "As expected from a feeble mind. I win. :x:"

    return (outcome_statement)


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)


bot.run("ODUyMzE4NjM5NjQyNTA5MzIy.YMFFlw.6c-444mJsxYJosc3YFjlJdzOlZo")
