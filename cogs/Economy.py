import io
import json
from typing import Any
from discord import app_commands, ui
import discord
from discord import Interaction
from discord._types import ClientT
from discord.ext import commands
from discord.ext.commands import Context
from mysql import connector
import requests
from bs4 import BeautifulSoup as bs
import lxml
from PIL import Image, ImageDraw, ImageFont, ImageOps
from cogs.func_storage.func_eco import buy_1, buy_2, buy_3, buy_4, eco_profile, work_t, work_p
from os import system
from mysql.connector.errors import OperationalError
from cogs.func_storage.BD_function import BD_Bot

na = []
op = []
t = None

try:
    class Modal_Test_Post(ui.Modal, title=f'Ссылку на ваш тест/пост'):
        link = ui.TextInput(label=f'Введите ссылку', placeholder='Ссылка...', style=discord.TextStyle.short)

        async def on_submit(self, inter: Interaction):
            await inter.response.defer(thinking=True, ephemeral=True)
            global na
            if na[0] == 'тест':
                await work_t(inter=inter, test=str(self.link))
            elif na[0] == 'пост':
                await work_p(inter=inter, post=str(self.link))

            na.clear()

    class Select_test_post(ui.Select):
        def __init__(self):
            op = [
                discord.SelectOption(label='Тест', description='Отправь ссылку на тест', value='test'),
                discord.SelectOption(label='Пост', description='Отправь ссылку на пост', value='post')
            ]

            super().__init__(placeholder='Выбери что хочешь отправить', min_values=1, max_values=1, options=op)

        async def callback(self, inter: Interaction):
            global na
            if str(self.values[0]) == 'test':
                na.append('тест')
                await inter.response.send_modal(Modal_Test_Post())
            elif str(self.values[0]) == 'post':
                na.append('пост')
                await inter.response.send_modal(Modal_Test_Post())

    class SelectMenu(ui.Select):
        def __init__(self):
            super().__init__(placeholder='Выбери товар из магазина', min_values=1, max_values=1, options=op)

        async def callback(self, inter: Interaction):
            cur = BD_Bot()

            bal = cur.get_(f"SELECT balance FROM accounts WHERE id = {inter.user.id}")['balance']
            cost = cur.get_(f"SELECT cost FROM shop WHERE id = {int(self.values[0])}")['cost']

            a = f'buy_{self.values[0]}'
            await eval(a)(bal, cost, inter)

            cur.close_()
            op.clear()

    class Menu_test_post(ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(Select_test_post())

    class Menu_View(ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(SelectMenu())

    class Views_Eco(ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        # @ui.button(emoji='📕', style=discord.ButtonStyle.green, row=1)
        # async def help_economy(self, inter: Interaction, button: ui.Button):
        #     await inter.response.defer(thinking=True, ephemeral=True)
        #     file = open('config/gude_economy.txt', 'r', encoding='utf-8')
        #     embed = discord.Embed(
        #         title='Гайд-бук и список команд по "Экономический Пикуко"',
        #         description=file.read()
        #     )
        #     file.close()
        #     embed.add_field(
        #         name='?эко_профиль',
        #         value='Показывает ваш эко профиль.'
        #     )
        #     embed.add_field(
        #         name='?старт',
        #         value='Вызвав эту команду, вы можете получить свой первый (наверно) гонорар'
        #     )
        #     embed.add_field(
        #         name='?work_test (Ссылка на ваш тест)',
        #         value='вы получайте свой зарабаток с теста. Коулдаун команды == 5 минут'
        #     )
        #     embed.add_field(
        #         name='?work_post (Ссылка на ваш пост)',
        #         value='вы получайте свой зарабаток с поста. Коулдаун команды == 5 минут'
        #     )
        #     embed.add_field(
        #         name='?economy_top',
        #         value='показывает список топ 20 экономистов'
        #     )
        #     embed.add_field(
        #         name='?эко_магазин',
        #         value='Открывает магазин с покупкой ролей, услуг и тд'
        #     )
        #
        #     await inter.edit_original_response(embed=embed)

        @ui.button(emoji='💰', style=discord.ButtonStyle.primary, row=1)
        async def start_economy(self, inter: Interaction, button: ui.Button):
            cur = BD_Bot()

            await inter.response.defer(thinking=True, ephemeral=True)
            row = cur.get_(f"SELECT * FROM accounts WHERE id = {inter.user.id}")
            if row["start_ec"] == 0:
                r = requests.get(f'https://pikuco.ru/profile/{row["authid"]}/')
                soup = bs(r.text, 'lxml')

                reting = int(soup.find("div", class_='col-xl-3 col-6 user_rating user_stat_block').find('p', class_='title').text)
                pos = int(soup.find('div', class_='col-xl-3 col-6 user_tests_passed user_stat_block').find('p', class_='title').text)

                bal = (reting*0.5)+(pos*0.5)
                cur.commit_(f"UPDATE accounts SET balance = balance + {bal} WHERE id = {inter.user.id}")
                cur.commit_(f"UPDATE accounts SET start_ec = 1 WHERE id = {inter.user.id}")
                await inter.edit_original_response(content="Поздравляю! вы получили гонорар в размере:**<:pikucoin:1139591723216027719>{bal}**!")
            else:
                embed = discord.Embed(
                    description='Извиинте, но вы уже использовали эту команду. Она приминяется только один раз!',
                    color=0xeb144c
                ).set_author(
                    name='Ошибка',
                    icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
                )

                await inter.edit_original_response(embed=embed)

            cur.close_()

        @ui.button(emoji='🖼', style=discord.ButtonStyle.primary, row=1)
        async def profile_economy(self, inter: Interaction, button: ui.Button):
            cur = BD_Bot()
            await inter.response.defer(thinking=True, ephemeral=True)

            row = cur.get_(f"SELECT authid FROM accounts WHERE id = {inter.user.id}")
            if row is None:
                await inter.edit_original_response(content='**ВЫ НЕ ЗАРЕГЕСТРИРОВАЛИСЬ!**')
            else:
                member = inter.user
                await eco_profile(member=member)

                await inter.edit_original_response(attachments=[discord.File(fp='config/user_card.png', filename='user_card.png')])

            cur.close_()

        @ui.button(emoji='📊', style=discord.ButtonStyle.primary, row=1)
        async def economy_top(self, inter: Interaction, button: ui.Button):
            cur = BD_Bot()

            await inter.response.defer(thinking=True, ephemeral=True)
            counter = 0
            embed = discord.Embed(title='Топ 10 Экономистов<:heartgreen:988022781201510410>')
            rows = cur.gets_("SELECT * FROM accounts ORDER BY balance DESC LIMIT 10")

            for row in rows:
                counter += 1
                embed.add_field(
                    name=f'{counter} место - `{row["name"]}`',
                    value=f'Баланс: {row["balance"]}<:pikucoin:1139591723216027719>',
                    inline=False
                )

            await inter.edit_original_response(embed=embed)

            cur.close_()

        @ui.button(emoji='💵', style=discord.ButtonStyle.green, row=1)
        async def money_add(self, inter: Interaction, button: ui.Button):
            await inter.response.defer(thinking=True, ephemeral=True)
            embed = discord.Embed(
                title='На что заработаешь?',
                description='Решай, на чем ты заработаешь свое состояние: На тесте, или на посте'
            )

            await inter.edit_original_response(embed=embed, view=Menu_test_post())

        @ui.button(emoji='🏪', style=discord.ButtonStyle.green, row=1)
        async def shop_pik(self, inter: Interaction, button: ui.Button):
            cur = BD_Bot()

            await inter.response.defer(thinking=True, ephemeral=True)
            global op
            rows = cur.gets_("SELECT * FROM shop")

            embed = discord.Embed(
                title='Магазин PIKUCO - Роли, услуги и тд',
                description='Для покупки пропишите команду ?buy (номер товара)'
            )

            for row in rows:
                op.append(discord.SelectOption(label=row['name'], description=row['description'], value=row['id']))
                embed.add_field(
                    name=f"{row['id']}# | {row['name']} = {row['cost']} ПикуКоинов",
                    value=row['description'],
                    inline=False
                )

            await inter.edit_original_response(embed=embed, view=Menu_View())

            cur.close_()

    class Economy(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @commands.command(name='эко_начало')
        @commands.is_owner()
        async def eco_admin_start(self, ctx: Context):
            embed = discord.Embed(
                description='## Экономический Pikuco - Начальная страница\n'
                            f'Экономический пикуко - интерактивное развлечение на официальном дискорд сервере пикуко с элементами экономики, но главный твой заработк - это твои тесты и посты.\nОт их популярности зависит твой заработок, а также ты можешь этот зарабаток удваивать, утриавать и тд, чтобы стать еще богаче.\n'
                            f'- Главная валюта сервера - Пикукоины, вот такие <>.\n'
                            f'- Зарабатывай, становись круче.\n'
                            f'### Список команд Экономического пикуко\n'
                            # f'- 📕 - Просмотреть гайд по экономического пикуко\n'
                            f'- 💵 - Заработать на тесте, или на посте\n'
                            f'- 🏪 - Просмотреть эко-магазин, где можно купить множетили, и кастомную роль\n'
                            f'- 💰 - Получить первый стартовый капитал (Зависит от вашего рейтинга и пройденных тестов)\n'
                            f'- 🖼 - Просмотреть свой профиль экономического пикуко\n'
                            f'- 📊 - Просмотреть топ 10 пользователей по балансу',
                color=0xFFD00D
            )

            await ctx.send(embed=embed, view=Views_Eco())

        @commands.command(name='Админ_Панель')
        @commands.has_permissions(administrator=True)
        async def list_admins_panels_economy(self, ctx):
            embed = discord.Embed(
                title='Список команд по Экономику'
            )
            embed.add_field(
                name='?set_cash',
                value='Установить кол-во ПикуКоинов',
                inline=False
            )
            embed.add_field(
                name='?remove_cash',
                value='Убирает кол-во ПикуКоинов',
                inline=False
            )
            embed.add_field(
                name='?set_change',
                value='Установить определенный шанс в казино',
                inline=False
            )
            await ctx.author.send(embed=embed)

        @commands.command()
        @commands.has_permissions(administrator=True)
        async def set_cash(self, ctx, cash: int = None, member: discord.Member = None):
            cur = BD_Bot()

            if (cash is None) and (member is None):
                embed = discord.Embed(
                    description='Не установлено значение кеша и не выбран игрок',
                    color=0xeb144c
                ).set_author(
                    name='Ошибка',
                    icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
                )

                await ctx.send(embed=embed)
            else:
                if cash < 0:
                    embed = discord.Embed(
                        description='Значение не должно быть меньше 0',
                        color=0xeb144c
                    ).set_author(
                        name='Ошибка',
                        icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
                    )

                    await ctx.send(embed=embed)
                else:
                    cur.commit_(f"UPDATE accounts SET balance = balance + {cash} WHERE authid = {member.id}")
                    await ctx.send(f'Был прибавлен баланс: **+{cash}<:pikucoin:1139591723216027719> игроку {member}**')

            cur.close_()

        @commands.command()
        @commands.has_permissions(administrator=True)
        async def remove_cash(self, ctx, cash: int = None, member: discord.Member = None):
            cur = BD_Bot()

            if (cash is None) and (member is None):
                embed = discord.Embed(
                    description='Не установлено значение кеша и не выбран игрок',
                    color=0xeb144c
                ).set_author(
                    name='Ошибка',
                    icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
                )

                await ctx.send(embed=embed)
            else:
                if cash < 0:
                    embed = discord.Embed(
                        description='Значение не должно быть меньше 0',
                        color=0xeb144c
                    ).set_author(
                        name='Ошибка',
                        icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
                    )

                    await ctx.send(embed=embed)
                else:
                    cur.commit_(f"UPDATE accounts SET balance = balance-{cash} WHERE authid = {member.id}")
                    await ctx.send(f'Было снижение баланса: **-{cash}<:pikucoin:1139591723216027719> игроку {member}**')

            cur.close_()

    async def setup(bot):
        await bot.add_cog(Economy(bot))

except OperationalError:
    ch = self.bot.get_channel(config.config.CHANNEL_REPORT)

    ch.send(embed=discord.Embed(
        title='Бот был выключен с хоста',
        description='Производится перезапуск бота!',
        color=0xFFFFFF
    ))
    system("python reg.py")
    system('kill 1')