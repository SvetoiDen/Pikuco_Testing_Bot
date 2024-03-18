import asyncio
import datetime
from mysql import connector
import time
from os import system
import discord
import requests
from discord.ext import commands, tasks
import io
from discord import app_commands, Interaction, ui
import config.config
from cogs.func_storage.BD_function import BD_Bot
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import pytz
from mysql.connector.errors import OperationalError
import unicodedata
from cogs.func_storage.func_storage import delete_game_ds

try:
    class Bot(commands.Bot):
        def __init__(self):
            super().__init__(command_prefix=commands.when_mentioned_or('pic!'), intents=discord.Intents().all(), help_command=None)

        async def setup_hook(self):
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    await bot.load_extension(f"cogs.{filename[:-3]}")

    bot = Bot()

    @bot.event
    async def on_ready():
        print(f'Бот готов к работе')
        print(f'Слеш команд: {str(len(await bot.tree.sync()))}')
        # print(f'Текст. каналы на сервере: {str(len(bot.get_guild(895664106999279626).channels))}')
        # print(f'Голос. каналы на сервере: {str(len(bot.get_guild(895664106999279626).voice_channels))}')
        # print(f'Людей на сервере: {bot.get_guild(895664106999279626).member_count}')
        # print(f'====================\n')

    @bot.command(name='restart')
    @commands.is_owner()
    async def rest_cogs(ctx):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.reload_extension(f"cogs.{filename[:-3]}")

        print("Произведен RELOAD файлов!")
        print(f'Слеш команд: {str(len(await bot.tree.sync()))}')
        # print(f'Текст. каналы на сервере: {str(len(bot.get_guild(895664106999279626).channels))}')
        # print(f'Голос. каналы на сервере: {str(len(bot.get_guild(895664106999279626).voice_channels))}')
        # print(f'Людей на сервере: {bot.get_guild(895664106999279626).member_count}')
        # print(f'====================\n')
        await ctx.message.add_reaction('✅')

    @bot.tree.context_menu(name='Профиль')
    async def lvl_profile(inter: Interaction, member: discord.Member):
        cur = BD_Bot()
        await inter.response.defer(ephemeral=True)

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
        url = member.avatar

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

        row = cur.get_(f"SELECT * FROM leaderboard WHERE id = {member.id}")
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

    @bot.tree.context_menu(name='Очистить сообщения')
    async def clear_message(inter: Interaction, message: discord.Message):
        count = 0
        await inter.response.defer(thinking=True)
        async for row in message.channel.history(limit=100):
            if not message.id == row.id:
                count += 1
            else:
                break

        await inter.edit_original_response(content=f'Сообщений будет удалено **{count}**, До сообщения\n**{message.content}**')
        await message.channel.purge(limit=count+1)


    bot.run(config.config.TOKEN)

except OperationalError:
    ch = bot.get_channel(config.config.CHANNEL_TEST)

    ch.send(embed=discord.Embed(
        title='Бот был выключен с хоста',
        description='Производится перезапуск бота!',
        color=0xFFFFFF
    ))
    system("python reg.py")
    system('kill 1')