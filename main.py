import discord
import os
import random
import traceback
import requests
import json
import sqlite3
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta

# Replace with your actual Discord User ID(s)
ALLOWED_USERS = [1101467683083530331, 987654321098765432]

# Check if user is allowed
def is_allowed_user():
    async def predicate(ctx):
        if ctx.author.id not in ALLOWED_USERS:
            raise commands.CheckFailure  # Just raise the error, don't send a message
        return True
    return commands.check(predicate)



intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Needed for role management & DMs
intents.presences = True  # Enables presence updates (required for status changes)

# Add rate limiting to prevent Discord API rate limits
import aiohttp
bot = commands.Bot(
    command_prefix=".", 
    intents=intents, 
    help_command=None,
    http_timeout=aiohttp.ClientTimeout(total=60)  # Longer timeout
)

# Do not create session at module level
# The session will be created properly by discord.py internally

@bot.event
async def on_ready():
    global bot  # Ensures bot is globally recognized
    await bot.wait_until_ready()

    print(f"✅ SHULKER BOT is online as {bot.user}!")

    activity = discord.Streaming(name="SHULKER SMP ⚔️", url="https://www.twitch.tv/minecraft")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("✅ Status should now be updated!")


# Help Command
# Help Command
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)  # 1 use every 3 seconds per user
async def help(ctx):
            embed = discord.Embed(title=" <a:star1:1345361132512088178> **SHULKER BOT COMMANDS** <a:star1:1345361132512088178> ", color=discord.Color.gold())
            embed.set_thumbnail(url=bot.user.avatar.url)

            embed.add_field(name="<:moderation:1345359844445524041> **Moderation**", 
                            value="╭───────────⟡\n"
                                  "│ <:kick:1345360371002900550> `.kick <user>`\n"
                                  "│ <:ban:1345360761236488276> `.ban <user>`\n"
                                  "│ <:unban:1345361440969724019> `.unban <user>`\n"
                                  "│ <a:purge:1345361946324631644> `.purge <amount>`\n"
                                  "│ <:dm:1345362152831320179> `.dm <user> <message>`\n"
                                  "│ <:timeout:1345362419475546173> `.timeout <user> <duration_in_seconds> [reason]`\n"
                                  "│ <:tmremove:1345362837610168321> `.removetimeout <user>`\n"
                                  "╰───────────⟡", inline=False)


            embed.add_field(name="<a:economy:1345373409659588661> **Economy**", 
                value="╭───────────⟡\n"
                      "│ <a:balance:1345373618070097982> `.balance / .bal`\n"
                      "│ <a:daily:1345377114223935519> `.daily`\n"
                      "│ <a:cf:1345374098427084922> `.cf <amount> <heads/tails> [X2 MONEY]`\n"
                      "│ <a:set:1345374633666416725> `.setbalance <user> <amount>`\n"
                      "│ <a:slots:1345374871734980608> `.slots <amount> [X5 MONEY]`\n"
                      "│ <:gcoin:1345375137100464168> `.give <user> <amount>`\n"
                      "│ <a:dice:1345375794490507274> `.dice <amount> <1-6> [X6 MONEY]`\n"
                      "│ <a:trophy:1345379999999999999> `.top` (Leaderboard of richest users)\n"
                      "╰───────────⟡", inline=False)



            embed.add_field(name="<:fun:1345375490965245996> **Fun**", 
                            value="╭───────────⟡\n"
                                  "│ <a:dice:1345375794490507274> `.roll`\n"
                                  "│ 🪙 `.flip`\n"
                                  "│ <:funny:1345378490358173819> `.joke`\n"
                                  "│ <:meme:1345378712907939902> `.meme`\n"
                                  "╰───────────⟡", inline=False)


            embed.add_field(name="<a:gift1:1345383111877202021> **Giveaway**", 
                            value="╭───────────⟡\n"
                                  "│ <a:giveaway21:1345378924481347584> `.giveaway <duration_in_seconds> <prize>`\n"
                                  "│ <:refresh:1345379475638063115> `.reroll <message_id>`\n"
                                  "│ <:gend:1345379981672316998> `.gend <message_id>`\n"
                                  "╰───────────⟡", inline=False)


            embed.add_field(name="📨 **Invites**", 
                            value="╭───────────⟡\n"
                                  "│ <:invites:1345380333222367285> `.invites <user>`\n"
                                  "│ <:rinvites:1345380642342572193> `.resetinvites <user>`\n"
                                  "│ <a:nuke:1345380973096734731> `.resetwholeserverinvite`\n"
                                  "╰───────────⟡", inline=False)


            embed.add_field(name="<:utility:1345381139354746984> **Utility**", 
                            value="╭───────────⟡\n"
                                  "│ <a:ping:1345381376433717269> `.ping`\n"
                                  "│ <:help:1345381592335646750> `.help`\n"
                                  "│ <a:message:1345402517277638762> `.say`\n"
                                  "│ <:embed:1345402784039571487> `.embed`\n"
                                  "│ <a:Serverinfo:1345403530701176873> `.serverinfo`\n"
                                  "╰───────────⟡", inline=False)

            embed.set_footer(text="🔥 BOT MADE BY SHREYANSH GAMETUBE! STAY ACTIVE ❤")

            await ctx.send(embed=embed)




# Server Info

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild

    embed = discord.Embed(
        title=f"Server Info - {guild.name}",
        color=discord.Color.blue()
    )

    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

    embed.add_field(name="📌 Server Name", value=guild.name, inline=True)
    embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
    embed.add_field(name="👑 Owner", value=guild.owner, inline=True)
    embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
    embed.add_field(name="📅 Created On", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="💬 Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="🔰 Roles", value=len(guild.roles), inline=True)

    await ctx.send(embed=embed)




# Dictionary to manually track invites (This should be replaced with a database in a real bot)
invite_data = {}
# Initialize database
conn = sqlite3.connect("invites.db")
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS invites (
             user_id INTEGER PRIMARY KEY,
             joins INTEGER DEFAULT 0,
             leaves INTEGER DEFAULT 0,
             fakes INTEGER DEFAULT 0,
             rejoins INTEGER DEFAULT 0)''')

conn.commit()
conn.close()

# Function to update invite stats
def update_invite_data(user_id, column):
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()

    # Ensure the user exists in the database
    c.execute("INSERT OR IGNORE INTO invites (user_id) VALUES (?)", (user_id,))

    # Update the relevant column
    c.execute(f"UPDATE invites SET {column} = {column} + 1 WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

@bot.event
async def on_member_join(member):
    """Triggered when a member joins."""
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()

    # Check if the user has joined before
    c.execute("SELECT joins FROM invites WHERE user_id = ?", (member.id,))
    result = c.fetchone()
    conn.close()

    if result and result[0] > 0:
        update_invite_data(member.id, "rejoins")  # Count as rejoin
    else:
        update_invite_data(member.id, "joins")  # First-time join

    await member.send("Welcome to the server!")

@bot.event
async def on_member_remove(member):
    """Triggered when a member leaves."""
    update_invite_data(member.id, "leaves")

    # Check if user should be marked as a fake
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins, leaves FROM invites WHERE user_id = ?", (member.id,))
    result = c.fetchone()
    conn.close()

    if result and result[0] == result[1]:  
        update_invite_data(member.id, "fakes")  # Mark as fake


# Fetch invite stats from the database
def get_invite_data(user_id):
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins, leaves, fakes, rejoins FROM invites WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()

    return result if result else (0, 0, 0, 0)


# Add this auto-responder below on_ready()
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    await bot.process_commands(message)  # Allow commands to work
    # Auto-Response Dictionary
    auto_responses = {
        "hello": "Hello there! 👋",
        "how are you?": "I'm just a bot, but I'm doing great! 😃",
        "who made you?": "I was created by **Shreyansh GameTube**! 🔥",
        "what is lifesteal smp?": "Lifesteal SMP is a Minecraft mode where you **steal hearts** from enemies! ❤️⚔️",
        "good bot": "Thank you! 😊",
        "<@1101467683083530331>": "BRO PLAYING WITH DANGER!! :skull:",
    }

    # Convert message to lowercase for case-insensitive matching
    user_message = message.content.lower()

    # Check if the message matches any auto-response
    for key in auto_responses:
        if key in user_message:
            await message.channel.send(auto_responses[key])
            break  # Stop checking after the first match

    # Note: bot.process_commands() is already called at the beginning of this function


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert seconds to milliseconds
    await ctx.send(f"<a:ping:1345381376433717269> Pong! {latency}ms")

# Moderation Commands
@bot.command()
@is_allowed_user()
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member.mention} has been **kicked** for: `{reason}`")

@bot.command()
@is_allowed_user()
async def timeout(ctx, member: discord.Member, duration: int, *, reason="No reason provided"):
    """Timeouts a user for a specified duration (in seconds)."""
    try:
        await member.timeout(timedelta(seconds=duration), reason=reason)
        await ctx.send(f"⏳ {member.mention} has been **timed out** for `{duration} seconds`! Reason: `{reason}`")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to timeout this user!")
    except Exception as e:
        await ctx.send(f"⚠️ An error occurred: `{e}`")

@bot.command()
@is_allowed_user()
async def removetimeout(ctx, member: discord.Member):
    """Removes timeout from a user."""
    try:
        await member.timeout(None)  # Removing timeout
        await ctx.send(f"✅ {member.mention}'s timeout has been **removed**!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to remove the timeout!")
    except Exception as e:
        await ctx.send(f"⚠️ An error occurred: `{e}`")

@bot.command()
@is_allowed_user()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🚫 {member.mention} has been **banned** for: `{reason}`")

@bot.command()
@is_allowed_user()
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"🔄 {user.mention} has been **unbanned**!")


@bot.command()
@is_allowed_user()
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🗑️ Deleted `{amount}` messages!", delete_after=3)

@bot.command()
@is_allowed_user()
async def dm(ctx, user: discord.User, *, message):
    try:
        await user.send(message)
        await ctx.send(f"📩 Successfully sent a DM to {user.mention}!")
    except:
        await ctx.send(f"❌ Failed to send a DM to {user.mention}. They may have DMs disabled.")

# Note: We're using SQLite (economy.db) for all economy functions now
# These JSON functions aren't being used and can be removed

# Initialize economy database
def init_economy_db():
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, balance INTEGER, last_daily INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS slots_history (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, bet_amount INTEGER, result TEXT, win_amount INTEGER, timestamp INTEGER)")
    conn.commit()
    conn.close()

# Initialize economy database at startup
init_economy_db()

@bot.command()
async def top(ctx):
    """Show the top 10 users with the highest coins."""
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Fetch the top 10 users sorted by balance (highest first)
    c.execute("SELECT user_id, balance FROM economy ORDER BY balance DESC LIMIT 10")
    top_users = c.fetchall()
    conn.close()

    if not top_users:
        await ctx.send("🚫 No users found in the leaderboard!")
        return

    # Create leaderboard embed
    embed = discord.Embed(title="🏆 **Top 10 Coin Leaderboard**", color=discord.Color.gold())
    
    for rank, (user_id, balance) in enumerate(top_users, start=1):
        user = bot.get_user(user_id)  # Fetch user object
        username = user.name if user else f"Unknown User ({user_id})"
        embed.add_field(name=f"#{rank} {username}", value=f"💰 {balance} coins", inline=False)

    embed.set_footer(text="🔥 Keep grinding to reach the top!")

    await ctx.send(embed=embed)

#slots

@bot.command()
async def slots(ctx, bet_amount: int):
    """Play a slot machine game! Bet your coins and try your luck."""
    user_id = ctx.author.id

    # Open Database Connection
    conn = sqlite3.connect("economy.db")
    cursor = conn.cursor()

    # Ensure table exists
    cursor.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, balance INTEGER, last_daily INTEGER)")

    # Fetch user's balance
    cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    # If user doesn't exist, insert them with a default balance of 500
    if result is None:
        balance = 500
        cursor.execute("INSERT INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (user_id, balance, 0))
        conn.commit()
        result = (balance,)

    if result[0] < bet_amount:
        conn.close()
        return await ctx.send("❌ You don't have enough coins to play!")

    balance = result[0]
    # Symbols for the slots
    symbols = ["🍎", "🍒", "🍋", "🍇", "🍊", "🍉", "🍓"]
    spin_result = [random.choice(symbols) for _ in range(3)]

    await ctx.send(f"🎰 **{spin_result[0]} | {spin_result[1]} | {spin_result[2]}**")

    win_amount = 0
    if spin_result[0] == spin_result[1] == spin_result[2]:
        win_amount = bet_amount * 5
        new_balance = balance + win_amount  # Win, 5x the bet
        await ctx.send(f"🎉 You won {win_amount} coins! New balance: {new_balance} coins.")
    else:
        new_balance = balance - bet_amount  # Lose, deduct the bet
        await ctx.send(f"😢 You lost {bet_amount} coins. New balance: {new_balance} coins.")

    # Update the user's balance in the database
    cursor.execute("UPDATE economy SET balance = ? WHERE user_id = ?", (new_balance, user_id))

    # Record the slots game in history
    current_time = int(datetime.utcnow().timestamp())
    result_str = f"{spin_result[0]}{spin_result[1]}{spin_result[2]}"
    cursor.execute("INSERT INTO slots_history (user_id, bet_amount, result, win_amount, timestamp) VALUES (?, ?, ?, ?, ?)", 
                  (user_id, bet_amount, result_str, win_amount, current_time))

    conn.commit()
    conn.close()

#Economy Commands


# Initialize invite tracking database
conn = sqlite3.connect("invites.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS invites (
             user_id INTEGER PRIMARY KEY,
             joins INTEGER DEFAULT 0,
             leaves INTEGER DEFAULT 0,
             fakes INTEGER DEFAULT 0,
             rejoins INTEGER DEFAULT 0)''')

conn.commit()
conn.close()

# Initialize economy database
conn = sqlite3.connect("economy.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS economy (
             user_id INTEGER PRIMARY KEY,
             balance INTEGER DEFAULT 0,
             last_daily INTEGER DEFAULT 0)''')

conn.commit()
conn.close()

# Function to update invite stats
def update_invite_data(user_id, column):
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()

    # Ensure user exists in the database
    c.execute("INSERT OR IGNORE INTO invites (user_id) VALUES (?)", (user_id,))

    # Update the relevant column
    c.execute(f"UPDATE invites SET {column} = {column} + 1 WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

# Function to update inviter's coins
def add_coins(user_id, amount):
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Ensure user exists in the economy database
    c.execute("INSERT OR IGNORE INTO economy (user_id, balance) VALUES (?, 0)", (user_id,))

    # Add coins
    c.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (amount, user_id))

    conn.commit()
    conn.close()

# Function to get invite stats
def get_invite_data(user_id):
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins, leaves, fakes, rejoins FROM invites WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()

    return result if result else (0, 0, 0, 0)

# Function to find inviter
async def find_inviter(member):
    invites = await member.guild.invites()
    
    for invite in invites:
        if invite.uses > 0:
            return invite.inviter  # Return the user who created the invite

    return None  # No inviter found

@bot.event
async def on_member_join(member):
    """Triggered when a member joins."""
    inviter = await find_inviter(member)

    if inviter:
        update_invite_data(inviter.id, "joins")  # Increase invite count
        add_coins(inviter.id, 500)  # Give inviter 500 coins

        await inviter.send(f"🎉 You invited {member.name} and earned **500 coins**!")

    # Check if it's a rejoin
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins FROM invites WHERE user_id = ?", (member.id,))
    result = c.fetchone()
    conn.close()

    if result and result[0] > 0:
        update_invite_data(member.id, "rejoins")  # Count as rejoin

@bot.event
async def on_member_remove(member):
    """Triggered when a member leaves."""
    update_invite_data(member.id, "leaves")

    # Check if user should be marked as a fake
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins, leaves FROM invites WHERE user_id = ?", (member.id,))
    result = c.fetchone()
    conn.close()

    if result and result[0] == result[1]:  
        update_invite_data(member.id, "fakes")  # Mark as fake

@bot.command()
async def invites(ctx, user: discord.Member = None):
    """Check a user's detailed invite stats from the database and show only coins earned from inviting."""
    if user is None:
        user = ctx.author  # Default to the command caller

    # Fetch invite data from the database
    stats = get_invite_data(user.id)

    # Prepare the stats dictionary
    stats_dict = {"joins": stats[0], "leaves": stats[1], "fakes": stats[2], "rejoins": stats[3]}
    net_invites = stats_dict["joins"] - (stats_dict["leaves"] + stats_dict["fakes"]) + stats_dict["rejoins"]

    # Calculate coins earned from inviting (assuming 500 coins per valid invite)
    coins_from_invites = net_invites * 500 if net_invites > 0 else 0

    embed = discord.Embed(title="📨 **Invite Log**", color=discord.Color.gold())
    embed.add_field(name="**User**", value=f"**{user.name}** has **{net_invites}** invites", inline=False)
    embed.add_field(name="✅ **Joins**", value=f"{stats_dict['joins']}", inline=True)
    embed.add_field(name="❌ **Left**", value=f"{stats_dict['leaves']}", inline=True)
    embed.add_field(name="⚠ **Fake**", value=f"{stats_dict['fakes']}", inline=True)
    embed.add_field(name="🔄 **Rejoins**", value=f"{stats_dict['rejoins']}", inline=True)
    embed.add_field(name="💰 **Coins Earned (Invites Only)**", value=f"{coins_from_invites} 🪙", inline=False)
    embed.set_footer(text="🔥 Invite tracking by SHULKER BOT")

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def resetinvites(ctx, user: discord.Member):
    """Reset a specific user's invite stats in the database without affecting their coins."""
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("UPDATE invites SET joins = 0, leaves = 0, fakes = 0, rejoins = 0 WHERE user_id = ?", (user.id,))
    conn.commit()
    conn.close()

    await ctx.send(f"✅ Successfully reset invites for **{user.name}**!")


@bot.command()
@commands.has_permissions(administrator=True)
async def resetwholeserverinvite(ctx):
    """Reset invite stats for all users in the database without affecting their coins."""
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("DELETE FROM invites")  # Clears all invite data
    conn.commit()
    conn.close()

    await ctx.send("✅ Successfully reset **all invite records** for the server!")


@bot.command()
async def dice(ctx, bet: int, guess: int):
    user_id = ctx.author.id

    if bet <= 0:
        return await ctx.send("❌ Bet must be greater than 0!")
    if guess < 1 or guess > 6:
        return await ctx.send("❌ You must guess a number between 1 and 6!")

    # Connect to the database
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Ensure economy table exists
    c.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, balance INTEGER)")

    # Fetch user balance
    c.execute("SELECT balance FROM economy WHERE user_id=?", (user_id,))
    data = c.fetchone()

    if data:
        balance = data[0]
    else:
        balance = 0  # Default balance if user is new
        c.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?)", (user_id, balance))

    if balance < bet:
        conn.close()
        return await ctx.send("❌ You don't have enough coins to bet that much!")

    # Roll the dice (1 to 6)
    roll = random.randint(1, 6)

    if guess == roll:
        winnings = bet * 6
        balance += winnings
        await ctx.send(f"🎲 You rolled `{roll}`! You won `{winnings}` coins! 🤑")
    else:
        balance -= bet
        await ctx.send(f"🎲 You rolled `{roll}`. You lost `{bet}` coins! 😢")

    # Update balance in the database
    c.execute("UPDATE economy SET balance=? WHERE user_id=?", (balance, user_id))
    conn.commit()
    conn.close()
    
@bot.command(aliases=["bal"])
async def balance(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author  # Default to command user

    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Check if user exists
    c.execute("SELECT balance FROM economy WHERE user_id=?", (user.id,))
    data = c.fetchone()
    conn.close()

    balance = data[0] if data else 0  # Default balance is 0

    await ctx.send(f"<a:balance:1345373618070097982> {user.mention} has **{balance} coins**.")

    # **Debugging: Print the actual balance**
    print(f"DEBUG: {user.name}'s balance is {balance}")


@bot.command()
async def give(ctx, member: discord.Member, amount: int):
    if amount <= 0:
        await ctx.send("❌ Amount must be greater than 0!")
        return

    giver_id = ctx.author.id
    receiver_id = member.id

    if giver_id == receiver_id:
        await ctx.send("❌ You cannot give coins to yourself!")
        return

    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Ensure both users exist in the database
    c.execute("INSERT OR IGNORE INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (giver_id, 0, 0))
    c.execute("INSERT OR IGNORE INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (receiver_id, 0, 0))

    # Fetch giver's balance
    c.execute("SELECT balance FROM economy WHERE user_id=?", (giver_id,))
    giver_balance = c.fetchone()

    if giver_balance is None or giver_balance[0] < amount:
        await ctx.send("❌ You don't have enough coins to give!")
        conn.close()
        return

    # Update balances
    c.execute("UPDATE economy SET balance = balance - ? WHERE user_id = ?", (amount, giver_id))
    c.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (amount, receiver_id))

    conn.commit()
    conn.close()

    # Get the current date and time
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    # Create embed for transaction log
    embed = discord.Embed(title="💸 **Transaction Log**", color=discord.Color.green())
    embed.add_field(name="📤 **Payer**", value=f"{ctx.author.mention} (`{ctx.author.name}`)", inline=True)
    embed.add_field(name="📥 **Receiver**", value=f"{member.mention} (`{member.name}`)", inline=True)
    embed.add_field(name="💰 **Amount**", value=f"{amount} 🪙", inline=False)
    embed.add_field(name="📅 **Date & Time**", value=f"`{now}`", inline=False)
    embed.set_footer(text="🔥 Secure transactions powered by SHULKER BOT")

    await ctx.send(embed=embed)



@bot.command()
async def setbalance(ctx, member: discord.Member, amount: int):
                            if ctx.author.id != 1101467683083530331:
                                await ctx.send("You don't have permission to use this command!")
                                return

                            conn = sqlite3.connect("economy.db")
                            c = conn.cursor()

                            # Ensure the user exists in the database
                            c.execute("INSERT OR IGNORE INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (member.id, 0, 0))

                            # Update balance
                            c.execute("UPDATE economy SET balance = ? WHERE user_id = ?", (amount, member.id))

                            conn.commit()  # Save changes
                            conn.close()

                            await ctx.send(f"✅ Set {member.mention}'s balance to **{amount} coins**!")

                            # **Extra Debugging: Check if balance updated**
                            conn = sqlite3.connect("economy.db")
                            c = conn.cursor()
                            c.execute("SELECT balance FROM economy WHERE user_id=?", (member.id,))
                            new_balance = c.fetchone()
                            conn.close()

                            if new_balance:
                                print(f"DEBUG: {member.name}'s new balance is {new_balance[0]}")

#daily command

@bot.command()
async def daily(ctx):
    user_id = ctx.author.id
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Create table if not exists
    c.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, balance INTEGER, last_daily INTEGER)")

    # Fetch user data
    c.execute("SELECT balance, last_daily FROM economy WHERE user_id=?", (user_id,))
    data = c.fetchone()

    now = int(datetime.utcnow().timestamp())  # Current time in seconds

    if data:
        balance, last_daily = data
        if now - last_daily < 86400:  # 24 hours
            await ctx.send("❌ You have already claimed your daily reward! Come back later.")
            conn.close()
            return
        balance += 100  # Add 100 coins
        c.execute("UPDATE economy SET balance=?, last_daily=? WHERE user_id=?", (balance, now, user_id))
    else:
        balance = 100  # First time claiming
        c.execute("INSERT INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (user_id, balance, now))

    conn.commit()
    conn.close()

    await ctx.send(f"✅ {ctx.author.mention}, you claimed **100 coins**! Your new balance is **{balance} coins**.")







# CF Command

@bot.command()
async def cf(ctx, amount: int, choice: str):
    """Coinflip command: Bet an amount and choose heads or tails."""
    choice = choice.lower()
    if choice not in ["heads", "tails"]:
        return await ctx.send("⚠️ Invalid choice! Please choose heads or tails.")

    user_id = ctx.author.id

    # Open Database Connection
    conn = sqlite3.connect("economy.db")
    cursor = conn.cursor()

    # Ensure table exists
    cursor.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, balance INTEGER, last_daily INTEGER)")

    # Fetch user's balance
    cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    # If user doesn't exist, insert them with a default balance of 500
    if result is None:
        balance = 500
        cursor.execute("INSERT INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (user_id, balance, 0))
        conn.commit()
    else:
        balance = result[0]

    # Check if user has enough balance
    if amount > balance or amount <= 0:
        conn.close()
        return await ctx.send("❌ You don't have enough coins to bet that amount!")

    # Flip the coin
    flip_result = random.choice(["heads", "tails"])

    if choice == flip_result:
        new_balance = balance + amount  # Win, add the bet amount
        await ctx.send(f"<:congrats:1345385894454100019> You won **{amount}** coins! <a:cf:1345374098427084922> The coin landed on **{flip_result}**! New balance: **{new_balance}** coins.")
    else:
        new_balance = balance - amount  # Lose, deduct the bet
        await ctx.send(f"<:sad:1345385609421656104> You lost **{amount}** coins. <a:cf:1345374098427084922> The coin landed on **{flip_result}**. New balance: **{new_balance}** coins.")

    # Update the user's balance in the database
    cursor.execute("UPDATE economy SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()
# say and embed

@bot.command()
async def say(ctx, *, message=None):
    if ctx.author.id != 1101467683083530331:
        await ctx.send("❌ You are not allowed to use this command!")
        return

    if message is None:
        await ctx.send("❌ Please provide a message to say!")
    else:
        await ctx.send(message)

@bot.command()
async def embed(ctx, *, message=None):
    if ctx.author.id != 1101467683083530331:
        await ctx.send("❌ You are not allowed to use this command!")
        return

    if message is None:
        await ctx.send("❌ Please provide a message for the embed!")
    else:
        embed = discord.Embed(
            description=message,
            color=discord.Color.blue()  # You can change the color if needed
        )
        embed.set_footer(text=f"💘 BOT BY SHREYANSH GAMETUBE 💘")

        await ctx.send(embed=embed)


# Giveaway Command
@bot.command()
@is_allowed_user()
async def giveaway(ctx, duration: int, *, prize: str):
    embed = discord.Embed(title="🎉 **GIVEAWAY TIME!** 🎉", color=discord.Color.gold())
    embed.add_field(name="<a:gift1:1345383111877202021> **Prize:**", value=prize, inline=False)
    embed.add_field(name="<a:time:1345383309458538518> **Duration:**", value=f"{duration} seconds", inline=False)
    embed.set_footer(text="React with 🎉 to enter!")

    giveaway_message = await ctx.send(embed=embed)
    await giveaway_message.add_reaction("🎉")

    await asyncio.sleep(duration)

    new_message = await ctx.channel.fetch_message(giveaway_message.id)
    reaction = discord.utils.get(new_message.reactions, emoji="🎉")

    if reaction:
        users = [user async for user in reaction.users() if not user.bot]
    else:
        users = []

    if users:
        winner = random.choice(users)
        await ctx.send(f"🎊 Congratulations {winner.mention}, you won **{prize}**! 🎉")
    else:
        await ctx.send("❌ No one entered the giveaway!")

@bot.command()
@is_allowed_user()
async def gend(ctx, message_id: int):
    try:
        message = await ctx.channel.fetch_message(message_id)
        if not message.embeds:
            return await ctx.send("❌ That message doesn't contain a giveaway embed!")

        embed = message.embeds[0]
        if "🎉 **GIVEAWAY TIME!** 🎉" not in embed.title:
            return await ctx.send("❌ That message is not a giveaway!")

        reaction = discord.utils.get(message.reactions, emoji="🎉")
        if not reaction:
            return await ctx.send("❌ No one entered the giveaway!")

        users = [user async for user in reaction.users() if not user.bot]
        if not users:
            return await ctx.send("❌ No valid participants in the giveaway!")

        # Prevent duplicate messages by limiting selection to one winner announcement
        winner = random.choice(users)

        # Log to console to check if command is running multiple times
        print(f"[DEBUG] Winner selected: {winner}")

        await ctx.send(f"🎊 Congratulations {winner.mention}! You won **{embed.fields[0].value}**! 🎉")

    except discord.NotFound:
        await ctx.send("❌ Couldn't find a message with that ID!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to fetch messages!")
    except discord.HTTPException:
        await ctx.send("❌ An error occurred while fetching the message!")

@bot.command()
@is_allowed_user()
async def reroll(ctx, message_id: int):
    """Rerolls a giveaway to pick a new winner."""
    try:
        giveaway_message = await ctx.channel.fetch_message(message_id)

        # Get reactions from the giveaway message
        reaction = discord.utils.get(giveaway_message.reactions, emoji="🎉")
        if not reaction:
            return await ctx.send("❌ No valid giveaway reactions found!")

        # Get users who reacted (excluding bots)
        users = [user async for user in reaction.users() if not user.bot]

        if users:
            new_winner = random.choice(users)
            await ctx.send(f"🎊 **New winner:** {new_winner.mention}! Congratulations! 🎉")
        else:
            await ctx.send("❌ No valid participants to reroll the giveaway.")

    except discord.NotFound:
        await ctx.send("❌ Couldn't find the giveaway message. Make sure you provided the correct message ID!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to fetch messages in this channel!")
    except Exception as e:
        await ctx.send(f"⚠️ An error occurred: `{e}`")

# Fun Commands
@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 You rolled a `{random.randint(1, 6)}`!")


@bot.command()
async def flip(ctx):
    await ctx.send(f"🪙 You got **{'Heads' if random.choice([True, False]) else 'Tails'}**!")

@bot.command()
async def joke(ctx):
    jokes = [
        "Why did the chicken cross the road? To get to the other side!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised!",
        "Why don’t skeletons fight each other? They don’t have the guts!",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my computer I needed a break, and now it won’t stop sending me vacation ads!",
        "Why don’t eggs tell jokes? Because they might crack up!",
        "Parallel lines have so much in common. It’s a shame they’ll never meet!",
        "I told my dog 10 jokes. He only laughed at one. Guess he’s not a paws-itively good audience!",
        "I asked my wife if I was the only one she’s been with. She said, 'Yes, the others were at least sevens or eights.'",
        "Did you hear about the restaurant on the moon? Great food, no atmosphere!",
        "Why did the golfer bring an extra pair of pants? In case he got a hole in one!",
        "What do you call fake spaghetti? An impasta!",
        "Why couldn't the bicycle stand up by itself? It was two-tired!",
        "I told my plants a joke. Now they’re rooted in laughter!",
        "How do you organize a space party? You planet!",
        "Why don’t some couples go to the gym? Because some relationships don’t work out!",
        "I only know 25 letters of the alphabet. I don’t know y.",
        "I used to be addicted to the hokey pokey, but then I turned myself around!"
    ]

    await ctx.send(f"🤣 {random.choice(jokes)}")

@bot.command()
async def meme(ctx):
    response = requests.get("https://meme-api.com/gimme/1")  # Corrected API URL
    if response.status_code == 200:
        meme_data = response.json()
        if 'memes' in meme_data and meme_data['memes']:  # Checking if memes exist
            meme = meme_data['memes'][0]  # Get the first meme
            embed = discord.Embed(title=meme['title'], url=meme['postLink'], color=discord.Color.random())
            embed.set_image(url=meme['url'])
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ No memes found. Try again later!")
    else:
        await ctx.send("❌ Couldn't fetch a meme. Try again later!")




@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return  # Prevents duplicate error handling

    if isinstance(error, commands.CommandOnCooldown):
        remaining = round(error.retry_after, 2)
        await ctx.send(f"⏳ Command on cooldown! Try again in {remaining} seconds.", delete_after=5)

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Missing arguments! Please provide all required inputs.")

    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f"❌ You don't have permission to use this command, {ctx.author.mention}!")

    else:
        # Log the error without sending it to the user
        print(f"Ignored error in command {ctx.command}: {error}")
        traceback.print_exc()  # Prints detailed error traceback for debugging








# Run the Bot
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("❌ ERROR: Discord bot token is missing! Set it in your environment variables.")
else:
    # Configure the http session with proper rate limiting
    bot.http.user_agent = 'ShulkerBot (https://discord.com, v1.0)'
    
    # More conservative approach with exponential backoff and session handling
    max_retries = 5
    retry_delay = 1800  # Start with 30 minutes (1800 seconds)
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print(f"🚀 Starting bot with rate limit handling... (Attempt {retry_count+1}/{max_retries})")
            # Create a fresh client session each time
            if retry_count > 0:
                # Recreate client session to avoid "Session is closed" errors
                bot.http._HTTPClient__session = None  # Clear the existing session
            
            bot.run(TOKEN, reconnect=True)
            break  # If successful, exit the loop
        except discord.errors.HTTPException as e:
            if e.status == 429:
                retry_count += 1
                print(f"⚠️ Rate limit exceeded! Waiting for cooldown period ({retry_delay} seconds)...")
                import time
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the delay each time
                print("🔄 Attempting to restart bot...")
            else:
                print(f"❌ HTTP Error: {e}")
                break
        except Exception as e:
            print(f"❌ Error: {e}")
            if "Session is closed" in str(e):
                print("⚠️ Session closed error detected. Recreating session...")
                retry_count += 1
                time.sleep(60)  # Wait a minute before retry
                continue
            else:
                break
    
    if retry_count >= max_retries:
        print("❌ Maximum retry attempts reached. Please try again later.")
        print("⚠️ Discord may have temporarily blocked your bot due to rate limits.")
        print("⚠️ Consider waiting 24 hours before trying again.")


@bot.command()
async def slotsstats(ctx, user: discord.Member = None):
    """View slots statistics for a user"""
    if user is None:
        user = ctx.author

    user_id = user.id

    conn = sqlite3.connect("economy.db")
    cursor = conn.cursor()

    # Get total games played
    cursor.execute("SELECT COUNT(*) FROM slots_history WHERE user_id = ?", (user_id,))
    total_games = cursor.fetchone()[0]

    if total_games == 0:
        conn.close()
        return await ctx.send(f"{user.mention} hasn't played any slots games yet!")

    # Get wins
    cursor.execute("SELECT COUNT(*) FROM slots_history WHERE user_id = ? AND win_amount > 0", (user_id,))
    wins = cursor.fetchone()[0]

    # Get total bet and won amounts
    cursor.execute("SELECT SUM(bet_amount), SUM(win_amount) FROM slots_history WHERE user_id = ?", (user_id,))
    total_bet, total_won = cursor.fetchone()

    # Get biggest win
    cursor.execute("SELECT bet_amount, win_amount, result FROM slots_history WHERE user_id = ? ORDER BY win_amount DESC LIMIT 1", (user_id,))
    biggest_win_data = cursor.fetchone()

    conn.close()

    # Calculate win rate and profit/loss
    win_rate = (wins / total_games) * 100 if total_games > 0 else 0
    profit_loss = total_won - total_bet

    # Create an embed
    embed = discord.Embed(title=f"🎰 Slots Statistics for {user.name}", color=discord.Color.gold())
    embed.add_field(name="Games Played", value=f"{total_games}", inline=True)
    embed.add_field(name="Wins", value=f"{wins} ({win_rate:.1f}%)", inline=True)
    embed.add_field(name="Total Bet", value=f"{total_bet} coins", inline=True)
    embed.add_field(name="Total Won", value=f"{total_won} coins", inline=True)
    embed.add_field(name="Profit/Loss", value=f"{profit_loss} coins", inline=True)

    if biggest_win_data and biggest_win_data[1] > 0:
        embed.add_field(name="Biggest Win", value=f"{biggest_win_data[1]} coins (bet: {biggest_win_data[0]}, result: {biggest_win_data[2]})", inline=False)

    embed.set_footer(text="Keep playing to improve your stats!")

    await ctx.send(embed=embed)
