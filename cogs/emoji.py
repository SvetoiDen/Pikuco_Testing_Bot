import requests
import lxml
import asyncio
import os, re, aiohttp
from typing import Optional
from bs4 import BeautifulSoup as BS
import discord
from discord.ext import commands
from discord import app_commands, ui

class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='покормить', description='Покорми человека')
    async def feed(self, inter: discord.Interaction, member: discord.Member, reason: str = None):
        if reason is None:
            reason = 'он(она) хочет покормить тебя! Надо же беречь здоровье!'

        tenor_token = "AIzaSyCz3zhcSkHZW3xFini4yKaOZI-u7iH0BkQ"
        ckey = "pikucobot"
        r = requests.get(f"https://tenor.googleapis.com/v2/search?key={tenor_token}&q=feed-anime&client_key={ckey}&random=true").json()
        gif = r['results'][0]['media_formats']['gif']['url']

        embed = discord.Embed(
        color=0x3AAACF
        ).set_image(url=gif)
        embed.set_footer(text="Они покушали)")

        await inter.response.send_message(content=f"{inter.user.mention} накормил {member.mention}, потому что **{reason}**", embed=embed)

    @app_commands.command(name='обнять', description='Обними человека')
    async def hug(self, inter: discord.Interaction, member: discord.Member, reason: str = None):
        if reason is None:
            reason = 'он(она) любит тебя!'

        tenor_token = "AIzaSyCz3zhcSkHZW3xFini4yKaOZI-u7iH0BkQ"
        ckey = "PikucoBot"
        r = requests.get(f"https://tenor.googleapis.com/v2/search?key={tenor_token}&q=hug-anime&client_key={ckey}&random=true").json()
        gif = r['results'][0]['media_formats']['gif']['url']

        embed = discord.Embed(
        color=0x3AAACF
        ).set_image(url=gif)
        embed.set_footer(text="Они обнялись)")

        await inter.response.send_message(content=f"{inter.user.mention} обнял {member.mention}, потому что **{reason}**", embed=embed)

    @app_commands.command(name='поцеловать', description='Поцелуй человека')
    async def kiss(self, inter: discord.Interaction, member: discord.Member, reason: str = None):
        if reason is None:
            reason = 'он(она) очень сильно любит тебя!'

        tenor_token = "AIzaSyCz3zhcSkHZW3xFini4yKaOZI-u7iH0BkQ"
        ckey = "PikucoBot"
        r = requests.get(f"https://tenor.googleapis.com/v2/search?key={tenor_token}&q=kiss-anime&client_key={ckey}&random=true").json()
        gif = r['results'][0]['media_formats']['gif']['url']

        embed = discord.Embed(
        color=0x3AAACF
        ).set_image(url=gif)
        embed.set_footer(text="Они поцеловались)")

        await inter.response.send_message(content=f"{inter.user.mention} поцеловал {member.mention}, потому что **{reason}**", embed=embed)

    @app_commands.command(name='ударить', description='Ударь человека')
    async def kick(self, inter: discord.Interaction, member: discord.Member, reason: str = None):
        if reason is None:
            reason = 'он(она) ударил тебя! Ударь в ответ и ты тоже!'

        tenor_token = "AIzaSyCz3zhcSkHZW3xFini4yKaOZI-u7iH0BkQ"
        ckey = "PikucoBot"
        r = requests.get(f"https://tenor.googleapis.com/v2/search?key={tenor_token}&q=hit-anime&client_key={ckey}&random=true").json()
        gif = r['results'][0]['media_formats']['gif']['url']

        embed = discord.Embed(
        color=0x3AAACF
        ).set_image(url=gif)
        embed.set_footer(text="Подрались.. опять)")

        await inter.response.send_message(content=f"{inter.user.mention} ударил {member.mention}, потому что **{reason}**", embed=embed)

    @app_commands.command(name='дразнить', description='Поиздевайся над человеком')
    async def kick_off(self, inter: discord.Interaction, member: discord.Member, reason: str = None):
        if reason is None:
            reason = 'он(она) поиздевался над твоей беспомощностью!'

        tenor_token = "AIzaSyCz3zhcSkHZW3xFini4yKaOZI-u7iH0BkQ"
        ckey = "PikucoBot"
        r = requests.get(f"https://tenor.googleapis.com/v2/search?key={tenor_token}&q=tease-anime&client_key={ckey}&random=true").json()
        gif = r['results'][0]['media_formats']['gif']['url']

        embed = discord.Embed(
        color=0x3AAACF
        ).set_image(url=gif)
        embed.set_footer(text="Ну обозвали тебя, обзови в ответ)")

        await inter.response.send_message(content=f"{inter.user.mention} подразнил {member.mention}, потому что **{reason}**", embed=embed)

    @app_commands.command(name='убить', description='Убей человека')
    async def kill_(self, inter: discord.Interaction, member: discord.Member, reason: str = None):
        if reason is None:
            reason = 'он(она) убил тебя! Как это жестоко...'

        tenor_token = "AIzaSyCz3zhcSkHZW3xFini4yKaOZI-u7iH0BkQ"
        ckey = "PikucoBot"
        r = requests.get(f"https://tenor.googleapis.com/v2/search?key={tenor_token}&q=kill-anime&client_key={ckey}&random=true").json()
        gif = r['results'][0]['media_formats']['gif']['url']

        embed = discord.Embed(
        color=0x3AAACF
        ).set_image(url=gif)
        embed.set_footer(text="Он убийца)")

        await inter.response.send_message(content=f"{inter.user.mention} убил {member.mention}, потому что **{reason}**", embed=embed)

    @commands.command(name='пожениться')
    async def marry(self, ctx, member: discord.Member):
        message = await ctx.send(f'Желайте ли вы, {member.mention}, жениться на {ctx.author.mention}?')
        await message.add_reaction('✅')
        await message.add_reaction('❌')

        def check(m):
            if member.id == m.user_id:
                return str(m.emoji) == '✅' or str(m.emoji) == '❌'

        try:
            payload = await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=check)
            if str(payload.emoji) == '✅':
                role = discord.utils.get(member.guild.roles, id=1074343102325735534)
                tenor_token = "AIzaSyCz3zhcSkHZW3xFini4yKaOZI-u7iH0BkQ"
                ckey = "PikucoBot"
                r = requests.get(
                    f"https://tenor.googleapis.com/v2/search?key={tenor_token}&q=marry-anime&client_key={ckey}&random=true").json()
                gif = r['results'][0]['media_formats']['gif']['url']

                embed = discord.Embed(
                    color=0x3AAACF
                ).set_image(url=gif)
                embed.set_footer(text="Они поцеловались)")

                await ctx.send(f"{ctx.author.mention} поженился с {member.mention}!\n**Поздравляем Молодожен!**", embed=embed)
                await member.add_roles(role)
                await ctx.author.add_roles(role)
            elif str(payload.emoji) == '❌':
                await ctx.send(f"{member.name} не согласился(")
        except asyncio.TimeoutError:
            embed = discord.Embed(
                description=f'{ctx.author.mention} Время вышло!',
                color=0xeb144c
            ).set_author(
                name='Ошибка',
                icon_url='https://media.discordapp.net/attachments/1175426440066498591/1195456379855573062/icons8--64.png?ex=65b40e83&is=65a19983&hm=110715400b7ff51b96309951ef3b843c61082d3028d8b1b68859839345c4892b&=&format=webp&quality=lossless&width=80&height=80'
            )

            return await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Emoji(bot))