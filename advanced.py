import discord
from discord.ext import commands


class Advanced(commands.Cog):
    """Commands specific to Rookie members"""

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db  # ✅ This is critical!

    @commands.command()
    async def advanced(self, ctx):
        """Intermediate workout selection"""

        user_progress = await self.db.user_progress.find_one({"user_id": ctx.author.id})
        if not user_progress:
            await ctx.send("🚫 You need to set your stats first using `!setstats`.")
            return

        # Proceed to show workout options or logic

        class WorkoutView(discord.ui.View):
            def __init__(self, advanced_cog):
                super().__init__(timeout=60.0)
                self.advanced_cog = advanced_cog

            @discord.ui.button(label="💪 Strength", style=discord.ButtonStyle.red)
            async def strength(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user != ctx.author:
                    await interaction.response.send_message("This isn't your selection!", ephemeral=True)
                    return
                await self.handle_selection(interaction, "strength")

            @discord.ui.button(label="🏃 Lean", style=discord.ButtonStyle.green)
            async def lean(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user != ctx.author:
                    await interaction.response.send_message("This isn't your selection!", ephemeral=True)
                    return
                await self.handle_selection(interaction, "lean")

            @discord.ui.button(label="⚖️ Hybrid", style=discord.ButtonStyle.blurple)
            async def hybrid(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user != ctx.author:
                    await interaction.response.send_message("This isn't your selection!", ephemeral=True)
                    return
                await self.handle_selection(interaction, "hybrid")

            async def handle_selection(self, interaction, workout_type):
                await interaction.response.defer()
                # Store the selection in database if needed
                # Then show the appropriate workout plan
                if workout_type == "strength":
                    await interaction.followup.send("**💪 Strength Program Selected**")
                    await self.advanced_cog.advanced_strength(ctx)
                elif workout_type == "lean":
                    await interaction.followup.send("**🏃 Lean Program Selected**")
                    await self.advanced_cog.advanced_lean(ctx)
                else:
                    await interaction.followup.send("**⚖️ Hybrid Program Selected**")
                    await self.advanced_cog.advanced_hybrid(ctx)
                self.stop()

        embed = discord.Embed(
            title="🏋️ Choose Your Workout Focus",
            description="Select the program that matches your goals:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="💪 Strength",
            value="Build muscle mass with resistance training",
            inline=False
        )
        embed.add_field(
            name="🏃 Lean",
            value="Lose weight with cardio and mobility",
            inline=False
        )
        embed.add_field(
            name="⚖️ Hybrid",
            value="Balance of strength and cardio",
            inline=False
        )

        await ctx.send(embed=embed, view=WorkoutView(self))

    @commands.command()
    async def advanced_strength(self, ctx):
        """Get a beginner workout routine"""
        workout = """
**For each exercise, do at least 1 warm up set for 8 - 12 reps using approximately 50% of your working set weight** 

**Strength Day 1: Push Day**
- **Incline Smith Machine Press:** 3 sets of 8 - 10 reps
- **Machine Shoulder Press:** 2 sets of 8 - 10 reps
- **Pec Fly:** 2 sets of 10 - 12 reps
- **Lateral Raise (cable/dumbbell/machine):** 2 sets of 8 - 10 reps
- **Cable Tricep Pushdown:** 2 sets of 8 - 10 reps
- **Cable Tricep Kickback:** 2 sets of 10 - 12 reps


**Strength Day 2: Pull Day**
- **Lat Pull-down:** 3 sets of 8 - 12 reps
- **Cable Row:** 3 sets of 8 - 12 reps
- **Chest Supported Machine Row:** 2 sets of 8 - 10 reps
- **Dumbbell Hammer Curl:** 2 sets of 8 - 10 reps
- **Cable Curl:** 2 sets of 8 - 12 reps
- **Preacher Curl:** 1 set of 15 - 15 reps 


**Strength Day 3: Leg Day**
- **Barbell Squat:** 3 sets of 8 - 12 reps
- **Leg Curl:** 2 sets of 8 - 12 reps
- **Leg Extension:** 3 sets of 8 - 12 reps
- **Hip Abductor:** 3 sets of 8 - 12 reps
- **Calf Raise:** 3 sets of 8 - 12 reps


**Strength Day 4: Rest Day**
- For your rest day, feel free to kick back and take a well deserved break. Good rest is just as important as good training!
- If you want to get a little more active, feel free to incorporate some light cardio into your rest day to make it an active rest
- Some examples of active rest can include:
1. A walk or light jog outside or on a treadmill
2. Playing a sport of your choice
3. Yogo / Stretching 

**Note: After day 4, repeat the routine from day 1 increasing the weight as needed.**

**If you want to view all the bot commands that are available for use, type `commands`.**

**If you are confused about how to do any of the listed exercises, use the command 'video' followed by the exercise's name to access a link to the exercise.**
Example: video lat pulldown
"""
        await ctx.send(workout)

    @commands.command()
    async def advanced_lean(self, ctx):
        """Get a beginner workout routine"""
        workout = """
**For each exercise, do at least 1 warm up set for 8 - 12 reps using approximately 50% of your working set weight** 

**Note: Between each set. rest for 1 - 3 minutes**

**Lean Day 1: Full Body and Light Cardio**
- Warm up for 5 minutes with some light stretching and jumping jacks
- **Body weight squats:** 2 sets of 8 - 12 reps
- **Push-ups (modify on knees if needed):** 2 sets of 5 - 10 reps
- **Plank Hold:** 3 sets of 15 - 30 seconds
- **Cardio:** 30 minute run/incline walk      


**Day 2: Cardio Focus (40-45 minutes)**

**Warm-up (5 minutes):**
- Gentle walking or marching in place

**Main Cardio (25-30 minutes):**
Choose one or mix and match:
- Brisk walking (outdoors or treadmill)
- Stationary bike at moderate pace
- Swimming if available
- Low-impact dance or fitness video
**Target intensity: You should be able to hold a conversation but feel slightly breathless**

**Cool-down (5-10 minutes):**
- Slow walking and gentle stretching


**Day 3: Rest Day**
- Complete rest or light activity like gentle yoga, stretching, or leisurely walk
- Active recovery is just as important as training for weight loss success!


**Day 4: Upper Body Strength + Cardio (40-45 minutes)**

**Warm-up (5 minutes):**
- Arm circles and light movement

**Strength Training (20 minutes):**
- Wall or Incline Push-ups: 2 sets of 10 - 20 reps
- Pull ups: 2 sets of 6 - 12 reps
- Tricep Dips (chair or bench): 2 sets of 5-8 reps
- Bicep Curls or Chin Ups: 2 sets of 8-12 reps

**Cardio (15-20 minutes):**
- Run or Incline Walk
"""

        workout2 = """
**Day 5: Lower Body Strength + Cardio (40-45 minutes)**

**Warm-up (5 minutes):**
- Leg swings and light movement

**Strength Training (20 minutes):**
- Bodyweight Squats: 2 sets of 10-15 reps
- Lunges (stationary): 2 sets of 6-8 each leg
- Calf Raises: 2 sets of 12-15 reps
- Glute Bridges: 2 sets of 12-15 reps
- Side-lying Leg Lifts: 2 sets of 8-10 each side
- Wall Sit: 2 sets of 15-30 seconds

**Cardio (15-20 minutes):**
- Choose preferred cardio activity
- Focus on consistent, moderate effort

**Weekend: Active Recovery**
- Saturday: 20-30 minutes of enjoyable activity (hiking, dancing, playing sports)
- Sunday: Rest day or gentle yoga/stretching

**Important Notes:**
- Consistency is more important than intensity for weight loss
- Aim for 150+ minutes of moderate cardio per week
- Don't skip strength training - it helps maintain muscle during weight loss
- Listen to your body - extra rest days are better than injury
- Weight loss happens primarily through creating a caloric deficit - combine this routine with healthy eating habits

**If you want to view all the bot commands that are available for use, type `commands`.**

**If you are confused about how to do any of the listed exercises, use the command 'video' followed by the exercise's name to access a link to the exercise.**
Example: video lat pulldown
"""
        await ctx.send(workout)
        await ctx.send(workout2)

    @commands.command()
    async def advanced_hybrid(self, ctx):
        """Get a beginner workout routine"""
        workout = """
**Before and after your workout, perform a cardio of your choice for 10 minutes. (Incline walk, light jog, stationary cycle, etc.)**        

**For each exercise, do at least 1 warm up set for 8 - 10 reps using approximately 50% of your working set weight** 

**Hybrid Day 1: Upper Day**
- **Smith Machine Incline Press:** 3 sets of 10 - 12 reps
- **Pec Fly:** 2 sets of 10 - 12 reps
- **Lat pulldown:** 3 sets of 10 - 12 reps
- **Cable Lateral Raise:** 2 sets of 10 - 12 reps
- **Tricep Pushdown:** 2 sets of 12 - 15 reps
- **Cable Curl:** 2 sets of 12 - 15 reps

**Hybrid Day 2: Lower Day**
- **Smith Machine Squats:** 3 sets of 10 - 12  reps
- **Leg Curl:** 2 sets of 10 - 12 reps
- **Leg Extension:** 2 sets of 10 - 12 reps
- **Calf Raise:** 3 sets of 10 - 15 reps

**Hybrid Day 3: Active Rest day**
- For an active rest day, perform a cardio of your choice for a minimum of 30 minutes. Examples of cardio include
- A run outside/treadmill
- Any sport of your choice
- Incline treadmill walk

**Active rest days are vital for the hybrid program, since they help your muscles recover while burning fat**

**Hybrid Day 4: Pull day**
- **Neutral Grip Lat Pulldown:** 2 sets of 10 - 12 reps
- **Chest-Supported Machine Row:** 3 sets of 10 - 12 reps
- **Cable Row:** 2 sets of 10 - 12 reps
- **Machine Shrug:** 2 sets of 10 - 12 reps
- **Cable Curl:** 2 sets of 10 - 12 reps
- **Machine Preacher Curl:** 1 set of 10 - 12 reps

"""
        workout2 = """
**Hybrid Day 5: Push day**
- **Barbell Bench Press:** 3 sets of 10 - 12 reps
- **Machine Shoulder Press:** 2 sets of 10 - 12 reps
- **Pec Fly:** 2 sets of 12 - 15 reps
- **Cable Lateral Raise:** 2 sets of 12 - 15 reps
- **Tricep Pushdown:** 2 sets of 12 - 15 reps 

**Hybrid Day 6: Leg Day**
- **Leg Press:** 3 sets of 8 - 12 reps
- **Leg Curl:** 3 sets of 8 - 12 reps
- **Leg Extension:** 2 sets of 8 - 12 reps
- **Hip Abductor:** 3 sets of 8 - 12 reps
- **Calf Raise:** 3 sets of 8 - 12 reps

**Hybrid Day 7: Active Rest day**
- For an active rest day, perform a cardio of your choice for a minimum of 30 minutes. Examples of cardio include
- A run outside/treadmill
- Any sport of your choice
- Incline treadmill walk

**Active rest days are vital for the hybrid program, since they help your muscles recover while burning fat**

**If you want to view all the bot commands that are available for use, type `commands`.**

**If you are confused about how to do any of the listed exercises, use the command 'video' followed by the exercise's name to access a link to the exercise.**
Example: **video lat pulldown**
"""
        await ctx.send(workout)
        await ctx.send(workout2)


async def setup(bot):
    await bot.add_cog(Advanced(bot))