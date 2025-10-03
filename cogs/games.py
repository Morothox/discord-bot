import discord
from discord.ext import commands
import random

class Games(commands.Cog):
    """Fun game commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.trivia_questions = [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is 2 + 2?", "answer": "4"},
            {"question": "What color is the sky?", "answer": "Blue"},
            {"question": "How many continents are there?", "answer": "7"},
            {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
        ]
    
    @commands.command(name='8ball')
    async def eight_ball(self, ctx, *, question):
        """Ask the magic 8-ball a question"""
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        
        embed = discord.Embed(
            title="🎱 Magic 8-Ball",
            color=discord.Color.red()
        )
        embed.add_field(name="Question", value=question, inline=False)
        embed.add_field(name="Answer", value=random.choice(responses), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='dice', aliases=['roll'])
    async def dice(self, ctx, sides: int = 6):
        """Roll a dice with specified number of sides"""
        if sides < 2:
            await ctx.send("Dice must have at least 2 sides!")
            return
        
        result = random.randint(1, sides)
        embed = discord.Embed(
            title="🎲 Dice Roll",
            description=f"You rolled a **{result}** on a {sides}-sided dice!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='coinflip', aliases=['flip'])
    async def coinflip(self, ctx):
        """Flip a coin"""
        result = random.choice(["Heads", "Tails"])
        embed = discord.Embed(
            title="🪙 Coin Flip",
            description=f"The coin landed on **{result}**!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='trivia')
    async def trivia(self, ctx):
        """Start a trivia question"""
        question_data = random.choice(self.trivia_questions)
        
        embed = discord.Embed(
            title="❓ Trivia Question",
            description=question_data["question"],
            color=discord.Color.red()
        )
        embed.set_footer(text="You have 30 seconds to answer!")
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            if msg.content.lower() == question_data["answer"].lower():
                await ctx.send(f"✅ Correct! The answer is **{question_data['answer']}**!")
            else:
                await ctx.send(f"❌ Wrong! The correct answer is **{question_data['answer']}**.")
        except:
            await ctx.send(f"⏰ Time's up! The answer was **{question_data['answer']}**.")
    
    @commands.command(name='rps')
    async def rock_paper_scissors(self, ctx, choice: str):
        """Play Rock, Paper, Scissors"""
        choices = ['rock', 'paper', 'scissors']
        choice = choice.lower()
        
        if choice not in choices:
            await ctx.send("Please choose rock, paper, or scissors!")
            return
        
        bot_choice = random.choice(choices)
        
        if choice == bot_choice:
            result = "It's a tie!"
            color = discord.Color.orange()
        elif (choice == 'rock' and bot_choice == 'scissors') or \
             (choice == 'paper' and bot_choice == 'rock') or \
             (choice == 'scissors' and bot_choice == 'paper'):
            result = "You win!"
            color = discord.Color.green()
        else:
            result = "I win!"
            color = discord.Color.red()
        
        embed = discord.Embed(
            title="✊✋✌️ Rock, Paper, Scissors",
            color=color
        )
        embed.add_field(name="Your choice", value=choice.capitalize(), inline=True)
        embed.add_field(name="My choice", value=bot_choice.capitalize(), inline=True)
        embed.add_field(name="Result", value=result, inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name='guess')
    async def guess_number(self, ctx, max_number: int = 100):
        """Play a number guessing game"""
        if max_number < 2:
            await ctx.send("Maximum number must be at least 2!")
            return
        
        number = random.randint(1, max_number)
        
        embed = discord.Embed(
            title="🔢 Number Guessing Game",
            description=f"I'm thinking of a number between 1 and {max_number}. You have 5 tries!",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
        
        for attempt in range(1, 6):
            try:
                msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                guess = int(msg.content)
                
                if guess == number:
                    await ctx.send(f"🎉 Correct! You guessed it in {attempt} {'try' if attempt == 1 else 'tries'}!")
                    return
                elif guess < number:
                    await ctx.send(f"📈 Too low! {5 - attempt} {'try' if 5 - attempt == 1 else 'tries'} left.")
                else:
                    await ctx.send(f"📉 Too high! {5 - attempt} {'try' if 5 - attempt == 1 else 'tries'} left.")
            except:
                await ctx.send(f"⏰ Time's up! The number was **{number}**.")
                return
        
        await ctx.send(f"💔 You ran out of tries! The number was **{number}**.")

async def setup(bot):
    await bot.add_cog(Games(bot))
