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

@client.event
async def on_ready():
    print(str(client.user.id)+" is ready")
    game = discord.Game("")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    global lst
    guild = message.guild
    if(guild.id != 562910440007532564):
        msg = await message.channel.send('댕댕이애호가 서버에서만 가능합니다. 이 메시지는 곧 삭제됩니다.')
        time.sleep(2)
        await message.delete()
        await msg.delete()
        return
    if message.content.startswith("*인증"):
        await message.channel.send(await authentication(message))
    if message.content.startswith("*활성화"):
        await message.channel.send(activity(message))
    if message.content.startswith("*투표"):
        channel = message.channel
        if(channel.id != 831486216280604672):
            msg = await message.channel.send('봇용 채널에서만 가능합니다. 이 메시지는 곧 삭제됩니다.')
            time.sleep(2)
            await msg.delete()
            return
        await vote(message)
    if message.content.startswith("*몰아주기"):
        channel = message.channel
        if(channel.id != 831486216280604672):
            msg = await message.channel.send('봇용 채널에서만 가능합니다. 이 메시지는 곧 삭제됩니다.')
            time.sleep(2)
            await msg.delete()
            return
        msg = await message.channel.send("몰아주기 결과는?!")
        time.sleep(2)
        await msg.delete()
        await message.channel.send("축하드립니다!```" + roulette(message) + "번 공대원님!```")
    if message.content.startswith("*사다리"):
        channel = message.channel
        if(channel.id != 831486216280604672):
            msg = await message.channel.send('봇용 채널에서만 가능합니다. 이 메시지는 곧 삭제됩니다.')
            time.sleep(2)
            await msg.delete()
            return
        msg = await message.channel.send("사다리타기 결과는?!")
        time.sleep(2)
        await msg.delete()
        await message.channel.send(ladder(message))

async def authentication(message=""):
    member = message.author
    nickname = message.content.split()[1]
    url = 'https://lostark.game.onstove.com/Profile/Character/'+nickname
    response = requests.get(url)
    if response.status_code != 200:
        return '로아 서버 오류!'
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__title > span:nth-child(2)').get_text()
    if title != '계승되는':
        return '서버 인증 실패'
    try:
        await member.send( "댕댕이애호가에 오신 것을 환영합니다!\n길드규칙 및 공지사항 게시판 글을 먼저 읽어주세요.\n서버 내 닉네임을 양식에 맡게 변경해주세요!\n같이 즐겁게 로아합시다^^")
        role = discord.utils.get(member.guild.roles, name="🔰길드원")
        await member.add_roles(role)
        print('add role.')
        await member.edit(nick="🔰닉네임/직업")
        print('edit nickname.')
        return '서버 인증 성공!'
    except Exception:
        return '서버 인증 에러'

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
        if(check_lst[i] == False):
           isFull = False;
           break
    return isFull

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
