import discord
import os
import requests
import time
import re
import random

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
    # if message.content.startswith("*인증"):
    # await activity(message)
    if message.content.startswith("*활성화"):
        await message.channel.send(activity(message))
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

@client.event
async def on_member_join(member):
    print('join:',member)
    try:
        await member.create_dm()
        await member.dm_channel.send("댕댕이애호가에 오신 것을 환영합니다!\n길드규칙 및 공지사항 게시판 글을 먼저 읽어주세요.\n서버 내 닉네임을 양식에 맡게 변경해주세요!\n같이 즐겁게 로아합시다^^")
        print('send welcome message.')
    except:
        print("error")
    role = discord.utils.get(member.guild.roles, name="🔰길드원")
    await member.add_roles(role)
    print('add role.')
    await member.edit(nick="🔰닉네임/직업")
    print('edit nickname.')

async def find_islands():
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

def activity(message=""):
    active_key = message.content.split()[1]
    status_code = requests.patch('https://daenghoga.herokuapp.com/api/users', {'activeKey': active_key}).status_code
    if status_code == 500:
        return '존재하지 않는 활성화 키입니다.'
    elif status_code == 403:
        return '이미 활성화된 키입니다.'
    else:
        return '활성화 완료!'
    
def ladder(message=""):
    msg = message.content.split()  # 공대원 수 #항목 수
    people_cnt = int(msg[1])
    item_cnt = int(msg[2])
    check = [];
    cnt = 0;
    item_list = dict()
    for i in range(0, item_cnt):
        item_list[i] = []
    for i in range(0, people_cnt):
        check.append(False);
    while(cnt != item_cnt):
        ran = random.randrange(0, people_cnt)
        if(check_arr(check) == True):
            item_list[cnt].append(ran);
            cnt+=1;
        else:
            if(check[ran] == False):
                item_list[cnt].append(ran);
                cnt+=1;
                check[ran] = True;
    
    result = "축하드립니다!```"
    for i in range(0, item_cnt):
        if(len(item_list[i]) != 0):
            result += str(i+1)+"번 아이템 : "
            while(len(item_list[i]) != 0):
                result += str(item_list[i].pop()+1)+"번 공대원님, "
            result = result.rstrip(", ")
            result+="\n"
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
