import datetime
import random
import requests
import discord
from discord.ext import commands
from discord.ext.commands import Context
import lxml
import io
import sqlite3
from Cybernator import Paginator
from random import randint
from mysql import connector
from discord import Interaction
import pytz
import os
from bs4 import BeautifulSoup as BS
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from discord import ui, app_commands
from mysql.connector.errors import OperationalError
from os import system

import config.config
from cogs.func_storage.BD_function import BD_Bot

li = ["Да", "Нет", "Наверно да", "Наверно нет"]

try:
    class Commands(commands.Cog):

        def __init__(self, bot):
            self.bot = bot

        @app_commands.command(name='шар', description='Узнай, что хочет от тебя бот')
        async def ball(self, inter: Interaction, reason: str):
            ran = random.choice(li)
            await inter.response.send_message(content=f"Вопрос от {inter.user.mention}\n**{reason}**\nОтвет: {ran}")

        @app_commands.command(name="тест", description='Рандомный тест из сайта')
        async def randomtest(self, inter: Interaction):
            await inter.response.defer(thinking=True)
            randoms = random.randint(1, 80000)
            await inter.edit_original_response(content=f"https://pikuco.ru/tests/{randoms}/")

        @app_commands.command(name='шипперим', description='Узнай, у кого любовные связи')
        async def shipping(self, inter: Interaction):
            a = []
            for user in inter.guild.members:
                a.append(user.id)

            await inter.response.send_message(f'У <@{random.choice(a)}> есть любовные связи с <@{random.choice(a)}>')
            a.clear()

        @commands.command(name='справочник')
        async def helps(self, ctx):
            embed = discord.Embed(
                title='Список Команд - Общие'
            )
            embed.add_field(
                name='/тест',
                value='Выдает рандомный тест из Pikuco (ВНИМАНИЕ: Может выдать нерабочий тест)'
            )
            embed.add_field(
                name='/шар (вопрос)',
                value='Выдает ответ на ваш вопрос (ВНИМАНИЕ: Ответы на ваши вопросы не несут никакой правды)'
            )

            embed2 = discord.Embed(
                title='Список Команд - Уровень'
            )
            embed2.add_field(
                name='pic!ур',
                value='Показывает текущий уровень у пользователя'
            )
            embed2.add_field(
                name='pic!топ',
                value='Вызывает топ 10 пользователей с высоким уровнем'
            )

            embed4 = discord.Embed(
                title='Список команд - Дополнительные'
            )
            embed4.add_field(
                name='/очистить (число)',
                value='Удаляет определенное кол-во сообщении'
            )
            embed4.add_field(
                name='/set_birthday',
                value='Установить день рождения (в нужный день и месяц появится соо об упоминании вашего дня рождения)'
            )

            embed3 = discord.Embed(
                title='Список Команд - Эмоции'
            )
            embed3.add_field(
                name='?поцеловать',
                value='Поцеловать пользователя (по желанию можете написать причину)'
            )
            embed3.add_field(
                name='?покормить',
                value='Покормить пользователя (по желанию можете написать причину)'
            )
            embed3.add_field(
                name='?обнять',
                value='Обнять пользователя (по желанию можете написать причину)'
            )
            embed3.add_field(
                name='?пожениться',
                value='Пожениться с пользователем (ВАЖНО: Нужно согласия упомянутого пользователя)'
            )

            embeds = [embed, embed2, embed4, embed3]
            message = await ctx.send(embed=embed)
            page = Paginator(self.bot, message, only=ctx.author, use_more=False, embeds=embeds)
            await page.start()

        @app_commands.command(name='set_birthday', description='Установи дату своего дня рождения')
        async def set_burthday(self, inter: Interaction, month: int, day: int):
            cur = BD_Bot()

            await inter.response.defer(thinking=True)
            row = cur.get_(f"SELECT id FROM birthday WHERE id = {inter.user.id}")
            if row is None:
                if int(day) < 10:
                    day = f"0{day}"

                if int(month) < 10:
                    month = f"0{month}"

                cur.commit_(f"INSERT INTO birthday VALUES ({inter.user.id}, {day}, {month})")

                await inter.edit_original_response('Твой день рождения был установлен!')
            else:
                embed = discord.Embed(
                    description='Твой день рождения итак уже установлен.',
                    color=0xeb144c
                ).set_author(
                    name='Ошибка',
                    icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
                )

                await inter.edit_original_response(embed=embed)

            cur.close_()

        @app_commands.command(name='ур', description='Посмотри свой уровень!')
        async def rank(self, inter: Interaction):
            cur = BD_Bot()
            await inter.response.defer()

            def prepare_mask(size, antialias=2):
                mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
                ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
                return mask.resize(size)

            def crop(im, s):
                w, h = im.size
                k = w / s[0] - h / s[1]
                if k > 0:
                    im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
                elif k < 0:
                    im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
                return im.resize(s)

            size = (97, 97)

            image = Image.open('config/lvl.png')
            url = inter.user.avatar

            x = 634
            y = 258

            r = requests.get(url, stream=True)
            p = Image.open(io.BytesIO(r.content))
            n = p.convert('RGBA')
            m = n.resize((97, 97))
            im = crop(m, size)
            im.putalpha(prepare_mask(size, 4))
            im.save('config/image_output1.png', format='png')

            images = Image.open('config/image_output1.png')
            image.paste(images, (269, 28), mask=images)

            row = cur.get_(f"SELECT * FROM leaderboard WHERE id = {inter.user.id}")
            idraw = ImageDraw.Draw(image)
            b = ImageFont.truetype('config/Montserrat-Bold.ttf', size=38)
            c = ImageFont.truetype('config/Montserrat-Bold.ttf', size=32)
            idraw.text((320, 150), f'{row["name"]}', font=c, anchor='mm', align='center')
            idraw.text((109, 174), f'{row["lvl"]}', font=b)
            idraw.text((285, 180), f'{row["lvl_progress"]} / {row["lvl_bar"]}', font=c)
            idraw.text((506, 175), f'{row["lvl_top"]}', font=b)
            image.save('config/lvl_card.png')

            await inter.edit_original_response(attachments=[discord.File(fp='config/lvl_card.png', filename='lvl_card.png')])
            cur.close_()

        @app_commands.command(name='топ', description='просмотр топ 10 по уровням')
        async def rank_top(self, inter: Interaction):
            cur = BD_Bot()

            await inter.response.defer(thinking=True)
            counter = 0

            embed = discord.Embed(title=f'Топ 10 Пользователей по рангу<:logo:905120503558201426>')
            rows = cur.gets_("SELECT name, lvl, id FROM leaderboard ORDER BY lvl DESC LIMIT 10")
            for row in rows:
                counter += 1
                embed.add_field(
                    name=f"{counter}# | `{row['name']}`",
                    value=f'**{row["lvl"]} Уровень**',
                    inline=False
                )

            await inter.edit_original_response(embed=embed)

            counter = 0
            for row in cur.gets_("SELECT id FROM leaderboard ORDER BY lvl DESC"):
                counter += 1
                cur.commit_(f"UPDATE leaderboard SET lvl_top = {counter} WHERE id = {row['id']}")

            cur.close_()

        @commands.command(name='embed1')
        @commands.is_owner()
        async def embed_test(self, ctx: Context):
            embed = discord.Embed(
                description="## Приветствуем на сервере PIKUCO!\n"
                            f"Хей, {ctx.author.mention}! Располагайся по-удобнее, ведь ты попал на официальный Discord сервер Pikuco! Давайте мы вам немного расскажем о нашем сервере!\n"
                            "### Несколько пунктов, которые тебе нужно сделать:\n"
                            "- Ознакомься с правилами сервера.\n"
                            "- Поздоровайся с нашими участниками, расскажи о себе!\n"
                            "- Скинь милую пикчу или мем в нашу галерею!\n"
                            "### Вот вся ваша статистика из сайта на момент захода в наш сервер:",
                color=0xFFD00D
            ).set_image(
                url='https://media.discordapp.net/attachments/1175426440066498591/1213821387991687198/download_1.gif?ex=65f6de42&is=65e46942&hm=a7d72d291c2a84096590919b0fe8fb53c5da8cc73852c5115f068d95c1f2e3de&=&width=750&height=250'
            ).set_footer(text='От незнаний правил вы не освобождайтесь от отвественности. Если вас нет на сайте больше 3 месяцев, вы кикайтесь из сервера (Именно кик, а не бан). Также не выдавайте себя за другого человека.')
            embed.add_field(name='Твой рейтинг', value='209')
            embed.add_field(name='Кол-во прохождений', value='20002')
            embed.add_field(name='Подписчиков', value='22')
            embed.add_field(name='Созданных тестов', value='2111')
            embed.add_field(name='Комментариев', value='22')
            embed.add_field(name='Средний бал', value='9.1')

            await ctx.send(f'{ctx.author.mention}', embed=embed)

    async def setup(bot):
        await bot.add_cog(Commands(bot))

except OperationalError:
    ch = self.bot.get_channel(config.config.CHANNEL_REPORT)

    ch.send(embed=discord.Embed(
        title='Бот был выключен с хоста',
        description='Производится перезапуск бота!',
        color=0xFFFFFF
    ))
    system("python reg.py")
    system('kill 1')