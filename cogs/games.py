import time
from typing import Any
import discord
from discord import ui, app_commands, Interaction
from discord._types import ClientT
from discord.ext import commands
from bs4 import BeautifulSoup as BS
import lxml
from mysql import connector
import requests
from os import system
from mysql.connector.errors import OperationalError
from PIL import Image
from cogs.func_storage.func_storage import on_join, embed_err
from cogs.func_storage.BD_function import BD_Bot

pe = []

class SelectG(ui.Select):
    def __init__(self):
        super().__init__(placeholder='Выбери игру', min_values=1, max_values=1, options=pe)

    async def callback(self, inter: Interaction):
        for row in inter.user.roles:
            if row.id == 1211743965380870226:
                try:
                    global pe
                    cur = BD_Bot()
                    await inter.response.defer(thinking=True, ephemeral=True)

                    row = cur.get_(f"SELECT * FROM games_event WHERE id_channel = {int(str(self.values[0]))}")

                    channel = discord.utils.get(inter.guild.channels, id=row['id_channel'])
                    await channel.delete()
                    role = discord.utils.get(inter.guild.roles, id=row['id_role'])
                    role_z = discord.utils.get(inter.guild.roles, id=row['id_role_z'])
                    await role.delete()
                    await role_z.delete()

                    cur.commit_(f"DELETE FROM games_event WHERE id_channel = {int(str(self.values[0]))}")

                    cur.close_()

                    pe.clear()
                    await inter.edit_original_response(content='Канал был удален!')

                except Exception:
                    embed = discord.Embed(
                        description='Ошибка. Игра была либо удалена, либо ее нет',
                        color=0xeb144c
                    ).set_author(
                        name='Ошибка',
                        icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
                    )

                    await inter.edit_original_response(embed=embed)

class SelectGame(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectG())

class Modal_games(ui.Modal, title='Создание информации об игре'):
    name = ui.TextInput(label='Напишите название игры', style=discord.TextStyle.short)
    dis = ui.TextInput(label='Напишите описание, что будет по игре', style=discord.TextStyle.paragraph)
    people = ui.TextInput(label='Сколько максимальное число участников будет?', style=discord.TextStyle.short)
    time_start = ui.TextInput(label='Во сколько будет игра?', placeholder='Писать так: 15:00 или 08:45', style=discord.TextStyle.short)
    time_end = ui.TextInput(label='Во сколько закончится игра?', placeholder='Писать так: 16:00 или 09:45', style=discord.TextStyle.short)

    async def on_submit(self, inter: discord.Interaction):
        cur = BD_Bot()

        await inter.response.defer(ephemeral=True, thinking=True)
        c = discord.utils.get(inter.guild.categories, id=1149010761029529611)
        channel = await inter.guild.create_text_channel(name=f'{self.name}', category=c)
        role = await inter.guild.create_role(name=f'Участник {self.name}', color=0x4B0082)
        role_z = await inter.guild.create_role(name=f'Зритель {self.name}', color=0xFFFFFF)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True

        await channel.set_permissions(target=discord.utils.get(inter.guild.roles, id=role.id), overwrite=overwrite)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False

        await channel.set_permissions(target=discord.utils.get(inter.guild.roles, id=role_z.id), overwrite=overwrite)
        embed = discord.Embed(
            title=f'Игра: {self.name}',
            description=f'Описание игры:\n{self.dis}'
        )
        embed.add_field(
            name='Начало и конец игры',
            value=f'{self.time_start} - {self.time_end}'
        )
        embed.add_field(
            name='Кол-во Участников',
            value=f'{self.people}'
        )

        message = await channel.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('👁')

        cur.commit_(f"INSERT INTO games_event VALUES ({channel.id}, {message.id}, {role.id}, {role_z.id}, '{self.name}', '{self.dis}', {int(str(self.people))}, '{self.time_start}', '{self.time_end}', 0)")

        cur.close_()

        await inter.edit_original_response(content="Ваша игра была создана!")

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='create_game', description='Создай свою игру (ВНИМАНИЕ: Только для инвентеров)')
    async def create_game_(self, inter: Interaction):
        for role in inter.user.roles:
            if role.id == 1211743965380870226:
                await inter.response.send_modal(Modal_games())

    @app_commands.command(name='del_game', description='Удали свою игру (ВНИМАНИЕ: Ток для овнеров)')
    async def delete_game_(self, inter: Interaction):
        for role in inter.user.roles:
            if role.id == 1211743965380870226:
                try:
                    global pe
                    cur = BD_Bot()

                    rows = cur.gets_(f"SELECT * FROM games_event")
                    for row in rows:
                        pe.append(discord.SelectOption(label=f'{row["name"]}', value=f'{row["id_channel"]}'))

                    cur.close_()

                    await inter.response.send_message(content='Выбери игру, которую хочешь удалить', view=SelectGame())

                except Exception:
                    embed = discord.Embed(
                        description='Ошибка. Никаких игр нету в списке',
                        color=0xeb144c
                    ).set_author(
                        name='Ошибка',
                        icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
                    )

                    await inter.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Games(bot))