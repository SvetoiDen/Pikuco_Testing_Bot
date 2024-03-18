import discord
from discord.ext import commands, tasks
from mysql import connector
from os import system
from mysql.connector.errors import OperationalError
from cogs.func_storage.BD_function import BD_Bot
import config.config
from cogs.func_storage.func_storage import on_join
import datetime
import pytz

WORD_HELLO = ['привет']
Channel_list = []
channel = None

try:

    class Event(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            self.tasks_discord.start()

        @tasks.loop(seconds=1)
        async def tasks_discord(self):
            cur = BD_Bot()
            guild = self.bot.get_guild(1149010761029529610)

            if datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")).strftime("%H:%M:%S") == '06:30:00':
                channel = self.bot.get_channel(1211304778424909854)
                rows = cur.gets_(f"SELECT id, day, month FROM birthday")
                for row in rows:
                    time_now = datetime.datetime.now().strftime("%d-%m")
                    if f"{row['day']}-{row['month']}" == time_now:
                        await channel.send(f"У пользователя <@{row['id']}> день рождения!")

            for row in cur.gets_("SELECT * FROM games_event"):
                if row is not None:
                    if datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")).strftime("%H:%M:%S") == f'{row["time_start"]}:00':
                        channel = self.bot.get_channel(row['id_channel'])
                        voice = await guild.create_voice_channel(name=f'Игровой {row["name"]}', category=discord.utils.get(guild.categories, id=1149010761029529611), user_limit=row['col_people'] + 1)
                        overwrite = discord.PermissionOverwrite()
                        overwrite.connect = False

                        await voice.set_permissions(target=discord.utils.get(inter.guild.roles, id=row['id_role_z']), overwrite=overwrite)

                        cur.commit_(f"UPDATE games_event SET id_voice = {voice.id} WHERE id_channel = {row['id_channel']}")
                        await channel.send(f'Игра начинается господа, <@&{row["id_role"]}>\nЗаходите в войс канал **{voice.name}**')

                    elif datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")).strftime("%H:%M:%S") == f'{row["time_end"]}:00':
                        channel = self.bot.get_channel(row['id_channel'])
                        voice_channel = self.bot.get_channel(row['id_voice'])
                        await voice_channel.delete()
                        await channel.send(f'Игра окончена господа, <@&{row["id_role"]}>\nБлагодарю за участие!')
                        time.sleep(2)
                        await delete_game_ds(guild=guild, ch=channel)

            if datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")).strftime("%H:%M:%S") == '12:00:00' or datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")).strftime("%H:%M:%S") == '23:59:59':
                count = 0
                for row in cur.gets_("SELECT * FROM clans ORDER BY balance DESC"):
                    count += 1
                    cur.commit_(f"UPDATE clans SET top = {count} WHERE id_clan = {row['id_clan']}")

                count = 0
                for row in cur.gets_("SELECT * FROM accounts ORDER BY balance DESC"):
                    count += 1
                    cur.commit_(f"UPDATE clans SET top_reting = {count} WHERE id = {row['id']}")

                count = 0
                for row in cur.gets_("SELECT * FROM leaderboard ORDER BY lvl DESC"):
                    count += 1
                    cur.commit_(f"UPDATE leaderboard SET lvl_top = {count} WHERE id = {row['id']}")

                cur.close_()

        @commands.Cog.listener()
        async def on_member_remove(self, member):
            try:
                cur = BD_Bot()
                cur.commit_(f"DELETE FROM leaderboard WHERE id = {member.id}")
                cur.close_()

            except OperationalError:
                ch = await self.bot.get_channel(config.config.CHANNEL_REPORT)

                await ch.send(embed=discord.Embed(
                    title='Бот был выключен с хоста',
                    description='Производится перезапуск бота!',
                    color=0xFFFFFF
                ))
                system("python reg.py")
                system('kill 1')

        @commands.Cog.listener()
        async def on_message(self, message):
            try:
                cur = BD_Bot()

                if not message.author.bot:
                    if message.channel.id != 899933101436837888:
                        try:
                            row = cur.get_(f"SELECT * FROM leaderboard WHERE id = {message.author.id}")
                            cur.commit_(f"UPDATE leaderboard SET lvl_progress = lvl_progress + 1 WHERE id = {message.author.id}")

                            if row['lvl_progress'] == row['lvl_bar']:
                                channel = self.bot.get_channel(903916593975816242)
                                cur.commit_(f"UPDATE leaderboard SET lvl = lvl + 1 WHERE id = {message.author.id}")
                                cur.commit_(f"UPDATE leaderboard SET lvl_bar = lvl_bar + 50 WHERE id = {message.author.id}")
                                cur.commit_(f"UPDATE leaderboard SET lvl_progress = 0 WHERE id = {message.author.id}")

                                count = 0
                                for s in cur.gets_(f"SELECT * FROM leaderboard ORDER BY lvl DESC"):
                                    count += 1
                                    if s['id'] == message.author.id:
                                        cur.commit_(f"UPDATE leaderboard SET lvl_top = {count} WHERE id = {message.author.id}")

                                row = cur.get_(f"SELECT * FROM leaderboard WHERE id = {message.author.id}")

                                emded = discord.Embed(
                                    title='Вы достигли нового уровня!',
                                    description=f">>> **Ваш тек. уровень:** `{row['lvl']}`\n"
                                                f"**Опыт до след. уровня:** `{row['lvl_bar']}` ",
                                    color=0xFFD00D
                                ).set_author(
                                    name=f'@{message.author.name}', icon_url=message.author.avatar
                                ).set_footer(text=f'Место в топе: {row["lvl_top"]} ●︎ Сегодня. в {datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")).strftime("%H:%M")}')

                                await channel.send(content=f'{message.author.mention}', embed=emded)

                        except Exception:
                            cur.commit_(f"INSERT INTO leaderboard VALUES ({message.author.id}, {message.author.name}, 0, 100, 0, 0)")

                for content in message.content.split():
                    for word_hello in WORD_HELLO:
                        if content.lower() == word_hello:
                            await message.add_reaction("👋")

                cur.close_()

            except OperationalError:
                ch = await self.bot.get_channel(config.config.CHANNEL_REPORT)

                await ch.send(embed=discord.Embed(
                    title='Бот был выключен с хоста',
                    description='Производится перезапуск бота!',
                    color=0xFFFFFF
                ))
                system("python reg.py")
                system('kill 1')

        @commands.Cog.listener()
        async def on_voice_state_update(self, member, before, after):
            cur = BD_Bot()

            voice_channel = 1216456190637379696
            voice_cate = 1216456083506335894

            if after.channel is not None and member.voice.channel.id == voice_channel and member.voice.channel is not None:
                global channel

                if before.channel is not None:
                    await before.channel.delete()
                    cur.commit_(f"DELETE FROM voice_private WHERE id_voice = {before.channel.id}")

                category = discord.utils.get(member.guild.categories, id=voice_cate)
                channel = await member.guild.create_voice_channel(name=f'Комната {member.display_name}',category=category)
                cur.commit_(f"INSERT INTO voice_private VALUES ({channel.id}, {member.id})")
                await channel.set_permissions(member, connect=True, mute_members=True, move_members=True, manage_channels=True)
                await member.move_to(channel)

            for row in cur.gets_("SELECT * FROM voice_private"):
                if not discord.utils.get(member.guild.voice_channels, id=row['id_voice']) is None:
                    channel = discord.utils.get(member.guild.voice_channels, id=row['id_voice'])
                    if after.channel is None and len(channel.members) == 0:
                        await channel.delete()
                        cur.commit_(f"DELETE FROM voice_private WHERE id_voice = {channel.id}")

            cur.close_()

        @commands.Cog.listener()
        async def on_raw_reaction_add(self, payload):
            cur = BD_Bot()
            guild = self.bot.get_guild(1149010761029529610)

            if payload.channel_id == 1211215434725199882:
                channel = self.bot.get_channel(payload.channel_id)
                rows = cur.gets_(f"SELECT * FROM message_ver")
                for row in rows:
                    if payload.message_id == row['id_message']:
                        message = await channel.fetch_message(payload.message_id)

                        if str(payload.emoji) == '✅':
                            user = discord.utils.get(guild.members, id=int(row['id_user']))
                            cur.commit_(f"INSERT INTO accounts VALUES ({row['id_pikuco']}, {row['id_user']}, '{row['name']}', 0, 0, 0, 0, 0)")
                            await user.send('Администрация одобрела вашу верификацию. Добро пожаловать на сервер!')

                            await on_join(member=user, pik_id=row['id_pikuco'])
                            cur.commit_(f"DELETE FROM message_ver WHERE id_message = {payload.message_id}")
                            await message.delete()
                        elif str(payload.emoji) == '❌':
                            user = self.bot.get_user(guild.members, id=int(row['id_user']))
                            await user.send('Администрация не одобрела вашу верификацию. Повторите попытку!')

                            await message.delete()

            for row in cur.gets_(f"SELECT * FROM games_event"):
                list_role = (row['id_role'], row['id_role_z'])

                if payload.channel_id == row['id_channel']:
                    channel = self.bot.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    member = discord.utils.get(message.guild.members, id=payload.user_id)

                    if str(payload.emoji) == '✅':
                        if len([i for i in member.roles if i.id in list_role]) < 1:
                            member = discord.utils.get(guild.members, id=payload.user_id)
                            role = discord.utils.get(guild.roles, id=row['id_role'])
                            await member.add_roles(role)
                        else:
                            await message.remove_reaction(payload.emoji, member)
                    elif str(payload.emoji) == '👁':
                        if len([i for i in member.roles if i.id in list_role]) < 1:
                            member = discord.utils.get(guild.members, id=payload.user_id)
                            role = discord.utils.get(guild.roles, id=row['id_role_z'])
                            await member.add_roles(role)
                        else:
                            await message.remove_reaction(payload.emoji, member)

                    list_role = None

            for row in cur.gets_(f"SELECT * FROM clans"):
                if payload.channel_id == row['id_channel']:
                    if payload.user_id == row['leader_id']:
                        for use in cur.gets_(f"SELECT * FROM clans_check WHERE id_clan = {row['id_clan']}"):
                            channel = self.bot.get_channel(payload.channel_id)
                            message = await channel.fetch_message(payload.message_id)

                            if str(payload.emoji) == '✅':
                                us = discord.utils.get(guild.members, id=use['id_user'])
                                cur.commit_(f"UPDATE clans SET member_clan = member_clan + 1 WHERE id_clan = {row['id_clan']}")

                                checks = cur.get_(f"SELECT * FROM clans WHERE id_clan = {row['id_clan']}")
                                if checks['member_clan'] >= row['col_member']:
                                    cur.commit_(f"UPDATE clans SET member_clan = member_clan - 1 WHERE id_clan = {row['id_clan']}")
                                    await us.remove_roles(discord.utils.get(guild.roles, id=row['id_role']))
                                    await us.send(f"Извините, но места в клане нет")
                                else:
                                    await us.add_roles(discord.utils.get(guild.roles, id=row['id_role']))
                                    await us.send(f'Вы вступили в клан **{row["name_clan"]}**')

                                cur.commit_(f"DELETE FROM clans_check WHERE id_user = {use['id_user']}")
                                await message.delete()

                            elif str(payload.emoji) == '❌':
                                us = discord.utils.get(guild.members, id=use['id_user'])
                                await us.send(f'Вы не вступили в клан **{row["name_clan"]}**, создатель дал отказ')

                                cur.commit_(f"DELETE FROM clans_check WHERE id_user = {use['id_user']}")
                                await message.delete()

            cur.close_()

        @commands.Cog.listener()
        async def on_raw_reaction_remove(self, payload):
            cur = BD_Bot()
            guild = self.bot.get_guild(1149010761029529610)

            for row in cur.gets_(f"SELECT * FROM games_event"):
                if payload.channel_id == row['id_channel']:
                    channel = self.bot.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)

                    if str(payload.emoji) == '✅':
                        member = discord.utils.get(guild.members, id=payload.user_id)
                        role = discord.utils.get(guild.roles, id=row['id_role'])
                        await member.remove_roles(role)
                    elif str(payload.emoji) == '👁':
                        member = discord.utils.get(guild.members, id=payload.user_id)
                        role = discord.utils.get(guild.roles, id=row['id_role_z'])
                        await member.remove_roles(role)

            cur.close_()


    async def setup(bot):
        await bot.add_cog(Event(bot))

except OperationalError:
    print('База Данных слетела! Перезапуск бота')
    system("python reg.py")
    system('kill 1')