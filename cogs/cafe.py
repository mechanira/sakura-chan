import discord, random, json, requests, math, time, datetime, aiohttp, asyncio
from typing import Optional
from discord import app_commands
from discord.ext import commands, tasks

class cafe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lb = {}
        self.total = []
        self.lb_update.start()

    @app_commands.command(name="cafe", description="Manage your personal café")
    async def cafe(self, interaction: discord.Interaction, user: Optional[discord.User]):
        dat = self.load_data()

        if user == None:
            user = interaction.user

        if str(user.id) in dat:
            profile = dat[str(user.id)]
            await interaction.response.send_message(f"**{user.name}'s Café**\n\nMoney: ${profile['money']:,}\nCoffee sold: {profile['coffee_sold']}\nCreated at: {datetime.datetime.utcfromtimestamp(profile['creation_date']).strftime('%B %d, %Y')}")
            return
        
        if interaction.user != user:
            await interaction.response.send_message(f"User {user.mention} does not have a café", ephemeral=True)
            return
        
        self.create_account(user.id)
        await interaction.response.send_message("Your account has been created! Use the command again to view your profile")

    
    @app_commands.command(name="work", description="Run your Café. Has a cooldown of 60 minutes")
    async def work(self, interaction: discord.Interaction):
        dat = self.load_data()

        if str(interaction.user.id) not in dat:
            await interaction.response.send_message("You haven't started a café yet. Do /cafe to get started", ephemeral=True)
            return
        
        if int(time.time()) < dat[str(interaction.user.id)]['cooldown']:
            await interaction.response.send_message(f"You can run the command again <t:{dat[str(interaction.user.id)]['cooldown']}:R>.", ephemeral=True)
            return

        sales = random.randrange(1,10)
        earned = sales
        
        with open("data.json", "w") as f:
            dat[str(interaction.user.id)]['coffee_sold'] += sales
            dat[str(interaction.user.id)]['money'] += earned
            dat[str(interaction.user.id)]['cooldown'] = int(time.time()) + 3600

            json.dump(dat, f, indent=4)

        emb = discord.Embed(title="Shift results...", description=f"Sold: {sales} coffee\nEarned: ${earned}\n\nBalance: {dat[str(interaction.user.id)]['money']}", color=interaction.user.top_role.color)
        await interaction.response.send_message(embed=emb)
    

    @tasks.loop(minutes=1)
    async def lb_update(self):
        dat = self.load_data()

        for data in dat:
            money_dat = int(data)
            total_amount = dat[data]["money"]
            self.lb[total_amount] = money_dat
            self.total.append(total_amount)

        self.total = set(self.total)
        self.total = sorted(self.total, reverse=True)


    @app_commands.command(name="leaderboard", description="View the top cafeterias")
    async def leaderboard(self, interaction: discord.Interaction):
        index = 1
        desc = ""

        for amt in self.total:
            id_ = self.lb[amt]
            member = await self.bot.fetch_user(id_)
            desc += f"#{index} - {member.mention}・${amt:,}\n"

            if index == 10:
                break

            index += 1
        
        emb = discord.Embed(title="Sakura-chan Leaderboard", description=desc)
        emb.set_author(name="Money", icon_url=self.bot.user.display_avatar.url)
        emb.set_footer(text="Leaderboard refreshes every 60 seconds")

        await interaction.response.send_message(embed=emb)


    @app_commands.command(name="give", description="Give a user some of your money")
    async def give(self, interaction: discord.Interaction, user: discord.User, amount: int):
        dat = self.load_data()

        if amount > dat[str(interaction.user.id)]['money']:
            await interaction.response.send_message(f"You don't have ${amount:,} to give\nBalance: ")
            return
        
        with open("data.json", "w") as f:
            dat[str(interaction.user.id)]['money'] -= amount
            dat[str(user.id)]['money'] += amount

            json.dump(dat, f, indent=4)

        await interaction.response.send_message(f"Gave **${amount:,}** to {user.mention}")


    def load_data(self):
        with open("data.json") as f:
            dat = json.load(f)
        return dat
    
    def create_account(self, id):
        dat = self.load_data()

        with open("data.json", "w") as f:
            dat[str(id)] = {
                "money": 0,
                "coffee_sold": 0,
                "cooldown": 0,
                "creation_date": int(time.time())
            }

            json.dump(dat, f, indent=4)
    



async def setup(bot):
    await bot.add_cog(cafe(bot))