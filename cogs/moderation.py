import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Moderation(commands.Cog):
    """Moderation commands for server management"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server"""
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Member Kicked",
            description=f"{member.mention} has been kicked from the server.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Reason", value=reason or "No reason provided")
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)
    
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from the server"""
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Member Banned",
            description=f"{member.mention} has been banned from the server.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Reason", value=reason or "No reason provided")
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)
    
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int):
        """Unban a user from the server"""
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        embed = discord.Embed(
            title="Member Unbanned",
            description=f"{user.mention} has been unbanned from the server.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)
    
    @commands.command(name='mute')
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: int = 60, *, reason=None):
        """Timeout a member for a specified duration (in minutes)"""
        await member.timeout(datetime.timedelta(minutes=duration), reason=reason)
        embed = discord.Embed(
            title="Member Muted",
            description=f"{member.mention} has been muted for {duration} minutes.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Reason", value=reason or "No reason provided")
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)
    
    @commands.command(name='unmute')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Remove timeout from a member"""
        await member.timeout(None)
        embed = discord.Embed(
            title="Member Unmuted",
            description=f"{member.mention} has been unmuted.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)
    
    @commands.command(name='warn')
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        """Warn a member"""
        embed = discord.Embed(
            title="Member Warned",
            description=f"{member.mention} has been warned.",
            color=discord.Color.orange(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Reason", value=reason or "No reason provided")
        embed.add_field(name="Moderator", value=ctx.author.mention)
        await ctx.send(embed=embed)
        
        # Send DM to warned member
        try:
            dm_embed = discord.Embed(
                title=f"Warning in {ctx.guild.name}",
                description=f"You have been warned by {ctx.author.mention}",
                color=discord.Color.orange(),
                timestamp=datetime.datetime.now()
            )
            dm_embed.add_field(name="Reason", value=reason or "No reason provided")
            await member.send(embed=dm_embed)
        except:
            pass
    
    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        """Delete a specified number of messages"""
        deleted = await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            title="Messages Cleared",
            description=f"Deleted {len(deleted) - 1} messages.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Moderator", value=ctx.author.mention)
        msg = await ctx.send(embed=embed)
        await msg.delete(delay=5)
    
    @commands.command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0):
        """Set slowmode for the current channel"""
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send(f"Slowmode has been disabled for {ctx.channel.mention}")
        else:
            await ctx.send(f"Slowmode set to {seconds} seconds for {ctx.channel.mention}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
