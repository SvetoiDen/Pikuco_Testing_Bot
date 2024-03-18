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

try:
    class Model_Role(ui.Modal, title='Создание уникальной роли'):
        name_r = ui.TextInput(label='Введите название вашей уникальной роли', placeholder='Введи название...', style=discord.TextStyle.short)
        hex_r = ui.TextInput(label='Введите HEX (цвет) вашей роли', placeholder='Пример: 0xffffff', style=discord.TextStyle.short)

        async def on_submit(self, inter: Interaction):
            cur = BD_Bot()

            await inter.response.defer(thinking=True, ephemeral=True)
            row = cur.get_(f"SELECT * FROM shop WHERE id = 1")

            server = inter.user.guild
            role = await server.create_role(name=str(self.name_r), color=discord.Colour.from_str(str(self.hex_r)))
            await role.edit(position=21)
            await inter.user.add_roles(role)

            cur.commit_(f"UPDATE accounts SET balance = balance - {row['cost']} WHERE id = {inter.user.id}")
            cur.commit_(f"UPDATE accounts SET shop_1 = 1 WHERE id = {inter.user.id}")

            await inter.edit_original_response('Ваша роль была создана!')

            cur.close_()

    async def buy_1(bal, cost, inter: Interaction):
        try:
            cur = BD_Bot()
            if bal > cost:
                row = cur.get_(f"SELECT shop_1 FROM accounts WHERE id = {inter.user.id}")
                if row['shop_1'] == 1:
                    await inter.response.send_message('Извините, но вы уже приобрели свою уникальную роль', ephemeral=True)
                else:
                    await inter.response.send_modal(Model_Role())
            else:
                await inter.response.send_message('У вас недостаточно средств на счету', ephemeral=True)
            cur.close_()

        except OperationalError:
            ch = await self.bot.get_channel(config.config.CHANNEL_REPORT)

            await ch.send(embed=discord.Embed(
                title='Бот был выключен с хоста',
                description='Производится перезапуск бота!',
                color=0xFFFFFF
            ))
            system("python reg.py")
            system('kill 1')

    async def buy_2(bal, cost, inter: Interaction):
        try:
            cur = BD_Bot()

            if bal > cost:
                role_1 = discord.utils.get(inter.user.guild.roles, id=921650820498477066)
                role_2 = discord.utils.get(inter.user.guild.roles, id=921650819386994699)
                role_3 = discord.utils.get(inter.user.guild.roles, id=921650818950766623)

                for a in inter.user.roles:
                    if a == role_2:
                        await inter.user.remove_roles(role_2)
                        break
                    elif a == role_3:
                        await inter.user.remove_roles(role_3)
                        break

                cur.commit_(f"UPDATE accounts SET balance = {bal} - {cost} WHERE id = {inter.user.id}")
                cur.commit_(f"UPDATE accounts SET shop_1 = 1 WHERE id = {inter.user.id}")

                await inter.user.add_roles(role_1)
                await inter.response.send_message('Ваша роль была выдана! Теперь, ваш зарабаток с тестов/постов будет увеличен в 2 раза.', ephemeral=True)
            else:
                await inter.response.send_message('У вас недостаточно средств на счету', ephemeral=True)

            cur.close_()

        except OperationalError:
            ch = await self.bot.get_channel(config.config.CHANNEL_REPORT)

            await ch.send(embed=discord.Embed(
                title='Бот был выключен с хоста',
                description='Производится перезапуск бота!',
                color=0xFFFFFF
            ))
            system("python reg.py")
            system('kill 1')

    async def buy_3(bal, cost, inter: Interaction):
        try:
            cur = BD_Bot()
            if bal > cost:
                role_1 = discord.utils.get(inter.user.guild.roles, id=921650820498477066)
                role_2 = discord.utils.get(inter.user.guild.roles, id=921650819386994699)
                role_3 = discord.utils.get(inter.user.guild.roles, id=921650818950766623)

                for a in inter.user.roles:
                    if a == role_1:
                        await inter.user.remove_roles(role_1)
                        break
                    elif a == role_3:
                        await inter.user.remove_roles(role_3)
                        break

                cur.commit_(f"UPDATE accounts SET balance = {bal} - {cost} WHERE id = {inter.user.id}")
                cur.commit_(f"UPDATE accounts SET shop_1 = 1 WHERE id = {inter.user.id}")

                await inter.user.add_roles(role_2)
                await inter.response.send_message('Ваша роль была выдана! Теперь, ваш зарабаток с тестов/постов будет увеличен в 4 раза.', ephemeral=True)
            else:
                await inter.response.send_message('У вас недостаточно средств на счету', ephemeral=True)

            cur.close_()

        except OperationalError:
            ch = await self.bot.get_channel(config.config.CHANNEL_REPORT)

            await ch.send(embed=discord.Embed(
                title='Бот был выключен с хоста',
                description='Производится перезапуск бота!',
                color=0xFFFFFF
            ))
            system("python reg.py")
            system('kill 1')

    async def buy_4(bal, cost, inter: Interaction):
        try:
            cur = BD_Bot()
            if bal > cost:
                role_1 = discord.utils.get(inter.user.guild.roles, id=921650820498477066)
                role_2 = discord.utils.get(inter.user.guild.roles, id=921650819386994699)
                role_3 = discord.utils.get(inter.user.guild.roles, id=921650818950766623)

                for a in inter.user.roles:
                    if a == role_1:
                        await inter.user.remove_roles(role_1)
                        break
                    elif a == role_2:
                        await inter.user.remove_roles(role_2)
                        break

                cur.commit_(f"UPDATE accounts SET balance = {bal} - {cost} WHERE id = {inter.user.id}")
                cur.commit_(f"UPDATE accounts SET shop_1 = 1 WHERE id = {inter.user.id}")

                await inter.user.add_roles(role_3)
                await inter.response.send_message('Ваша роль была выдана! Теперь, ваш зарабаток с тестов/постов будет увеличен в 8 раза.', ephemeral=True)
            else:
                await inter.response.send_message('У вас недостаточно средств на счету', ephemeral=True)

            cur.close_()

        except OperationalError:
            ch = await self.bot.get_channel(config.config.CHANNEL_REPORT)

            await ch.send(embed=discord.Embed(
                title='Бот был выключен с хоста',
                description='Производится перезапуск бота!',
                color=0xFFFFFF
            ))
            system("python reg.py")
            system('kill 1')

    async def eco_profile(member: discord.Member):
        try:
            cur = BD_Bot()
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

            size = (127, 127)

            image = Image.open('config/Frame_1849_2.png')

            url = member.avatar

            r = requests.get(url, stream=True)
            p = Image.open(io.BytesIO(r.content))
            n = p.convert('RGBA')
            m = n.resize((127, 127))
            im = crop(m, size)
            im.putalpha(prepare_mask(size, 4))
            im.save('config/image_output.png', format='png')

            images = Image.open('config/image_output.png')
            image.paste(images, (43, 68), mask=images)

            row = cur.get_(f"SELECT * FROM accounts WHERE id = {member.id}")
            idraw = ImageDraw.Draw(image)
            h = ImageFont.truetype('config/Montserrat-Bold.ttf', size=50)
            a = ImageFont.truetype('config/Montserrat-Regular.ttf', size=35)
            b = ImageFont.truetype('config/Montserrat-Bold.ttf', size=38)
            if member.id == 638003115068751912:
                idraw.text((43, 200), f'Создатель Эко. Пикуко', font=b)
            idraw.text((198, 78), f'{row["name"]}', font=h)
            idraw.text((260, 138), f'{row["authid"]}', font=a)
            idraw.text((737, 20), f'{row["balance"]}', font=b)
            idraw.text((738, 98), f'{row["tests_col"]}', font=b)
            idraw.text((739, 178), f'{row["top_reting"]}', font=b)
            image.save('config/user_card.png')

            cur.close_()

        except OperationalError:
            pass

    async def work_t(inter: Interaction, test: str):
        try:
            cur = BD_Bot()

            rs = cur.get_(f"SELECT link FROM storage_test WHERE id = {inter.user.id}")
            if rs is None:
                role_1 = discord.utils.get(inter.user.guild.roles, id=1146759005667078226)
                role_2 = discord.utils.get(inter.user.guild.roles, id=1146759261771280536)
                role_3 = discord.utils.get(inter.user.guild.roles, id=1146759498304864296)

                headers = {
                    'accept': 'text/template, text/javascript, */*',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46'
                }

                r = requests.get(test, headers=headers)
                soup = bs(r.text, 'html.parser')

                java = soup.find('script', {"id": "testResult"}).text
                file = open('config/jva.json', 'w', encoding='utf-8')
                file.write(java)
                file.close()

                read_f = open('config/jva.json', 'r')
                data = json.load(read_f)

                name = data['AUTHOR_NAME']
                id = int(data['AUTHOR'])

                row = cur.gets_(f"SELECT name, authid FROM accounts WHERE id = {inter.user.id}")
                id1 = row['authid']

                k = int(data['RATING'])
                l = int(data['PASSES'])

                if (name == row['name']) or (id == row['authid']):
                    for a in inter.user.roles:
                        if a == role_1:
                            res = ((k * 1.5) + (l * 0.5)) * 2
                            break
                        elif a == role_2:
                            res = ((k * 1.5) + (l * 0.5)) * 4
                            break
                        elif a == role_3:
                            res = ((k * 1.5) + (l * 0.5)) * 8
                            break
                        else:
                            res = (k * 1.5) + (l * 0.5)

                    cur.commit_(f"UPDATE accounts SET balance = balance + {res} WHERE id = {inter.user.id}")
                    cur.commit_(f"UPDATE accounts SET tests_col = tests_col + 1 WHERE id = {inter.user.id}")
                    cur.commit_(f"INSERT INTO storage_test VALUES ({id1}, {inter.user.id}, '{test}', 0)")

                    cur.close_()
                    return await inter.edit_original_response(content=f'Поздравляю, ваш тест набрал **{k}**<:heartred:988022775463694336> рейтинга и **{l}<:logo:905120503558201426>** прохождении. Ваш заработок составляет **{res}<:pikucoin:1139591723216027719>**!')
                else:
                    cur.close_()
                    return await inter.edit_original_response(content='Извините, но вы отправили не свой тест. Проверьте, правильно ли вы ввели свой никнейм и айди профиля из Pikuco')

            else:
                rows = cur.gets_(f"SELECT link FROM storage_test WHERE id = {inter.user.id}")
                for row in rows:
                    if row['link'] == test:
                        t = test
                        break
                    else:
                        t = 'NO'

                if (test == t):
                    cur.close_()
                    return await inter.edit_original_response(content='Извините, но вы отправляли уже этот тест.')
                elif (t == 'NO'):
                    role_1 = discord.utils.get(inter.user.guild.roles, id=1146759005667078226)
                    role_2 = discord.utils.get(inter.user.guild.roles, id=1146759261771280536)
                    role_3 = discord.utils.get(inter.user.guild.roles, id=1146759498304864296)

                    headers = {
                        'accept': 'text/template, text/javascript, */*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46'
                    }

                    r = requests.get(test, headers=headers)
                    soup = bs(r.text, 'html.parser')

                    java = soup.find('script', {"id": "testResult"}).text
                    file = open('config/jva.json', 'w', encoding='utf-8')
                    file.write(java)
                    file.close()

                    read_f = open('config/jva.json', 'r')
                    data = json.load(read_f)

                    name = data['AUTHOR_NAME']
                    id = int(data['AUTHOR'])

                    row = cur.get_(f"SELECT name, authid FROM accounts WHERE id = {inter.user.id}")
                    id1 = row['authid']

                    k = int(data['RATING'])
                    l = int(data['PASSES'])

                    if (name == row['name']) or (id == row['authid']):
                        for a in inter.user.roles:
                            if a == role_1:
                                res = ((k * 1.5) + (l * 0.5)) * 2
                                break
                            elif a == role_2:
                                res = ((k * 1.5) + (l * 0.5)) * 4
                                break
                            elif a == role_3:
                                res = ((k * 1.5) + (l * 0.5)) * 8
                                break
                            else:
                                res = (k * 1.5) + (l * 0.5)

                        cur.commit_(f"UPDATE accounts SET balance = balance + {res} WHERE id = {inter.user.id}")
                        cur.commit_(f"UPDATE accounts SET tests_col = tests_col + 1 WHERE id = {inter.user.id}")
                        cur.commit_(f"INSERT INTO storage_test VALUES ({id1}, {inter.user.id}, '{test}', 0)")

                        cur.close_()
                        return await inter.edit_original_response(content=f'Поздравляю, ваш тест набрал **{k}**<:heartred:988022775463694336> рейтинга и **{l}<:logo:905120503558201426>** прохождении. Ваш заработок составляет **{res}<:pikucoin:1139591723216027719>**!')
                    else:
                        cur.close_()
                        return await inter.edit_original_response(content='Извините, но вы отправили не свой тест. Проверьте, правильно ли вы ввели свой никнейм и айди профиля из Pikuco')

        except OperationalError:
            ch = await self.bot.get_channel(config.config.CHANNEL_REPORT)

            await ch.send(embed=discord.Embed(
                title='Бот был выключен с хоста',
                description='Производится перезапуск бота!',
                color=0xFFFFFF
            ))
            system("python reg.py")
            system('kill 1')

    async def work_p(inter: Interaction, post: str):
        try:
            cur = BD_Bot()

            rs = cur.get_(f"SELECT link_post FROM storage_test WHERE id = {inter.user.id}")
            if rs is None:
                role_1 = discord.utils.get(inter.user.guild.roles, id=1146759005667078226)
                role_2 = discord.utils.get(inter.user.guild.roles, id=1146759261771280536)
                role_3 = discord.utils.get(inter.user.guild.roles, id=1146759498304864296)

                headers = {
                    'accept': 'text/template, text/javascript, */*',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46'
                }

                r = requests.get(post, headers=headers)
                soup = bs(r.text, 'html.parser')

                java = soup.find('script', {"id": "postResult"}).text
                file = open('config/jva.json', 'w', encoding='utf-8')
                file.write(java)
                file.close()

                read_f = open('config/jva.json', 'r')
                data = json.load(read_f)

                id = int(data['POST']['UF_AUTHOR'])
                name = data['USER']['LOGIN']

                row = cur.get_(f"SELECT name, authid FROM accounts WHERE id = {inter.user.id}")
                id1 = row['authid']

                k = int(data['POST']['UF_RATING'])
                l = int(data['POST']['UF_VIEWS'])

                if (name == row['name']) or (id == row['authid']):
                    for a in inter.user.roles:
                        if a == role_1:
                            res = ((k * 3) + (l * 2)) * 2
                            break
                        elif a == role_2:
                            res = ((k * 3) + (l * 2)) * 4
                            break
                        elif a == role_3:
                            res = ((k * 3) + (l * 2)) * 8
                            break
                        else:
                            res = (k * 3) + (l * 2)

                    cur.commit_(f"UPDATE accounts SET balance = {bal} + {res} WHERE id = {inter.user.id}")
                    cur.commit_(f"UPDATE accounts SET tests_col = {test_col} + 1 WHERE id = {inter.user.id}")
                    cur.commit_(f"INSERT INTO storage_test VALUES ({id1}, {inter.user.id}, 0, '{post}')")

                    cur.close_()
                    return await inter.edit_original_response(content=f'Поздравляю, ваш пост набрал **{k}**<:heartred:988022775463694336> рейтинга и **{l}<:logo:905120503558201426>** просмотра. Ваш заработок составляет **{res}<:pikucoin:1139591723216027719>**!')
                else:
                    cur.close_()
                    return await inter.edit_original_response(content='Извините, но вы отправили не свой тест. Проверьте, правильно ли вы ввели свой никнейм и айди профиля из Pikuco')
            else:
                rows = cur.gets_(f"SELECT link_post FROM storage_test WHERE id = {inter.user.id}")
                for row in rows:
                    if row['link_post'] == post:
                        t = post
                        break
                    else:
                        t = 'NO'

                if (post == t):
                    cur.close_()
                    return await inter.edit_original_response(content='Извините, но вы отправляли уже этот тест.')
                elif (t == 'NO'):
                    role_1 = discord.utils.get(inter.user.guild.roles, id=1146759005667078226)
                    role_2 = discord.utils.get(inter.user.guild.roles, id=1146759261771280536)
                    role_3 = discord.utils.get(inter.user.guild.roles, id=1146759498304864296)

                    headers = {
                        'accept': 'text/template, text/javascript, */*',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46'
                    }

                    r = requests.get(post, headers=headers)
                    soup = bs(r.text, 'html.parser')

                    java = soup.find('script', {"id": "postResult"}).text
                    file = open('config/jva.json', 'w', encoding='utf-8')
                    file.write(java)
                    file.close()

                    read_f = open('config/jva.json', 'r')
                    data = json.load(read_f)

                    id = int(data['POST']['UF_AUTHOR'])
                    name = data['USER']['LOGIN']

                    row = cur.get_(f"SELECT name, authid FROM accounts WHERE id = {inter.user.id}")
                    id1 = row['authid']

                    k = int(data['POST']['UF_RATING'])
                    l = int(data['POST']['UF_VIEWS'])

                    if (name == row['name']) or (id == row['authid']):
                        for a in inter.user.roles:
                            if a == role_1:
                                res = ((k * 3) + (l * 2)) * 2
                                break
                            elif a == role_2:
                                res = ((k * 3) + (l * 2)) * 4
                                break
                            elif a == role_3:
                                res = ((k * 3) + (l * 2)) * 8
                                break
                            else:
                                res = (k * 3) + (l * 2)

                        cur.commit_(f"UPDATE accounts SET balance = balance + {res} WHERE id = {inter.user.id}")
                        cur.commit_(f"UPDATE accounts SET tests_col = tests_col + 1 WHERE id = {inter.user.id}")
                        cur.commit_("INSERT INTO storage_test VALUES ({id1}, {inter.user.id}, 0, '{post}')")

                        cur.close_()
                        return await inter.edit_original_response(content=f'Поздравляю, ваш пост набрал **{k}**<:heartred:988022775463694336> рейтинга и **{l}<:logo:905120503558201426>** просмотра. Ваш заработок составляет **{res}<:pikucoin:1139591723216027719>**!')
                    else:
                        cur.close_()
                        return await inter.edit_original_response(content='Извините, но вы отправили не свой пост. Проверьте, правильно ли вы ввели свой никнейм и айди профиля из Pikuco')

        except OperationalError:
            ch = await self.bot.get_channel(config.config.CHANNEL_REPORT)

            await ch.send(embed=discord.Embed(
                title='Бот был выключен с хоста',
                description='Производится перезапуск бота!',
                color=0xFFFFFF
            ))
            system("python reg.py")
            system('kill 1')

except:
    ch = self.bot.get_channel(config.config.CHANNEL_REPORT)

    ch.send(embed=discord.Embed(title='Бот был выключен с хоста',description='Производится перезапуск бота!',color=0xFFFFFF))
    system("python reg.py")
    system('kill 1')