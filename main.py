import discord
from discord.ext import commands
import requests
import os

# ENVIRONMENT VARIABLES
DISCORD_TOKEN = os.getenv("VISION_MONITOR_BOT_TOKEN")
STATUS_CHANNEL_ID = int(os.getenv("STATUS_CHANNEL_ID"))  # Channel ID where !status should work

# SERVICE LINKS
BOT_SERVICES = {
    "Attendance Bot": "https://attendance-bot-0glg.onrender.com",
    "Meme Bot": "https://mememachine-rl9p.onrender.com",
    "Quote Bot": "https://dailyquote-cz9i.onrender.com",
    "Inspo Bot": "https://inspo-bot.onrender.com",
    "Client Brief Bot": "https://clientbriefwebhook.onrender.com"
}

# DISCORD BOT SETUP
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ VisionMonitorBot is online as {bot.user}!")

@bot.command()
async def status(ctx):
    if ctx.channel.id != STATUS_CHANNEL_ID:
        return

    embed = discord.Embed(
        title="🔍 Bot Status Report",
        color=0x9ef01a
    )

    for name, url in BOT_SERVICES.items():
        try:
            res = requests.get(url, timeout=10)
            status = "🟢 Online" if res.status_code == 200 else f"🔴 Error ({res.status_code})"
        except Exception as e:
            status = "🔴 Offline"

        embed.add_field(name=name, value=status, inline=False)

    embed.set_footer(text="VisionMonitorBot • AfterVision")
    await ctx.send(embed=embed)

bot.run(DISCORD_TOKEN)
