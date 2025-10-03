import discord
from discord.ext import commands
import aiosqlite
import os
import random

class Levels(commands.Cog):
    """Level and XP tracking system"""
    
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}
    
    async def init_db(self):
        """Initialize the levels database"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS levels (
                    user_id INTEGER,
                    guild_id INTEGER,
                    xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, guild_id)
                )
            ''')
            await db.commit()
    
    def calculate_level(self, xp):
        """Calculate level from XP"""
        return int((xp / 100) ** 0.5)
    
    def calculate_xp_for_level(self, level):
        """Calculate XP required for a level"""
        return (level ** 2) * 100
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Award XP for messages"""
        if message.author.bot:
            return
        
        if not message.guild:
            return
        
        # Cooldown check (1 minute)
        key = (message.author.id, message.guild.id)
        if key in self.cooldowns:
            return
        
        self.cooldowns[key] = True
        
        # Award XP
        xp_gain = random.randint(15, 25)
        
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            # Get current stats
            cursor = await db.execute(
                'SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?',
                (message.author.id, message.guild.id)
            )
            row = await cursor.fetchone()
            
            if row:
                current_xp, current_level = row
                new_xp = current_xp + xp_gain
                new_level = self.calculate_level(new_xp)
                
                await db.execute(
                    'UPDATE levels SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?',
                    (new_xp, new_level, message.author.id, message.guild.id)
                )
                
                # Level up notification
                if new_level > current_level:
                    embed = discord.Embed(
                        title="🎉 Level Up!",
                        description=f"{message.author.mention} is now level **{new_level}**!",
                        color=discord.Color.red()
                    )
                    await message.channel.send(embed=embed, delete_after=10)
            else:
                # Create new entry
                new_level = self.calculate_level(xp_gain)
                await db.execute(
                    'INSERT INTO levels (user_id, guild_id, xp, level) VALUES (?, ?, ?, ?)',
                    (message.author.id, message.guild.id, xp_gain, new_level)
                )
            
            await db.commit()
        
        # Remove from cooldown after 60 seconds
        await discord.utils.sleep_until(discord.utils.utcnow() + discord.timedelta(seconds=60))
        if key in self.cooldowns:
            del self.cooldowns[key]
    
    @commands.command(name='rank', aliases=['level'])
    async def rank(self, ctx, member: discord.Member = None):
        """Check your or another user's rank"""
        member = member or ctx.author
        
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            # Get user stats
            cursor = await db.execute(
                'SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?',
                (member.id, ctx.guild.id)
            )
            row = await cursor.fetchone()
            
            if not row:
                await ctx.send(f"{member.mention} has no XP yet!")
                return
            
            xp, level = row
            
            # Get rank
            cursor = await db.execute(
                'SELECT COUNT(*) FROM levels WHERE guild_id = ? AND xp > ?',
                (ctx.guild.id, xp)
            )
            rank_row = await cursor.fetchone()
            rank = rank_row[0] + 1 if rank_row else 1
            
            # Calculate XP for next level
            xp_for_current = self.calculate_xp_for_level(level)
            xp_for_next = self.calculate_xp_for_level(level + 1)
            xp_progress = xp - xp_for_current
            xp_needed = xp_for_next - xp_for_current
            
            embed = discord.Embed(
                title=f"📊 Rank - {member.display_name}",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(name="Rank", value=f"#{rank}", inline=True)
            embed.add_field(name="Level", value=level, inline=True)
            embed.add_field(name="XP", value=f"{xp:,}", inline=True)
            embed.add_field(
                name="Progress to Next Level",
                value=f"{xp_progress}/{xp_needed} XP ({int(xp_progress/xp_needed*100)}%)",
                inline=False
            )
            
            await ctx.send(embed=embed)
    
    @commands.command(name='leaderboard', aliases=['lb', 'top'])
    async def leaderboard(self, ctx, page: int = 1):
        """View the server leaderboard"""
        if page < 1:
            page = 1
        
        per_page = 10
        offset = (page - 1) * per_page
        
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            # Get total count
            cursor = await db.execute(
                'SELECT COUNT(*) FROM levels WHERE guild_id = ?',
                (ctx.guild.id,)
            )
            total_row = await cursor.fetchone()
            total = total_row[0] if total_row else 0
            
            if total == 0:
                await ctx.send("No one has earned XP yet!")
                return
            
            # Get leaderboard
            cursor = await db.execute(
                'SELECT user_id, xp, level FROM levels WHERE guild_id = ? ORDER BY xp DESC LIMIT ? OFFSET ?',
                (ctx.guild.id, per_page, offset)
            )
            rows = await cursor.fetchall()
            
            embed = discord.Embed(
                title=f"📊 Leaderboard - {ctx.guild.name}",
                description=f"Page {page}/{((total - 1) // per_page) + 1}",
                color=discord.Color.red()
            )
            
            description = ""
            for idx, (user_id, xp, level) in enumerate(rows, start=offset + 1):
                user = ctx.guild.get_member(user_id)
                if user:
                    medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "▫️"
                    description += f"{medal} **{idx}.** {user.mention} - Level {level} ({xp:,} XP)\n"
            
            embed.description = description or "No entries on this page"
            await ctx.send(embed=embed)
    
    @commands.command(name='givexp')
    @commands.has_permissions(administrator=True)
    async def give_xp(self, ctx, member: discord.Member, amount: int):
        """Give XP to a user (Admin only)"""
        async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
            cursor = await db.execute(
                'SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?',
                (member.id, ctx.guild.id)
            )
            row = await cursor.fetchone()
            
            if row:
                current_xp, current_level = row
                new_xp = max(0, current_xp + amount)
                new_level = self.calculate_level(new_xp)
                
                await db.execute(
                    'UPDATE levels SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?',
                    (new_xp, new_level, member.id, ctx.guild.id)
                )
            else:
                new_xp = max(0, amount)
                new_level = self.calculate_level(new_xp)
                await db.execute(
                    'INSERT INTO levels (user_id, guild_id, xp, level) VALUES (?, ?, ?, ?)',
                    (member.id, ctx.guild.id, new_xp, new_level)
                )
            
            await db.commit()
            
            embed = discord.Embed(
                title="✅ XP Updated",
                description=f"{'Added' if amount > 0 else 'Removed'} {abs(amount)} XP {'to' if amount > 0 else 'from'} {member.mention}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    cog = Levels(bot)
    await cog.init_db()
    await bot.add_cog(cog)
