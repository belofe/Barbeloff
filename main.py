import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import motor.motor_asyncio  # <-- Import Motor
from keep_alive import keep_alive


from exercisevideos import ExerciseVideos
from rookie import Rookie
from fitness_tracker import FitnessTracker

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=lambda bot, message: '' if isinstance(message.channel, discord.DMChannel) else '!',
    intents=intents,
    case_insensitive=True
)

roles = ["Rookie", "Intermediate", "Advanced"]

# Initialize Motor client and DB here globally or in main()
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_URL', 'MONGO_URL'))
db = mongo_client["fitness_db"]  # Your MongoDB database name

@bot.event
async def on_ready():
    print(f"We are ready to lift in, {bot.user.name}")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.event
async def on_member_join(member):
    try:
        # Compose the DM
        welcome_message = (
            f"👋 Welcome to Barbelloff, {member.name}!\n\n"
            "To get started with your fitness journey, please use the **setstats** command "
            "to enter your age, gender, height, and weight.\n\n"
            "Example: **setstats 20 male 59 169** (20 year old male with a height of 5 feet 9 inches weighing 169 pounds)"
        )

        # Send the DM
        await member.send(welcome_message)
    except discord.Forbidden:
        print(f"❌ Could not send DM to {member.name}. They may have DMs disabled.")


# (Your existing events and commands go here...)

async def main():
    async with bot:
        # Attach db to bot before loading cogs
        bot.db = db

        await bot.load_extension('rookie')
        await bot.load_extension('fitness_tracker')
        await bot.load_extension('intermediate')
        await bot.load_extension('advanced')
        await bot.load_extension('exercisevideos')
        await bot.load_extension('helpcommand')



        await bot.start(token)

if __name__ == "__main__":
    import asyncio
    keep_alive()
    asyncio.run(main())
