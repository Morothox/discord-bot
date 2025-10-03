import discord
from discord.ext import commands
import datetime

class Tickets(commands.Cog):
    """Ticket management system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.ticket_category = None
        self.ticket_counter = {}
    
    @commands.command(name='setuptickets')
    @commands.has_permissions(administrator=True)
    async def setup_tickets(self, ctx, category: discord.CategoryChannel = None):
        """Setup the ticket system with a category"""
        if category is None:
            category = await ctx.guild.create_category("Tickets")
        
        self.ticket_category = category
        
        embed = discord.Embed(
            title="🎫 Ticket System Setup",
            description=f"Ticket system has been set up in {category.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='ticket', aliases=['new', 'createticket'])
    async def create_ticket(self, ctx, *, reason=None):
        """Create a new support ticket"""
        guild = ctx.guild
        
        # Get or create ticket category
        if self.ticket_category is None or self.ticket_category.guild != guild:
            category = discord.utils.get(guild.categories, name="Tickets")
            if category is None:
                category = await guild.create_category("Tickets")
            self.ticket_category = category
        
        # Generate ticket number
        if guild.id not in self.ticket_counter:
            self.ticket_counter[guild.id] = 0
        self.ticket_counter[guild.id] += 1
        ticket_num = self.ticket_counter[guild.id]
        
        # Create ticket channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        channel = await self.ticket_category.create_text_channel(
            name=f"ticket-{ticket_num:04d}",
            overwrites=overwrites
        )
        
        # Send ticket information
        embed = discord.Embed(
            title=f"🎫 Ticket #{ticket_num:04d}",
            description=f"Welcome {ctx.author.mention}! A staff member will be with you shortly.",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Created by", value=ctx.author.mention, inline=True)
        embed.add_field(name="Reason", value=reason or "Not specified", inline=True)
        embed.set_footer(text="Use !close to close this ticket")
        
        await channel.send(embed=embed)
        
        # Confirm ticket creation
        confirm_embed = discord.Embed(
            title="✅ Ticket Created",
            description=f"Your ticket has been created: {channel.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=confirm_embed, delete_after=10)
    
    @commands.command(name='close', aliases=['closeticket'])
    async def close_ticket(self, ctx):
        """Close the current ticket"""
        if not ctx.channel.name.startswith('ticket-'):
            await ctx.send("This command can only be used in ticket channels!")
            return
        
        embed = discord.Embed(
            title="🎫 Closing Ticket",
            description="This ticket will be closed in 5 seconds...",
            color=discord.Color.red(),
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name="Closed by", value=ctx.author.mention)
        await ctx.send(embed=embed)
        
        await discord.utils.sleep_until(datetime.datetime.now() + datetime.timedelta(seconds=5))
        await ctx.channel.delete()
    
    @commands.command(name='claim', aliases=['claimticket'])
    @commands.has_permissions(kick_members=True)
    async def claim_ticket(self, ctx):
        """Claim a ticket as a staff member"""
        if not ctx.channel.name.startswith('ticket-'):
            await ctx.send("This command can only be used in ticket channels!")
            return
        
        embed = discord.Embed(
            title="🎫 Ticket Claimed",
            description=f"This ticket has been claimed by {ctx.author.mention}",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='adduser')
    @commands.has_permissions(kick_members=True)
    async def add_user_to_ticket(self, ctx, member: discord.Member):
        """Add a user to the current ticket"""
        if not ctx.channel.name.startswith('ticket-'):
            await ctx.send("This command can only be used in ticket channels!")
            return
        
        await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
        
        embed = discord.Embed(
            title="👤 User Added",
            description=f"{member.mention} has been added to this ticket",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='removeuser')
    @commands.has_permissions(kick_members=True)
    async def remove_user_from_ticket(self, ctx, member: discord.Member):
        """Remove a user from the current ticket"""
        if not ctx.channel.name.startswith('ticket-'):
            await ctx.send("This command can only be used in ticket channels!")
            return
        
        await ctx.channel.set_permissions(member, overwrite=None)
        
        embed = discord.Embed(
            title="👤 User Removed",
            description=f"{member.mention} has been removed from this ticket",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
