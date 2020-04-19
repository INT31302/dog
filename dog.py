import discord
import os
client = discord.Client()


@client.event
async def on_ready():
    print(str(client.user.id)+" is ready")
    game = discord.Game("테스트")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.content.startswith("/안녕"):
        await message.channel.send("할말")
    if message.content.startswith("/테스트"):
        await message.channel.send("메롱")


@client.event
async def on_member_join(member):
    try:
        await member.create_dm()
        await member.dm_channel.send("댕댕이애호가에 오신 것을 환영합니다! 공지사항 게시판에서 공지사항을 먼저 읽어주세요. 같이 즐겁게 로아합시다^^")
    except:
        print("error")
    role = discord.utils.get(member.guild.roles, name="🔰길드원")
    await member.add_roles(role)

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
