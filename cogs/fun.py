import discord, random, json, requests, math, datetime, aiohttp, asyncio, typing, functions, time
from discord import app_commands
from discord.ext import commands
from bs4 import BeautifulSoup

class fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="qotd", description="Displays a daily qoute")
    async def qotd(self, interaction: discord.Interaction):
        response = requests.get("https://quotes.rest/qod?language=en")
        json_resp = response.json()
        quote = json_resp["contents"]["quotes"][0]["quote"]
        author = json_resp["contents"]["quotes"][0]["author"]
        banner = json_resp["contents"]["quotes"][0]["background"]

        emb = discord.Embed(
            title="Quote of the Day",
            description=f"{quote}\n**~ {author}**",
            timestamp=datetime.date.today()
        )
        emb.set_image(url=banner)

        await interaction.response.send_message(embed=emb)


    @app_commands.command(name="ship", description="Ship two members")
    async def ship(self, interaction: discord.Interaction, member: discord.Member, member_2: typing.Optional[discord.Member] = None):
        if member_2 is None:
            member_2 = interaction.user

        pair = str(member.id) + str(member_2.id)
        random.seed(hash(pair))
        percentage = random.randint(0, 100)

        loaded = 0
        emojis = ["broken_heart", "sob", "pensive", "slight_smile", "relieved", "wink", "relaxed", "smiling_face_with_3_hearts", "heart_eyes", "heart_on_fire"]

        emoji = emojis[math.trunc(percentage / len(emojis))]
        
        await interaction.response.send_message(f"*Calculating {member.mention}'s love for {member_2.mention}...*")

        await asyncio.sleep(1)

        while(loaded < percentage): # loading screen loop
            await asyncio.sleep(1)

            loaded += random.randint(1,30)
            if loaded > percentage:
                loaded = percentage

            load_div = round(loaded / 5)
            bar = "█" * load_div
            bar += "░" * (20 - load_div)

            await interaction.edit_original_response(content=f"*Calculating {member.mention}'s love for {member_2.mention}...*\n| {bar} | ???")

        await interaction.edit_original_response(content=f"{member.mention} x {member_2.mention} = **{percentage}%**\n| {bar} | :{emoji}:")

        if percentage == 69:
            await interaction.original_response.add_reaction("ok_hand")

    
    @app_commands.command(name="meter", description="Show someone's meter")
    async def meter(self, interaction: discord.Interaction, name: str, member: typing.Optional[discord.Member] = None):
        value = random.randint(0,100)
        divide = math.trunc(value / 5)

        bar = "█" * divide
        bar += "░" * (20 - divide)

        if member is None:
            member = interaction.user
        await interaction.response.send_message(f"{member.mention}'s **\"{name}\"** meter is at **{value}%**\n| {bar} |")


    @app_commands.command(name="gelbooru", description="View the gelbooru gallery", nsfw=True)
    async def gelbooru(self, cmd_interaction: discord.Interaction, tags: str):
        img = functions.gelbooru(tags)

        if img is None:
            await cmd_interaction.response.send_message("No results.", ephemeral=True)

        view = discord.ui.View()
        next_btn = discord.ui.Button(label="New Image", style=discord.ButtonStyle.primary)

        async def next_callback(button_inter: discord.Interaction): 
            await button_inter.response.send_message(random.choice(img), view=view)

        next_btn.callback = next_callback
        view.add_item(next_btn)

        await cmd_interaction.response.send_message(random.choice(img), view=view)


async def setup(bot):
    await bot.add_cog(fun(bot))