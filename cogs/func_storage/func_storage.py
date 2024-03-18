import io
import json
from typing import Any
from discord import app_commands, ui
import discord
from discord import Interaction
from discord._types import ClientT
from discord.ext import commands
from mysql import connector
import requests
from bs4 import BeautifulSoup as bs
import lxml
from PIL import Image, ImageDraw, ImageFont, ImageOps
from os import system
from mysql.connector.errors import OperationalError
from cogs.func_storage.BD_function import BD_Bot

embed_err = discord.Embed(
    description='Нехватка средств! Для создания клана нужно 10000 пикукоинов',
    color=0xeb144c
).set_author(
    name='Ошибка',
    icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
)

embed_err_clans = discord.Embed(
    description='Извините, но похоже у вас нет своего клана, или в нем нет участника, или заместитель уже есть!',
    color=0xeb144c
).set_author(
    name='Ошибка',
    icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
)

def get_pikuco_profile(pikuco_id: int):
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }

    r = requests.get(f'https://pikuco.ru/profile/{pikuco_id}/', headers=user_agent)
    b = bs(r.content, 'html.parser')
    return b

async def on_join(member, pik_id: int):
    cur = BD_Bot()

    cur.commit_(f"INSERT INTO leaderboard VALUES ({member.id}, '{member.name}', 0, 100, 0, 0)")

    role = discord.utils.get(member.guild.roles, id=1211282956283543563)
    channel = discord.utils.get(member.guild.channels, id=1211282900411093043)
    await member.add_roles(role)
    user_p = get_pikuco_profile(pik_id)

    reting = user_p.find('div', class_='user_rating').find('p', class_='title').text
    comment = user_p.find('div', class_='user_comments').find('p', class_='title').text
    user_tests_passed = user_p.find('div', class_='user_tests_passed').find('p', class_='title').text
    user_tests_added = user_p.find('div', class_='user_tests_added').find('p', class_='title').text
    user_subscribers = user_p.find('div', class_='user_subscribers').find('p', class_='title').text
    user_average = user_p.find('div', class_='user_average').find('p', class_='title').text

    embed = discord.Embed(
        description="## Приветствуем на сервере PIKUCO!\n"
                    f"Хей, {member.mention}! Располагайся поудобнее, ведь ты попал на официальный Discord сервер Pikuco!\n"
                    "### Несколько пунктов, которые тебе нужно сделать:\n"
                    "- Ознакомься с правилами сервера.\n"
                    "- Поздоровайся с нашими участниками, расскажи о себе!\n"
                    "- Скинь милую пикчу или мем в нашу галерею!\n"
                    "### Вот вся твоя статистика из сайта на момент захода в наш сервер:",
        color=0xFFD00D
    ).set_image(
        url='https://media.discordapp.net/attachments/1175426440066498591/1213821387991687198/download_1.gif?ex=65f6de42&is=65e46942&hm=a7d72d291c2a84096590919b0fe8fb53c5da8cc73852c5115f068d95c1f2e3de&=&width=750&height=250'
    ).set_footer(text='От незнаний правил вы не освобождайтесь от отвественности. Если вас нет на сайте и в дискорде больше 3 месяцев, вы кикайтесь из сервера (Именно кик, а не бан). Также не выдавайте себя за другого человека.')
    embed.add_field(name='Твой рейтинг', value=reting)
    embed.add_field(name='Теста пройдено', value=user_tests_passed)
    embed.add_field(name='Подписчиков', value=user_subscribers)
    embed.add_field(name='Созданных тестов', value=user_tests_added)
    embed.add_field(name='Комментариев', value=comment)
    embed.add_field(name='Средний бал', value=user_average)

    message = await channel.send(f"{member.mention}", embed=embed)
    await message.add_reaction('👋')

    cur.close_()

async def delete_game_ds(guild, ch):
    cur = BD_Bot()
    row = cur.get_(f"SELECT * FROM games_event WHERE id_channel = {ch.id}")

    channel = discord.utils.get(guild.channels, id=row['id_channel'])
    await channel.delete()
    role = discord.utils.get(guild.roles, id=row['id_role'])
    role_z = discord.utils.get(guild.roles, id=row['id_role_z'])
    await role.delete()
    await role_z.delete()

    cur.commit_(f"DELETE FROM games_event WHERE id_channel = {ch.id}")
    cur.close_()