import discord
from discord.ext import commands
from discord.ext.commands import Bot
import time

Bot = commands.Bot(command_prefix= '+')
Bot.remove_command('help')

@Bot.command()
@commands.has_permissions( administrator = True)
async def setup(ctx, arg1, arg2):
	startclass = arg1
	endclass = int(int(arg2) + 1)
	id = ctx.message.guild.id
	guild = Bot.get_guild(id)
	category = await guild.create_category("Classrooms", overwrites=None, reason='setup')
	await guild.create_text_channel("Bot-channel", overwrites=None, category=category, reason='setup')
	if int(startclass) < 11:
		for i in range(int(startclass),int(endclass)):
			await guild.create_role(name=str(i) + "А")
			await guild.create_role(name=str(i) + "Б")
			await guild.create_role(name=str(i) + "В")
			await guild.create_role(name=str(i) + "Г")
			await guild.create_role(name=str(i) + "Д")
			await guild.create_role(name=str(i) + "Е")
	await ctx.send('Setup was succesful ended!')

@Bot.event
async def on_ready():
	print("Ready")
	file1 = open("timings.txt", "r")
	month = file1.read(2)
	file1.seek(4)
	day = file1.read(2)
	file1.seek(7)
	hour = file1.read(2)
	file1.seek(10)
	minute = file1.read(2)
	file1.seek(13)
	minute = file1.read(18)
	file1.seek(35)
	categoryid = file1.read(18)

def func():
	file2 = open('timings.txt','r')
	file2.seek(32)
	category = file2.read(18)


@Bot.command()
async def create_vc(ctx, arg1, arg2, arg3):
	channel = discord.utils.get(ctx.guild.channels, name='bot-channel')
	categoryid = channel.id
	serverid = ctx.message.guild.id
	f = open("timings.txt", "a+")
	message = arg1 + ' ' + arg2 + ' ' + arg3 + ' ' + str(categoryid) + ' ' + str(serverid) +'\n'
	f.write(message)
	f.close()
	await ctx.send('Урок будет создан в заданное время') 

