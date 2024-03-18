import time
import discord
from urllib.request import urlopen
import re
import asyncio
import lxml
import requests
from bs4 import BeautifulSoup as bs
from discord._types import ClientT
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands, Interaction, ui
import ffmpeg
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
import yt_dlp as youtube_dl
from cogs.func_storage.BD_function import BD_Bot
import os

class Modal_get_Music(ui.Modal, title='Трек'):
    track = ui.TextInput(label='Введите название вашего трека', style=discord.TextStyle.short)

    async def on_submit(self, inter: Interaction):
        cur = BD_Bot()
        await inter.response.defer(thinking=True, ephemeral=True)
        
        def sourse_get():
            options = EdgeOptions()
            options.add_argument('--headless')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0')
            driver = Edge(executable_path='msedgedriver.exe', options=options)

            tr = str(self.track)
            searchs = tr.replace(" ", "+")
            driver.get(url=f"https://www.youtube.com/results?search_query={searchs}")
            r = driver.find_element(By.ID, "video-title").get_attribute('href')
            return r

        cur.commit_(f"INSERT INTO music_list VALUES ({inter.user.id}, '{sourse_get()}', '{str(self.track)}')")
        await inter.edit_original_response(content='Ваша музыка была добавлена')


class Button_Music(ui.View):
    def __init__(self):
        super().__init__()

    @ui.button(label=None, emoji='➕', style=discord.ButtonStyle.primary)
    async def get_music(self, inter: Interaction, button: ui.Button):
        await inter.response.send_modal(Modal_get_Music())

    @ui.button(label=None, emoji='▶️', style=discord.ButtonStyle.primary)
    async def play(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()
        row = cur.get_(f"SELECT * FROM music_list WHERE id_user = {inter.user.id}")
        if row is None:
            return await inter.response.send_message('У вас нету музыки, которую вы добавляли!')

        url = row['link_music']

        song_there = os.path.isfile("song.mp3")

        await inter.response.send_message(content='Загрузка музыки:▇ 0%')

        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        await inter.edit_original_response(content='Загрузка музыки:▇ ▇ ▇ 15%')

        try:
            vc = await inter.user.voice.channel.connect()
        except:
            return await inter.edit_original_response(content='ОШИБКА: Вы не зашли в войс канал')

        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': os.path.realpath('ffmpeg/bin/ffmpeg.exe'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        await inter.edit_original_response(content='Загрузка музыки:▇ ▇ ▇ ▇ ▇ ▇ 45%')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await inter.edit_original_response(content='Загрузка музыки:▇ ▇ ▇ ▇ ▇ ▇ ▇ ▇ 70%')
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")

        await inter.edit_original_response(content='Загрузка музыки:▇ ▇ ▇ ▇ ▇ ▇ ▇ ▇ ▇ ▇ 100%')

        embed = discord.Embed(
            description=f'## Музыка: {row["name_music"]}\n'
                        f'- Заказал: {inter.user.mention}',
            color=0x3AAACF
        )
        embed.set_author(name='DJ Pikuco', icon_url='https://cdn.discordapp.com/attachments/701876665516687431/1217538911727780000/zJ2-sOdCKdA.jpg?ex=66046479&is=65f1ef79&hm=e808495b112b7909efe397728f46d209f2f08b64d1e5e1668bd3940b8c8c1d3d&')
        embed.set_footer(text='Приятного слушания!')

        await inter.edit_original_response(content=None, embed=embed)
        vc.play(discord.FFmpegPCMAudio("song.mp3", executable='ffmpeg/bin/ffmpeg.exe'))

        while vc.is_playing():
            await asyncio.sleep(.1)
        cur.commit_(f"DELETE FROM music_list WHERE link_music = '{url}'")
        await vc.disconnect()

        cur.close_()

    # @ui.button(label=None, emoji='⏸', style=discord.ButtonStyle.primary)
    # async def pause(self, inter: Interaction):
    #     voice = discord.utils.get(self.bot.voice_clients, guild=inter.guild)
    #     if voice.is_playing():
    #         voice.pause()
    #         await inter.response.send_message('Музыка на паузе')
    #     else:
    #         await inter.response.send_message("Currently no audio is playing.")
    #
    #
    # @ui.button(label=None, emoji='▶️', style=discord.ButtonStyle.primary)
    # async def resume(self, inter: Interaction):
    #     voice = discord.utils.get(self.bot.voice_clients, guild=inter.guild)
    #     if voice.is_paused():
    #         voice.resume()
    #         await inter.response.send_message('Музыка продолжился')
    #     else:
    #         await inter.response.send_message("The audio is not paused.")

    @ui.button(label=None, emoji='⏹', style=discord.ButtonStyle.primary)
    async def stop(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()
        voice = inter.user.voice.channel
        voice.stop()
        cur.commit_(f"DELETE FROM music_list WHERE link_music = '{url}' AND WHERE id_user = {inter.user.id}")
        await inter.response.send_message('Музыка убрана из вашего плейлиста')
        await inter.guild.voice_client.disconnect()
        cur.close_()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='музыка')
    async def music_embed(self, ctx: Context):
        embed = discord.Embed(
            title='Музыка',
            description='Музыка, смотри сам!'
        )
        await ctx.send(embed=embed, view=Button_Music())

async def setup(bot):
    await bot.add_cog(Music(bot))