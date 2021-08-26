import discord
from discord import guild
from discord.ext import commands
from discord.ext.commands import Bot
import sqlite3
import datetime
import asyncio

Bot = commands.Bot(command_prefix='+')
Bot.remove_command('help')


@Bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx, arg1, arg2):
    startclass = arg1
    endclass = int(int(arg2) + 1)
    id = ctx.message.guild.id
    print(id)
    guild = Bot.get_guild(id)
    print(guild)
    category = await guild.create_category("Classrooms", overwrites=None, reason='setup')
    print(category)
    await guild.create_text_channel("Bot-channel", overwrites=None, category=category, reason='setup')
    if int(startclass) < 11:
        for i in range(int(startclass), int(endclass)):
            await guild.create_role(name=str(i) + "А")
            await guild.create_role(name=str(i) + "Б")
            await guild.create_role(name=str(i) + "В")
            await guild.create_role(name=str(i) + "Г")
            await guild.create_role(name=str(i) + "Д")
            await guild.create_role(name=str(i) + "Е")
    await ctx.send('Setup was ended!')


@Bot.event
async def on_ready():
    while True:
        conn = sqlite3.connect("timings.db")
        c = conn.cursor()
        time_now = datetime.datetime.now()
        a = c.execute("""SELECT month, day, hour, minute, sid FROM requests ORDER BY month, day, hour, minute """).fetchone()
        month = a[0]
        day = a[1]
        hour = a[2]
        minute = a[3]
        gid = a[4]
        guild1 = Bot.get_guild(gid)
        print('________________________________________________________________')
        print('time i need----> ', month, end='/')
        print(day, end=' ')
        print(hour, end=':')
        print(minute, ' ---->', guild1,'<----')
        print('nowtime--------> ', time_now.month, end='/')
        print(time_now.day,  end=' ')
        print(time_now.hour, end=':')
        print(time_now.minute, end=':')
        print(time_now.second, )
        if month < time_now.month:
            c.execute(
                "DELETE from requests WHERE month = :month AND day = :day AND hour = :hour AND minute = :minute",
                {'month': month, 'day': day, 'hour': hour, 'minute': minute})
            print('Delete_reason: month')
            conn.commit()
            conn.close()
        elif month == time_now.month:
            if day < time_now.day:
                c.execute(
                    "DELETE from requests WHERE month = :month AND day = :day AND hour = :hour AND minute = :minute",
                    {'month': month, 'day': day, 'hour': hour, 'minute': minute})
                print('Delete_reason: day')
                conn.commit()
                conn.close()
            elif day == time_now.day:
                if hour < time_now.hour:
                    c.execute(
                        "DELETE from requests WHERE month = :month AND day = :day AND hour = :hour AND minute = :minute",
                        {'month': month, 'day': day, 'hour': hour, 'minute': minute})
                    print('Delete_reason:hour')
                    conn.commit()
                    conn.close()
                elif hour == time_now.hour:
                    if minute < time_now.minute:
                        c.execute(
                            "DELETE from requests WHERE month = :month AND day = :day AND hour = :hour AND minute = :minute",
                            {'month': month, 'day': day, 'hour': hour, 'minute': minute})
                        print('Delete_reason: minute')
                        conn.commit()
                        conn.close()
                    elif minute == time_now.minute:
                        pass
        if time_now.hour == hour and time_now.minute == minute and time_now.day == day and time_now.month == month:
            print('________________________________________________________________')
            print('addin...')  # индикатор
            s = c.execute("""SELECT sid, cid FROM requests ORDER BY month,day,hour,minute""")
            g = s.fetchone()  # вывод id сервера
            sid = g[0]  # вывод значения из кортежа
            cid = g[1]
            print('category_id->', cid)
            print('server_id->', sid)  # индикатор
            guild = Bot.get_guild(sid)  # получение названия сервера
            print('Server---->', guild)  # индикатор
            category = Bot.get_channel(cid)
            await guild.create_voice_channel(f"aboba {day} {hour}:{minute}", overwrites=None, category=category, reason='From command')
            c.execute(
                "DELETE from requests WHERE month = :month AND day = :day AND hour = :hour AND minute = :minute AND sid = :sid",
                {'month': month, 'day': day, 'hour': hour, 'minute': minute, 'sid': sid})
            print('Channel added...')
            conn.commit()
            conn.close()
        try:
            conn.close()
        except:
            pass
        await asyncio.sleep(0.5)  # 2 seconds delay


@Bot.command()
@commands.has_permissions(administrator=True)
async def create_vc(ctx, arg1, arg2, arg3, arg4):
    conn = sqlite3.connect("timings.db")
    c = conn.cursor()
    channel = discord.utils.get(ctx.guild.channels, name='Classrooms')
    cid = channel.id
    sid = ctx.message.guild.id  # id guild(server) of channel, where was message
    c.execute(f"""INSERT INTO requests
            VALUES ({arg1}, {arg2}, {arg3},
            {arg4},{sid},{cid})""")
    await ctx.send('Урок будет создан в заданное время)')
    try:
        conn.commit()
        conn.close()
    except:
        pass


@Bot.command()
async def delch(ctx):
    for c in ctx.guild.channels:  # iterating through each guild channel
        await c.delete()


Bot.run(open('token.txt', 'r').readline())
