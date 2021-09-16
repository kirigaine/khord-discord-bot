import os

from discord import FFmpegPCMAudio
from discord.ext import commands

import shared

ffmpeg_options = {
    'options': '-vn'
}

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leave(self, ctx):
        """Asks Khord to leave your voice realm"""
        shared.log_command(ctx,'leave')

        voice = ctx.voice_client

        if voice:
            await voice.disconnect()
            await ctx.send("Fine. I know when I'm not wanted.")
        else:
            await ctx.send("I'm not in your mortal channel, nor would I want to be.")

    @commands.command()
    async def pause(self, ctx):
        """Pauses Khord's serenading"""
        shared.log_command(ctx,'pause')
        voice = ctx.voice_client
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Already paused / no audio playing")

    @commands.command()
    async def play(self, ctx, music_url:str):
        """Khord projects your music to all minds in your subrealm"""
        shared.log_command(ctx,f'play {music_url}')

        if ctx.author.voice and not ctx.voice_client:
            await ctx.author.voice.channel.connect()
            # await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_mute=True, self_deaf=True)
            voice = ctx.voice_client

            # TO DO:
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    voice.play(FFmpegPCMAudio('test.mp3',executable='./ffmpeg/bin/ffmpeg.exe'))
        else:
            await ctx.send("You're not even in the server")
            # raise commands.CommandError("User wasn't connected to a voice channel")

    @commands.command(alias='unpause')
    async def resume(self, ctx):
        """Resumes Khord's serenading"""
        shared.log_command(ctx,'resume')
        voice = ctx.voice_client
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.sent("Voice not paused")

    
    @commands.command()
    async def stop(self, ctx):
        """Stops Khord's serenading"""
        shared.log_command(ctx,'stop')

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()