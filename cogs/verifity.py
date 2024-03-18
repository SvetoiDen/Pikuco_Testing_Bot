import time
import discord
from discord import ui, app_commands, Interaction
from discord.ext import commands
from bs4 import BeautifulSoup as BS
import lxml
from mysql import connector
import requests
from os import system
from mysql.connector.errors import OperationalError
from PIL import Image
from cogs.func_storage.func_storage import on_join
from cogs.func_storage.BD_function import BD_Bot

try:
    class Modal_veri(ui.Modal, title='Верификация'):
        id_pikuco =  ui.TextInput(label='Напиши ID пикуко', placeholder='Найти можешь в странице "Топы", введя свой ник...', style=discord.TextStyle.short)
        picture = ui.TextInput(label='Ссылка на скриншот своего профиля Пикуко', placeholder='Какая должна быть: https://cdn.discordapp.com/attachments/../example.png', style=discord.TextStyle.paragraph)

        async def on_submit(self, inter: discord.Interaction):
            cur = BD_Bot()
            await inter.response.defer(thinking=True, ephemeral=True)
            # with open('config/image_verif.png', 'wb') as im:
            #     im.write(requests.get(str(self.picture)).content)

            embed = discord.Embed(
                title=f'Пользователь ждет потверждения или отклонения. Ссылка на его профиль: https://pikuco.ru/profile/{int(str(self.id_pikuco))}/',
                color=0xffffff
            ).set_image(url=str(self.picture))

            channel = discord.utils.get(inter.guild.channels, id=1211215434725199882)

            message = await channel.send(embed=embed)
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            cur.commit_(f"INSERT INTO message_ver VALUES ({message.id}, {inter.user.id}, {int(str(self.id_pikuco))}, '{inter.user.name}')")
            cur.close_()
            await inter.edit_original_response(content='Ваша верификация отправлена на обработку. Ожидайте ~1 минуту. Мы вам сообщим')


    class Veri_Button(ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @ui.button(label='Пройти верификацию', style=discord.ButtonStyle.green, emoji='✅')
        async def verity(self, inter: discord.Interaction, button: ui.Button):
            await inter.response.send_modal(Modal_veri())

    class Verify(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @commands.command(name='верифик')
        async def verify(self, ctx):
            embed = discord.Embed(
                title='Пройди верификацию',
                description='Нажми на кнопку, чтобы пройти верификацию'
            )

            await ctx.send(embed=embed, view=Veri_Button())


    async def setup(bot):
        await bot.add_cog(Verify(bot))

except OperationalError:
    ch = self.bot.get_channel(config.config.CHANNEL_REPORT)

    ch.send(embed=discord.Embed(
        title='Бот был выключен с хоста',
        description='Производится перезапуск бота!',
        color=0xFFFFFF
    ))
    system("python reg.py")
    system('kill 1')