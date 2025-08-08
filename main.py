import os
import discord
from discord.ext import commands

from keep_alive import keep_alive # keep browser open
keep_alive()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
# call action
async def ping(ctx):
    await ctx.send("I'm here.")
    
    
# Role 自動分配設定
ROLES = os.environ["ROLE_MESSAGE_ID"]  # ← 換成你要讓大家點 emoji 的訊息 ID
ROLE_EMOJI_MAP = {
    "🎮": "Gamer",       # emoji 對應到 Discord 裡的角色名稱
    "📚": "Student",
    "🎨": "Artist"
}

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != ROLES:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    emoji = str(payload.emoji)
    role_name = ROLE_EMOJI_MAP.get(emoji)
    if role_name is None:
        return

    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        return

    member = await guild.fetch_member(payload.user_id)
    if member is not None:
        await member.add_roles(role)
        print(f"✅ Added {role.name} to {member.display_name}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != ROLES:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    emoji = str(payload.emoji)
    role_name = ROLE_EMOJI_MAP.get(emoji)
    if role_name is None:
        return

    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
        return

    member = await guild.fetch_member(payload.user_id)
    if member is not None:
        await member.remove_roles(role)
        print(f"🗑️ Removed {role.name} from {member.display_name}")

    
    
TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN) # token from bot
