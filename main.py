import discord
import json
import requests
import asyncio
import os
from discord.ext import commands
from discord.ext.commands import has_permissions

bot = commands.Bot(command_prefix = '>')

bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    print('Bot id:', bot.user.id)
    print('--------------------------')

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Привет, {author.mention}!')

@bot.command()
async def hug(ctx,member:discord.Member):
    if ctx.author == member:
        embed = discord.Embed(color = 0xff9900, description = f'Вы не можете сам себя обнять')
        return await ctx.send(embed = embed)
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)

    embed = discord.Embed(color = 0xff9900, description = f'{ctx.author.mention} обнял {member.mention}')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)

@bot.command()
async def pat(ctx,member:discord.Member):
    if ctx.author == member:
        embed = discord.Embed(color = 0xff9900, description = f'Вы не можете сам себя погладить')
        return await ctx.send(embed = embed)
    response = requests.get('https://some-random-api.ml/animu/pat')
    json_data = json.loads(response.text)

    embed = discord.Embed(color = 0xff9900, description = f'{ctx.author.mention} погладил {member.mention}')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)
    
@bot.command( pass_context = True )
@commands.has_permissions( manage_messages = True )
async def clear( ctx, amount = 1 ):
    await ctx.channel.purge( limit = 1 )
    await ctx.channel.purge( limit = amount )
    await ctx.send(f'Удалено {amount} сообщений')
    await ctx.channel.purge( limit = 1 )

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Animat", description="Все команды бота:", color=0xeee657)

    embed.add_field(name=">hello", value="Сказать привет боту", inline=False)
    embed.add_field(name=">hug", value="Обнять кого-то", inline=False)
    embed.add_field(name=">pat", value="Погладить кого-то", inline=False)
    embed.add_field(name=">info", value="Немного информации о боте", inline=False)
    embed.add_field(name=">help", value="Показывает это сообщение", inline=False)
    embed.add_field(name=">clear", value="Удаляет сообщения(Только модератором доступна эта команда)", inline=False)
    embed.add_field(name=">avatar", value="Показывает аватарку игрока", inline=False)
    embed.add_field(name=">kick", value="Кикает участника(Только модератором доступна эта команда)", inline=False)
    embed.add_field(name=">ban", value="Банит участника(Только модератором доступна эта команда)", inline=False)
    embed.add_field(name=">clear", value="Отчищает чат(Только модераторам доступна эта команда) ", inline=False)
    embed.add_field(name=">level", value="Показывает ваш уровень", inline=False)
    embed.add_field(name=">invite", value="(Работает только в лс бота)", inline=False)
    

    await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Animat", description="Рп бот сделанный просто по фану", color=0xeee657)

    embed.add_field(name="Автор", value="Animat#7603", inline=False)
    
    embed.add_field(name="Серверов", value=f"{len(bot.guilds)}", inline=False)

    members=ctx.guild.member_count
    embed.add_field(name="Людей", value=(members), inline=False)
    
    embed.add_field(name="Пригласить бота", value="https://discord.com/api/oauth2/authorize?client_id=784328529462558730&permissions=0&scope=bot", inline=False)

    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx,member:discord.Member):
    aef = member.avatar_url
    embed = discord.Embed(color = 0xff9900, description = f'Аватар участника {member.mention}')
    embed.set_image(url = aef)
    await ctx.send(embed = embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.purge(limit = 1)
        await ctx.send(embed = discord.Embed(description = f'** {ctx.author.name}, У вас нету доступа, для этой команды!.**', color=0x0c0c0c), delete_after=2)

@bot.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(color = 0xff9900, description = f'{member} был кикнут')
    await member.kick(reason=reason)
    await ctx.send(embed = embed)
  

@bot.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, member : discord.Member, *, reason=None):
    embed = discord.Embed(color = 0xff9900, description = f'{member} был забанен')
    await member.ban(reason=reason)
    await ctx.send(embed = embed)

@bot.command()
@commands.dm_only()
async def invite(ctx):
    embed = discord.Embed(title="Animat", description="Рп бот сделанный просто по фану", color=0xeee657)

    embed.add_field(name="Автор", value="Animat#7603", inline=False)
    
    embed.add_field(name="Пригласить бота", value="https://discord.com/api/oauth2/authorize?client_id=784328529462558730&permissions=0&scope=bot", inline=False)

    embed.add_field(name="Официальный сервер бота", value="https://discord.gg/xeghGZNKnQ", inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if not message.author.bot:
        with open('level.json','r') as f:
            users = json.load(f)
        await update_data(users, message.author,message.guild)
        await add_experience(users, message.author, 4, message.guild)
        await level_up(users, message.author,message.channel, message.guild)

        with open('level.json','w') as f:
            json.dump(users, f)
    await bot.process_commands(message)

async def update_data(users, user,server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1

async def add_experience(users, user, exp, server):
  users[str(user.guild.id)][str(user.id)]['experience'] += exp

async def level_up(users, user, channel, server):
  experience = users[str(user.guild.id)][str(user.id)]['experience']
  lvl_start = users[str(user.guild.id)][str(user.id)]['level']
  lvl_end = int(experience ** (1/4))
  
  if lvl_start < lvl_end:
      await channel.send('Поздравляю {}! ты достиг {} уровня'.format(user.mention, lvl_end))
      users[str(user.guild.id)][str(user.id)]['level'] = lvl_end


@bot.command(aliases = ['rank','lvl'])
async def level(ctx,member: discord.Member = None):

    if not member:
        user = ctx.message.author
        with open('level.json','r') as f:
            users = json.load(f)
            lvl = users[str(ctx.guild.id)][str(user.id)]['level']
            exp = users[str(ctx.guild.id)][str(user.id)]['experience']

        embed = discord.Embed(title = 'Уровень {}'.format(lvl), description = f"{exp} Опыт " ,color = discord.Color.green())
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
    else:
      with open('level.json','r') as f:
          users = json.load(f)
      lvl = users[str(ctx.guild.id)][str(member.id)]['level']
      exp = users[str(ctx.guild.id)][str(member.id)]['experience']
      embed = discord.Embed(title = 'Уровень {}'.format(lvl), description = f"{exp} Опыт" ,color = discord.Color.green())
      embed.set_author(name = member, icon_url = member.avatar_url)

      await ctx.send(embed = embed)
    
@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, message=None):
    await ctx.send(message)
    
@bot.event
async def on_guild_join(guild):
    category = guild.categories[0]
    channel = category.channels[0]
    
    embed = discord.Embed(title="Спасибо", description="Что пригласили меня на ваш сервер! Список всех команд:", color=0xeee657)

    embed.add_field(name=">hello", value="Сказать привет боту", inline=False)
    embed.add_field(name=">hug", value="Обнять кого-то", inline=False)
    embed.add_field(name=">pat", value="Погладить кого-то", inline=False)
    embed.add_field(name=">info", value="Немного информации о боте", inline=False)
    embed.add_field(name=">help", value="Показывает это сообщение", inline=False)
    embed.add_field(name=">clear", value="Удаляет сообщения(Только модератором доступна эта команда)", inline=False)
    embed.add_field(name=">avatar", value="Показывает аватарку игрока", inline=False)
    embed.add_field(name=">kick", value="Кикает участника(Только модератором доступна эта команда)", inline=False)
    embed.add_field(name=">ban", value="Банит участника(Только модератором доступна эта команда)", inline=False)
    embed.add_field(name=">clear", value="Отчищает чат(Только модераторам доступна эта команда) ", inline=False)
    embed.add_field(name=">level", value="Показывает ваш уровень", inline=False)
    embed.add_field(name=">invite", value="(Работает только в лс бота)", inline=False)
    embed.add_field(name="Автор", value="Animat#7603", inline=False)
    embed.add_field(name="Серверов", value=f"{len(bot.guilds)}", inline=False)
    embed.add_field(name="Пригласить бота", value="https://discord.com/api/oauth2/authorize?client_id=784328529462558730&permissions=0&scope=bot", inline=False)

    await channel.send(embed=embed)

token = os.environ.get('BOT_TOKEN')

bot.run(str(token))
