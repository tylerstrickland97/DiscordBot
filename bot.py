import discord
from discord.ext import commands
from command_handler import CommandHandler
from dotenv import load_dotenv
import os

# Initialize a CommandHandler instance, and our bot and force it to use a ! prefix.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
ch = CommandHandler()

@bot.event
async def on_ready():
    """Function to let us know that the bot has gone online"""
    print(f'We have logged in as {bot.user}')



@bot.command()
async def stats(context):
    """Function that is called when the stats command is used"""
    if context.author == bot.user:
        return
    response = await ch.handle_commands(context)
    await context.send(response)

@bot.command()
async def fantasy(context):
    """Function that is called when the fantasy command is used"""
    if context.author == bot.user:
        return
    response = await ch.handle_commands(context)
    await context.send(response)

@bot.command()
async def helpme(context):
    """Function that is called when the helpme command is used"""
    if context.author == bot.user:
        return
    response = await ch.handle_commands(context)
    await context.send(response)

@bot.event
async def on_command_error(context, error):
    """Function that is called when an error occurs with one of the commands"""
    if isinstance(error, commands.CommandNotFound):
        sender_tag = context.author.mention
        await context.send(f"Sorry @{sender_tag}, that\'s not a valid command")
    else:
        print(f"An error occurred: {error}")



if __name__ == '__main__':
    """Main function that starts the bot"""
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    bot.run(token)
