from random import choice, choices, randint

from discord.ext import commands

import shared

dnd_characters = ["Snorck", "Vikkus", "Nova'Norr", "Mateus", "Viktor", "Rilk"]

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def age(self, ctx):
        """Ask Khord for your age"""
        shared.log_command(ctx,'age')
        await ctx.send(f"Mortal {ctx.author.mention} joined this realm on {str(ctx.author.joined_at)[:-7]}")

    @commands.command()
    async def dnd(self, ctx):
        """Khord picks a character from our D&D campaign"""
        shared.log_command(ctx,'dnd')
        await ctx.send("**" + choice(dnd_characters) + "**, you have been chosen!")

    @commands.command()
    async def hello(self, ctx):
        """Greets Khord"""
        shared.log_command(ctx,'hello')
        await ctx.send(f"Hello, mortal {ctx.author.display_name}.")

    @commands.command()
    async def pick(self, ctx, *given_list):
        """Khord will pick for you"""
        shared.log_command(ctx,f'pick {given_list}')
        if not given_list:
            raise commands.MissingRequiredArgument(given_list)
        await ctx.send(choice(given_list))

    @pick.error
    async def pick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: ;pick a1 a2 a3...")

    @commands.command()
    async def pray(self, ctx):
        """Prays to Khord"""
        # TO DO: Turn this into slots/gambling
        shared.log_command(ctx,'pray')
        await ctx.send(choices(["*nothing happens*","Sup","Have my blessing, Child of Khord"], weights=(5,3,1))[0])

    @commands.command()
    async def roll(self, ctx, dice:str):
        """Khord rolls dice for you"""
        shared.log_command(ctx,f'roll {dice}')
        
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
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: ;roll XdX")
        elif isinstance(error, ValueError):
            await ctx.send("Can't roll a die with 0 values")