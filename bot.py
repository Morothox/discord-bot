import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import aiosqlite

# Load environment variables
load_dotenv()

# Database initialization
async def init_db():
    async with aiosqlite.connect(os.getenv('DATABASE_PATH')) as db:
        await db.execute('CREATE TABLE IF NOT EXISTS example (id INTEGER PRIMARY KEY)')
        await db.commit()

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=intents)

# Error handling
@bot.event
def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
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
    await init_db()
    await load_cogs()

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))