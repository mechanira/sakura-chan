import os, asyncio, config, time, platform
import discord
from discord.ext import commands
from colorama import Back, Fore, Style

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="sc!", intents=intents)



@bot.event
async def on_ready():
    await bot.change_presence(
        status = discord.Status.online,
        activity = discord.Game("unstable beta | in development...")
        )
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prfx + " Logged in as " + Fore.YELLOW + bot.user.name)
    print(prfx + " Bot ID " + Fore.YELLOW + str(bot.user.id))
    print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
    print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
    synced = await bot.tree.sync()
    print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")


async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')



async def main():
    await load()
    await bot.start(config.BOT_TOKEN)

asyncio.run(main())