import os
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "MAHSER 7/24"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

Thread(target=run).start()
import discord
from discord.ext import commands
import re
from datetime import timedelta

intents = discord.Intents.all()
intents.members = True 

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

TOKEN = 'MTQ5NDMxNzU3NTk0Mzc1Mzc4OA.Gn7JZ9.3GgOfndH_bhDzDMYjRSykitJ85eoKpsG6-qVWs' 

GELEN_GIDEN_ID = 1492334113829552199 
KAYITLI_ROL_ID = 1492329498572755137
KAYITSIZ_ROL_ID = 1494319749759504394

@bot.event
async def on_ready():
    print(f'------------------------------------')
    print(f'MAHSER FULL AKTIF: {bot.user}')
    print(f'Butun komutlar yuklendi, sistem canavar!')
    print(f'------------------------------------')
    await bot.change_presence(activity=discord.Streaming(name="MAHŞER'in Tek Hakimi ⚔️", url="https://www.twitch.tv/discord"))

# --- ANTI-REKLAM ---
@bot.event
async def on_message(message):
    if message.author.bot: return
    if not message.author.guild_permissions.administrator:
        if re.search(r"(discord\.gg/|discord\.com/invite/)", message.content.lower()):
            await message.delete()
            await message.channel.send(f"⚠️ {message.author.mention}, reklam yasak!", delete_after=5)
            return
    await bot.process_commands(message)

# --- BILGI KOMUTU ---
@bot.command()
async def bilgi(ctx):
    embed = discord.Embed(title="⚔️ MAHŞER Komut Listesi", color=0xff0000)
    embed.add_field(name=".kayitkur", value="Kayıt sistemini başlatır.", inline=False)
    embed.add_field(name=".duyuru [mesaj]", value="Duyuru geçer.", inline=False)
    embed.add_field(name=".sustur @üye [dakika]", value="Üyeyi susturur.", inline=True)
    embed.add_field(name=".infaz @üye", value="Banlar.", inline=True)
    embed.add_field(name=".sil [sayı]", value="Mesaj siler.", inline=True)
    embed.add_field(name=".kilit", value="Kanalı kilitler/açar.", inline=True)
    await ctx.send(embed=embed)

# --- SUSTUR (MUTE) ---
@bot.command()
@commands.has_permissions(moderate_members=True)
async def sustur(ctx, member: discord.Member, sure: int, *, sebep="Kural İhlali"):
    time = timedelta(minutes=sure)
    await member.timeout(time, reason=sebep)
    await ctx.send(f"🔇 {member.mention}, {sure} dakika boyunca susturuldu. Sebep: {sebep}")

# --- KILIT ---
@bot.command()
@commands.has_permissions(manage_channels=True)
async def kilit(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    if overwrite.send_messages is False:
        overwrite.send_messages = None
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("🔓 Kanal kilidi açıldı.")
    else:
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("🔒 Kanal kilitlendi.")

# --- DIĞER STANDART KOMUTLAR ---
@bot.command()
@commands.has_permissions(administrator=True)
async def duyuru(ctx, *, mesaj):
    await ctx.message.delete()
    embed = discord.Embed(title="📢 DUYURU", description=mesaj, color=0xff0000)
    await ctx.send("@everyone", embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def kayitkur(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="⚔️ MAHŞER'E GİRİŞ", description="✅ bas ve katıl.", color=0xff0000)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id: return
    if str(payload.emoji) == "✅":
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id) or await guild.fetch_member(payload.user_id)
        k, ks = guild.get_role(KAYITLI_ROL_ID), guild.get_role(KAYITSIZ_ROL_ID)
        if k and k not in member.roles:
            await member.add_roles(k)
            if ks: await member.remove_roles(ks)

@bot.event
async def on_member_join(member):
    k = bot.get_channel(GELEN_GIDEN_ID)
    r = member.guild.get_role(KAYITSIZ_ROL_ID)
    if r: await member.add_roles(r)
    if k: await k.send(f"🔥 **{member.mention}** geldi!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def sil(ctx, miktar: int):
    await ctx.channel.purge(limit=miktar + 1)

@bot.command()
@commands.has_permissions(ban_members=True)
async def infaz(ctx, u: discord.Member):
    await u.ban()
    await ctx.send(f"💀 {u.name} infaz edildi.")

bot.run(TOKEN)