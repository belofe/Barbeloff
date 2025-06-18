import discord
from discord.ext import commands

class ExerciseVideos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db  # ✅ This is critical!


        # A simple dictionary of exercise names to YouTube links
        self.exercise_links = {
            "lat pulldown": "https://www.youtube.com/watch?v=CAwf7n6Luuc",
            "bench press": "https://www.youtube.com/shorts/hWbUlkb5Ms4",
            "squat": "https://www.youtube.com/watch?v=Dy28eq2PjcM",
            "chest press machine": "https://www.youtube.com/shorts/KVDPkBDPT9o",
            "machine shoulder press": "https://www.youtube.com/watch?v=WvLMauqrnK8",
            "pec fly": "https://www.youtube.com/watch?v=FDay9wFe5uE",
            "cable lateral raise": "https://www.youtube.com/shorts/f_OGBg2KxgY",
            "dumbbell lateral raise": "https://www.youtube.com/shorts/HeovYNoZDRg",
            "machine lateral raise": "https://www.youtube.com/watch?v=0o07iGKUarI",
            "cable tricep pushdown": "https://www.youtube.com/watch?v=6Fzep104f0s",
            "cable tricep kickback": "https://www.youtube.com/watch?v=ZvF4Oi_6Vtg",
            "cable row": "https://www.youtube.com/watch?v=UCXxvVItLoM",
            "dumbbell hammer curl": "https://www.youtube.com/watch?v=BRVDS6HVR9Q",
            "cable curl": "https://www.youtube.com/watch?v=N2k3qcs0WLQ",
            "preacher curl": "https://www.youtube.com/watch?v=3mtXqrkbEfI",
            "leg press": "https://www.youtube.com/shorts/nDh_BlnLCGc",
            "leg curl": "https://www.youtube.com/watch?v=Orxowest56U",
            "leg extension": "https://www.youtube.com/watch?v=m0FOpMEgero",
            "hip abductor": "https://www.youtube.com/shorts/ktLkqP1upq0",
            "calf raise": "https://www.youtube.com/shorts/_OewEscCsbo",
            "body weight squats": "https://www.youtube.com/shorts/cSJP4moytoo",
            "push up": "https://www.youtube.com/watch?v=WDIpL0pjun0",
            "push-ups": "https://www.youtube.com/watch?v=WDIpL0pjun0",
            "push ups": "https://www.youtube.com/watch?v=WDIpL0pjun0",
            "plank hold": "https://www.youtube.com/shorts/j6WVxGJZv5Y",
            "burpees": "https://www.youtube.com/shorts/gYiE_2BtSTg",
            "burpee": "https://www.youtube.com/shorts/gYiE_2BtSTg",
            "arm circles": "https://www.youtube.com/shorts/lzR7tzI1JUI",
            "wall push ups": "https://www.youtube.com/shorts/JlrVJaPn5o4",
            "wall push up": "https://www.youtube.com/shorts/JlrVJaPn5o4",
            "seated row": "https://www.youtube.com/watch?v=UCXxvVItLoM",
            "seated rows": "https://www.youtube.com/watch?v=UCXxvVItLoM",
            "standing row": "https://www.youtube.com/shorts/uYiL7Cl4q0k",
            "standing rows": "https://www.youtube.com/shorts/uYiL7Cl4q0k",
            "overhead press": "https://www.youtube.com/shorts/eNMl9UoO7YA",
            "chair tricep dips": "https://www.youtube.com/shorts/9llvBAV4RHI",
            "chair tricep dip": "https://www.youtube.com/shorts/9llvBAV4RHI",
            "bicep curl": "https://www.youtube.com/shorts/803JIAWBj_c",
            "dead bug exercise": "https://www.youtube.com/watch?v=o4GKiEoYClI",
            "dead bug": "https://www.youtube.com/watch?v=o4GKiEoYClI",
            "leg swing": "https://www.youtube.com/shorts/7YMIIpxHJEc",
            "leg swings": "https://www.youtube.com/shorts/7YMIIpxHJEc",
            "glute bridges": "https://www.youtube.com/shorts/X_IGw8U_e38",
            "side lying leg lifts": "https://www.youtube.com/watch?v=jgh6sGwtTwk",
            "side lying leg lift": "https://www.youtube.com/watch?v=jgh6sGwtTwk",
            "wall sit": "https://www.youtube.com/shorts/mDdLC-yKudY",
            "smith machine incline press": "https://www.youtube.com/shorts/ohRa_YRmVCk",
            "smith machine squats": "https://www.youtube.com/watch?v=-eO_VydErV0",
            "neutral grip lat pulldown": "https://www.youtube.com/shorts/QuSqYj7tFbI",
            "chest supported machine row": "https://www.youtube.com/shorts/FTwvmczf7bE",
            "machine shrug": "https://www.youtube.com/shorts/NJ8U95vMtZg",
            "machine preacher curl": "https://www.youtube.com/watch?v=Ja6ZlIDONac",
            "barbell squat": "https://www.youtube.com/shorts/PPmvh7gBTi0",
            "barbell bench press": "https://www.youtube.com/shorts/hWbUlkb5Ms4",
            "tricep pushdown": "https://www.youtube.com/shorts/1FjkhpZsaxc"
            # Add more exercises here
        }

    @commands.command()
    async def video(self, ctx, *, exercise: str):
        """Get a video demonstration of an exercise."""
        exercise = exercise.lower()
        link = self.exercise_links.get(exercise)
        if link:
            await ctx.send(f"🎥 Here's a video for **{exercise.title()}**:\n{link}")
        else:
            await ctx.send("❌ Sorry, I don't have a video for that exercise. Try another!")

async def setup(bot):
    await bot.add_cog(ExerciseVideos(bot))
