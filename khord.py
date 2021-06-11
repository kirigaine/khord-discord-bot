from random import randint, choice
import re

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=';')
rps_choices = ["rock", "paper", "scissors"]
dnd_characters = ["Snorck", "Vikkus", "Nova'Norr", "Matteus", "Viktor", "Rilk"]

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
    result = rps_game("rock")
    await ctx.send(result)

@bot.command()
async def paper(ctx):
    result = rps_game("paper")
    await ctx.send(result)

@bot.command()
async def scissors(ctx):
    result = rps_game("scissors")
    await ctx.send(result)

def rps_game(player_choice):
    bool_victory = False
    npc_choice = choice(rps_choices)
    if player_choice == "rock" and npc_choice == "scissors":
        bool_victory = True
    elif player_choice == "scissors" and npc_choice == "paper":
        bool_victory = True
    elif player_choice == "paper" and npc_choice =="rock":
        bool_victory = True
    return (player_choice, npc_choice, bool_victory)


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    message.content = message.content.lower()
    if message.author == bot.user:
        return
    else:
        if message.content.startswith("hello"):
            await message.channel.send("Hello, mortal.")
    
    await bot.process_commands(message)


bot.run("")
