import os
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import re

app = Flask('')
@app.route('/')
def home():
    return "MAHSER 7/24"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

Thread(target=run).start()

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

GELEN_GIDEN_ID = 1492334113829552199
KAYITLI_ROL_ID = 1492329498572755137
KAYITSIZ_ROL_ID = 149431949759504394

@bot.event
async def on_ready():
    print(f'MAHSER FULL AKTIF: {bot.user}')
    await bot.change_presence(activity=discord.Streaming(name="MAHŞER'in Tek Hakimi ⚔️", url="https://www.twitch.tv/discord"))

@bot.event
async def on_message(message):
    if message.author.bot: return
    if not message.author.guild_permissions.administrator:
        if re.search(r"(discord\.gg/|discord\.com/invite/)", message.content.lower()):
            await message.delete()
            return
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(GELEN_GIDEN_ID)
    if channel:
        await channel.send(f"Hoş geldin {member.mention}! Seninle birlikte {len(member.guild.members)} kişi olduk.")
    rol = member.guild.get_role(KAYITSIZ_ROL_ID)
    if rol:
        await member.add_roles(rol)

@bot.command()
async def sunucu(ctx):
    await ctx.send(f"Sunucu İsmi: {ctx.guild.name}\nÜye Sayısı: {ctx.guild.member_count}")

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
