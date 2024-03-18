from typing import Any
import discord
from discord._types import ClientT
from discord.ext import commands, tasks
from discord.ext.commands import Context
from discord import utils, Interaction, app_commands, ui
from cogs.func_storage.BD_function import BD_Bot
from cogs.func_storage.func_storage import embed_err, embed_err_clans

oa = []
ob = []
oc = []
pp = []
dd = []
users_select = []

class Create_Clan_Modal(ui.Modal, title='Создание вашего сквада'):
    name_clan = ui.TextInput(label='Введите название вашего сквада', placeholder='Важно, чтобы оно не нарушало правило сервера..', style=discord.TextStyle.short, min_length=5, max_length=50)
    des_clam = ui.TextInput(label='Введите описание вашего сквада', placeholder='как пример, напишите оссобеность вашего клана...', style=discord.TextStyle.paragraph, max_length=1000)
    avatar_clam = ui.TextInput(label='Вставьте ссылку аватарки вашего сквада', placeholder='Какая должна быть: https://cdn.discordapp.com/attachments/../example.png', style=discord.TextStyle.paragraph)
    col_people = ui.TextInput(label='Какое макс. число людей будут в вашем скваде?', placeholder='Максимум 100 человек...', style=discord.TextStyle.short)

    async def on_submit(self, inter: Interaction):
        cur = BD_Bot()

        await inter.response.defer(thinking=True, ephemeral=True)
        cr = inter.guild

        category = await cr.create_category(name=f'Уголок {self.name_clan}', position=1)
        channel = await cr.create_text_channel(name=f'чат-{self.name_clan}', category=category, position=1)
        voice = await cr.create_voice_channel(name=f'Войс уголок {self.name_clan}', category=category, position=2)

        role_owner = await cr.create_role(name=f'Создатель клана {self.name_clan}')
        role_zam = await cr.create_role(name=f'Заместитель клана {self.name_clan}')
        role = await cr.create_role(name=f'Участник клана {self.name_clan}')

        await category.set_permissions(target=inter.guild.default_role, read_messages=False)
        await category.set_permissions(target=role_owner, read_messages=True)
        await category.set_permissions(target=role_zam, read_messages=True)
        await category.set_permissions(target=role, read_messages=True)

        await inter.user.add_roles(role_owner)

        cur.commit_(
            f"INSERT INTO clans VALUES ({category.id}, {channel.id}, {voice.id}, "
            f"'{self.name_clan}', '{self.des_clam}', '{self.avatar_clam}' ,{int(str(self.col_people))}, 0, 0, 0, "
            f"{inter.user.id}, 0, {role_owner.id}, "
            f"{role_zam.id}, {role.id})"
        )
        cur.commit_(f"UPDATE accounts SET balance = balance - 10000 WHERE id = {inter.user.id}")

        cur.close_()

        await inter.edit_original_response(content=f'Ваш клан {self.name_clan} был создан! Удачи в развитии!')

class Select_Join(ui.Select):
    def __init__(self):
        super().__init__(placeholder='Выбери нужный тебе клан', max_values=1, min_values=1, options=oa)

    async def callback(self, inter: Interaction):
        await inter.response.defer(thinking=True, ephemeral=True)
        global oa
        cur = BD_Bot()

        row = cur.get_(f"SELECT * FROM clans WHERE id_clan = {int(self.values[0])}")
        channel = discord.utils.get(inter.guild.channels, id=row['id_channel'])
        message = await channel.send(f'Пользователь {inter.user.mention} желает вступить в клан **{row["name_clan"]}**\nПримите его?')
        await message.add_reaction('✅')
        await message.add_reaction('❌')

        cur.commit_(f"INSERT INTO clans_check VALUES ({row['id_clan']}, {inter.user.id})")

        cur.close_()
        oa.clear()
        await inter.edit_original_response(content='Ваше вступление отправлено создателю клана. Ожидайте его потверждения!')

class Clan_Select(ui.Select):
    def __init__(self):
        super().__init__(placeholder='Выбери нужный тебе клан', max_values=1, min_values=1, options=ob)

    async def callback(self, inter: Interaction):
        global ob
        cur = BD_Bot()

        row = cur.get_(f"SELECT * FROM clans WHERE id_clan = {int(self.values[0])}")

        embed = discord.Embed(
            title=f'Клан {row["name_clan"]} - Информация',
            description=f'{row["dis_clan"]}',
            color=0xdceb63
        )
        embed.set_thumbnail(url=row['image'])
        embed.add_field(name='Макс. Число людей', value=row['col_member'])
        embed.add_field(name='Кол-во Участников', value=row['member_clan'])
        embed.add_field(name='Создатель клана', value=discord.utils.get(inter.guild.members, id=row['leader_id']).mention)
        if row['zam_id'] != 0:
            embed.add_field(name='Зам. создателя', value=discord.utils.get(inter.guild.members, id=row['zam_id']).mention)
        else:
            embed.add_field(name='Зам. создателя', value='None')
        embed.add_field(name='Баланс клана', value=row['balance'])
        embed.add_field(name='В топе по кланам', value=row['top'])
        embed.set_footer(text='Если создателя нет, на его место идет зам. Если же нету зама и создателя, клан удаляется. Также, информация о клане будет обновляется раз в один час')

        await inter.response.send_message(embed=embed, ephemeral=True)

        cur.close_()
        ob.clear()

class Select_Clans(ui.Select):
    def __init__(self):
        super().__init__(placeholder='Выберите пользователя', max_values=1, min_values=1, options=users_select)

    async def callback(self, inter: Interaction):
        cur = BD_Bot()
        await inter.response.defer(thinking=True, ephemeral=True)
        global users_select

        row = cur.get_(f"SELECT * FROM clans WHERE leader_id = {inter.user.id}")
        cur.commit_(f"UPDATE clans SET zam_id = {int(self.values[0])} WHERE leader_id = {inter.user.id}")

        users = discord.utils.get(inter.guild.members, id=int(self.values[0]))
        role_zam = discord.utils.get(inter.guild.roles, id=row['id_zam_role'])
        role = discord.utils.get(inter.guild.roles, id=row['id_role'])
        await users.add_roles(role_zam)
        await users.remove_roles(role)

        channel = discord.utils.get(inter.guild.channels, id=row['id_channel'])
        await channel.send(f'<@{users.id}>, вы стали заместителем клана! Поздравляю вас!')
        await inter.edit_original_response(f'<@{users.id}> стал вашим заместителем!')

        users_select.clear()

class Edit_Clan_Name(ui.Modal, title='Изменение имени клана'):
    name = ui.TextInput(label='Введи новое имя клана', min_length=10, max_length=30, style=discord.TextStyle.short)

    async def on_submit(self, inter: Interaction):
        cur = BD_Bot()
        await inter.response.defer(thinking=True, ephemeral=True)
        cur.commit_(f"UPDATE clans SET name_clan = '{str(self.name)}' WHERE leader_id = {inter.user.id}")

        row = cur.get_(f"SELECT * FROM clans WHERE leader_id = {inter.user.id}")

        channel = discord.utils.get(inter.guild.channels, id=row['id_channel'])
        cat = discord.utils.get(inter.guild.categories, id=row['id_clan'])
        voice = discord.utils.get(inter.guild.voice_channels, id=row['id_voice'])

        role = discord.utils.get(inter.guild.roles, id=row['id_role'])
        role_zam = discord.utils.get(inter.guild.roles, id=row['id_zam_role'])
        role_owner = discord.utils.get(inter.guild.roles, id=row['id_owner_role'])

        await cat.edit(name=f'Уголок {str(self.name)}')
        await channel.edit(name=f'чат-{str(self.name)}')
        await voice.edit(name=f'Войс уголок {str(self.name)}')

        await role.edit(name=f'Участник клана {str(self.name)}')
        await role_zam.edit(name=f'Заместитель клана {str(self.name)}')
        await role_owner.edit(name=f'Создатель клана {str(self.name)}')

        await inter.edit_original_response(content=f'Вы изменили название вашего клана на **{str(self.name)}**')
        cur.close_()

class Edit_Clan_Des(ui.Modal, title='Изменение описания клана'):
    des = ui.TextInput(label='Введи новое описание клана', min_length=50, max_length=3000, style=discord.TextStyle.paragraph)

    async def on_submit(self, inter: Interaction):
        cur = BD_Bot()
        cur.commit_(f"UPDATE clans SET dis_clan = '{str(self.des)}' WHERE leader_id = {inter.user.id}")
        await inter.response.send_message(content=f'Вы изменили описание вашего клана на\n**{str(self.des)}**', ephemeral=True)
        cur.close_()

class Edit_Clan_Image(ui.Modal, title='Изменение иконки клана'):
    image = ui.TextInput(label='Введи новую ссылку на иконку клана', placeholder='Какая должна быть: https://cdn.discordapp.com/attachments/../example.png', style=discord.TextStyle.paragraph)

    async def on_submit(self, inter: Interaction):
        cur = BD_Bot()
        cur.commit_(f"UPDATE clans SET image = '{str(self.image)}' WHERE leader_id = {inter.user.id}")
        await inter.response.send_message(content=f'Вы изменили иконку вашего клана на {str(self.image)}', ephemeral=True)
        cur.close_()

class Balance_Modal(ui.Modal):
    def __init__(self, clan: int):
        super().__init__(title='Занесение баланса в клан')
        self.clan = clan

    balance = ui.TextInput(label='Напишите, сколько хотите положить в клан', placeholder='Напишите больше из вашего баланса, заберется все', style=discord.TextStyle.short)

    async def on_submit(self, inter: Interaction):
        id_clan = self.clan
        bal = int(str(self.balance))
        cur = BD_Bot()
        row = cur.get_(f"SELECT * FROM accounts WHERE id = {inter.user.id}")

        if bal < 0:
            cur.close_()
            return await inter.response.send_message('Извините, но у вас нет денег')
        elif bal > row['balance']:
            balic = row['balance']
            cur.commit_(f"UPDATE clans SET balance = balance + {balic} WHERE id_clan = {id_clan}")
            cur.commit_(f"UPDATE accounts SET balance = balance - {balic} WHERE id = {inter.user.id}")
            cur.close_()
            return await inter.response.send_message(f'Вы пополнили баланс клана на **{balic}** пикукоинов', ephemeral=True)
        elif bal < row['balance']:
            cur.commit_(f"UPDATE clans SET balance = balance + {bal} WHERE id_clan = {id_clan}")
            cur.commit_(f"UPDATE accounts SET balance = balance - {bal} WHERE id = {inter.user.id}")
            cur.close_()
            return await inter.response.send_message(f'Вы пополнили баланс клана на **{self.balance}** пикукоинов', ephemeral=True)

class User_Get_Modal(ui.Modal):
    def __init__(self, user: int):
        super().__init__(title='Занесение баланса участников клана')
        self.user = user

    balance = ui.TextInput(label='Сколько денег отправите пользователю?', default='100', placeholder='Превысите баланс клана, спишется все...', style=discord.TextStyle.short)

    async def on_submit(self, inter: Interaction):
        bal = int(str(self.balance))
        cur = BD_Bot()
        row = cur.get_(f"SELECT * FROM clans WHERE leader_id = {inter.user.id}")

        if bal < 0:
            cur.close_()
            return await inter.response.send_message("Извините, но введеный вами баланс не может быть ниже нуля!", ephemeral=True)

        elif bal < row['balance']:
            name = row['name_clan']
            cur.commit_(f"UPDATE accounts SET balance = balance + {bal} WHERE id = {self.user}")
            cur.commit_(f"UPDATE clans SET balance = balance - {bal} WHERE leader_id = {inter.user.id}")
            cur.close_()
            await discord.utils.get(inter.guild.members, id=self.user).send(f"Вам было переведено из баланса клана **{name}** - **{bal}** пикукоинов")
            return await inter.response.send_message(f"Вы перевели пользователю <@{self.user}> **{bal}** пикукоинов из баланса клана", ephemeral=True)

        elif bal > row['balance']:
            name = row['name_clan']
            balan = row['balance']
            cur.commit_(f"UPDATE accounts SET balance = balance + {balan} WHERE id = {self.user}")
            cur.commit_(f"UPDATE clans SET balance = balance - {balan} WHERE leader_id = {inter.user.id}")
            cur.close_()
            await discord.utils.get(inter.guild.members, id=self.user).send(f"Вам было переведено из баланса клана **{name}** - **{balan}** пикукоинов")
            return await inter.response.send_message(f"Вы перевели пользователю <@{self.user}> **{balan}** пикукоинов из баланса клана", ephemeral=True)

class Balance_Select(ui.Select):
    def __init__(self):
        super().__init__(placeholder='Выбери клан', max_values=1, min_values=1, options=oc)

    async def callback(self, inter: Interaction):
        id_clan = int(self.values[0])
        oc.clear()
        await inter.response.send_modal(Balance_Modal(id_clan))

class User_Get_Select(ui.Select):
    def __init__(self):
        super().__init__(placeholder='Выбери пользователя из клана', max_values=1, min_values=1, options=pp)

    async def callback(self, inter: Interaction):
        user_id = int(self.values[0])
        pp.clear()
        await inter.response.send_modal(User_Get_Modal(user_id))

class Leave_Get_Select(ui.Select):
    def __init__(self):
        super().__init__(placeholder='Выбери клан', min_values=1, max_values=1, options=dd)

    async def callback(self, inter: Interaction):
        cur = BD_Bot()
        global dd

        row = cur.get_(f"SELECT * FROM clans WHERE id_clan = {int(self.values[0])}")
        role = discord.utils.get(inter.guild.roles, id=row['id_role'])
        channel = discord.utils.get(inter.guild.channels, id=row['id_channel'])
        await inter.user.remove_roles(role)
        cur.commit_(f"UPDATE clans SET member_clan = member_clan - 1 WHERE id_clan = {int(self.values[0])}")

        await channel.send(f'{inter.user.mention} покинул клан.')
        await inter.response.send_message(f'Вы успешно покинули клан **{row["name_clan"]}**', ephemeral=True)

        dd.clear()
        cur.close_()

class List_View(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Clan_Select())

class Join_View(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Select_Join())

class Users_View(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Select_Clans())

class User_Get_View(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(User_Get_Select())

class Leave_User_View(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Leave_Get_Select())

class Edit_View(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label=None, emoji='📃', style=discord.ButtonStyle.primary)
    async def edit_name(self, inter: Interaction, button: ui.Button):
        await inter.response.send_modal(Edit_Clan_Name())

    @ui.button(label=None, emoji='📑', style=discord.ButtonStyle.primary)
    async def edit_desc(self, inter: Interaction, button: ui.Button):
        await inter.response.send_modal(Edit_Clan_Des())

    @ui.button(label=None, emoji='🌉', style=discord.ButtonStyle.primary)
    async def edit_avatar(self, inter: Interaction, button: ui.Button):
        await inter.response.send_modal(Edit_Clan_Image())

    @ui.button(label=None, emoji='💸', style=discord.ButtonStyle.primary)
    async def get_money_user(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()
        global pp

        row = cur.get_(f"SELECT * FROM clans WHERE leader_id = {inter.user.id}")
        for user in inter.guild.members:
            for role in user.roles:
                if role.id == row['id_owner_role'] or role.id == row['id_zam_role'] or role.id == row['id_role']:
                    pp.append(discord.SelectOption(label=f'{user.name}', value=f'{user.id}'))

        await inter.response.send_message(content='Выбери пользователя, которому хочешь выдать денег. Даже себе.', view=User_Get_View(), ephemeral=True)
        cur.close_()
        pp.clear()

    @ui.button(label=None, emoji='🔻', style=discord.ButtonStyle.primary)
    async def remove_user_zam(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()
        row = cur.get_(f"SELECT * FROM clans WHERE leader_id = {inter.user.id}")
        user = discord.utils.get(inter.guild.members, id=row['zam_id'])
        role = discord.utils.get(inter.guild.roles, id=row['id_zam_role'])
        role_2 = discord.utils.get(inter.guild.roles, id=row['id_role'])
        channel = discord.utils.get(inter.guild.channels, id=row['id_channel'])

        await user.remove_roles(role)
        await user.add_roles(role_2)
        cur.commit_(f"UPDATE clans SET zam_id = 0 WHERE leader_id = {inter.user.id}")
        await channel.send(f'{user.mention}, вы были сняты с должности заместителя клана **{row["name_clan"]}**')
        await inter.response.send_message(f'Вы сняли с должности заместителя {user.mention}', ephemeral=True)

        cur.close_()

class Balance_View(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Balance_Select())

class Button_Clan(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(emoji='0️⃣', style=discord.ButtonStyle.green, row=1)
    async def create_clan_(self, inter: Interaction, button: ui.Button):
        try:
            cur = BD_Bot()

            if cur.get_(f"SELECT balance FROM accounts WHERE id = {inter.user.id}")['balance'] > 10000:
                if not cur.get_(f"SELECT * FROM clans WHERE leader_id = {inter.user.id}")['leader_id'] == inter.user.id:
                    await inter.response.send_modal(Create_Clan_Modal())
                else:
                    await inter.response.send_message('Извините, но вы уже создали клан!', ephemeral=True)
            else:
                await inter.response.send_message(embed=embed_err, ephemeral=True)

            cur.close_()

        except Exception:
            await inter.response.send_message(embed=embed_err, ephemeral=True)

    @ui.button(emoji='3️⃣', style=discord.ButtonStyle.primary, row=2)
    async def list_clan_(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()

        global ob
        try:
            for row in cur.gets_(f"SELECT * FROM clans"):
                ob.append(discord.SelectOption(label=f'{row["name_clan"]}', value=row["id_clan"]))

            await inter.response.send_message('Посмотри информацию о клане', view=List_View(), ephemeral=True)
        except Exception:
            await inter.response.send_message('Кланов нет!', ephemeral=True)

        ob.clear()
        cur.close_()

    @ui.button(emoji='4️⃣', style=discord.ButtonStyle.primary, row=2)
    async def join_clan_(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()

        global oa
        try:
            for row in cur.gets_(f"SELECT * FROM clans"):
                if not inter.user.id == row['leader_id']:
                    for roles in inter.user.roles:
                        if not roles.id == row['id_role']:
                            oa.append(discord.SelectOption(label=f'{row["name_clan"]}', value=row["id_clan"]))

            await inter.response.send_message('К какому клану хочешь вступить?', view=Join_View(), ephemeral=True)
        except Exception:
            await inter.response.send_message('Кланов нет, или вы являйтесь создателем клана, или вы уже вступили в клан!', ephemeral=True)

        oa.clear()
        cur.close_()

    @ui.button(emoji='1️⃣', style=discord.ButtonStyle.green, row=1)
    async def join_zam_(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()
        global users_select

        try:
            for row in cur.gets_(f"SELECT * FROM clans WHERE leader_id = {inter.user.id}"):
                for user in inter.guild.members:
                    for roles in user.roles:
                        if roles.id == row['id_role']:
                            users_select.append(discord.SelectOption(label=user.name, value=user.id))
                        elif roles.id == row['id_zam_role']:
                            continue

            await inter.response.send_message('Выберите из ваших участников заместителя', view=Users_View(), ephemeral=True)

        except Exception:
            await inter.response.send_message(embed=embed_err_clans, ephemeral=True)

        users_select.clear()
        cur.close_()

    @ui.button(emoji='2️⃣', style=discord.ButtonStyle.green, row=1)
    async def edit_clan_(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()

        try:
            row = cur.get_(f"SELECT * FROM clans WHERE leader_id = {inter.user.id}")

            embed = discord.Embed(
                description=f'## Редактирование клана {row["name_clan"]}\n'
                            f'Редактируй свое оформление в клане\n'
                            f'- 📃 - Поменять название клана\n'
                            f'- 📑 - Поменяять описание клана\n'
                            f'- 🌉 - Поменять аватарку клана\n'
                            f'- 💸 - изьять деньги из клана, и передать участнику клана\n'
                            f'- 🔻 - Снять заместителя с его должности',
                color=0xFFD00D
            ).set_author(name=inter.user.name, icon_url=inter.user.avatar)
            embed.set_footer(text='Функции могут дополняться')

            await inter.response.send_message(embed=embed, ephemeral=True, view=Edit_View())

            cur.close_()
        except Exception:
            await inter.response.send_message(embed=embed_err_clans, ephemeral=True)

    @ui.button(emoji='5️⃣', style=discord.ButtonStyle.primary, row=2)
    async def set_balance_(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()
        global oc

        try:
            for row in cur.gets_(f"SELECT * FROM clans"):
                for user in inter.guild.members:
                    for roles in user.roles:
                        if (roles.id == row['id_role'] or roles.id == row['id_owner_role'] or roles.id == row['id_zam_role']) and user.id == inter.user.id:
                            oc.append(discord.SelectOption(label=f'{row["name_clan"]}', value=row["id_clan"]))

            await inter.response.send_message('Выберите клан, в котором вы хотите положить деньги. Вы можете положить любую сумму, но не ниже нуля', ephemeral=True, view=Balance_View())

        except Exception:
            await inter.response.send_message('Вы не вступили в никакой клан!', ephemeral=True)

        oc.clear()
        cur.close_()

    @ui.button(emoji='6️⃣', style=discord.ButtonStyle.primary, row=2)
    async def leave_clan(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()
        global dd

        try:
            for row in cur.gets_(f"SELECT * FROM clans"):
                for role in inter.user.roles:
                    if role.id == row['id_role']:
                        dd.append(discord.SelectOption(label=f'{row["name_clan"]}', value=f'{row["id_clan"]}'))

            await inter.response.send_message('Выберите клан, от которого вы хотите уйти', ephemeral=True, view=Leave_User_View())
        except Exception:
            await inter.response.send_message('Вы не состоите ни в каком клане, или вы являйтесь создателем или замом клана!', ephemeral=True)

        dd.clear()
        cur.close_()

    @ui.button(emoji='7️⃣', style=discord.ButtonStyle.primary, row=2)
    async def top_clans(self, inter: Interaction, button: ui.Button):
        cur = BD_Bot()
        await inter.response.defer(thinking=True, ephemeral=True)

        embed = discord.Embed(
            description='## Топ 10 кланов по балансу\n',
            color=0xFFD00D
        )

        count = 0
        for row in cur.gets_("SELECT * FROM clans ORDER BY balance DESC LIMIT 10"):
            count += 1
            embed.add_field(
                name=f'`{count}`: Клан {row["name_clan"]}',
                value=f'Баланс: {row["balance"]}\nУчастников: {row["member_clan"]}/{row["col_member"]}'
            )

        ro = cur.gets_("SELECT * FROM clans ORDER BY balance DESC")
        embed.set_footer(text=f'Лучший клан: {row["name_clan"]}', icon_url=row['image'])

        await inter.edit_original_response(embed=embed)

class Clans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='клан')
    @commands.is_owner()
    async def clan_list(self, ctx: Context):
        embed = discord.Embed(
            description='## Добро пожаловать в панель по Кланам сервера!\n'
                        'В этой панели есть все нужные и базовые функции для управления и создания клана. Вот несколько из них:\n'
                        '- 0️⃣ - Создайте свой клан (Только один раз). Стоимость создания = **10.000 пикукоинов**\n'
                        '- 1️⃣ - Сделайте участника из вашего клана замом! **(Зам может быть только один, а также у вас должен быть свой клан)**\n'
                        '- 2️⃣ - Редактируйте свой клан, изменив ему имя, описание и иконку. Также можете из баланса клана выдать деньги участнику, или выгнать зама\n'
                        '- 3️⃣ - Просмотрите список имеющийся кланов, и посмотрите на их статистику\n'
                        '- 4️⃣ - Присоеденитесь к клану, если сделали свой выбор. **ВНИМАНИЕ: Только создатель и зам могут вас добавить или не добавить в клан**\n'
                        '- 5️⃣ - Внесите денег из вашего баланса в баланс клана!\n'
                        '- 6️⃣ - Покиньте клан, в котором вы находитесь. Вы можете быть только в двух кланах. **ВНИМАНИЕ, Зам не может покидать клан.**\n'
                        '- 7️⃣ - Просмотрите топ кланов по балансу, и посмотрите, кто крут!',
            color=0xFFD00D
        ).set_footer(text='Функции могут дополняться. С уважением, создатель ДС сервера', icon_url=ctx.author.avatar)
        await ctx.send(embed=embed, view=Button_Clan())

    @commands.command(name='удалить_клан')
    @commands.has_role(1211743965380870226)
    async def delete_clan_(self, ctx: Context, id_clan: int):
        cur = BD_Bot()
        row = cur.get_(f"SELECT * FROM clans WHERE id_clan = {id_clan}")

        await discord.utils.get(ctx.guild.channels, id=row['id_channel']).delete()
        await discord.utils.get(ctx.guild.voice_channels, id=row['id_voice']).delete()
        await discord.utils.get(ctx.guild.roles, id=row['id_owner_role']).delete()
        await discord.utils.get(ctx.guild.roles, id=row['id_zam_role']).delete()
        await discord.utils.get(ctx.guild.roles, id=row['id_role']).delete()
        await discord.utils.get(ctx.guild.categories, id=id_clan).delete()

        cur.commit_(f"DELETE FROM clans WHERE id_clan = {id_clan}")

        await ctx.send('Клан был успешен удален!')

async def setup(bot):
    await bot.add_cog(Clans(bot))