import discord
from discord.ext import commands
import asyncio

class Music(commands.Cog):
    """Music playback commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.now_playing = {}
    
    @commands.command(name='join')
    async def join(self, ctx):
        """Join the voice channel"""
        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel!")
            return
        
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await channel.connect()
            await ctx.send(f"Joined {channel.mention}")
        else:
            await ctx.voice_client.move_to(channel)
            await ctx.send(f"Moved to {channel.mention}")
    
    @commands.command(name='leave')
    async def leave(self, ctx):
        """Leave the voice channel"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            if ctx.guild.id in self.queue:
                self.queue[ctx.guild.id] = []
            await ctx.send("Left the voice channel")
        else:
            await ctx.send("I'm not in a voice channel!")
    
    @commands.command(name='play')
    async def play(self, ctx, *, query):
        """Play a song (Note: This is a placeholder - requires yt-dlp or similar)"""
        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel!")
            return
        
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        
        embed = discord.Embed(
            title="🎵 Music Player",
            description=f"**Note:** Full music functionality requires additional setup with yt-dlp.\n\nQueried: `{query}`",
            color=discord.Color.red()
        )
        embed.add_field(name="Status", value="Placeholder - Music playback not fully implemented")
        embed.set_footer(text="Install yt-dlp and configure for full functionality")
        await ctx.send(embed=embed)
    
    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pause the current song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Paused")
        else:
            await ctx.send("Nothing is playing!")
    
    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resume the paused song"""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Resumed")
        else:
            await ctx.send("Nothing is paused!")
    
    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop the current song"""
        if ctx.voice_client:
            ctx.voice_client.stop()
            if ctx.guild.id in self.queue:
                self.queue[ctx.guild.id] = []
            await ctx.send("⏹️ Stopped")
        else:
            await ctx.send("Nothing is playing!")
    
    @commands.command(name='skip')
    async def skip(self, ctx):
        """Skip the current song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ Skipped")
        else:
            await ctx.send("Nothing is playing!")
    
    @commands.command(name='queue')
    async def show_queue(self, ctx):
        """Show the current music queue"""
        guild_id = ctx.guild.id
        if guild_id not in self.queue or not self.queue[guild_id]:
            await ctx.send("The queue is empty!")
            return
        
        embed = discord.Embed(
            title="🎵 Music Queue",
            description="Upcoming songs",
            color=discord.Color.red()
        )
        
        for idx, song in enumerate(self.queue[guild_id][:10], 1):
            embed.add_field(name=f"{idx}. Song", value=song, inline=False)
        
        if len(self.queue[guild_id]) > 10:
            embed.set_footer(text=f"And {len(self.queue[guild_id]) - 10} more...")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='volume')
    async def volume(self, ctx, vol: int = None):
        """Set the volume (0-100)"""
        if vol is None:
            await ctx.send("Current volume: 100%")
            return
        
        if vol < 0 or vol > 100:
            await ctx.send("Volume must be between 0 and 100!")
            return
        
        if ctx.voice_client:
            ctx.voice_client.source.volume = vol / 100
            await ctx.send(f"🔊 Volume set to {vol}%")
        else:
            await ctx.send("I'm not in a voice channel!")
    
    @commands.command(name='nowplaying', aliases=['np'])
    async def now_playing(self, ctx):
        """Show the currently playing song"""
        guild_id = ctx.guild.id
        if guild_id in self.now_playing:
            embed = discord.Embed(
                title="🎵 Now Playing",
                description=self.now_playing[guild_id],
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Nothing is playing!")

async def setup(bot):
    await bot.add_cog(Music(bot))
