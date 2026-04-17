import os
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import re

app = Flask('')
@app.route('/')
def home():
    return "MAHSER 7/24 AKTIF"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

GELEN_GIDEN_ID = 1492334113829552199
KAYITLI_ROL_ID = 1492329498572755137
KAYITSIZ_ROL_ID = 149431949759504394

@bot.event
async def on_ready():
    print('------------------------------------------')
    print(f'MAHSER SISTEMI BASLATILDI: {bot.user.name}')
    print('------------------------------------------')
    await bot.change_presence(activity=discord.Streaming(name="MAHŞER'in Tek Hakimi ⚔️", url="https://www.twitch.tv/discord"))

@bot.event
async def on_message(message):
    if message.author.bot: return
    if not message.author.guild_permissions.administrator:
        if re.search(r"(discord\.gg/|discord\.com/invite/|discordapp\.com/invite/)", message.content.lower()):
            await message.delete()
            return
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(GELEN_GIDEN_ID)
    if channel:
        embed = discord.Embed(title="Bir Yolcu Geldi!", description=f"Hoş geldin {member.mention}!\nSeninle birlikte **{len(member.guild.members)}** kişi olduk.", color=discord.Color.red())
        await channel.send(embed=embed)
    rol = member.guild.get_role(KAYITSIZ_ROL_ID)
    if rol:
        await member.add_roles(rol)

@bot.command()
async def sunucu(ctx):
    await ctx.send(f"Sunucu İsmi: {ctx.guild.name}\nÜye Sayısı: {ctx.guild.member_count}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! **{round(bot.latency * 1000)}ms**")

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("HATA: DISCORD_TOKEN bulunamadı!")
