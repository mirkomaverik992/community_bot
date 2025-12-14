import discord
from discord.ext import commands
import json
import random
import asyncio
import os
TOKEN = os.getenv("DISCORD_BOT_TOKEN")



intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ⚠️ SOSTITUISCI CON L'ID DELLA TUA CATEGORIA "STANZE"
ROOM_CATEGORY_ID = 1449790657505005618 # <-- METTI QUI L'ID (numero)


ROOM_NAME_PRESETS = {
    "valorant": "🎯-valorant-lobby",
    "lol": "🧿-league-of-legends",
    "league": "🧿-league-of-legends",
    "cs": "🔫-counter-strike",
    "cs2": "🔫-cs2-lobby",
    "fortnite": "🎮-fortnite",
    "minecraft": "⛏️-minecraft",
    "warzone": "🎯-warzone",
    "apex": "🏹-apex-legends",
    "overwatch": "🛡️-overwatch",
    "rocket": "⚽-rocket-league",
    "fifa": "⚽-fifa",
    "ea-fc": "⚽-ea-fc",
    "gta": "🚗-gta-online",
    "cod": "🔫-call-of-duty",
    "pubg": "🎯-pubg",
    "among": "👽-among-us",
    "fallguys": "🎪-fall-guys",
}

# ============================
# XP SYSTEM
# ============================

try:
    with open('xp.json', 'r') as f:
        xp_data = json.load(f)
except:
    xp_data = {}

def save_xp():
    with open('xp.json', 'w') as f:
        json.dump(xp_data, f)

def get_level(xp: int):
    if xp >= 2000: return 6, "💎 ELITE"
    elif xp >= 1000: return 5, "⭐⭐⭐⭐⭐ LEGEND"
    elif xp >= 600: return 4, "⭐⭐⭐⭐ VETERAN"
    elif xp >= 300: return 3, "⭐⭐⭐ REGULAR"
    elif xp >= 100: return 2, "⭐⭐ ACTIVE"
    else: return 1, "⭐ NEWBIE"

cooldowns = {}
room_owners = {}  # {channel_id: owner_id}

# ============================
# EVENTI
# ============================

@bot.event
async def on_ready():
    print(f"🤖 {bot.user} online in {len(bot.guilds)} server!")
    print("✅ Comandi disponibili: !comandi, !level, !top, !profilo, !creastanza, !chiudistanza")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    uid = str(message.author.id)
    now = asyncio.get_event_loop().time()

    if uid in cooldowns and now - cooldowns[uid] < 45:
        await bot.process_commands(message)
        return

    cooldowns[uid] = now

    xp_gain = random.randint(2, 6)
    old_xp = xp_data.get(uid, 0)
    xp_data[uid] = old_xp + xp_gain

    old_level, _ = get_level(old_xp)
    new_level, badge = get_level(xp_data[uid])

    if new_level > old_level:
        embed = discord.Embed(
            title="🎉 LEVEL UP!",
            description=f"{message.author.mention} è salito al **Livello {new_level}** {badge}!\n(+{xp_gain} XP)",
            color=0xffd700
        )
        embed.set_thumbnail(url=message.author.display_avatar.url)
        await message.channel.send(embed=embed)

    save_xp()
    await bot.process_commands(message)

# ============================
# COMANDI XP
# ============================

@bot.command()
async def level(ctx):
    uid = str(ctx.author.id)
    xp = xp_data.get(uid, 0)
    level, badge = get_level(xp)

    embed = discord.Embed(
        title=f"📊 Profilo di {ctx.author.display_name}",
        color=0x00ff88
    )
    embed.add_field(name="Livello", value=f"**{level}** {badge}", inline=True)
    embed.add_field(name="XP totali", value=f"**{xp}**", inline=True)
    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def top(ctx):
    if not xp_data:
        await ctx.send("🏆 Nessun dato XP ancora, inizia a scrivere in chat!")
        return

    top_users = sorted(xp_data.items(), key=lambda x: int(x[1]), reverse=True)[:10]
    embed = discord.Embed(title="🏆 TOP 10 del server", color=0xffd700)

    for i, (uid, xp) in enumerate(top_users, 1):
        user = bot.get_user(int(uid))
        name = user.display_name if user else f"User {uid[-4:]}"
        level, badge = get_level(xp)
        embed.add_field(
            name=f"{i}. {name}",
            value=f"Livello **{level}** {badge} — {xp} XP",
            inline=False
        )

    await ctx.send(embed=embed)

@bot.command(aliases=["rank", "profile"])
async def profilo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    uid = str(member.id)
    xp = xp_data.get(uid, 0)
    level, badge = get_level(xp)

    embed = discord.Embed(
        title=f"📊 Profilo di {member.display_name}",
        color=0x5865F2
    )
    embed.add_field(name="Livello", value=f"**{level}** {badge}", inline=True)
    embed.add_field(name="XP", value=f"**{xp}**", inline=True)
    embed.set_thumbnail(url=member.display_avatar.url)
    await ctx.send(embed=embed)

# ============================
# HELP / COMANDI
# ============================

def build_commands_embed():
    embed = discord.Embed(
        title="🤖 Comandi Bot Community",
        description="Bot pensato per tenere viva la community con XP e stanze veloci.",
        color=0x7289da
    )
    embed.add_field(
        name="📊 Livelli & XP",
        value="`!level` — vedi il tuo livello\n"
              "`!top` — classifica server\n"
              "`!profilo [@utente]` — profilo dettagliato",
        inline=False
    )
    embed.add_field(
        name="🕹️ Stanze",
        value="`!creastanza [gioco/nome]` — crea una stanza temporanea\n"
              "`!chiudistanza` — chiudi la stanza in cui sei",
        inline=False
    )
    embed.add_field(
        name="ℹ️ Info",
        value="`!comandi` — mostra questa lista\n"
              "`!helpme` — stessa cosa di `!comandi`",
        inline=False
    )
    embed.set_footer(text="Partecipa in chat, sali di livello e crea stanze per giocare o parlare.")
    return embed

@bot.command()
async def comandi(ctx):
    await ctx.send(embed=build_commands_embed())

@bot.command()
async def helpme(ctx):
    await ctx.send(embed=build_commands_embed())

# ============================
# STANZE TEMPORANEE
# ============================

@bot.command()
async def creastanza(ctx, *, nome: str = None):
    if ROOM_CATEGORY_ID == 0:
        await ctx.send("⚠️ La categoria per le stanze non è configurata. Avvisa l'admin del server.")
        return

    guild = ctx.guild
    category = guild.get_channel(ROOM_CATEGORY_ID)
    if category is None:
        await ctx.send("⚠️ Non trovo la categoria per le stanze. Avvisa l'admin del server.")
        return

    if nome is None:
        base_name = f"stanza-di-{ctx.author.display_name}"
    else:
        key = nome.lower().strip()
        if key in ROOM_NAME_PRESETS:
            base_name = ROOM_NAME_PRESETS[key]
        else:
            base_name = nome.lower().replace(" ", "-")

    safe_name = "".join(
        c for c in base_name
        if c.isalnum() or c in "-_🇮🇹🎯🧿🔫🎮⛏️🚗⚽👽🎪"
    ).strip("-")[:80]

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(connect=True, speak=True),
        ctx.author: discord.PermissionOverwrite(manage_channels=True)
    }

    try:
        channel = await category.create_voice_channel(name=safe_name, overwrites=overwrites)
        room_owners[channel.id] = ctx.author.id

        await ctx.send(
            f"🎤 Stanza vocale creata: {channel.mention}\n"
            f"Entra nel canale vocale e parla! Usa `!chiudistanza` per chiuderla."
        )
    except Exception as e:
        await ctx.send(f"❌ Errore nella creazione della stanza: {e}")

@bot.command()
async def chiudistanza(ctx):
    channel = ctx.channel
    if channel.id not in room_owners:
        await ctx.send("❌ Questo canale non è una stanza temporanea creata dal bot.")
        return

    owner_id = room_owners[channel.id]
    if ctx.author.id != owner_id and not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ Solo il creatore della stanza o lo staff possono chiuderla.")
        return

    await ctx.send("🧹 Ok, chiudo questa stanza…")
    del room_owners[channel.id]
    await channel.delete(reason="Stanza temporanea chiusa dal comando !chiudistanza")

if __name__ == "__main__":
    bot.run(TOKEN)
