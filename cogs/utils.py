import discord, random, json, requests, asyncio, openai, time
from typing import Optional
from discord import app_commands
from discord.ext import commands


class utils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="ping", description="Is the bot on?")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")


    @app_commands.command(name="messageraw", description="Fetch raw message content data")
    async def messageraw(self, interaction: discord.Interaction, msg: str):
        message = await interaction.channel.fetch_message(msg)

        emb=discord.Embed(
            title=message.author.name + "#" + message.author.discriminator,
            description=f"`{message.content}`",
            color=0x2f3136
        )
        emb.set_author(name="#" + message.channel.name, url=message.channel.jump_url, icon_url=message.guild.icon.url)
        emb.set_thumbnail(url=message.author.avatar.url)
        await interaction.response.send_message(embed=emb, ephemeral=True)


    @app_commands.command(name="avatar", description="Get the user's avatar")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(member.avatar.url, ephemeral=True)


    @app_commands.command(name="say", description="Say something")
    async def say(self, interaction: discord.Interaction, text: str, reference: Optional[str], file: Optional[discord.Attachment]):
        if interaction.user.id in [1091792738929877126]:
            await interaction.response.send_message(f"Message sending...\nETA: {len(text) * 0.05} seconds", ephemeral=True)

            async with interaction.channel.typing():
                await asyncio.sleep(len(text) * 0.05)
            
            if reference is not None:
                ref = await interaction.channel.fetch_message(reference)
                await interaction.channel.send(text, reference=ref, file=file)
            else:
                await interaction.channel.send(text, file=file)
            await interaction.delete_original_response()


    @app_commands.command(name="emoji", description="Sends image file of emoji")
    async def getemoji(self, interaction: discord.Interaction, emoji: str):
        emoji_data = discord.PartialEmoji.from_str(emoji)

        if not emoji_data.is_custom_emoji():
            await interaction.response.send_message("This command only works with custom emojis.", ephemeral=True)

        await interaction.response.send_message(emoji_data.url, ephemeral=True)


    @app_commands.command(name="hyperlink", description="Generates a neat marked down hyperlink")
    async def hyperlink(self, interaction: discord.Interaction, text: str, link: str):
        await interaction.response.send_message(f"[{text}]({link})", suppress_embeds=True)


    @app_commands.command(name="chatgpt", description="ChatGPT API inside Discord")
    async def chatgpt(self, interaction: discord.Interaction, prompt: str, tags: Optional[str]):
        await interaction.response.send_message(f'Prompt: {prompt}\nTags: {tags}')

        try:
            async with interaction.channel.typing():
                openai.api_key = "key"
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{prompt}"}])
                completed = completion.choices[0].message.content

            emb = discord.Embed(title="Prompt complete!", description=completed)
            await interaction.channel.send(embed=emb)
        except Exception as e:
            await interaction.channel.send(f"Process failed: {e}")



async def setup(bot):
    await bot.add_cog(utils(bot))
