import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import aiosqlite
import datetime

# Load environment variables
load_dotenv()

# Database initialization
async def init_db():
    async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
        # Create tables for various features
        await db.execute('CREATE TABLE IF NOT EXISTS example (id INTEGER PRIMARY KEY)')
        await db.commit()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content
intents.members = True  # Required for member events
bot = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=intents)
bot.remove_command('help')  # Remove default help command to use custom one

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Missing required argument: {error.param}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument provided!")
    else:
        # Handle other errors
        print(f'Error: {error}')

# Load cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    print(f'Discord.py Version: {discord.__version__}')
    print('------')
    
    # Store start time for uptime command
    bot.start_time = datetime.datetime.now()
    
    await init_db()
    await load_cogs()
    
    # Set bot status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{os.getenv('PREFIX')}help | {len(bot.guilds)} servers"
        )
    )
    
    print(f'Bot is ready! Loaded {len(bot.cogs)} cogs with {len(list(bot.commands))} commands')
    print('------')

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))