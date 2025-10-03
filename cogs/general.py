import discord
from discord.ext import commands
import datetime

class General(commands.Cog):
    """General bot commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check the bot's latency"""
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: **{round(self.bot.latency * 1000)}ms**",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='help')
    async def help_command(self, ctx, *, command_name: str = None):
        """Show help for commands"""
        if command_name:
            # Show help for specific command
            command = self.bot.get_command(command_name)
            if command is None:
                await ctx.send(f"Command `{command_name}` not found!")
                return
            
            embed = discord.Embed(
                title=f"Help - {command.name}",
                description=command.help or "No description available",
                color=discord.Color.red()
            )
            
            if command.aliases:
                embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)
            
            usage = f"{ctx.prefix}{command.name}"
            if command.signature:
                usage += f" {command.signature}"
            embed.add_field(name="Usage", value=f"`{usage}`", inline=False)
            
            await ctx.send(embed=embed)
        else:
            # Show all commands
            embed = discord.Embed(
                title="📚 Bot Commands",
                description=f"Use `{ctx.prefix}help <command>` for more info on a command",
                color=discord.Color.red()
            )
            
            for cog_name, cog in self.bot.cogs.items():
                commands_list = [cmd.name for cmd in cog.get_commands() if not cmd.hidden]
                if commands_list:
                    embed.add_field(
                        name=f"**{cog_name}**",
                        value=", ".join(f"`{cmd}`" for cmd in commands_list[:10]),
                        inline=False
                    )
            
            embed.set_footer(text=f"Total Commands: {len(list(self.bot.commands))}")
            await ctx.send(embed=embed)
    
    @commands.command(name='about')
    async def about(self, ctx):
        """Learn more about the bot"""
        embed = discord.Embed(
            title=f"About {self.bot.user.name}",
            description="A comprehensive Discord bot with moderation, music, games, and much more!",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        embed.add_field(
            name="Features",
            value="• Moderation Tools\n• Music Playback\n• Fun Games\n• Ticket System\n• Level Tracking\n• Utility Commands\n• And more!",
            inline=False
        )
        
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=len(self.bot.users), inline=True)
        embed.add_field(name="Commands", value=len(list(self.bot.commands)), inline=True)
        
        embed.add_field(
            name="Support",
            value="Need help? Contact the server administrators!",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='uptime')
    async def uptime(self, ctx):
        """Check how long the bot has been running"""
        if not hasattr(self.bot, 'start_time'):
            await ctx.send("Uptime tracking not available!")
            return
        
        delta = datetime.datetime.now() - self.bot.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        embed = discord.Embed(
            title="⏰ Uptime",
            description=f"**{days}** days, **{hours}** hours, **{minutes}** minutes, **{seconds}** seconds",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='suggest')
    async def suggest(self, ctx, *, suggestion):
        """Submit a suggestion"""
        embed = discord.Embed(
            title="💡 New Suggestion",
            description=suggestion,
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        
        await ctx.send("✅ Your suggestion has been submitted!", delete_after=5)
    
    @commands.command(name='feedback')
    async def feedback(self, ctx, *, message):
        """Send feedback to the bot developers"""
        embed = discord.Embed(
            title="📬 Feedback Received",
            description="Thank you for your feedback! It has been recorded.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        
        # Log feedback (in a real bot, you'd send this to a logging channel)
        print(f"Feedback from {ctx.author}: {message}")
    
    @commands.command(name='servericon')
    async def servericon(self, ctx):
        """Get the server's icon"""
        if ctx.guild.icon:
            embed = discord.Embed(
                title=f"{ctx.guild.name}'s Icon",
                color=discord.Color.red()
            )
            embed.set_image(url=ctx.guild.icon.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("This server doesn't have an icon!")
    
    @commands.command(name='stats')
    async def stats(self, ctx):
        """Display bot statistics"""
        embed = discord.Embed(
            title="📊 Bot Statistics",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=len(self.bot.users), inline=True)
        embed.add_field(name="Commands", value=len(list(self.bot.commands)), inline=True)
        
        embed.add_field(name="Text Channels", value=len(list(self.bot.get_all_channels())), inline=True)
        embed.add_field(name="Cogs Loaded", value=len(self.bot.cogs), inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))
