import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Disable default help command to avoid conflicts
bot.remove_command("help")

# Role & Channel IDs
ADMIN_ROLE_ID = int(os.getenv('ADMIN_ROLE_ID'))
CLIENT_ROLE_ID = int(os.getenv('CLIENT_ROLE_ID'))
ADMIN_CHANNEL_ID = int(os.getenv('ADMIN_CHANNEL_ID'))

# Check if the user has a role
def has_role(ctx, role_id):
    return any(role.id == role_id for role in ctx.author.roles)

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="!help for commands"))

# HWID Reset Command
@bot.command()
async def hwid(ctx, key: str):
    if not has_role(ctx, CLIENT_ROLE_ID):
        await ctx.send("❌ You do not have permission to request HWID reset.")
        return
    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if admin_channel:
        await admin_channel.send(f"⚙️ HWID reset requested for key `{key}` from `{ctx.author.name}`")
        await ctx.send(f"✅ Your HWID reset request for key `{key}` has been sent to the admin.")

# Freeze Key Command
@bot.command()
async def freeze(ctx, key: str):
    if not has_role(ctx, CLIENT_ROLE_ID):
        await ctx.send("❌ You do not have permission to freeze keys.")
        return
    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if admin_channel:
        await admin_channel.send(f"🧊 Key `{key}` has been frozen by `{ctx.author.name}`")
        await ctx.send(f"✅ The key `{key}` has been frozen and reported to the admin.")

# Ban Key Command
@bot.command()
async def ban(ctx, key: str):
    if not has_role(ctx, CLIENT_ROLE_ID):
        await ctx.send("❌ You do not have permission to ban keys.")
        return
    admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if admin_channel:
        await admin_channel.send(f"⛔ Key `{key}` has been banned by `{ctx.author.name}`")
        await ctx.send(f"✅ The key `{key}` has been banned and reported to the admin.")

# Generate Key Command
@bot.command()
async def gen(ctx, key_type: str, amount: int):
    if not has_role(ctx, CLIENT_ROLE_ID):
        await ctx.send("❌ You do not have permission to generate keys.")
        return

    key_type = key_type.lower()
    if key_type not in ["day", "week", "month", "lifetime", "4hour"]:
        await ctx.send("❌ Invalid key type. Valid types: `day`, `week`, `month`, `lifetime`, `4hour`.")
        return

    # Simulating key generation (replace with actual key logic)
    generated_keys = [f"{key_type.upper()}-KEY-{i+1}" for i in range(amount)]

    try:
        await ctx.author.send(f"🔑 Your `{key_type}` keys: {', '.join(generated_keys)}")
        await ctx.send(f"✅ `{amount}` `{key_type}` key(s) have been sent to your DMs.")
    except discord.Forbidden:
        await ctx.send("⚠️ I couldn't DM you! Please enable DMs and try again.")

# Start the keep_alive server and run the bot
keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
