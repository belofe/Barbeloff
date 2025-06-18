import os

import discord
import datetime
from datetime import datetime

import motor
from discord.ext import commands
from mongo_utility import user_progress, user_goals

class FitnessTracker(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = bot.db  # Keep this so you can use self.db if needed
        self.user_progress = db["fitness"]["user_progress"]
        self.user_goals = db["fitness"]["user_goals"]



    @commands.command()
    async def example(self, ctx):
        user_data = await self.db.user_progress.find_one({"user_id": ctx.author.id})
        if user_data:
            await ctx.send(f"Your start weight is {user_data['start_weight']}")
        else:
            await ctx.send("No data found.")




    def create_or_update_progress(self, user_id, height, weight, age, gender):
        """Create or update user progress"""
        now = datetime.utcnow().isoformat()

        user_progress.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "height": height,
                    "start_weight": weight,
                    "current_weight": weight,
                    "age": age,
                    "gender": gender,
                    "last_updated": now
                }
            },
            upsert=True
        )

    def create_or_update_goal(self, user_id, target_weight, goal_type, start_weight, experience):
        """Create or update user goal"""
        start_date = datetime.utcnow().isoformat()

        user_goals.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "target_weight": target_weight,
                    "goal_type": goal_type,
                    "start_weight": start_weight,
                    "experience": experience,
                    "start_date": start_date
                }
            },
            upsert=True
        )

    def get_user_progress(self, user_id):
        """Retrieve user's progress data"""
        return user_progress.find_one({"user_id": user_id})

    def get_user_goal(self, user_id):
        """Retrieve user's goal data"""
        return user_goals.find_one({"user_id": user_id})

    @commands.command()
    async def setstats(self, ctx, age: int, gender: str, height: str, start_weight: float):
        """Set your initial stats with confirmation buttons"""

        class StatsConfirmation(discord.ui.View):
            def __init__(self, parent):
                super().__init__(timeout=60.0)
                self.parent = parent
                self.value = None

            @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.green)
            async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user != ctx.author:
                    await interaction.response.send_message("You can't confirm someone else's stats!", ephemeral=True)
                    return

                try:
                    height_clean = height.strip()
                    feet = int(height_clean[0])
                    inches = int(height_clean[1:]) if len(height_clean) > 1 else 0
                    total_inches = feet * 12 + inches
                    bmi = (start_weight / (total_inches ** 2)) * 703

                    # ✅ Fix: Await MongoDB call
                    await self.parent.db.user_progress.update_one(
                        {"user_id": ctx.author.id},
                        {
                            "$set": {
                                "user_id": ctx.author.id,
                                "height": total_inches,
                                "start_weight": start_weight,
                                "current_weight": start_weight,
                                "age": age,
                                "gender": gender.lower(),
                                "last_updated": discord.utils.utcnow()
                            }
                        },
                        upsert=True
                    )

                    # BMI categories
                    if bmi < 18.5:
                        category = "Underweight"
                    elif bmi < 25:
                        category = "Healthy Weight"
                    elif bmi < 30:
                        category = "Overweight"
                    else:
                        category = "Obese"

                    goal_prompt = (
                        "\n\nNow that your stats are set, you can set a fitness goal with the command 'mygoal':\n"
                        f"`mygoal [gain/lose] [amount]`\n"
                        f"Example: **mygoal lose 10** (to lose 10 lbs)"
                    )

                    # ✅ Use followup for extra messages
                    await interaction.response.send_message(
                        f"✅ **Stats confirmed!**\n"
                        f"Age: {age}\nGender: {gender.capitalize()}\nHeight: {feet}'{inches}\"\n"
                        f"Weight: {start_weight}lbs\nBMI: {bmi:.2f} ({category})"
                        f"{goal_prompt}"
                    )

                except Exception as e:
                    await interaction.followup.send(f"❌ Error saving stats: {str(e)}")

                finally:
                    self.stop()

            @discord.ui.button(label="🔄 Reset", style=discord.ButtonStyle.red)
            async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user != ctx.author:
                    await interaction.response.send_message("You can't reset someone else's stats!", ephemeral=True)
                    return
                await interaction.response.send_message(
                    "Stats reset. Use `!setstats [age] [gender] [height] [weight]` again."
                )
                self.stop()

        try:
            if gender.lower() not in ['male', 'female', 'other']:
                await ctx.send("❌ Invalid gender. Use male, female, or other.")
                return

            if age < 13 or age > 120:
                await ctx.send("❌ Age must be between 13 and 120.")
                return

            height_clean = height.strip()
            if not (2 <= len(height_clean) <= 3):
                await ctx.send("❌ Height must be 2 or 3 digits like 59 or 511.")
                return

            feet = int(height_clean[0])
            inches = int(height_clean[1:]) if len(height_clean) > 1 else 0
            total_inches = feet * 12 + inches
            bmi = (start_weight / (total_inches ** 2)) * 703

            embed = discord.Embed(
                title="📊 Confirm Your Stats",
                color=discord.Color.blue()
            )
            embed.add_field(name="Age", value=age, inline=True)
            embed.add_field(name="Gender", value=gender.capitalize(), inline=True)
            embed.add_field(name="Height", value=f"{feet}'{inches}\"", inline=True)
            embed.add_field(name="Weight", value=f"{start_weight} lbs", inline=True)
            embed.add_field(name="BMI", value=f"{bmi:.2f}", inline=True)
            embed.set_footer(text="Confirm within 60 seconds")

            view = StatsConfirmation(self)
            await ctx.send(embed=embed, view=view)




        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

    @commands.command()
    async def updateweight(self, ctx, direction: str, amount: float):
        """Update your current weight using change (e.g. !updateweight lost 10)"""
        direction = direction.lower()
        if direction not in ["lost", "gained"]:
            await ctx.send("❌ Please use `lost` or `gained` followed by the amount. Example: `!updateweight lost 5`")
            return

        try:
            # Retrieve user progress - using await for async operation
            user_data = await self.user_progress.find_one({"user_id": ctx.author.id})

            if not user_data:
                await ctx.send("❌ You need to set your stats first with !setstats.")
                return

            current_weight = user_data.get("current_weight")
            if current_weight is None:
                await ctx.send("❌ Could not find your current weight. Try using !setstats again.")
                return

            # Apply weight change
            if direction == "lost":
                new_weight = current_weight - amount
            else:
                new_weight = current_weight + amount

            # Update with await
            result = await self.user_progress.update_one(
                {"user_id": ctx.author.id},
                {
                    "$set": {
                        "current_weight": new_weight,
                        "last_updated": discord.utils.utcnow()
                    }
                }
            )

            if result.modified_count == 0:
                await ctx.send("⚠️ No changes were made. Double check your previous weight and try again.")
                return

            await ctx.send(
                f"✅ Weight updated! You've {direction} {amount:.1f} lbs. "
                f"New current weight: {new_weight:.1f} lbs."
            )

        except Exception as e:
            await ctx.send(f"❌ Error updating weight: {str(e)}")
    @commands.command()
    async def mygoal(self, ctx, goal_type: str, target_weight: float):
        """Set your weight goal (gain/lose X pounds)"""
        try:
            goal_type = goal_type.lower()
            if goal_type not in ['gain', 'lose']:
                await ctx.send("❌ Please specify 'gain' or 'lose' first (e.g. mygoal gain 10)")
                return
            if target_weight <= 0 or target_weight > 100:
                await ctx.send("❌ Please enter a reasonable goal amount (1-100 lbs)")
                return

            self.ctx = ctx
            self.goal_type = goal_type
            self.target_weight = target_weight

            class ExperienceView(discord.ui.View):
                def __init__(self, original_command):
                    super().__init__(timeout=60.0)
                    self.original_command = original_command

                @discord.ui.button(label="Rookie", style=discord.ButtonStyle.grey)
                async def rookie(self, interaction: discord.Interaction, button: discord.ui.Button):
                    await self.handle_experience(interaction, "rookie")

                @discord.ui.button(label="Intermediate", style=discord.ButtonStyle.blurple)
                async def intermediate(self, interaction: discord.Interaction, button: discord.ui.Button):
                    await self.handle_experience(interaction, "intermediate")

                @discord.ui.button(label="Advanced", style=discord.ButtonStyle.green)
                async def advanced(self, interaction: discord.Interaction, button: discord.ui.Button):
                    await self.handle_experience(interaction, "advanced")

                async def handle_experience(self, interaction: discord.Interaction, experience: str):
                    await interaction.response.defer()  # Acknowledge the interaction

                    if interaction.user != self.original_command.ctx.author:
                        await interaction.followup.send("You can't set someone else's experience!", ephemeral=True)
                        return

                    try:
                        user_id = self.original_command.ctx.author.id
                        user_progress = await self.original_command.db.user_progress.find_one({"user_id": user_id})


                        if not user_progress:
                            await interaction.followup.send("❌ You need to set your stats first with !setstats")
                            return

                        current_weight = user_progress['current_weight']

                        # Save goal
                        await self.original_command.db.user_goals.update_one(
                            {"user_id": user_id},
                            {
                                "$set": {
                                    "user_id": user_id,
                                    "target_weight": float(self.original_command.target_weight),
                                    "goal_type": self.original_command.goal_type,
                                    "start_weight": float(current_weight),
                                    "experience": experience,
                                    "start_date": datetime.utcnow()
                                }
                            },
                            upsert=True
                        )

                        # Calculate target weight
                        if self.original_command.goal_type == 'gain':
                            target_total = current_weight + self.original_command.target_weight
                            progress_text = f"Gain {self.original_command.target_weight}lbs"
                        else:
                            target_total = current_weight - self.original_command.target_weight
                            progress_text = f"Lose {self.original_command.target_weight}lbs"

                        embed = discord.Embed(title="✅ Goal Successfully Set", color=discord.Color.green())
                        embed.add_field(name="Current Weight", value=f"{current_weight}lbs", inline=True)
                        embed.add_field(name="Goal", value=progress_text, inline=True)
                        embed.add_field(name="Target Weight", value=f"{target_total}lbs", inline=True)
                        embed.add_field(name="Experience Level", value=experience.capitalize(), inline=False)
                        embed.set_footer(text="View your progress with !mystats")
                        await interaction.followup.send(embed=embed)

                        # Handle specific experience levels
                        cog_name = experience.capitalize()
                        experience_embed = discord.Embed(
                            title=f"🌟 Welcome, {cog_name}!",
                            description=f"Great choice! As a {experience.lower()}, we'll guide you on your fitness journey.",
                            color=discord.Color.gold()
                        )
                        await interaction.followup.send(embed=experience_embed)

                        cog = self.original_command.bot.get_cog(cog_name)
                        if cog:
                            await getattr(cog, experience.lower())(self.original_command.ctx)
                        else:
                            await interaction.followup.send(
                                f"Please use `{experience.lower()}` to select your workout type")

                    except Exception as e:
                        await interaction.followup.send(f"❌ Unexpected error: {str(e)}")
                    finally:
                        self.stop()

            view = ExperienceView(self)
            embed = discord.Embed(
                title="🏋️ Set Your Experience Level",
                description="This helps customize your fitness plan:",
                color=discord.Color.blue()
            )
            embed.add_field(name="Goal Type", value=goal_type.capitalize(), inline=True)
            embed.add_field(name="Target Weight", value=f"{target_weight}lbs", inline=True)
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            await ctx.send(f"❌ Error setting goal: {str(e)}")


    @commands.command()
    async def mystats(self, ctx):
        """View your complete fitness stats and goal progress"""
        try:
            user_id = ctx.author.id

            # Get user progress document
            user_progress = await self.db.user_progress.find_one({"user_id": user_id})
            if not user_progress:
                await ctx.send("❌ You haven't set your stats yet. Use **setstats** first.")
                return

            height_inches = user_progress.get("height")
            start_weight = user_progress.get("start_weight")
            current_weight = user_progress.get("current_weight")
            age = user_progress.get("age")
            gender = user_progress.get("gender")
            last_updated = user_progress.get("last_updated")

            # Get user goal document (if exists)
            user_goal = await self.db.user_goals.find_one({"user_id": user_id})

            # Convert height to feet and inches
            feet = int(height_inches // 12)
            inches = int(height_inches % 12)

            # Calculate BMI
            bmi = (current_weight / (height_inches ** 2)) * 703
            if bmi < 18.5:
                bmi_category = "Underweight"
            elif 18.5 <= bmi < 25:
                bmi_category = "Healthy Weight"
            elif 25 <= bmi < 30:
                bmi_category = "Overweight"
            else:
                bmi_category = "Obese"

            embed = discord.Embed(
                title=f"{ctx.author.display_name}'s Fitness Profile",
                color=discord.Color.blue()
            )

            # Basic Info
            embed.add_field(name="📊 Basic Info",
                            value=f"**Age:** {age}\n"
                                  f"**Gender:** {gender.capitalize()}\n"
                                  f"**Height:** {feet}'{inches}\"",
                            inline=False)

            # Weight Info
            embed.add_field(name="⚖️ Weight",
                            value=f"**Start:** {start_weight}lbs\n"
                                  f"**Current:** {current_weight}lbs\n"
                                  f"**BMI:** {bmi:.2f} ({bmi_category})",
                            inline=False)

            # Goal Progress
            if user_goal:
                target_weight = user_goal.get("target_weight")
                goal_type = user_goal.get("goal_type")
                goal_start_weight = user_goal.get("start_weight")
                start_date = user_goal.get("start_date")

                # Ensure start_date is datetime
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S.%f")


                if goal_type == 'gain':
                    progress = current_weight - goal_start_weight
                    remaining = target_weight - progress
                    target_total = goal_start_weight + target_weight
                else:  # lose
                    progress = goal_start_weight - current_weight
                    remaining = target_weight - progress
                    target_total = goal_start_weight - target_weight

                percentage = min(100, max(0, (progress / target_weight) * 100))
                days_active = (datetime.utcnow() - start_date).days


                embed.add_field(name="🎯 Goal Progress",
                                value=f"**Goal:** {goal_type.capitalize()} {target_weight}lbs\n"
                                      f"**Progress:** {progress:.1f}lbs ({percentage:.1f}%)\n"
                                      f"**Remaining:** {remaining:.1f}lbs to {target_total}lbs\n"
                                      f"**Active:** {days_active} days",
                                inline=False)
            else:
                embed.add_field(name="🔜 No Active Goal",
                                value="Set a goal with `mygoal [gain/lose] [amount]`",
                                inline=False)

            if last_updated:
                # If last_updated is a datetime object, format nicely
                if isinstance(last_updated, str):
                    try:
                        last_updated_dt = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S.%f")
                    except Exception:
                        last_updated_dt = None
                else:
                    last_updated_dt = last_updated

                if last_updated_dt:
                    last_updated_str = last_updated_dt.strftime("%Y-%m-%d %H:%M:%S UTC")
                    embed.set_footer(text=f"Last updated: {last_updated_str}")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error fetching stats: {str(e)}")

    @commands.command()
    async def resetstats(self, ctx):
        """Completely reset your fitness stats"""

        # Confirmation UI
        class ConfirmView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=30.0)
                self.value = None

            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.danger)
            async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message("This isn't your confirmation!", ephemeral=True)
                    return
                self.value = True
                self.stop()

            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
            async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message("This isn't your confirmation!", ephemeral=True)
                    return
                self.value = False
                self.stop()

        view = ConfirmView()
        embed = discord.Embed(
            title="⚠️ Confirm Stats Reset",
            description="This will **permanently delete** all your fitness data!\n\nAre you sure?",
            color=discord.Color.red()
        )
        msg = await ctx.send(embed=embed, view=view)

        await view.wait()
        await msg.delete()

        if view.value is None:
            return await ctx.send("Reset cancelled (timed out).")
        if not view.value:
            return await ctx.send("Reset cancelled.")

        try:
            user_id = ctx.author.id

            # Delete user data from both collections
            await self.db.user_progress.delete_one({"user_id": user_id})
            await self.db.user_goals.delete_one({"user_id": user_id})

            await ctx.send("✅ All your fitness stats have been reset!")

        except Exception as e:
            await ctx.send(f"❌ Error resetting stats: {str(e)}")


# fitness_tracker.py

async def setup(bot):
    mongo_url = os.getenv("MONGO_URL")
    if not mongo_url:
        raise Exception("MONGO_URL environment variable not found.")

    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    db = client["fitness_db"]

    cog = FitnessTracker(bot, db)
    await bot.add_cog(cog)
