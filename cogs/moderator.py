import discord
from discord import app_commands, Interaction
from discord.ext import commands
from cogs.func_storage.BD_function import BD_Bot

class Moderator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='очистить', description='Очистка чата')
    async def clear(self, inter: Interaction, clear_chat: int):
        await inter.response.send_message(f"Очистилось {clear_chat} сообщений, ожидайте!")
        await inter.channel.purge(limit=clear_chat + 1)

    @commands.command(name='reload_member')
    @commands.is_owner()
    async def reload_member_(self, ctx):
        cur = BD_Bot()
        for user in ctx.guild.members:
            mem = cur.get_(f"SELECT * FROM leaderboard WHERE id = {user.id}")
            if mem is None:
                cur.commit_(f"INSERT INTO leaderboard VALUES ({user.id}, '{user.name}', 0, 100, 0, 0)")

        await ctx.message.add_reaction('✅')
        cur.close_()

async def setup(bot):
    await bot.add_cog(Moderator(bot))