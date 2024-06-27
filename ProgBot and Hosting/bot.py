from flask import Flask, request, jsonify
import discord
from discord.ext import commands


app = Flask(__name__)

intents = discord.Intents.default()
intents.messages = True  # Enable the intent to receive message events
intents.message_content = True
intents.guilds = True    # Enable the intent to receive guild events (necessary for the bot to start properly)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    guild = bot.guilds[0]  # Assuming your bot is only in one guild
    bot_member = guild.get_member(bot.user.id)
    print(f'Bot Permissions in {guild.name}: {bot_member.guild_permissions}')


@bot.event
async def on_message(message):
    print(f'Message from {message.author}: {message.content}')
    await bot.process_commands(message)  # Ensure commands are processed correctly

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, I am your Discord bot!')

@app.route('/')
def index():
    return 'Hello, Discord Bot!'

if __name__ == '__main__':
    bot.run('your/bot/token')
