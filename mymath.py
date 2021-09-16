from discord.ext import commands

import shared

class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(alias='addition')
    async def add(self, ctx, base:float, *additives:float):
        shared.log_command(ctx,'add')
        total = base
        for num in additives:
            total += num
        await ctx.send(f"{base} + {additives} = {total}")

    @commands.command(alias='subtract')
    async def sub(self, ctx, base:float, *subs:float):
        shared.log_command(ctx,'sub')
        total = base
        for num in subs:
            total -= num
        await ctx.send(f"{base} - {subs} = {total}")

    @commands.command(alias='multiply')
    async def mul(self, ctx, base:float, *subs:float):
        shared.log_command(ctx,'mul')
        total = base
        for num in subs:
            total *= num
        await ctx.send(f"{base} * {subs} = {total}")

    @commands.command(alias='divide')
    async def div(self, ctx, base:float, *subs:float):
        shared.log_command(ctx,'div')

        total = base
        for num in subs:
            total /= num
        await ctx.send(f"{base} / {subs} = {total}")
