import discord
import json
import requests
import asyncio
import os
from discord.ext import commands
from discord.ext.commands import has_permissions

bot = commands.Bot(command_prefix = '>')
client = commands.Bot(command_prefix = '>')

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
    response = requests.get('https://some-random-api.ml/animu/hug')
    json_data = json.loads(response.text)

    embed = discord.Embed(color = 0xff9900, description = f'{ctx.author.mention} обнял {member.mention}')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)

@bot.command()
async def pat(ctx,member:discord.Member):
    response = requests.get('https://some-random-api.ml/animu/pat')
    json_data = json.loads(response.text)

    embed = discord.Embed(color = 0xff9900, description = f'{ctx.author.mention} погладил {member.mention}')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)

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
@commands.has_permissions(administrator = True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

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
    
@bot.command(pass_context = True)
@commands.has_permissions(administrator = True)
async def say(ctx, *args):
    mesg = ' '.join(args)
    await bot.delete_message(ctx.message)
    return await bot.say(mesg)
    
token = os.environ.get('BOT_TOKEN')

bot.run(str(token))
