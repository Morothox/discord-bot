import discord
from discord.ext import commands
import datetime
import platform
import psutil

class Utility(commands.Cog):
    """Utility commands for information and tools"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='userinfo', aliases=['ui', 'whois'])
    async def userinfo(self, ctx, member: discord.Member = None):
        """Get information about a user"""
        member = member or ctx.author
        
        roles = [role.mention for role in member.roles[1:]]  # Exclude @everyone
        roles_str = ', '.join(roles) if roles else 'None'
        
        embed = discord.Embed(
            title=f"User Info - {member}",
            color=member.color if member.color != discord.Color.default() else discord.Color.red()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Bot", value="Yes" if member.bot else "No", inline=True)
        
        embed.add_field(
            name="Account Created",
            value=f"<t:{int(member.created_at.timestamp())}:F>",
            inline=False
        )
        embed.add_field(
            name="Joined Server",
            value=f"<t:{int(member.joined_at.timestamp())}:F>",
            inline=False
        )
        embed.add_field(name=f"Roles [{len(roles)}]", value=roles_str[:1024], inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='serverinfo', aliases=['si', 'guildinfo'])
    async def serverinfo(self, ctx):
        """Get information about the server"""
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"Server Info - {guild.name}",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Region", value=str(guild.preferred_locale), inline=True)
        
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        
        embed.add_field(name="Boost Level", value=guild.premium_tier, inline=True)
        embed.add_field(name="Boosts", value=guild.premium_subscription_count or 0, inline=True)
        embed.add_field(name="Emojis", value=len(guild.emojis), inline=True)
        
        embed.add_field(
            name="Created",
            value=f"<t:{int(guild.created_at.timestamp())}:F>",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='avatar', aliases=['av', 'pfp'])
    async def avatar(self, ctx, member: discord.Member = None):
        """Get a user's avatar"""
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"{member}'s Avatar",
            color=discord.Color.red()
        )
        embed.set_image(url=member.display_avatar.url)
        embed.add_field(
            name="Links",
            value=f"[PNG]({member.display_avatar.replace(format='png').url}) | "
                  f"[JPG]({member.display_avatar.replace(format='jpg').url}) | "
                  f"[WEBP]({member.display_avatar.replace(format='webp').url})"
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='roleinfo')
    async def roleinfo(self, ctx, *, role: discord.Role):
        """Get information about a role"""
        embed = discord.Embed(
            title=f"Role Info - {role.name}",
            color=role.color
        )
        
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Position", value=role.position, inline=True)
        
        embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
        embed.add_field(name="Hoisted", value="Yes" if role.hoist else "No", inline=True)
        embed.add_field(name="Members", value=len(role.members), inline=True)
        
        embed.add_field(
            name="Created",
            value=f"<t:{int(role.created_at.timestamp())}:F>",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='channelinfo', aliases=['ci'])
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        """Get information about a channel"""
        channel = channel or ctx.channel
        
        embed = discord.Embed(
            title=f"Channel Info - {channel.name}",
            color=discord.Color.red()
        )
        
        embed.add_field(name="ID", value=channel.id, inline=True)
        embed.add_field(name="Type", value=str(channel.type), inline=True)
        embed.add_field(name="Category", value=channel.category or "None", inline=True)
        
        embed.add_field(name="NSFW", value="Yes" if channel.is_nsfw() else "No", inline=True)
        embed.add_field(name="Position", value=channel.position, inline=True)
        embed.add_field(name="Slowmode", value=f"{channel.slowmode_delay}s" if channel.slowmode_delay else "Off", inline=True)
        
        embed.add_field(
            name="Created",
            value=f"<t:{int(channel.created_at.timestamp())}:F>",
            inline=False
        )
        
        if channel.topic:
            embed.add_field(name="Topic", value=channel.topic[:1024], inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='botinfo')
    async def botinfo(self, ctx):
        """Get information about the bot"""
        embed = discord.Embed(
            title=f"{self.bot.user.name} - Bot Information",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=len(self.bot.users), inline=True)
        embed.add_field(name="Commands", value=len(self.bot.commands), inline=True)
        
        embed.add_field(name="Python Version", value=platform.python_version(), inline=True)
        embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        # System info
        cpu_usage = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        embed.add_field(name="CPU Usage", value=f"{cpu_usage}%", inline=True)
        embed.add_field(name="RAM Usage", value=f"{ram.percent}%", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='invite')
    async def invite(self, ctx):
        """Get the bot's invite link"""
        embed = discord.Embed(
            title="Invite Me!",
            description=f"Click [here](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands) to invite me to your server!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='poll')
    async def poll(self, ctx, question, *options):
        """Create a poll with up to 10 options"""
        if len(options) > 10:
            await ctx.send("You can only have up to 10 options!")
            return
        
        if len(options) < 2:
            await ctx.send("You need at least 2 options!")
            return
        
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        description = []
        for idx, option in enumerate(options):
            description.append(f"{reactions[idx]} {option}")
        
        embed = discord.Embed(
            title=f"📊 {question}",
            description="\n".join(description),
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Poll by {ctx.author}")
        
        poll_msg = await ctx.send(embed=embed)
        
        for idx in range(len(options)):
            await poll_msg.add_reaction(reactions[idx])
    
    @commands.command(name='reminder')
    async def reminder(self, ctx, time: int, *, message):
        """Set a reminder (time in seconds)"""
        await ctx.send(f"✅ Reminder set for {time} seconds from now!")
        await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(seconds=time))
        
        embed = discord.Embed(
            title="⏰ Reminder!",
            description=message,
            color=discord.Color.red()
        )
        await ctx.send(f"{ctx.author.mention}", embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
