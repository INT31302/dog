import discord
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random
client = discord.Client()

lst = dict()
attend_list = dict()

lst['루스덮밥'] = lst['꿀다람'] = lst['매니저들'] = 1
attend_list['면코튼'] = '루스덮밥'
attend_list['욤욤'] = '꿀다람'
attend_list['오드스(블레이드)'] = '매니저들'

@client.event
async def on_ready():
    print(str(client.user.id)+" is ready")
    game = discord.Game("인사왕 이벤트")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.content.startswith("/눈사람"):
        await message.channel.send(snowman())
    if message.content.startswith("/모험섬"):
        await message.channel.send("잠시만 기다려주세요!")
        await message.channel.send(find_islands())
    if message.content.startswith("/투표"):
        await message.channel.send(vote(message))
    if(message.author.discriminator == '8757'):
        if message.content.startswith("/초기화"):
            lst.clear()
            attend_list.clear()
            await message.channel.send("초기화 되었습니다.")
        if message.content.startswith("/결과"):
            await message.channel.send(printResult())
        if message.content.startswith("/추첨"):
            await message.channel.send(drawLots())


@client.event
async def on_member_join(member):
    try:
        await member.create_dm()
        await member.dm_channel.send("댕댕이애호가에 오신 것을 환영합니다! 공지사항 게시판에서 공지사항을 먼저 읽어주세요. 같이 즐겁게 로아합시다^^  서버 내 닉네임을 양식에 맡게 변경해주세요!")
    except:
        print("error")
    role = discord.utils.get(member.guild.roles, name="🔰길드원")
    await member.add_roles(role)
    await member.edit(nick="🔰닉네임/직업")

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

def find_islands():
    webpage = urlopen("http://loawa.com")
    soup = BeautifulSoup(webpage, "html.parser")
    islands = "```diff\n오늘 모험의 섬은 아래와 같습니다.\n"
    try:
        islands += "" + soup.find(attrs={'class': re.compile('text-lightcyan.*?')}
                                  ).get_text()+"\n"
        for content in soup.find_all(attrs={'class': re.compile('text-wblack tfs.*?')}):
            temp2 = ""
            temp1 = "+ "+content.get_text()
            if(temp1.find("골드") != -1 or temp1.find("실링") != -1 or temp1.find("제련 재료") != -1 or temp1.find("해적 주화") != -1):
                for in_content in content.find_all(attrs={'class': re.compile("text-.*?")}):
                    temp2 += in_content.get_text()+" "
                index = temp1.find(temp2.strip())
                islands += temp1[:index] + '\n- ' + temp2+"\n"
        islands += "```"
        return islands
    except:
        return "오류 발생"

def vote(message=""):
    name = message.content.split()
    tag = message.author.discriminator
    global lst
    global attend_list
    if tag in attend_list:
        return '이미 ' + str(attend_list[tag])+'님을 투표하셨습니다.'
    else:
        attend_list[tag] = name[1]
        if name[1] in lst:
            lst[name[1]] += 1
        else:
            lst[name[1]] = 1
        return "'"+name[1]+"'님을 투표하였습니다."


def printResult():
    global lst
    result = "득표 수\n"
    for k, v in lst.items():
        result += k + '님 ' + str(v) + "표\n"
    return result

def drawLots():
    global attend_list
    r = random.randrange(0, len(attend_list))
    cnt = 0
    result = '추첨결과\n'
    for k in attend_list.keys():
        if(random == r):
            result += '당첨자는 ' + k+"입니다!"
        cnt += 1
    return result

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
