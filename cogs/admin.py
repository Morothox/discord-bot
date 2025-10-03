import discord
from discord.ext import commands
import aiosqlite
import os

class Admin(commands.Cog):
    """Administrative commands for server configuration"""
    
    def __init__(self, bot):
        self.bot = bot
    
    async def init_db(self):
        """Initialize the admin database"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS guild_settings (
                    guild_id INTEGER PRIMARY KEY,
                    prefix TEXT DEFAULT NULL,
                    welcome_channel_id INTEGER DEFAULT NULL,
                    welcome_message TEXT DEFAULT NULL,
                    leave_message TEXT DEFAULT NULL,
                    autorole_id INTEGER DEFAULT NULL
                )
            ''')
            await db.commit()
    
    @commands.command(name='setprefix')
    @commands.has_permissions(administrator=True)
    async def set_prefix(self, ctx, prefix: str):
        """Set a custom prefix for this server"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            await db.execute(
                'INSERT OR REPLACE INTO guild_settings (guild_id, prefix) VALUES (?, ?)',
                (ctx.guild.id, prefix)
            )
            await db.commit()
        
        embed = discord.Embed(
            title="✅ Prefix Updated",
            description=f"Server prefix has been set to `{prefix}`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='setwelcome')
    @commands.has_permissions(administrator=True)
    async def set_welcome(self, ctx, channel: discord.TextChannel, *, message: str):
        """Set welcome message for new members"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            await db.execute(
                'INSERT OR REPLACE INTO guild_settings (guild_id, welcome_channel_id, welcome_message) VALUES (?, ?, ?)',
                (ctx.guild.id, channel.id, message)
            )
            await db.commit()
        
        embed = discord.Embed(
            title="✅ Welcome Message Set",
            description=f"Welcome messages will be sent to {channel.mention}",
            color=discord.Color.green()
        )
        embed.add_field(name="Message", value=message[:1024], inline=False)
        embed.set_footer(text="Use {user} for user mention, {server} for server name")
        await ctx.send(embed=embed)
    
    @commands.command(name='setleave')
    @commands.has_permissions(administrator=True)
    async def set_leave(self, ctx, *, message: str):
        """Set leave message for members who leave"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            await db.execute(
                'INSERT OR REPLACE INTO guild_settings (guild_id, leave_message) VALUES (?, ?)',
                (ctx.guild.id, message)
            )
            await db.commit()
        
        embed = discord.Embed(
            title="✅ Leave Message Set",
            description="Leave message has been configured",
            color=discord.Color.green()
        )
        embed.add_field(name="Message", value=message[:1024], inline=False)
        embed.set_footer(text="Use {user} for username, {server} for server name")
        await ctx.send(embed=embed)
    
    @commands.command(name='setautorole')
    @commands.has_permissions(administrator=True)
    async def set_autorole(self, ctx, role: discord.Role):
        """Set a role to be automatically assigned to new members"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            await db.execute(
                'INSERT OR REPLACE INTO guild_settings (guild_id, autorole_id) VALUES (?, ?)',
                (ctx.guild.id, role.id)
            )
            await db.commit()
        
        embed = discord.Embed(
            title="✅ Auto-role Set",
            description=f"New members will automatically receive {role.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='removeautorole')
    @commands.has_permissions(administrator=True)
    async def remove_autorole(self, ctx):
        """Remove the auto-role"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            await db.execute(
                'UPDATE guild_settings SET autorole_id = NULL WHERE guild_id = ?',
                (ctx.guild.id,)
            )
            await db.commit()
        
        embed = discord.Embed(
            title="✅ Auto-role Removed",
            description="Auto-role has been disabled",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='settings')
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        """View current server settings"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            cursor = await db.execute(
                'SELECT prefix, welcome_channel_id, welcome_message, leave_message, autorole_id FROM guild_settings WHERE guild_id = ?',
                (ctx.guild.id,)
            )
            row = await cursor.fetchone()
        
        embed = discord.Embed(
            title=f"⚙️ Server Settings - {ctx.guild.name}",
            color=discord.Color.red()
        )
        
        if row:
            prefix, welcome_ch_id, welcome_msg, leave_msg, autorole_id = row
            
            embed.add_field(
                name="Prefix",
                value=prefix or f"`{os.getenv('PREFIX')}` (default)",
                inline=False
            )
            
            if welcome_ch_id:
                channel = ctx.guild.get_channel(welcome_ch_id)
                embed.add_field(
                    name="Welcome Channel",
                    value=channel.mention if channel else "Channel not found",
                    inline=True
                )
                embed.add_field(
                    name="Welcome Message",
                    value=welcome_msg[:100] + "..." if len(welcome_msg) > 100 else welcome_msg,
                    inline=False
                )
            
            if leave_msg:
                embed.add_field(
                    name="Leave Message",
                    value=leave_msg[:100] + "..." if len(leave_msg) > 100 else leave_msg,
                    inline=False
                )
            
            if autorole_id:
                role = ctx.guild.get_role(autorole_id)
                embed.add_field(
                    name="Auto-role",
                    value=role.mention if role else "Role not found",
                    inline=True
                )
        else:
            embed.description = "No custom settings configured. Using defaults."
        
        await ctx.send(embed=embed)
    
    @commands.command(name='nickname')
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, nickname: str = None):
        """Change a member's nickname"""
        await member.edit(nick=nickname)
        
        if nickname:
            await ctx.send(f"✅ Changed {member.mention}'s nickname to `{nickname}`")
        else:
            await ctx.send(f"✅ Removed {member.mention}'s nickname")
    
    @commands.command(name='createrole')
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx, *, name: str):
        """Create a new role"""
        role = await ctx.guild.create_role(name=name)
        
        embed = discord.Embed(
            title="✅ Role Created",
            description=f"Created role {role.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='deleterole')
    @commands.has_permissions(manage_roles=True)
    async def delete_role(self, ctx, role: discord.Role):
        """Delete a role"""
        await role.delete()
        
        embed = discord.Embed(
            title="✅ Role Deleted",
            description=f"Deleted role `{role.name}`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='addrole')
    @commands.has_permissions(manage_roles=True)
    async def add_role(self, ctx, member: discord.Member, role: discord.Role):
        """Add a role to a member"""
        await member.add_roles(role)
        
        embed = discord.Embed(
            title="✅ Role Added",
            description=f"Added {role.mention} to {member.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='removerole')
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, member: discord.Member, role: discord.Role):
        """Remove a role from a member"""
        await member.remove_roles(role)
        
        embed = discord.Embed(
            title="✅ Role Removed",
            description=f"Removed {role.mention} from {member.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Handle member join events"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            cursor = await db.execute(
                'SELECT welcome_channel_id, welcome_message, autorole_id FROM guild_settings WHERE guild_id = ?',
                (member.guild.id,)
            )
            row = await cursor.fetchone()
            
            if row:
                welcome_ch_id, welcome_msg, autorole_id = row
                
                # Send welcome message
                if welcome_ch_id and welcome_msg:
                    channel = member.guild.get_channel(welcome_ch_id)
                    if channel:
                        msg = welcome_msg.replace("{user}", member.mention).replace("{server}", member.guild.name)
                        embed = discord.Embed(
                            description=msg,
                            color=discord.Color.green()
                        )
                        embed.set_thumbnail(url=member.display_avatar.url)
                        await channel.send(embed=embed)
                
                # Assign auto-role
                if autorole_id:
                    role = member.guild.get_role(autorole_id)
                    if role:
                        await member.add_roles(role)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Handle member leave events"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            cursor = await db.execute(
                'SELECT welcome_channel_id, leave_message FROM guild_settings WHERE guild_id = ?',
                (member.guild.id,)
            )
            row = await cursor.fetchone()
            
            if row and row[1]:
                channel_id, leave_msg = row
                if channel_id:
                    channel = member.guild.get_channel(channel_id)
                    if channel:
                        msg = leave_msg.replace("{user}", str(member)).replace("{server}", member.guild.name)
                        embed = discord.Embed(
                            description=msg,
                            color=discord.Color.red()
                        )
                        await channel.send(embed=embed)

async def setup(bot):
    cog = Admin(bot)
    await cog.init_db()
    await bot.add_cog(cog)
