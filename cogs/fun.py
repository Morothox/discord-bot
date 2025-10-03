import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    """Fun and entertaining commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why can't you hear a pterodactyl go to the bathroom? Because the 'P' is silent!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the bicycle fall over? It was two-tired!",
            "What do you call a fish with no eyes? Fsh!",
        ]
        
        self.facts = [
            "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that's still edible!",
            "A group of flamingos is called a 'flamboyance'.",
            "Octopuses have three hearts and blue blood.",
            "Bananas are berries, but strawberries aren't!",
            "A day on Venus is longer than its year.",
            "The shortest war in history lasted 38 to 45 minutes.",
            "Sharks existed before trees.",
            "The unicorn is the national animal of Scotland.",
        ]
    
    @commands.command(name='joke')
    async def joke(self, ctx):
        """Get a random joke"""
        embed = discord.Embed(
            title="😂 Random Joke",
            description=random.choice(self.jokes),
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='fact')
    async def fact(self, ctx):
        """Get a random fact"""
        embed = discord.Embed(
            title="🧠 Random Fact",
            description=random.choice(self.facts),
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='meme')
    async def meme(self, ctx):
        """Get a random meme (placeholder)"""
        embed = discord.Embed(
            title="😂 Meme Command",
            description="Meme functionality requires API integration (e.g., Reddit API).\nThis is a placeholder for meme retrieval.",
            color=discord.Color.red()
        )
        embed.set_footer(text="Configure Reddit API or similar for full functionality")
        await ctx.send(embed=embed)
    
    @commands.command(name='choose')
    async def choose(self, ctx, *choices):
        """Choose between multiple options"""
        if len(choices) < 2:
            await ctx.send("Please provide at least 2 options!")
            return
        
        embed = discord.Embed(
            title="🤔 Choice Maker",
            description=f"I choose: **{random.choice(choices)}**",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"Options: {', '.join(choices)}")
        await ctx.send(embed=embed)
    
    @commands.command(name='rate')
    async def rate(self, ctx, *, thing):
        """Rate something out of 10"""
        rating = random.randint(0, 10)
        
        if rating >= 8:
            emoji = "😍"
        elif rating >= 6:
            emoji = "😊"
        elif rating >= 4:
            emoji = "😐"
        else:
            emoji = "😞"
        
        embed = discord.Embed(
            title="⭐ Rating",
            description=f"I'd rate **{thing}** a **{rating}/10** {emoji}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='say')
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, message):
        """Make the bot say something"""
        await ctx.message.delete()
        await ctx.send(message)
    
    @commands.command(name='reverse')
    async def reverse(self, ctx, *, text):
        """Reverse the given text"""
        reversed_text = text[::-1]
        embed = discord.Embed(
            title="🔄 Reversed Text",
            description=reversed_text,
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='ascii')
    async def ascii_art(self, ctx):
        """Display random ASCII art"""
        arts = [
            "```\n(•_•)\n<)  )╯\n /  \\\n```",
            "```\n¯\\_(ツ)_/¯\n```",
            "```\n(づ｡◕‿‿◕｡)づ\n```",
            "```\n(╯°□°）╯︵ ┻━┻\n```",
            "```\n┬─┬ノ( º _ ºノ)\n```",
        ]
        
        await ctx.send(random.choice(arts))
    
    @commands.command(name='emojify')
    async def emojify(self, ctx, *, text):
        """Convert text to emoji"""
        emoji_dict = {
            'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪',
            'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯',
            'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴',
            'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹',
            'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾',
            'z': '🇿', ' ': '   '
        }
        
        emojified = ''.join(emoji_dict.get(char.lower(), char) for char in text[:20])
        await ctx.send(emojified)
    
    @commands.command(name='ship')
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member):
        """Ship two users together"""
        compatibility = random.randint(0, 100)
        
        if compatibility >= 80:
            message = "Perfect match! 💕"
            color = discord.Color.green()
        elif compatibility >= 60:
            message = "Great potential! 💖"
            color = discord.Color.blue()
        elif compatibility >= 40:
            message = "It could work! 💛"
            color = discord.Color.gold()
        elif compatibility >= 20:
            message = "Not the best match... 💔"
            color = discord.Color.orange()
        else:
            message = "Maybe not meant to be... 💀"
            color = discord.Color.red()
        
        embed = discord.Embed(
            title="💘 Love Calculator",
            description=f"{user1.mention} 💕 {user2.mention}",
            color=color
        )
        embed.add_field(name="Compatibility", value=f"{compatibility}%")
        embed.add_field(name="Result", value=message)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
