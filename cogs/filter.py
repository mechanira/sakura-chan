import discord, random, json, requests, functions, time
from typing import Optional
from discord import app_commands
from discord.ext import commands

class filter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.uwuify = []


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.id in self.uwuify:
            webhook_name = "Bitling Messaging"
            webhooks = await message.channel.webhooks()
            webhook_names = [x.name for x in webhooks]

            if webhook_name in webhook_names:
                for x in webhooks:
                    if x.name == webhook_name:
                        webhook = x
                        break
            else:
                webhook = await message.channel.create_webhook(name=webhook_name)  
            
                    
            if message.author.id in self.uwuify:
                filtered_content = functions.uwuify(message.content)
            else:
                return

            if message.reference is not None:
                msg = await message.channel.fetch_message(message.reference.message_id)
                embed = discord.Embed(description=msg.content)
                embed.set_author(
                    name=f"{msg.author.display_name} ↩️",
                    url=msg.jump_url,
                    icon_url=msg.author.display_avatar.url
                    )
            else:
                embed = None

            await webhook.send(
                    filtered_content,
                    username=message.author.display_name,
                    avatar_url=message.author.display_avatar.url,
                    embed=embed,
                    files=message.attachments
                )
            await message.delete()


    @app_commands.command(name="uwu", description="uwuify yourself~")
    async def uwu(self, interaction: discord.Interaction):
        if interaction.user.id not in self.uwuify:
            self.uwuify.append(interaction.user.id)
            await interaction.response.send_message("Uwuifier activated! Use `/uwu` again to deactivate it", ephemeral=True)
        else:
            self.uwuify.remove(interaction.user.id)
            await interaction.response.send_message("Uwuifier deactivated!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(filter(bot))