import discord
from discord.ext import commands, tasks
import random
import os
from keep_alive import keep_alive
import requests
import json

client = commands.Bot(command_prefix = '.')

statuses = ['i can .help you', 'figure it out yourself', '.invite', 'ur mom needs .help', 'with my toys, .help', 'say .8ball nerds', 'stfu retro didnt make this he needs .help', 'qwertyuiopasdfghjklzxcvbnm', 'its next to the slash key']

@client.event
async def on_ready():
    change_status.start()
    print('Bot is ready!')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Your message is missing 1 or more arguments')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That's not a command.")

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(random.choice(statuses)))


def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! :ping_pong:{round(client.latency * 1000)} ms")

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    await ctx.send(f':8ball: {random.choice(responses)}')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
  await user.kick(reason=reason)
  await ctx.send(f"{user} have been kicked sucessfully")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
  await user.ban(reason=reason)
  await ctx.send(f"{user} have been banned sucessfully")

@client.command()
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)
    await ctx.send(f"{user} have been unbanned sucessfully")
    return

@client.command()
async def copy(ctx, *, words):
    await ctx.send(words)

@client.command()
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=881650063628181574&permissions=261993005047&scope=bot")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, ammount : int):
    await ctx.channel.purge(limit=ammount)

@client.command()
async def quote(ctx):
  await ctx.send(get_quote())

token = os.environ.get("TOKEN")
keep_alive()
client.run(token)
