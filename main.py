import discord
from discord.ext import commands, tasks
import random
import os
from keep_alive import keep_alive
import requests
import json
import time

client = commands.Bot(command_prefix = '.')

statuses = ['imagine using slash commands', 'figure it out yourself', '.invite', 'ur mom needs .help', 'with my toys, .help', 'say .8ball nerds', 'stfu retro didnt make this he needs .help', 'qwertyuiopasdfghjklzxcvbnm', 'its the next to the slash key', 'say .bal first before doing the currency commands.']

os.chdir("data")


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
  """Checks Latency."""
  await ctx.send(f'Pong! :ping_pong:{round(client.latency * 1000)} ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
  """Answers your questions about life."""
  responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes, definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
  await ctx.send(f':8ball: {random.choice(responses)}')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
  """Kicks people."""
  await user.kick(reason=reason)
  await ctx.send(f"{user} has been kicked sucessfully")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
  """Bans people."""
  await user.ban(reason=reason)
  await ctx.send(f"{user} has been banned sucessfully")

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  """Unbans people."""
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
    user = ban_entry.user

  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)
    await ctx.send(f"{user} has been unbanned sucessfully")
    return

@client.command()
async def copy(ctx, *, words):
  """Copys what you says, faker beware!"""
  await ctx.send(words)

@client.command()
async def invite(ctx):
  """Sends you my invite!"""
  await ctx.send("https://discord.com/api/oauth2/authorize?client_id=881650063628181574&permissions=292057984006&scope=bot")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, ammount : int):
  """Clears the chat."""
  await ctx.channel.purge(limit=ammount)

@client.command()
async def quote(ctx):
  """Inspires you with a quote."""
  await ctx.send(get_quote())

@client.command()
async def pr0n(ctx):
  """Sends some... intresting videos."""
  await ctx.send("nah bro go to horny jail :joy: caught in 4k :camera_with_flash:")

@client.command()
async def swagcheck(ctx):
  """How swag are you? Use this to check!"""
  await ctx.send("Swag Detector running... :sunglasses:")
  time.sleep(2)
  swaggerness = random.randint(0,100)
  await ctx.send(f':100: You are {swaggerness}% swag.')
  await updatebal(ctx.author,change=swaggerness,mode="swag")

@client.command()
async def bitchcheck(ctx):
  """Checks for bitches."""
  await ctx.send("Bitch Checker Running..")
  time.sleep(1)
  await ctx.send("Checking bitch dictionary...")
  time.sleep(1)
  await ctx.send("Verifying bitch count...")
  time.sleep(1)
  bitches = random.randint(0,2)
  if (bitches == 0):
    await ctx.send(f'{bitches} bitches found. :neutral_face:')
    await updatebal(ctx.author,change=bitches,mode="bitches")
  elif (bitches == 1):
    await ctx.send(f'{bitches} bitch found. :thumbsup:')
    await updatebal(ctx.author,change=bitches,mode="bitches")
  else:
    await ctx.send(f'{bitches} bitches found. :question:')
    await updatebal(ctx.author,change=bitches,mode="bitches")

@client.command()
async def bal(ctx, user: discord.Member=None):
  """Checks your balances."""
  if not user:
    user = ctx.author
  await open_account(user)

  users = await getdata()
  user = user

  bitch_count = users[str(user.id)]["bitches"]
  swag_count = users[str(user.id)]["swag"]

  #embed = discord.Embed(title = "Balance", color = 0x26F18B)
  #embed.add_field(name = "Bitches", value = bitch_count)
  #embed.add_field(name = "Swag", value = swag_count)

  await ctx.send(f"{ctx.author} has {bitch_count} bitches, and {swag_count}% swaggy")

async def open_account(user):
  users = await getdata()


  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["bitches"] = 0
    users[str(user.id)]["swag"] = 0
    users[str(user.id)]["items"] = []

  with open("userstats.json","w") as f:
    json.dump(users,f,indent=4)
    
  return True

async def getdata():
  with open("userstats.json","r") as f:
    users = json.loads(f)
  return users

async def updatebal(user,change,mode):
  users = await getdata()
  users[str(user.id)][mode] += change

  with open("userstats.json","w") as f:
    json.dump(users,f,indent=4)

async def giveitem(user, item):
    users = await getdata()
    users[str(user)]["items"].append(item)
  
    with open("userstats.json", 'w') as f:
        json.dump(users, f, indent=4)

@client.command()
async def give(ctx, person: discord.Member, theitem):
  if ctx.author.id == 768608833622638624:
    await giveitem(person.id, theitem)
    await ctx.send(f'Gave {theitem} to {person.mention}!')

token = os.environ.get("TOKEN")
keep_alive()
client.run(token)
