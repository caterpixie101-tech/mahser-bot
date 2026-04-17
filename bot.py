import os
from flask import Flask
from threading import Thread
import discord
from discord.ext import commands
import re
import asyncio

# --- FLASK SİSTEMİ (7/24 AKTİF TUTAR) ---
app = Flask('')
@app.route('/')
def home():
    return "MAHSER SISTEMI ONLINE"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT AYARLARI ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

# --- SENİN SUNUCU BİLGİLERİN ---
GELEN_GIDEN_ID = 1492334113829552199
KAYITLI_ROL_ID = 1492329498572755137
KAYITSIZ_ROL_ID = 149431949759504394

# --- KORUMA AYARLARI ---
KUFUR_ENGEL = True
REKLAM_ENGEL = True

@bot.event
async def on_ready():
    print(f'------------------------------------------')
    print(f'MAHSER FULL AKTIF: {bot.user.name}')
    print(f'Butun koruma sistemleri devreye girdi!')
    print(f'------------------------------------------')
    await bot.change_presence(activity=discord.Streaming(name="MAHŞER'in Tek Hakimi ⚔️", url="https://www.twitch.tv/discord"))

# --- ANA KORUMA MOTORU ---
@bot.event
async def on_message(message):
    if message.author.bot: return

    # Yetkili değilse korumalara takılır
    if not message.author.guild_permissions.administrator:
        
        # Reklam Engeli
        if REKLAM_ENGEL and re.search(r"(discord\.gg/|discord\.com/invite/|http|https|www)", message.content.lower()):
            await message.delete()
            return await message.channel.send(f"{message.author.mention}, reklam yasak! ⚠️", delete_after=4)

        # Küfür Engeli (Temel Kelimeler)
        kufurler = ["amk", "pıc", "sik", "ananı", "orospu", "oç", "göt", "yarrak"]
        if KUFUR_ENGEL and any(word in message.content.lower() for word in kufurler):
            await message.delete()
            return await message.channel.send(f"{message.author.mention}, üslubuna dikkat et! ⛔", delete_after=4)

    await bot.process_commands(message)

# --- OTOMATİK KAYIT VE HOŞ GELDİN ---
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(GELEN_GIDEN_ID)
    if channel:
        embed = discord.Embed(title="Mahşere Yeni Bir Ruh Geldi!", description=f"Hoş geldin {member.mention}!\n\nSeninle birlikte **{len(member.guild.members)}** kişi olduk.\n\nKayıt için yetkilileri bekle!", color=0xff0000)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.set_footer(text="MAHŞER Koruma Sistemi")
        await channel.send(embed=embed)
    
    # Kayıtsız rolünü ver
    rol = member.guild.get_role(KAYITSIZ_ROL_ID)
    if rol:
        await member.add_roles(rol)

# --- YETKİLİ VE KULLANICI KOMUTLARI ---
@bot.command()
@commands.has_permissions(administrator=True)
async def temizle(ctx, miktar: int = 100):
    await ctx.channel.purge(limit=miktar)
    await ctx.send(f"🗑️ **{miktar}** mesaj mahşerin ateşinde yakıldı.", delete_after=5)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def kayıt(ctx, member: discord.Member, *, isim: str):
    k_rol = ctx.guild.get_role(KAYITLI_ROL_ID)
    u_rol = ctx.guild.get_role(KAYITSIZ_ROL_ID)
    if k_rol and u_rol:
        await member.add_roles(k_rol)
        await member.remove_roles(u_rol)
        await member.edit(nick=f"⚔️ {isim}")
        await ctx.send(f"✅ {member.mention} başarıyla kayıt edildi!")

@bot.command()
async def sunucu(ctx):
    embed = discord.Embed(title=f"🛡️ {ctx.guild.name} Bilgileri", color=0x000000)
    embed.add_field(name="Toplam Üye", value=ctx.guild.member_count, inline=True)
    embed.add_field(name="Sunucu Sahibi", value=ctx.guild.owner, inline=True)
    embed.set_image(url=ctx.guild.icon.url if ctx.guild.icon else None)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f"⚡ Mahşer Hızı: **{round(bot.latency * 1000)}ms**")

@bot.command()
async def yardim(ctx):
    embed = discord.Embed(title="📜 MAHŞER KOMUT MENÜSÜ", color=0xffffff)
    embed.add_field(name=".sunucu", value="Sunucu durumunu gösterir.", inline=False)
    embed.add_field(name=".ping", value="Botun gecikmesini gösterir.", inline=False)
    embed.add_field(name=".temizle <sayı>", value="Mesajları siler (Yetkili).", inline=False)
    embed.add_field(name=".kayıt @üye isim", value="Üyeyi kaydeder (Yetkili).", inline=False)
    embed.set_footer(text="Reklam ve Küfür koruması otomatik aktiftir.")
    await ctx.send(embed=embed)

# --- ÇALIŞTIRMA ---
if __name__ == "__main__":
    keep_alive()
    # Şifreyi Render'ın Environment kısmındaki DISCORD_TOKEN'dan çeker
    TOKEN = os.getenv('DISCORD_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("HATA: DISCORD_TOKEN bulunamadı!")
