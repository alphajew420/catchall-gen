import discord
from discord.ext import commands
import random
import os
import json
import logging

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Load names from files
with open("firstname.txt", "r") as f:
    first_names = [line.strip() for line in f.readlines()]
with open("lastname.txt", "r") as f:
    last_names = [line.strip() for line in f.readlines()]

# Load or create a new data file to store user settings
try:
    with open("catchall_data.json", "r") as file:
        catchall_data = json.load(file)
except FileNotFoundError:
    catchall_data = {}

# Set domain command
@bot.command()
async def setcatchall(ctx, domain: str):
    if not isinstance(ctx.channel, discord.DMChannel):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            logging.error(f"Failed to delete message in {ctx.guild.name} due to insufficient permissions.")
            await ctx.send("I don't have permission to delete messages, but please use DMs to send sensitive commands.")
        else:
            await ctx.author.send("Please send catchall information through DM for security. Use the command here.")
        return
    user_id = str(ctx.author.id)
    catchall_data[user_id] = {'domain': domain}
    with open("catchall_data.json", "w") as file:
        json.dump(catchall_data, file)
    await ctx.send(f"Your catchall domain has been set to {domain}.")

@bot.command()
async def catchall(ctx, number: int):
    if not isinstance(ctx.channel, discord.DMChannel):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            logging.error(f"Failed to delete message in {ctx.guild.name} due to insufficient permissions.")
            await ctx.send("I don't have permission to delete messages, but please use DMs to send sensitive commands.")
        else:
            await ctx.author.send("Please send catchall information through DM for security. Use the command here.")
        return
    user_id = str(ctx.author.id)
    if user_id not in catchall_data or 'domain' not in catchall_data[user_id]:
        await ctx.send("Please set your catchall domain first using /setcatchall.")
        return
    
    domain = catchall_data[user_id]['domain']
    emails = []
    filename = f"{ctx.author.id}_emails.txt"
    for _ in range(number):
        first = random.choice(first_names)
        last = random.choice(last_names)
        numbers = random.randint(1000, 9999)
        email = f"{first.lower()}{last.lower()}{numbers}@{domain}"
        emails.append(email)
    
    with open(filename, "w") as file:
        file.write("\n".join(emails))
    
    await ctx.send(file=discord.File(filename))

    # Delete the file after sending it
    os.remove(filename)

# Running the bot
bot.run('MTIzODcyMjE4NDY5Mjc2MDYzNw.GJHtrk.9un7OSpCO4OdT9xWf3hjfyjCP1JeLAOLR5EfHg')
