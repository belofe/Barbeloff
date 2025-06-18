from discord.ext import commands
import discord

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db  # ✅ This is critical!


    @commands.command(name="commands", help="List all available commands and their descriptions")
    async def list_commands(self, ctx):
        embed = discord.Embed(
            title="📚 Barbelloff Command Guide",
            description="Here are the commands you can use:",
            color=discord.Color.green()
        )

        command_descriptions = {
            "setstats [age] [gender] [height] [weight]": "Set your age, gender, height (like 59 for 5'9\"), and starting weight.",
            "mystats": "View your current fitness stats, BMI, and goal progress.",
            "mygoal [gain/lose] [amount]": "Set a weight gain or loss goal.",
            "updateweight": "Update your current weight (e.g., updateweight lost 5)",
            "hello": "Say hi to the bot!",
            "video [exercise]": "Provides a youtube link for an exercise. (Example: lat pulldown)",
            "resetstats": "Resets your current fitness stats.",

        }

        for cmd, desc in command_descriptions.items():
            embed.add_field(name=f"`{cmd}`", value=desc, inline=False)

        embed.set_footer(text="More features coming soon!")
        await ctx.send(embed=embed)

# ✅ This must be outside the class
async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
