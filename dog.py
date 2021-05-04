import discord
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import re
import random
client = discord.Client()

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
    if message.content.startswith("*모험섬"):
        msg = await message.channel.send("잠시만 기다려주세요!")
        time.sleep(2)
        await msg.delete()
        await message.channel.send(find_islands())
    if message.content.startswith("*투표"):
        await vote(message)
    if message.content.startswith("*몰아주기"):
        msg = await message.channel.send("몰아주기 결과는?!")
        time.sleep(2)
        await msg.delete()
        await message.channel.send("축하드립니다!```"+roulette(message)+"번 공대원님!```")
    if message.content.startswith("*사다리타기"):
        msg = await message.channel.send("사다리타기 결과는?!")
        time.sleep(2)
        await msg.delete()
        await message.channel.send(ladder(message))
    # if message.content.startswith("/이벤트"):
    #     await message.channel.send(voteEvent(message))
    # if(message.author.discriminator == '8757'):
    #     if message.content.startswith("/초기화"):
    #         lst.clear()
    #         attend_list.clear()
    #         await message.channel.send("초기화 되었습니다.")
    #     if message.content.startswith("/결과"):
    #         await message.channel.send(printVoteResult())
    #     if message.content.startswith("/추첨"):
    #         await message.channel.send(drawLots())


@client.event
async def on_member_join(member):
    try:
        await member.create_dm()
        await member.dm_channel.send("댕댕이애호가에 오신 것을 환영합니다! 공지사항 게시판에서 공지사항을 먼저 읽어주세요. 같이 즐겁게 로아합시다^^ 서버 내 닉네임을 양식에 맡게 변경해주세요!")
    except:
        print("error")
    role = discord.utils.get(member.guild.roles, name="🔰길드원")
    await member.add_roles(role)
    await member.edit(nick="🔰닉네임/직업")

def find_islands():
    webpage = urlopen("http://loawa.com")
    soup = BeautifulSoup(webpage, "html.parser")

    islands = "\n오늘 모험의 섬은 아래와 같습니다." + \
        soup.select_one("span.text-theme-0.tfs14").text+"\n```"
    try:
        contents = soup.select(
            'div.row.pl-1.pr-1.pt-0.pb-0.m-0.justify-content-md-center > div.col-6.col-sm-6.col-md-6.col-lg-6.col-xl-4.pl-1.pr-1')
        for content in contents:
            islands += "{:^15}".format(content.select_one('p > strong').text)
        islands += "\n"
        for content in contents:
            islands += "{:^15}".format(content.select_one('span > strong').text)
        islands += "\n"
        islands += "```"
        return islands
    except:
        return "오류 발생"

async def vote(message=""):
    emoji_number = ['1️⃣', '2️⃣', '3️⃣']
    p = re.compile('"(.*?)"')
    msg = p.findall(message.content)
    msg_len = len(msg)-1
    result = '📊'+'**'+msg[0]+'**'+'\n'
    for i in range(0, msg_len):
        result += '> '+emoji_number[i] + ' ' + msg[i+1]+'\n'
    msg = await message.channel.send(result)
    for i in range(0, msg_len):
        await msg.add_reaction(emoji_number[i])
        
def roulette(message=""):
    msg = message.content.split()  # 공대원 수
    cnt = int(msg[1])
    return str(random.randrange(1, cnt+1))

def ladder(message=""):
    msg = message.content.split()  # 공대원 수 #항목 수
    people_cnt = int(msg[1])
    item_cnt = int(msg[2])
    people_lst = dict()
    item_list = []
    for i in range(1, item_cnt+1):
        item_list.append(i)
    for i in range(0, people_cnt):
        people_lst[i] = []
    while(len(item_list) != 0):
        ran = random.randrange(0, people_cnt)
        if(check(people_lst)):
            people_lst[ran].push(item_list.pop())
        else:
            if(people_lst[ran] != 0):
                continue
            people_lst[ran].push(item_list.pop())
    
    result = "축하드립니다!```"
    for i in range(0, people_cnt):
        result += str(i+1)+"번째 공대원님 : "
        for j in range(0, len(people_lst[i])):
            result += str(people_lst[i])+"번 아이템, "
        result.rstrip(", ")
        result+="\n"
    result += '```'
    return result

def check(people_lst=dict()):
    isFull = True
    for i in range(0, len(people_lst)):
        if(people_lst[i] != 0):
           isFull = False;
           break
    return isFull
    
# def printResult():
#     global lst
#     result = "득표 수\n"
#     for k, v in lst.items():
#         result += k + '님 ' + str(v) + "표\n"
#     return result

# def drawLots():
#     global attend_list
#     r = random.randrange(0, len(attend_list))
#     cnt = 0
#     result = '추첨결과\n'
#     for k in attend_list.keys():
#         if(cnt == r):
#             result += '당첨자는 ' + k+"입니다!"
#         cnt += 1
#     return result

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
