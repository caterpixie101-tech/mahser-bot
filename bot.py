Haklısın kral, botu çalıştıracağız diye asıl "mahşer" kısmını, yani o ağır korumaları ve komutları iskelette unuttuk. Bot açıldıysa motoru çalıştırdık demektir, şimdi içine silahları yükleme vakti.

O "az komut" meselesini kökten çözüyoruz. İstediğin o 120 satırlık doluluğu verecek; küfür engelinden, reklam korumasına, kayıt sisteminden, gelişmiş yetkili komutlarına kadar her şeyi içine ekledim.

GitHub'daki bot.py dosyasını tamamen sil ve bu "full paket" kodu yapıştır:

Python
import os
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import re
import asyncio

# --- FLASK SİSTEMİ (7/24) ---
app = Flask('')
@app.route('/')
def home():
    return "MAHSER 7/24 AKTIF"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT AYARLARI ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

# --- SENİN IDLERİN ---
GELEN_GIDEN_ID = 1492334113829552199
KAYITLI_ROL_ID = 1492329498572755137
KAYITSIZ_ROL_ID = 149431949759504394

# --- KORUMA LİSTELERİ ---
KUFUR_LISTESI = ["amk", "piç", "oç", "sik", "amına", "göt", "yarrak", "daşşak"] # Burayı istediğin kadar uzatabilirsin

@bot.event
async def on_ready():
    print(f'------------------------------------------')
    print(f'MAHSER FULL AKTIF: {bot.user.name}')
    print(f'Sistem canavar gibi calisiyor!')
    print(f'------------------------------------------')
    await bot.change_presence(activity=discord.Streaming(name="MAHŞER'in Tek Hakimi ⚔️", url="https://www.twitch.tv/discord"))

# --- ANA KORUMA VE MESAJ SİSTEMİ ---
@bot.event
async def on_message(message):
    if message.author.bot: return

    # 1. REKLAM KORUMASI
    if not message.author.guild_permissions.administrator:
        if re.search(r"(discord\.gg/|discord\.com/invite/|http|https)", message.content.lower()):
            await message.delete()
            return await message.channel.send(f"{message.author.mention}, reklam yasak evlat! ⚠️", delete_after=3)

    # 2. KÜFÜR KORUMASI
    if not message.author.guild_permissions.administrator:
        if any(kelime in message.content.lower() for kelime in KUFUR_LISTESI):
            await message.delete()
            return await message.channel.send(f"{message.author.mention}, üslubunu takın! ⛔", delete_after=3)

    await bot.process_commands(message)

# --- KAYIT VE HOŞ GELDİN ---
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(GELEN_GIDEN_ID)
    if channel:
        embed = discord.Embed(title="Mahşere Bir Ruh Düştü!", description=f"Hoş geldin {member.mention}!\n\nSeninle birlikte **{len(member.guild.members)}** kişi olduk.\nKayıt için yetkilileri bekle!", color=0xff0000)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        await channel.send(embed=embed)
    
    rol = member.guild.get_role(KAYITSIZ_ROL_ID)
    if rol: await member.add_roles(rol)

# --- KOMUTLAR ---
@bot.command()
@commands.has_permissions(administrator=True)
async def temizle(ctx, miktar: int = 100):
    await ctx.channel.purge(limit=miktar)
    await ctx.send(f"🗑️ **{miktar}** mesaj mahşerin ateşinde yok edildi!", delete_after=5)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def kayıt(ctx, member: discord.Member, *, isim: str):
    kayitli = ctx.guild.get_role(KAYITLI_ROL_ID)
    kayitsiz = ctx.guild.get_role(KAYITSIZ_ROL_ID)
    if kayitli and kayitsiz:
        await member.add_roles(kayitli)
        await member.remove_roles(kayitsiz)
        await member.edit(nick=f"⚔️ {isim}")
        await ctx.send(f"✅ {member.mention} başarıyla kaydedildi!")

@bot.command()
async def sunucu(ctx):
    embed = discord.Embed(title=f"🛡️ {ctx.guild.name} Bilgileri", color=0x000000)
    embed.add_field(name="Üye Sayısı", value=ctx.guild.member_count, inline=True)
    embed.add_field(name="Sahibi", value=ctx.guild.owner, inline=True)
    embed.set_image(url=ctx.guild.icon.url if ctx.guild.icon else None)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, sebep="Yok"):
    await member.ban(reason=sebep)
    await ctx.send(f"🚀 {member.name} mahşerden kovuldu! Sebep: {sebep}")

@bot.command()
async def ping(ctx):
    await ctx.send(f"⚡ Hızımız: **{round(bot.latency * 1000)}ms**")

@bot.command()
async def yardim(ctx):
    help_text = """
**🛡️ MAHŞER SİSTEMİ KOMUTLARI**
`.sunucu` : Sunucu istatistiklerini gösterir.
`.ping` : Botun hızını ölçer.
`.temizle <sayı>` : Mesajları toplu siler (Yetkili).
`.kayıt @üye isim` : Üyeyi kaydeder (Yetkili).
`.ban @üye` : Üyeyi banlar (Yetkili).

*Botta otomatik Reklam ve Küfür koruması aktiftir!*
    """
    await ctx.send(help_text)

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
