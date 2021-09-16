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

from discord.ext import commands

import basic as b
import games as g
import music as mu
import mymath as ma
import shared

print(shared.LOGO)
bot = commands.Bot(command_prefix=';')
print("[CONSOLE] Attempting to log in to Discord")

# Add cogs
bot.add_cog(b.Basic(bot))
bot.add_cog(g.Games(bot))
bot.add_cog(mu.Music(bot))
bot.add_cog(ma.Math(bot))

@bot.event
async def on_connect():
    print('[CONSOLE] Successfully logged in as {0.user}'.format(bot))

@bot.event
async def on_ready():
    print('[CONSOLE] {0.user}'.format(bot) + ' is now ready!')

@bot.event
async def on_message(message):
    """Responds to an inside joke"""
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
