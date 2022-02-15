import discord
import os
import requests
import time
import re
import random
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

lst = dict()
attend_list = dict()

class AuthenticationError(Exception):
    def __str__(self):
        return "길드원 인증에 실패하였습니다. 이 메시지는 곧 삭제됩니다."
    
class BotPermissionError(Exception):
    def __str__(self):
        return "봇 오류가 발생하였습니다. 관리자에게 문의해주세요. 이 메시지는 곧 삭제됩니다."
class ServerError(Exception):
    def __str__(self):
        return "로스트아크 홈페이지 오류가 발생하였습니다. 이 메시지는 곧 삭제됩니다."

@client.event
async def on_ready():
    print(str(client.user.id) + " is ready")
    game = discord.Game("")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_member_join(member):
    await member.send(
            "안녕하세요! [응애들나가신다] 길드에 오신것을 환영합니다.\n길드원 사칭사기 예방 및 길드원 구분을 위해 인증 후 저희 디스코드 채널을 이용하실 수 있습니다.\n\n-[응애들의 공간] 디스코드 서버 인증 방법 안내-```1. 인게임 내 칭호를 '초보 탈출'로 변경\n2. [인증채널]에 [*인증 닉네임]을 작성하면 '새싹🌱 '역할을 부여해 드리고, 디스코드 서버 내 별명을 변경해 드립니다. \n ex) *인증 짱짱쎔 \n3. '새싹'역할을 부여받으신 분은 [길드규정]채널에서 길드 규정 정독 후 하단 병아지  클릭\n4. '길드원'역할 부여 완료!```")

@client.event
async def on_message(message):
    global lst
    channel = message.channel
    try:
        if message.content.startswith("*인증"):
            if (channel.id != 908571168041213992):
                msg = await message.channel.send('서버인증 채널에서만 가능합니다. 이 메시지는 곧 삭제됩니다.')
                time.sleep(2)
                await message.delete()
                await msg.delete()
                return
            msg = await message.channel.send(await authentication(message))
            time.sleep(2)
            await message.delete()
            await msg.delete()
            return
        if message.content.startswith("*활성화"):
            if (channel.id != 941018584262524939):
                msg = await message.channel.send('봇용 채널에서만 가능합니다. 이 메시지는 곧 삭제됩니다.')
                time.sleep(2)
                await msg.delete()
                await message.delete()
                return
            msg = await message.channel.send(activity(message))
            time.sleep(2)
            await message.delete()
            await msg.delete()
            return
    except AuthenticationError as e:
        msg = await message.channel.send(e)
        time.sleep(2)
        await message.delete()
        await msg.delete()
        return
    except ServerError as e:
        msg = await message.channel.send(e)
        time.sleep(2)
        await message.delete()
        await msg.delete()
        return
    except BotPermissionError as e:
        msg = await message.channel.send(e)
        time.sleep(2)
        await message.delete()
        await msg.delete()
        return
    except:
        msg = await message.channel.send('사용법에 맞게 입력해주세요. 이 메시지는 곧 삭제됩니다.')
        time.sleep(2)
        await message.delete()
        await msg.delete()
        return

    if message.content.startswith('*눈사람'):
        await message.channel.send(snowman())
        
    if message.content.startswith("*투표"):
        await vote(message)
        
    if message.content.startswith("*몰아주기"):
        msg = await message.channel.send("몰아주기 결과는?!")
        time.sleep(2)
        await msg.delete()
        await message.channel.send("축하드립니다!```" + roulette(message) + "번 공대원님!```")
    if message.content.startswith("*사다리"):
        msg = await message.channel.send("사다리타기 결과는?!")
        time.sleep(2)
        await msg.delete()
        await message.channel.send(ladder(message))


def snowman():
    string = ".\n"
    string += "\t\t\t\t ┌─┐\n"
    string += "\t\t\t\t │─ |\n"
    string += "\t\t\t┌└─┘┐\n"
    string += "\t\t\t│───│\n"
    string += "\t\t\t└───┘\n"
    string += "\t\t\t/ \t\t\t\t \ \n"
    string += "\t\t\t() ^ \t\t ^  () \n"
    string += "\t\t\t\ \t.  ──. / \n"
    string += "\t\_\ /  \ \t . . . .  /   \ /\_\n"
    string += "\t\t \     {'──'}     /\n"
    string += "\t\t  \  /'──/','\\\\/\n"
    string += "\t\t   /' 0 \t|\t| \ \'\\\n"
    string += "\t\t  |'\t\t   |\t|  \/    | \n"
    string += "\t\t  |'\t0\t \\ │\t  | \n"
    string += "\t\t  |\t0 \t\t\t\t   | \n"
    string += "\t\t  \\ \_\_\_\_\_\_\_\_\_\_\_/ \n"
    return string

async def authentication(message=""):
    member = message.author
    nickname = message.content.split()[1]
    url = 'https://lostark.game.onstove.com/Profile/Character/' + nickname
    response = requests.get(url)
    if response.status_code != 200:
        raise ServerError()
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__title > span:nth-child(2)').get_text()
    guild = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__guild > span:nth-child(2)').get_text()
    nickname = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-character-info > span.profile-character-info__name').get_text()
    className = str(soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-character-info > img')).split('"')[1]

    if guild != '응애들나가신다' or title != '초보 탈출':
        raise AuthenticationError()

    try:
        role = discord.utils.get(member.guild.roles, name="새싹 🌱")
        await member.add_roles(role)
        print('add role.')
        await member.edit(nick=nickname)
        print('edit nickname.')
        return '서버 인증 성공!'
    except:
        raise BotPermissionError()


async def vote(message=""):
    emoji_number = ['1️⃣', '2️⃣', '3️⃣']
    p = re.compile('"(.*?)"')
    msg = p.findall(message.content)
    msg_len = len(msg) - 1
    result = '📊' + '**' + msg[0] + '**' + '\n'
    for i in range(0, msg_len):
        result += '> ' + emoji_number[i] + ' ' + msg[i + 1] + '\n'
    msg = await message.channel.send(result)
    for i in range(0, msg_len):
        await msg.add_reaction(emoji_number[i])


def activity(message=""):
    active_key = message.content.split()[1]
    status_code = requests.patch('https://daenghoga.herokuapp.com/api/users', {'activeKey': active_key}).status_code
    if status_code == 500:
        return '존재하지 않는 활성화 키입니다.'
    elif status_code == 403:
        return '이미 활성화된 키입니다.'
    else:
        return '활성화 완료!'


def roulette(message=""):
    msg = message.content.split()  # 공대원 수
    cnt = int(msg[1])
    return str(random.randrange(1, cnt + 1))


def ladder(message=""):
    msg = message.content.split()  # 공대원 수 #항목 수
    people_cnt = int(msg[1])
    item_cnt = int(msg[2])
    check = []
    cnt = 0
    item_list = dict()
    for i in range(0, item_cnt):
        item_list[i] = []
    for i in range(0, people_cnt):
        check.append(False)
    while (cnt != item_cnt):
        ran = random.randrange(0, people_cnt)
        if (check_arr(check) == True):
            item_list[cnt].append(ran)
            cnt += 1
        else:
            if (check[ran] == False):
                item_list[cnt].append(ran)
                cnt += 1
                check[ran] = True

    result = "축하드립니다!```"
    for i in range(0, item_cnt):
        if (len(item_list[i]) != 0):
            result += str(i + 1) + "번 아이템 : "
            while (len(item_list[i]) != 0):
                result += str(item_list[i].pop() + 1) + "번 공대원님, "
            result = result.rstrip(", ")
            result += "\n"
    result += '```'
    return result


def check_arr(check_lst=[]):
    isFull = True
    for i in range(0, len(check_lst)):
        if (check_lst[i] == False):
            isFull = False
            break
    return isFull

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
