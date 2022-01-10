# -*- coding: utf-8 -*-

a = 1
b = 0

from ast import Bytes
import atexit, shelve, random, time, math, datetime, sys, os, pickle, nacl, numpy, glob, pydub, traceback,\
subprocess, shlex, threading, importlib, requests, unicodedata, tempfile, pyperclip
from logging import exception
from discord.errors import Forbidden
from tokenize import TokenError as TKE

import periodictable as ptb

from io import BytesIO
from PIL import Image

from gtts import gTTS
from gtts.tts import tts_langs as tl

from importlib.machinery import SourceFileLoader as SFL
from faker import Faker
import cryptocode as ccd

import asyncio
from concurrent.futures import ThreadPoolExecutor

from dateutil.parser import ParserError, parse as pt
from humanfriendly import format_timespan as fts

import discord
from discord.ext import commands, tasks
from discord import NotFound

import views

from hgtk.letter import decompose as dcp, compose as cp
from hgtk.exception import NotHangulException as NHE
from hangul_utils import join_jamos as jj

from googletrans import Translator as Ts, LANGUAGES as tlangs

translator = Ts(user_agent = 'Mozilla/5.0')

from capt import acap

from hurry.filesize import size

sys.path.append(r"E:\TOKEN")

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


### LOADING CUSTOM MODULES ###

module = {}

for r, _, __ in os.walk("./_modules/"):
    if r != "./_modules/" and not ("__pycache__" in r):
        module[r.split("/")[-1]] = SFL(r.split("/")[-1], f"{r}/main.py").load_module()

print("로딩된 커스텀 모듈 : {}".format(', '.join(list(module.keys()))))

vard = {}
for v in glob.glob("./pickled_vars/*.pkl"):
    vard[v.split("\\")[-1].split(".")[0]] = pickle.load(open(v, "rb"))

print("로딩된 변수 : {}".format(', '.join(list(vard.keys()))))

### END OF LOADING ###


discord.TextChannel.create_thread = module["utils"].create_thread

intents = discord.Intents.all()
discord.member = True

bot = commands.Bot(command_prefix="&",intents=intents, help_command=None) # 사과
_bot = commands.Bot(command_prefix="&", help_command=None, intents = intents) # 청사과


maF = {"mention_author" : False}

with open("./storage/botdata/landic.pkl",'rb') as f:
    landic = pickle.load(f)
with open("./storage/botdata/pdt.pkl",'rb') as f:
    pdt = pickle.load(f)
enkey = pickle.load(open(r"E:\KEY.KEY", "rb"))

if b:
    with open("./cmds.pkl", "wb") as f:
        pickle.dump({}, f)
with open("./cmds.pkl",'rb') as f:
    cmdl = pickle.load(f)

true = True
false = False

ptable = list(ptb.elements)[1:]

def rq(s:str):
    while ((s.startswith(("'",'"')) and s.endswith(("'",'"')))):
        s = s[1:-1]
    return s

global isInited

global primelist
primelist = list(map(int,open("./storage/botdata/primes.txt", "r").read().split(",")))

global storage
if a:
    with open("./s.pkl", "rb") as f:
        storage = pickle.load(f)
    # print(storage)
else:
    storage = {"guild":{},"user":{}, 'bot':{}}
    storage["bot"]["tpl"] = 400

global tempstorage
tempstorage = {"guild" : {}, "user" : {}}

kf = Faker("ko_KR")

global ut
ut = datetime.datetime.now()

IAA = lambda: requests.get("http://192.168.25.28:5000/alive")

async def aiter(it):
    for i in it:
        yield i

async def aiviter(it):
    for i,v in it:
        yield i,v

async def awhile():
    while 1:
        yield 1

async def anow():
    with ThreadPoolExecutor(1, "AsyncNow") as executor:
        return await asyncio.get_event_loop().run_in_executor(executor, time.time)

async def warn(s, d=None):
    return discord.Embed(
        title = f":warning: {s}",
        description = d,
        color = discord.Colour.red()
    ) if d else discord.Embed(
        title = f":warning: {s}",
        color = discord.Colour.red()
    )

async def complete(s, d=None):
    return discord.Embed(
        title = f":white_check_mark: {s}",
        description = d,
        color = discord.Colour.green()
    ) if d else discord.Embed(
        title = f":white_check_mark: {s}",
        color = discord.Colour.green()
    )

async def autosave():
    global storage
    c = 0
    while 1:
        c += 1
        with open("./s.pkl", "wb") as f:
            pickle.dump(storage,f)
        if c % 5 == 0: print(f"{c}th saved.")
        await asyncio.sleep(60)


async def makestorage(id):
    global storage
    storage["guild"][id] = {"msgcount":0,
        "msgcc":{},
        "msgcu":{},
        "game":{},
        "cmr":{},
        "custom":{
            "welcome":{
            'enabled' : True,
            'title' : "Default",
            'desc' : "Default",
            'color' : 0x00ff00,
            'url' : None,
            'image' : 'Default'
        }, "bye":{
            'enabled' : True,
            'title' : "Default",
            'desc' : "Default",
            'color' : 0x00ff00,
            'url' : None,
            'image' : 'Default'}
        },
        'UserAgreement' : 1,
        "schedules" : [],
        "random" : {"seed" : "{now}"}
        }

async def checkGuild(id):
    global storage
    if not (id in list(storage["guild"].keys())):
        await makestorage(id)
        return 0
    else:
        if not storage["guild"][id]:
            await makestorage(id)
            return 0
    return 1

async def checkUser(id):
    global storage
    if not (id in list(storage["user"].keys())):
        storage["user"][id] = {"cmr" : {}, 'color' : 0, 'game' : {}}
        return 0
    else:
        return 1

async def botKeyCheck(name):
    global storage
    if not name in list(storage["bot"].keys()):
        storage["bot"][name] = None

async def isDir(id, create=True):
    if os.path.isdir(f"./storage/{id}"):
        return 1
    else:
        if create:
            os.mkdir(f"./storage/{id}")
            os.mkdir(f"./storage/{id}/cs")
        return 0

async def subj(name):
    if ord(name[-1]) in range(ord("가"), ord("힣")+1):
        if dcp(name[-1])[2]: return True
        else: return False

async def srl(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

async def cmdd():
    return {"name" : '',
            "syntax" : '',
            "alias" : [],
            "desc" : '',}
            
async def captstr(len, space=False):
    st = """산모퉁이를 돌아 논가 외딴 우물을 홀로 찾아가선 가만히 들여다봅니다 우물 속에는 달이 밝고 구름이 흐르고 하늘이 펼치고 파아란 바람이 불고 가을이 있습니다 그리고 한 사나이가 있습니다 어쩐지 그 사나이가 미워져 돌아갑니다 돌아가다 생각하니 그 사나이가 가엾어집니다. 도로 가 들여다보니 사나이는 그대로 있습니다 다시 그 사나이가 미워져 돌아갑니다 돌아가다 생각하니 그 사나이가 그리워집니다 우물 속에는 달이 밝고 구름이 흐르고 하늘이 펼치고 파아란 바람이 불고 가을이 있고 추억처럼 사나이가 있습니다"""
    return ''.join(random.sample(st.split(" "), len)) if not space else ' '.join(random.sample(st.split(" "), len))

async def tonum(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return None

async def toint(n):
    try:
        return int(n)
    except:
        return None
mention = lambda u: f"<@!{u}>"

EmojiList = []
@bot.event
async def on_ready():
    import inspect
    global EmojiList
    async for i in aiter(bot.guilds):
        tempstorage["guild"][i.id] = {"game" : {}}
    print(f"사과 - {bot.user}로 로그인됨.")


@bot.event
async def on_guild_join(guild):
    await makestorage(id)
    try:
        async for entry in guild.audit_logs(limit=10):
            if entry.action == discord.AuditLogAction.bot_add:
                if entry.target.id == 902511727147618304:
                    try:
                        await entry.user.send("u invited meh")
                    except discord.Forbidden:
                        pass
                    break
    except discord.Forbidden:
        pass

@bot.event
async def on_member_join(member):
    await checkGuild(member.guild.id)
    if storage["guild"][member.guild.id]["custom"]["welcome"]["enabled"]:
        emb = discord.Embed(
            title = storage["guild"][member.guild.id]["custom"]["welcome"]["title"].format(member=member)
            if storage["guild"][member.guild.id]["custom"]["welcome"]["title"] != "Default"
            else f"안녕하세요, {member}님!",
            description = storage["guild"][member.guild.id]["custom"]["welcome"]["desc"]\
                .format(member=member,time=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                if storage["guild"][member.guild.id]["custom"]["welcome"]["desc"] != "Default"
                else f"{member.guild} 서버에 오신 것을 환영합니다!",
            color = storage["guild"][member.guild.id]["custom"]["welcome"]["color"],
        ).set_image(url = 
            storage["guild"][member.guild.id]["custom"]["welcome"]["image"] if 
            storage["guild"][member.guild.id]["custom"]["welcome"]["image"] != "Default"
            else r"https://cdn.discordapp.com/attachments/906784867285610506/906784905571205150/Defaultwelcome.jpg"
        )
        for i in member.guild.text_channels:
            if i.topic:
                if "#사과봇-인사" in i.topic:
                        await i.send(embed = emb)
class ReturnException(Exception):
    pass

@bot.event
async def on_message(message : discord.Message):
    global storage
    pc = 1
    ctx = message.channel



    try:
        msgl = shlex.split(message.content, posix=False)
    except:
        msgl = message.content.split(" ")

    await checkUser(message.author.id)

    if message.guild:
        await checkGuild(message.guild.id)
    elif message.author.id != 902511727147618304:
        if "arith" in list(storage["user"][message.author.id]["game"].keys()):
            if (storage["user"][message.author.id]["game"]["arith"]["sentnum"] == False):
                gid = storage["user"][message.author.id]["game"]["arith"]["id"]
                added = storage["guild"][gid]["game"]["arith"]["added"]
                if await tonum(message.content) != None:
                    storage["guild"][gid]["game"]["arith"]["strg"]\
                           [storage["user"][message.author.id]["game"]["arith"]["team"]]["nums"].append(await tonum(message.content))
                    storage["user"][message.author.id]["game"]["arith"]["num"] = await tonum(message.content)
                    co = await discord.utils.get(bot.get_guild(id = gid).text_channels,
                                            id = storage["guild"][gid]["game"]["arith"]["strg"]["countmsg"]["c"])\
                                            .fetch_message(id = storage["guild"][gid]["game"]["arith"]["strg"]["countmsg"]["m"])
                    storage["guild"][gid]["game"]["arith"]["sc"] += 1
                    await co.edit(content =  "%d/%d" % (storage["guild"][gid]["game"]["arith"]["sc"], len(storage["guild"][gid]["game"]["arith"]["plrs"])))
                    if storage["guild"][gid]["game"]["arith"]["sc"] == len(storage["guild"][gid]["game"]["arith"]["plrs"]) - int(added):
                        tempstorage["guild"][gid]["arith"]["cw"].set()
                    storage["user"][message.author.id]["game"]["arith"]["sentnum"] == True
                    await message.add_reaction("✅")
                else:
                    message.channel.send("잘못된 숫자입니다!")
        return
    if message.author.id == 902511727147618304: return
    if len(msgl) != 0:
        try:
            if msgl[0] in ["사과야", "ㅅ", "apple"]:
                if not (message.author.id in tempstorage["user"].keys()):
                    tempstorage["user"][message.author.id] = {"ttt" : {"started" : false}, "mjb" : {"started" : false}}
                if len(msgl) == 1:
                    await message.reply(":apple:", mention_author=False)
                    raise ReturnException
                elif msgl[1] == "따라해":
                    await message.reply(' '.join(msgl[2:]), mention_author=False)
                elif msgl[1] == "핑":
                    await message.reply(embed = discord.Embed(
                        title = "현재 핑"
                    ).add_field(
                        name = "`봇`", value = f"```{round(bot.latency*1000)}ms```"
                    ).add_field(
                        name = "`API 서버`", value = "```{}```".format(
                            module["utils"].getapiping()
                        )
                    ).set_footer(
                        text = "🏓 퐁~"
                    )
                    , mention_author=False)
                elif msgl[1].startswith("어디야"):
                    await ctx.send(embed = discord.Embed(
                        title = "저는 지금...",
                        description = "```%s```\n에 있답니다!" % kf.address()
                    ))
                elif msgl[1].startswith("애인"):
                    s = random.choice([
                        "니가 뭘 알아",
                        "당신에게 없는 거요?",
                        "없다고요? 저도 없어요 걱정마세요"
                    ])

                    m = await message.reply(f"**{s}**")
                    await asyncio.sleep(2/3)
                    await m.edit("ㅔ?")

                #1단어 기능

                # 저장공간
                elif msgl[1] in ["저장공간"]:
                    s = size(module["utils"].get_size(f"./storage/{message.guild.id}"))
                    await message.reply(s+"B" + " / 2MB (%d%%)" % ((int(module["utils"].get_size(f"./storage/{message.guild.id}")) / 2000000)*100), **maF)
                
                elif msgl[1] in ["웃어"]:
                    await message.reply(
                        ''.join(random.sample(list("ㅋ"*100 + "ㅎ"*100), random.randint(50, 100)))
                    , **maF)

                #도움말
                elif msgl[1] == "도움말":
                    await message.reply(embed = discord.Embed(
                        title = "여기를 눌러 도움말을 읽으세요.",
                        url = "https://zustfancake.github.io/AppleBot/help"
                    ), **maF)
                
                # 증명
                elif msgl[1] == "hellothisisverification":
                    await message.reply("Pancake # 4788")
                #초대링크
                elif msgl[1] == "초대링크":
                    await message.reply(embed=discord.Embed(
                    title = "여기를 눌러 봇을 초대하세요!",
                    url = "https://discord.com/api/oauth2/authorize?client_id=902511727147618304&permissions=8&scope=applications.commands%20bot"
                    ), **maF)

                # 업타임
                elif msgl[1] == "업타임":
                    tm = (datetime.datetime.now() - ut)
                    try:
                        stm = requests.get("http://192.168.25.28:5000/ut").text
                    except requests.exceptions.ConnectionError:
                        stm = "css\n[정보를 가져올 수 없음]"

                    await message.reply(embed = discord.Embed(
                        title = "업타임 정보"
                    ).add_field(name = "`봇`", value = f"```{fts(int(tm.total_seconds() // 1))}```").add_field(
                        name = "`API 서버`", value = f"```{stm}```"
                    ), **maF)
                # purge
                elif msgl[1] == "핵폭탄":
                    if not message.author.top_role.permissions.administrator:
                        await message.reply(embed = await warn("이 명령을 실행할 권한이 없어요!"))
                        raise ReturnException
                    rs = ''.join(random.sample([i for i in "가나다라마바사아자차카타파하게네데레메베세에제체케테페헤기니디리미비시이지치키티피히고노도로모보소오조초코토포호구누두루무부수우주추쿠투푸후"], 6))
                    cap = discord.File(fp = await acap(rs), filename = "nuke.png")
                    await message.reply(embed = discord.Embed(
                        title = "경고!",
                        description = f"이 명령어는 **이 채널을 완전히 삭제**한 후, 다시 개설합니다.\n이 명령을 실행함으로써 생기는 피해는 본인에게 있습니다.\n계속 진행하시려면 이미지에 있는 글자를 입력해주세요.",
                        color = 0xff0000
                    ).set_image(url = f"attachment://{message.guild.id}nukecapt.png"), file=cap)
                    try:
                        msg = await bot.wait_for("message", check = lambda m : m.content == rs and m.channel == message.channel and m.author == message.author, timeout=10)
                    except asyncio.TimeoutError:
                        await message.channel.send("시간 초과로 핵폭탄의 격발이 취소되었습니다.")
                        raise ReturnException

                    nc = await message.channel.clone()
                    author = message.author
                    await message.channel.delete()
                    await nc.send(f"{author.mention} 핵폭탄이 성공적으로 격발되었습니다.")

                elif msgl[1] == "수소폭탄":
                    if not message.author.top_role.permissions.administrator:
                        await message.reply(embed = await warn("이 명령을 실행할 권한이 없어요!"))
                        raise ReturnException
                    rs = ''.join(random.sample([i for i in "가나다라마바사아자차카타파하거너더러머버서어저처커터퍼허구누두루무부수우주추쿠투푸후고노도로모보소오조초코토포호"*2], 9))
                    await acap(rs, message.guild.id, "hdgbomb")
                    cap = discord.File(f"./storage/{message.guild.id}/hdgbomb.png", filename = f"{message.guild.id}hdg.png")

                    await message.reply(embed = discord.Embed(
                        title = "경고!",
                        description = f"이 명령어는 **이 카테고리를 완전히 삭제**한 후, 다시 개설합니다.\n이 명령을 실행함으로써 생기는 피해는 본인에게 있습니다.\n계속 진행하시려면 이미지에 있는 글자를 입력해주세요.",
                        color = 0xff0000
                    ).set_image(url = f"attachment://{message.guild.id}hdg.png"), file=cap)

                    try:
                        msg = await bot.wait_for("message", check = lambda m : m.content == rs and m.channel == message.channel and m.author == message.author, timeout=10)
                    except asyncio.TimeoutError:
                        await message.channel.send("시간 초과로 수소폭탄의 격발이 취소되었습니다.")
                        raise ReturnException
                    
                    author = message.author
                    cat = await message.channel.category.clone()
                    async for i in aiter((message.channel).category.channels):
                        ci = await i.clone()
                        await ci.edit(category=cat)
                        await i.delete()
                    
                    await message.channel.category.delete()
                    
                    async for i in aiter(cat.text_channels):
                        if type(i) == discord.TextChannel and not i.is_news():
                            await i.send(f"{author.mention} 수소폭탄이 성공적으로 격발되었습니다.")
                            break
                #반응
                elif msgl[1] == "사과":
                    await ctx.send(":apple: 아삭!")

                elif msgl[1] == "지워":
                    if message.reference:
                        await message.reference.resolved.delete()
                    else:
                        await message.reply("뭘 지우라는 거죠?")
                
                elif msgl[1].startswith(("고정", "핀")):
                    if message.reference:
                        await message.reference.resolved.pin()
                
                elif msgl[1] == "스탯":
                    await message.reply(embed = module["utils"].hwinfo(), **maF)
                
                #음향
                elif msgl[1].startswith(tuple(landic.keys())) and msgl[1].endswith("로"):
                    if (msgl[2] == "말해") or (msgl[3] in ["라고","이라고"] and msgl[4] == "말해") or (msgl[2].endswith(("라고","이라고")) and msgl[3] == "말해"):
                        await checkUser(message.author.id)
                        lang = landic[msgl[1][:-1]]
                        string = (' ' if msgl[2] == "말해" else '')\
                                .join(msgl[3:] if msgl[2] == "말해" else
                                msgl[2] if not msgl[2].endswith(("라고","이라고")) else
                                await srl(msgl[2], "라고", "") if (msgl[2].endswith("라고") and not msgl[2].endswith("이라고"))
                                else await srl(msgl[2], "이라고", ""))
                        
                        # await ctx.send(string)

                        if not len((string)) > storage['bot']['tpl']:
                            try:
                                t = gTTS(text=str((string)), lang=lang)
                                await isDir(ctx.guild.id)
                                t.save(f"./storage/{ctx.guild.id}/tts-result.mp3")
                                if not discord.utils.get(bot.voice_clients, guild=message.guild):
                                    try:
                                        vc = await message.author.voice.channel.connect()
                                    except AttributeError:
                                        pass                                
                                elif message.author.voice.channel and message.author.voice.channel != message.guild.voice_client.channel:
                                    await message.guild.voice_client.move_to(message.author.voice.channel)
                                    vc = message.guild.voice_client
                                else:
                                    vc = message.guild.voice_client
                                try:
                                    async for i in awhile():
                                        if not vc.is_playing():
                                            break
                                        await asyncio.sleep(.01)
                                except UnboundLocalError:
                                    pass
                            except AttributeError:
                                pass

                            try:
                                if "tpmp" in list(storage["user"][message.author.id].keys()):
                                    vc.play(discord.FFmpegPCMAudio(f"./storage/{ctx.guild.id}/tts-result.mp3", before_options = "-re", 
                                                                    options = "-speed 24  %s" % '-filter:a "asetrate={}"'.format(storage["user"][message.author.id]['tpmp'] )))
                                else:
                                    vc.play(discord.FFmpegPCMAudio(f"./storage/{ctx.guild.id}/tts-result.mp3", before_options = "-re", 
                                                                    options = "-speed 24  %s" % '-filter:a "asetrate={}"'.format(24000)))
                                vc.source = discord.PCMVolumeTransformer(vc.source)
                                if "volume" in list(storage["guild"][ctx.guild.id].keys()):
                                    vc.source.volume = storage["guild"][ctx.guild.id]["volume"]
                                else:
                                    vc.source.volume = 0.5
                                await message.add_reaction("✅")
                            except discord.ClientException:
                                vc = None
                            except UnboundLocalError:
                                pass
                        else:
                            await message.channel.send(embed = await warn("글자 제한 수를 넘겼어요!"))
                            raise ReturnException
                elif msgl[1] in ["목소리", "TTS", 'tts'] and msgl[2] == ["배속", "속도"] and msgl[3].endswith(("로", "으로")) and msgl[4] in ["설정해줘", "해줘", "맞춰줘", "맞춰"]:
                    v = await tonum(msgl[3].replace("배속으로",""))
                    await checkUser(message.author.id)
                    if v != None:
                        if v >= 0.5 and v <= 2.0:
                            storage["user"][message.author.id]['tpmp'] = 24000 * eval(v)
                            await ctx.send(embed = discord.Embed(
                                title = f"tts 배속을 `{v}`배로 설정했어요.",
                                description = "배속은 개인적으로 적용되며, 모든 서버에서 적용돼요.",
                                color = discord.Colour.green()
                            ))
                        else:
                            await ctx.send(embed = await warn("배속은 0.5보다 크거나 같고, 2.0보다 작거나 같아야 해요."))
                elif msgl[1] == "효과음":
                    if f'.\\storage\\soundeff\\%s.mp3' % msgl[2].strip('"') in glob.glob(".\\storage\\soundeff/*"):
                        if msgl[3] == "재생해":
                            sound = msgl[2].strip('"')
                            if not discord.utils.get(bot.voice_clients, guild=message.guild):
                                try:
                                    vc = await message.author.voice.channel.connect()
                                except AttributeError:
                                    pass
                            elif message.author.voice.channel and message.author.voice.channel != message.guild.voice_client.channel:
                                await message.guild.voice_client.move_to(message.author.voice.channel)
                                vc = message.guild.voice_client
                            else:
                                vc = message.guild.voice_client
                            try:
                                async for i in awhile():
                                    if not vc.is_playing():
                                        break
                                    await asyncio.sleep(.01)
                            except UnboundLocalError:
                                pass
                            try:
                                vc.play(discord.FFmpegPCMAudio(f"./storage/soundeff/{sound}.mp3", before_options = "-re", 
                                                                options = "-speed 32  %s" %
                                                                '-filter:a "asetrate={}"'.format(round(pydub.AudioSegment.from_mp3(f'./storage/soundeff/{sound}.mp3').frame_rate))))
                            except:
                                vc.play(discord.FFmpegPCMAudio(f"./storage/soundeff/{sound}.mp3", before_options = "-re", 
                                                                options = "-speed 32  %s" %
                                                                '-filter:a "asetrate={}"'.format(46000)))
                            vc.source = discord.PCMVolumeTransformer(vc.source)
                            if "volume" in list(storage["guild"][ctx.guild.id].keys()):
                                vc.source.volume = storage["guild"][ctx.guild.id]["volume"] * (5/6)
                            else:
                                vc.source.volume = 0.5
                    else:
                        await ctx.send(embed = discord.Embed(
                            title = f":warning: {msgl[2]} 효과음이 없습니다.",
                            description = "개발자에게 연락해서 추가해달라고 할 수도 있습니다.",
                            color = discord.Colour.orange()
                        ))
                elif msgl[1] == "볼륨" and msgl[2].endswith("로") and msgl[3] in ["설정해줘", "맞춰줘", "해줘"]:
                    if not message.author.top_role.permissions.administrator: raise ReturnException
                    v = msgl[2].replace("%",'').replace("로", '')
                    if type(eval(v)) in [int, float]:
                        if eval(v) in range(1,101):
                            storage["guild"][ctx.guild.id]["volume"] = eval(v) / 100
                            await ctx.send(embed = discord.Embed(
                                title = f"볼륨을 `{v}`(으)로 설정했어요!",
                                color = discord.Colour.green()
                            ))
                        else:
                            await message.reply(embed = await warn("볼륨은 0에서 100 사이여야 해요."))

                # 랜덤
                elif msgl[-1].startswith("확률") and dcp(msgl[-2][-1])[2] == "ㄹ":
                    await message.reply(f"%s 확률은 ||%d||%%예요!" % (' '.join(msgl[1:-1]),random.randint(0,100)),mention_author=False)
                elif msgl[1] == "동전":
                    try:
                        b = int(msgl[2])
                    except:
                        pass
                    else:
                        x = random.randint(b // 16, b // 8)
                        y = random.choice([-1, 1])
                        await message.reply(embed = discord.Embed(
                            title = f"동전을 {b}번 던진 결과",
                            description = f"앞면 : {b + (x * (-1 * y))}번\n뒷면 : {b - (x * (-1 * y))}번"
                        ))
                elif msgl[1].endswith(("과", "와")) and (msgl[3] in ["사이의"] and msgl[4] in ["무작위", "랜덤"]) if len(msgl) > 5 else False:
                    x, y = await tonum(await srl (await srl(msgl[1], "와", '') , "과", '')), await tonum(msgl[2])
                    if msgl[5] == "정수":
                        await message.reply(f"> {x}와 {y} 사이의 무작위 정수 : `{random.randint(x, y)}`", **maF)
                    elif msgl[5] == "소수":
                        await message.reply(f"> {x}와 {y} 사이의 무작위 소수 : `{random.uniform(x, y)}`", **maF)
                elif msgl[1] == "랜덤":
                    if msgl[2] == "이름":
                        sex = random.choice([0,1])
                        n = lambda l : l if l else n(l)
                        name = n(kf.last_name()) + (kf.first_name_male() if sex else kf.first_name_female())
                        await message.reply(embed = discord.Embed(
                            title = "랜덤으로 생성된 이름",
                            description = "%s (%s)" % (name, {True:"남",False:"여"}[sex])
                        ), mention_author=False)

                    elif msgl[2] == "멤버":
                        msg = await message.reply(embed = discord.Embed(
                                title = "<a:appleloading:908699735597125643> 멤버를 뽑는 중입니다..."
                            ), mention_author=False)
                        if "-봇포함" in msgl[2:]:
                            su = random.choice(message.guild.members)
                            await asyncio.sleep(1)
                            await msg.edit(embed = discord.Embed(
                                title = "뽑힌 멤버는...",
                                description = f"<@!{su.id}>"
                            ))
                        else:
                            ul = []
                            async for i in aiter(message.guild.members):
                                if not i.bot: ul.append(i)
                            su = random.choice(ul)
                            await asyncio.sleep(1)
                            await msg.edit(embed = discord.Embed(
                                title = "뽑힌 멤버는...",
                                description = f"<@!{su.id}>"
                            ))
                    elif msgl[2] == "문장":
                        if len(msgl) > 3:
                            if msgl[3] == "-섞어":
                                u = (await module["rnds"].randomtxt()).split(" ")
                                random.shuffle(u)
                                await message.reply(embed = discord.Embed(
                                    title = "랜덤으로 생성되고 섞인 문장",
                                    description = "`%s`" % " ".join(u)
                                ), mention_author = False)
                                raise ReturnException
                        await message.reply(embed = discord.Embed(
                            title = "랜덤으로 생성된 문장",
                            description = "`%s`" % await module["rnds"].randomtxt()
                        ), mention_author = False)
                    #
                    elif msgl[2] == "한국어":
                        await message.reply(chr(random.randint(ord("가"),ord("힣"))))
                    elif msgl[2] == "사진":
                        await message.reply("https://picsum.photos/%d/%d" % (300+(random.randint(-10,10)),300+(random.randint(-10,10))),mention_author=False)
                    elif msgl[2] == "주소":
                        await message.reply(embed = discord.Embed(
                                title = "랜덤으로 생성된 주소",
                                description = "%s" % Faker("ko_KR").address()), mention_author= False)
                    elif msgl[2] == "옛한글":
                        await message.reply(file = discord.File(fp=BytesIO(requests.get(f"http://192.168.25.28:5000/ryh").content), filename="yethan.png"), **maF)
                elif msgl[1] == "골라":
                    if len(msgl) > 3:
                        await message.reply(random.choice(msgl[2:]))
                elif msgl[1] == "명언":
                    ws = await module["rnds"].randomwisesay()
                    if "-" in ws:
                        name = "- " + ws.split("-")[-1].lstrip() + " | 이 명언은 @QWER님의 API에서 가져왔습니다."
                        data = ws.split("-")[0].rstrip()
                    else:
                        name = "이 명언은 @QWER님의 API에서 가져왔습니다."
                        data = ws
                    await message.reply(embed = discord.Embed(
                        title = "명언",
                        description = data,
                    ).set_footer(text = name), mention_author = False)
                

                # 날씨
                elif msgl[1] == "일기예보":
                    await message.reply(embed = discord.Embed(
                        title = "일기예보",
                        description = storage["bot"]["weather"]
                        ).set_footer(
                            text = "%s 기준 | 기상청 중기예보 조회서비스 API" % module["weather"].tn()
                        ), **maF)
                        

                # 관리
                elif (msgl[1].startswith("<#") and msgl[1].endswith(">") and msgl[2] == "에서") or (msgl[2] in ["채널에서", "에서"]) if len(msgl) > 2 else false:
                    channel = message.guild.get_channel(int(msgl[1].replace("<#", "").replace(">", ""))) if (msgl[1].startswith("<#") and msgl[1].endswith(">")) else\
                            message.channel if msgl[1] == "이" else "all" if msgl[1] == "모든" else None
                    if channel:
                        if msgl[2] in ["채널에서", "채널의", "에서"]:
                            if msgl[3] == "역할":
                                if msgl[4].startswith("<@&") and msgl[4].endswith(">"):
                                    if msgl[7].startswith("권한을"):
                                        role = message.guild.get_role(int(msgl[4].replace("<@&", '').replace(">", '')))
                                        try:
                                            if channel != "all":
                                                await channel.set_permissions(role, **{vard["permdic"][rq(msgl[6])] : True if msgl[8].startswith(("추가", "허용")) else False})
                                            else:
                                                for i in message.guild.text_channels:
                                                    await i.set_permissions(role, **{vard["permdic"][rq(msgl[6])] : True if msgl[8].startswith(("추가", "허용")) else False})
                                        except KeyError:
                                            await message.reply("> :warning:  권한의 이름이 잘못되었습니다.\n`권한 목록 : %s`" % (
                                            ', '.join(list(vard["permdic"].keys()))
                                            ), **maF)
                            elif msgl[3] in ["유저", "멤버"]:
                                if msgl[4].startswith("<@!") and msgl[4].endswith(">"):
                                    user = bot.get_user(int(msgl[4].replace("<@!", '').replace(">", '')))
                                    try:
                                        if channel != "all":
                                            await channel.set_permissions(user, **{vard["permdic"][rq(msgl[6])] : True if msgl[8].startswith(("추가", "허용")) else False})
                                        else:
                                            for i in message.guild.text_channels:
                                                await i.set_permissions(user, **{vard["permdic"][rq(msgl[6])] : True if msgl[8].startswith(("추가", "허용")) else False})
                                    except KeyError:
                                        await message.reply("> :warning:  권한의 이름이 잘못되었습니다.\n`권한 목록 : %s`" % (
                                            ', '.join(list(vard["permdic"].keys()))
                                        ), **maF)
                    else:
                        await message.reply("> :warning:  채널 지정이 잘못되었습니다.\n`채널 멘션 (사진 참고), '모든 채널', '이 채널'만 가능합니다.`", file = discord.File(
                                r"C:\Users\Dodoh\Desktop\Apple\storage\unknown.png"
                            ), **maF)

                elif msgl[1] == "여기":
                    if len(msgl) == 2:
                        await ctx.send(embed = discord.Embed(
                            description = f"여기는 <#{message.channel.id}>%s예요!"%("이" if await subj(message.channel.name) else '')
                        ))
                    else:
                        if msgl[2] in ["포스트채널","포스트채널로"] and msgl[3] == "설정해":
                            if message.channel.topic:
                                await message.channel.edit(topic = message.channel.topic + " #포스트")
                                pc = 0
                            else:
                                await message.channel.edit(topic = "#포스트")
                                pc = 0
                            await message.delete()
                            await ctx.send(embed = await complete("이 채널을 포스트 채널로 설정했어요!"))
                
                # 채팅 분석
                elif msgl[1] == "채팅분석":
                    l,s,n = list({k: v for k, v in sorted(storage["guild"][ctx.guild.id]["msgcc"].items(), key=lambda item: item[1])[::-1]}.items()), [], 0
                    e = ["first","second","third"]
                    for i in l[:3]:
                        s.append(":{}_place: : <#{}> ({} 건)".format(e[n],i[0],i[1]))
                        n+=1
                    
                    l,u,n = list({k: v for k, v in sorted(storage["guild"][ctx.guild.id]["msgcu"].items(), key=lambda item: item[1])[::-1]}.items()), [], 0
                    e = ["first","second","third"]
                    for i in l[:3]:
                        u.append(":{}_place: : <@{}> ({} 건)".format(e[n],i[0],i[1]))
                        n+=1
                    
                    embed = discord.Embed(
                        title = f"{ctx.guild.name} 서버의 채팅 현황",
                        description = '`총합 채팅 수 : {}`\n\n'.format(storage["guild"][ctx.guild.id]["msgcount"]),
                        colour = discord.Colour.dark_green()
                    ).add_field(
                        name = "채널", value = '\n'.join(s)
                    ).add_field(
                        name = "유저", value = "\n".join(u)
                    )
                    
                    m = await message.reply(embed = discord.Embed(title = "<a:appleloading:908699735597125643> 분석 중..."))
                    await asyncio.sleep(random.uniform(1/9, 2/3))
                    await m.edit(embed = embed)

                # 커뮤니티
                elif msgl[-1] == "달아줘" and msgl[-2] == "반응" and msgl[2] == "단어에":
                    await ctx.send((msgl[1], msgl[3]))

                elif msgl[1] == "번역해":
                    if message.reference:
                        await message.reply(
                            translator.translate(message.reference.resolved.content, dest = "ko").text
                        , **maF)
                elif len(msgl) > 4:
                    if len(msgl) < 6:
                        if msgl[2].endswith(("를", "을")) and msgl[3].startswith(tuple(module["langlib"].kolangd.keys())) and msgl[3].endswith(("로", "으로")) and msgl[4].startswith("번역"):
                            lang = await srl(msgl[3], "으로", "")
                            lang = await srl(lang, "로", "")

                            try:
                                strt = translator.detect(rq(msgl[1]))
                                result = translator.translate(rq(msgl[1]), dest = module["langlib"].kolangd[lang])
                            except KeyError:
                                raise ReturnException

                            await message.reply(embed = discord.Embed(
                                title = f"{msgl[1] if len(rq(msgl[1])) < 32 else '(생략)'}의 번역 결과",
                                description = f"{result.text}\n",
                            ).set_footer(text = (f"출발 언어 : %s -> 목표 언어 : {lang}") % (module['langlib'].rkolangd[strt.lang])) if not all(result.pronunciation if result.pronunciation else [[]]) else
                            discord.Embed(
                                title = f"{msgl[1] if len(rq(msgl[1])) < 32 else '(생략)'}의 번역 결과",
                                description = f"{result.text}\n",
                            ).set_footer(text = f"출발 언어 : %s -> 목표 언어 : {lang} | 발음은 정확하지 않을 수 있습니다." % module['langlib'].rkolangd[strt.lang])
                            .add_field(name = "발음", value = f"{result.pronunciation}\n(%s)" % module['langlib'].prns(module['langlib'].remove_accents(result.pronunciation))
                            .replace("ㅏ", "아").replace("ㅓ", "어").replace("ㅗ", "오").replace("ㅜ", "우").replace("ㅣ", "이").replace("ㅔ", "에"))
                            , mention_author = false)
                
                    elif len(msgl) < 9:
                        if msgl[2] in ["의"] and msgl[3].startswith(("초성", "중성", "종성", "받침")) and msgl[3].endswith(("을", "를")):
                            if msgl[4] == "모두":
                                try:
                                    if msgl[5].strip('"').strip("'") in [_ for _ in "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉㄳㄶㄵㄺㄻㄼㄽㄾㄿㅀㅄㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"] + [""] and msgl[6] in ["로", "으로"] and msgl[7] == "바꿔":
                                        to =  (await srl ( await srl (msgl[3], "을", "") , "를", "")) 
                                        if to == "초성":
                                            await message.reply(''.join([cp(msgl[5].strip('"').strip("'"), *dcp(i)[1:]) if ord(i) in range(ord("가"), ord("힣")+1) else i for i in msgl[1].strip('"').strip("'")])
                                                                , mention_author = False)
                                        elif to == "중성":
                                            await message.reply(''.join([cp(dcp(i)[0], msgl[5].strip('"').strip("'"), dcp(i)[2]) if ord(i) in range(ord("가"), ord("힣")+1) else i for i in msgl[1].strip('"').strip("'")])
                                                                , mention_author = False)
                                        elif to in ["종성", "받침"]:
                                            await message.reply(''.join([cp(*dcp(i)[:2], msgl[5].strip('"').strip("'")) if ord(i) in range(ord("가"), ord("힣")+1) else i for i in msgl[1].strip('"').strip("'")])
                                                                , mention_author = False)
                                except NHE:
                                    await ctx.send("오류네요. >;")
                        elif (msgl[1] in ["한"] and msgl[2] in ["변의", "변에"] and msgl[3] in ["길이가"] and msgl[4].endswith("인")
                                and msgl[5].startswith("정") and msgl[5].endswith(("각형", "각형의")) and msgl[6] in ["넓이"]):
                                s = await srl(msgl[4], "인", '')
                                if (s := await tonum(s)) != None:
                                    pass
                                else:
                                    raise ReturnException
                                
                                m = msgl[5]
                                n = msgl[5].rstrip("정").lstrip("각형의").lstrip("각형")
                                
                                if s == 0:
                                    await message.reply("**답 뻔히 알면서도 나 고생시킬려고 이러는 거 다 압니다.**", **maF)
                                else:
                                    if (n := module["numlib"].decode(n)) != 0:
                                        if n in [0, 1, 2]:
                                            await message.reply("장난하세요?", **maF)
                                        else:
                                            if type(n) == float:
                                                await message.reply("각의 개수가 올바르지 않습니다.", **maF)
                                            else:
                                                a = round((n * (s ** 2)) / (4 * math.tan( (math.pi / n) )),5)
                                                await message.reply(embed = discord.Embed(
                                                    title = f"한 변의 길이가 {s}인 {m} 넓이",
                                                    description = (int if a % 1 == 0 else lambda x : x)(a)) ,**maF)
                    
                elif msgl[1] in ["번역"] and msgl[2] in ["언어"]:
                    await ctx.send('`'+ ', '.join(sorted(list(module['langlib'].kolangd.keys()))) + '`')

                

                # 돈
                elif msgl[1] in ["황금사과", "골든애플"]:
                    await ctx.send("<:applecoin:914850229612851230>")
                elif msgl[1] == "뽑기":
                    if len(msgl) > 2:
                        r = [0, 0, 0, 0, 0, 0]
                        if int(msgl[2]) > 5000: raise ReturnException
                        for i in range(int(msgl[2])):
                            n = random.randint(1, 10000)
                            if n < 2:
                                r[0] += 1
                            elif n < 50:
                                r[1] += 1
                            elif n < 250:
                                r[2] += 1
                            elif n < 1000:
                                r[3] += 1
                            elif n < 5000:
                                r[4] += 1
                            else:
                                r[5] += 1
                        await message.reply(embed = discord.Embed(
                            title = f"{msgl[2]}번 뽑기를 수행한 결과",
                            description = f"```??? : {r[0]}번 ( 0.02% )\n레전더리 : {r[1]}번 ( 0.5% )\n유니크 : {r[2]}번 ( 2.5% )\n에픽 : {r[3]}번 ( 10% )\n레어 : {r[4]}번 ( 50% )\n일반 : {r[5]}번```"
                        ))
                    else:
                        n = random.randint(1, 10000)
                        if n < 2:
                            await message.reply("??? ( 0.02% )", mention_author = False)
                        elif n < 50:
                            await message.reply("레전더리 ( 0.5% )", mention_author = False)
                        elif n < 250:
                            await message.reply("유니크 ( 2.5% )", mention_author = False)
                        elif n < 1000:
                            await message.reply("에픽 ( 10% )", mention_author = False)
                        elif n < 5000:
                            await message.reply("레어 ( 50% )", mention_author = False)
                        else:
                            await message.reply("일반", mention_author = False)
                
                # 공부
                elif msgl[1] == "계산기":
                    emojis = [bot.get_emoji(922087202450722886), bot.get_emoji(922087202241007648), bot.get_emoji(922087202442317834)]
                    v = views.Calculator.CalculatorDropDown(emojis)
                    x = await message.reply("계산기에는 여러 옵션이 있습니다. 하나를 골라주세요.", view = v, **maF)
                elif msgl[1] == "원자번호":
                    n = (await toint(msgl[2]))
                    if n > 0 and n < 119:
                        n = pdt[n]
                        await message.reply(
                            embed = discord.Embed(
                                title = f"**{n[1]}**",
                                description = f"**기호** : {n[0]}\n**{n[3]}주기 {n[2]}족 원소**\n**원자량** : {n[4]}\n**밀도** : {n[5]}\n**녹는점** : {n[6]} K\n**끓는점** : {n[7]} K\n"
                            )
                        )

                elif msgl[1].endswith("의"):
                    if (x := await toint(msgl[1].replace("의", ""))) != None:
                        if msgl[2] in ["거울수", "대칭수"]:
                            mir = lambda x, m : (x, m) if str(x) == str(x)[::-1] else mir(x + int(str(x)[::-1]), m + 1)
                            try:
                                m = mir(x, 0)
                                await message.reply(embed = discord.Embed(
                                    title = f"{x}의 대칭수",
                                    description = f"`{m[0]}`"
                                ).set_footer(text = f"연산 횟수 : {m[1]}"), **maF)
                            except RecursionError:
                                pass
                        elif msgl[2].endswith("제곱근"):
                            try:
                                if (y := await toint(msgl[2].replace("제곱근", ""))) != None:
                                    z = x ** (1 / y); z = z if z % 1 != 0 else int(z); z = (-z, z) if y % 2 == 0 else z
                                    await message.reply(embed = discord.Embed(
                                        title = f"{x}의 %s제곱근" % ({2 : "", 3 : "세", 4 : "네"}[y] if y in [2,3,4] else y),
                                        description = f"{z}"
                                    ), **maF)
                                else:
                                    y = msgl[2].replace("제곱근", "")
                                    d = {'' : 2, "세" : 3, "네" : 4}
                                    if y in list(d.keys()):
                                        z = x ** (1 / d[y]); z = z if z % 1 != 0 else int(z); z = (-z, z) if d[y] % 2 == 0 else z
                                        await message.reply(embed = discord.Embed(
                                        title = f"{x}의 {y}제곱근",
                                        description = f"{z}"
                                        ), **maF)
                            except TypeError:
                                pass
                        elif msgl[2].endswith(("제곱", "승")):
                            if (y := await tonum(msgl[2].replace("제곱", '').replace("승",""))) != None:
                                try:
                                    z = math.pow(x, y)
                                except OverflowError:
                                    z = float("inf")
                                await message.reply(embed = discord.Embed(
                                        title = f"{x}의 %s제곱" % ({2 : "", 3 : "세", 4 : "네"}[y] if y in [2,3,4] else y),
                                        description = f"{z}"
                                    ), **maF)
                            else:
                                y = msgl[2].replace("제곱", '').replace("승","")
                                d = {'' : 2, "세" : 3, "네" : 4}
                                if y in list(d.keys()):
                                    try:
                                        z = math.pow(x, d[y])
                                    except OverflowError:
                                        z = float("inf")
                                    await message.reply(embed = discord.Embed(
                                    title = f"{x}의 {y}제곱",
                                    description = f"{int(z) if z % 1== 0 else z}"
                                    ), **maF)

                elif msgl[1] in ["거울수", "대칭수"]:
                    mir = lambda x, m : (x, m) if str(x) == str(x)[::-1] else mir(x + int(str(x)[::-1]), m + 1)
                    try:
                        m = mir(int(msgl[2]), 0)
                        await message.reply(embed = discord.Embed(
                            title = f"{msgl[2]}의 대칭수",
                            description = f"`{m[0]}`"
                        ).set_footer(text = f"연산 횟수 : {m[1]}"), **maF)
                    except RecursionError:
                        pass
                elif msgl[1] in ["팩토리얼"]:
                    if not int(msgl[2]) > 10000:
                        z = math.factorial(int(msgl[2]))
                        if len(str(z)) > 4096:
                            with tempfile.NamedTemporaryFile(dir = f"./storage/{message.guild.id}", mode = "w", delete=False, suffix = ".txt") as f:
                                f.write(str(z))
                            await message.reply(file = discord.File(f.name), **maF)
                            f.close()
                        else:
                            await message.reply(embed = discord.Embed(
                                    title = f"{msgl[2]}의 팩토리얼",
                                    description = f"`{z}`"
                                ), **maF)
                    else:
                        await message.reply("**나를 암살할 셈이세요?**", **maF)
            
                elif msgl[1] in ["암호화"]:
                    await message.reply(
                        f"`{ccd.encrypt(msgl[2], enkey)}`"
                    , **maF)
                elif msgl[1] in ["복호화"]:
                    await message.reply(
                        f"`{ccd.decrypt(msgl[2], enkey)}`"
                    , **maF)

                # 게임
                elif msgl[1] in ["가위바위보"]:
                    v = views.RockScissorPaper()
                    m = await message.reply("> 가위, 바위... ", view = v)
                    await v.wait()
                    
                    winl = [[0, -1, 1],
                            [1, 0, -1],
                            [-1, 1, 0]]

                    c = random.choice([0, 1, 2])
                    w = winl[v.value][c]

                    await m.edit("> 당신은 %s\n> 저는 %s\n %s" % (
                        ["가위", "바위", "보"][v.value],
                        ["가위", "바위", "보"][c],
                        {-1 : "제가 이겼네요. :D", 0 : "비겼네요.", 1 : "당신이 이겼습니다."}[w]
    ))
                elif msgl[1] in ["틱택토", "ㅌㅌㅌ"]:
                    m = await message.reply("> 이 분과 틱택토를 하실 분을 구해요!", **maF)
                    await m.add_reaction("👍")
                    try:
                        r = await bot.wait_for("reaction_add", check = lambda r, u: (not u.id in [902511727147618304, message.author.id]) and r.emoji == "👍" and r.message == m, timeout = 20)
                    except asyncio.TimeoutError:
                        await m.edit("할 사람이 없네요. >;")
                        raise ReturnException
                    async for i in r[0].users():
                        if i.id not in [902511727147618304, message.author.id]:
                            u = i
                    ttt = views.TicTacToe([message.author, u])
                    await ctx.send("> " + ttt.plrs[0].mention + "의 턴입니다.", view = ttt)
                elif msgl[1] in ["사칙연산", "사칙", "ㅅㅊ"]:
                    aridic = lambda: {"hiring" : False,
                                    "started" : False,
                                    "number" : 0,
                                    "op" : "",
                                    "plrs" : [],
                                    "teams" : [],
                                    "strg" : {},
                                    "botteam": None
                                    }
                    await checkGuild(message.guild.id)
                    if len(msgl) == 2:
                        await message.reply("나중에작성")
                        raise ReturnException
                    if msgl[2] in ["ㅇㄴ"]:
                        if (not "arith" in list(storage["guild"][message.guild.id]["game"].keys())):
                            storage["guild"][message.guild.id]["game"]["arith"] = aridic()
                        storage["guild"][message.guild.id]["game"]["arith"] = aridic()
                        await ctx.send("inited")
                    elif msgl[2] in ["시작해", "시작", "ㅅㅈ"]:

                        rnd = lambda x : int(x) if x % 1 == 0 else x
                        if (not "arith" in list(storage["guild"][message.guild.id]["game"].keys())):
                            storage["guild"][message.guild.id]["game"]["arith"] = aridic()
                        await ctx.send(":1234: 20초 뒤에 사칙연산 게임을 시작합니다.\n`사과야 사칙연산 참여`로 참여하세요.")

                        storage["guild"][message.guild.id]["game"]["arith"]["hiring"] = True
                        await asyncio.sleep(20)
                        storage["guild"][message.guild.id]["game"]["arith"]["hiring"] = False

                        storage["guild"][message.guild.id]["game"]["arith"]["added"] = False

                        if len(storage["guild"][message.guild.id]["game"]["arith"]["plrs"]) % 2 == 1:
                            storage["guild"][message.guild.id]["game"]["arith"]["added"] = True
                            storage["guild"][message.guild.id]["game"]["arith"]["plrs"].append(902511727147618304)

                        await ctx.send(":traffic_light: 팀을 구성하는 중...")
                        async for i in aiter((1,1,1)):
                            random.shuffle(storage["guild"][message.guild.id]["game"]["arith"]["plrs"])
                        
                        plrs = storage["guild"][message.guild.id]["game"]["arith"]["plrs"][:]

                        async for i in aiter(range(len(storage["guild"][message.guild.id]["game"]["arith"]["plrs"]) // 2)):
                            csp = random.sample(plrs, 2)
                            storage["guild"][message.guild.id]["game"]["arith"]["teams"].append(csp)
                            async for j in aiter(csp):
                                plrs.remove(j)

                        storage["guild"][message.guild.id]["game"]["arith"]["number"] = random.randint(-1000,1000)
                        storage["guild"][message.guild.id]["game"]["arith"]["op"] = random.choice(["/","*","-","+"])
                        
                        mention = []
                        tc = 1

                        async for i in aiter(storage["guild"][message.guild.id]["game"]["arith"]["teams"]):
                            storage["guild"][message.guild.id]["game"]["arith"]["strg"][tc] = {"nums" : [], "result" : []}
                            mention.append( "{tc}팀 : {t}, {c}".format(tc = tc, t = f"<@!{i[0]}>" if i[0] != 902511727147618304 else "사과봇",
                                                                                    c = f"<@!{i[1]}>" if i[1] != 902511727147618304 else "사과봇",))
                            async for j in aiter(i):
                                if j == 902511727147618304:
                                    storage["guild"][message.guild.id]["game"]["arith"]["botteam"] = tc
                                else:
                                    storage["guild"][message.guild.id]["game"]["arith"]["strg"][j] =\
                                        {"number" : 0, "team" : tc}
                                    storage["user"][j]["game"]["arith"] = {"sentnum" : False, "id" : message.guild.id, "team" : tc}
                            tc += 1
                        await ctx.send(":handshake: 팀이 구성되었습니다!\n %s" % ' / '.join(mention))
                        await ctx.send("제시된 숫자는 `%d`이며, 연산자는 `%s`입니다. \n**봇의 개인 디엠**으로 숫자를 보내주세요." % (
                                        storage["guild"][message.guild.id]["game"]["arith"]["number"],
                                        {"+":"+", "-":"-", "/":"÷", "*":"×"}[storage["guild"][message.guild.id]["game"]["arith"]["op"]]))

                        tempstorage["guild"][message.guild.id]["arith"] = {"cw" : asyncio.Event(), }
                        storage["guild"][message.guild.id]["game"]["arith"]["sc"] = 0
                        count = await ctx.send("0/%d" % len(storage["guild"][message.guild.id]["game"]["arith"]["plrs"]))
                        storage["guild"][message.guild.id]["game"]["arith"]["strg"]["countmsg"] = {"c" : message.channel.id, "m" : count.id}
                    
                        await tempstorage["guild"][message.guild.id]["arith"]["cw"].wait()

                        th = 0

                        if storage["guild"][message.guild.id]["game"]["arith"]["added"]:
                            prob = lambda x: random.random() < x
                        
                            bt = storage["guild"][message.guild.id]["game"]["arith"]["botteam"]
                            storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"].append(None)
                            random.shuffle(storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"])
                            th = storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"].index(None)

                            if prob(10 / 100):
                                df = 0
                            elif prob(30 / 100):
                                df = random.uniform(-5.0, 5.0)
                            elif prob(50 / 100):
                                df = random.uniform(-10.0, 10.0)
                            else:
                                df = random.uniform(-10000000000000, 10000000000000000)

                            dst = storage["guild"][message.guild.id]["game"]["arith"]["number"] + df

                            if th == 0:
                                o = storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"][1]
                                op = storage["guild"][message.guild.id]["game"]["arith"]["op"]
                                try:
                                    storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"][0] =\
                                        eval("%f - %f" % (dst, o)) if op == "+"\
                                        else eval("%f + %f" % (dst, o)) if op == "-"\
                                        else eval("%f / %f" % (dst, o)) if op == "*"\
                                        else eval("%f * %f" % (dst, o))
                                except ZeroDivisionError:
                                    storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"][0] = 0
                            else:
                                o = storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"][0]
                                op = storage["guild"][message.guild.id]["game"]["arith"]["op"]
                                try:
                                    storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"][1] =\
                                        eval("%f - %f" % (dst, o)) if op == "+"\
                                        else eval("%f + %f" % (dst, o)) if op == "-"\
                                        else eval("%f / %f" % (dst, o)) if op == "*"\
                                        else eval("%f * %f" % (dst, o))
                                except ZeroDivisionError:
                                    storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"][1] = 0
                        
                            await count.edit("%d/%d" % (len(storage["guild"][message.guild.id]["game"]["arith"]["plrs"]), len(storage["guild"][message.guild.id]["game"]["arith"]["plrs"])))
                        
                        await ctx.send(":symbols: 계산 중입니다...")
                        await asyncio.sleep(random.choice([1/3, 2/3, 1]))
                        if storage["guild"][message.guild.id]["game"]["arith"]["added"]:
                            botnum = storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"][0] if not th else storage["guild"][message.guild.id]["game"]["arith"]["strg"][bt]["nums"][1]
                        
                        storage["guild"][message.guild.id]["game"]["arith"]["dfl"] = {}
                        op = storage["guild"][message.guild.id]["game"]["arith"]["op"]

                        async for i in aiter(list(storage["guild"][message.guild.id]["game"]["arith"]["strg"].keys())):
                            if type(i) != int:
                                pass
                            else:
                                try:
                                    f, s = tuple(storage["guild"][message.guild.id]["game"]["arith"]["strg"][i]["nums"])
                                    try:
                                        storage["guild"][message.guild.id]["game"]["arith"]["strg"][i]["result"] =\
                                                eval("%f - %f" % (f, s)) if op == "-"\
                                                else eval("%f + %f" % (f,s)) if op == "+"\
                                                else eval("%f / %f" % (f, s)) if op == "/"\
                                                else eval("%f * %f" % (f, s))
                                        result = storage["guild"][message.guild.id]["game"]["arith"]["strg"][i]["result"]
                                        
                                    except ZeroDivisionError:
                                        storage["guild"][message.guild.id]["game"]["arith"]["strg"][i]["result"] = float("inf")

                                    storage["guild"][message.guild.id]["game"]["arith"]["strg"][i]["resultstr"] =\
                                            "%s %s %s = %s" % (str(rnd(f)), op, str(rnd(s)), str(rnd(result)))
                                    storage["guild"][message.guild.id]["game"]["arith"]["dfl"][i] = abs(result - storage["guild"][message.guild.id]["game"]["arith"]["number"])
                                except KeyError:
                                    pass
                        mindf = min(storage["guild"][message.guild.id]["game"]["arith"]["dfl"].values())
                        winteam = []
                        async for i, v in aiviter(storage["guild"][message.guild.id]["game"]["arith"]["dfl"].items()):
                            
                            if v == mindf:
                                winteam.append(i)
                        
                        res = []
                        async for i in aiter(storage["guild"][message.guild.id]["game"]["arith"]["strg"]):
                            if type(i) != int:
                                pass
                            elif not (i in range(1, len(storage["guild"][message.guild.id]["game"]["arith"]["plrs"])+1)):
                                continue
                            else:
                                n = []
                                async for j in aiter(storage["guild"][message.guild.id]["game"]["arith"]["teams"][i-1]):
                                    n.append ( (f"  <@!{j}> : %s" % str(rnd(storage["user"][j]["game"]["arith"]["num"]))) if j != 902511727147618304 else f"  사과봇 : {botnum}")
                                n = "\n".join(n) + "\n  결과 : `%s`\n  제시된 숫자와의 차이 : %s" %\
                                (storage["guild"][message.guild.id]["game"]["arith"]["strg"][i]["resultstr"], str(storage["guild"][message.guild.id]["game"]["arith"]["dfl"][i]))
                                res.append(f"{i}팀 : \n{n}")
                        await ctx.send(":smile: 결과가 나왔습니다!")
                        await ctx.send("**결과의 계산 순서는 제출한 순서대로 계산됩니다.**\n\n"+'\n\n'.join(res) + "\n\n우승 팀 : %s" % ', '.join(map(str,winteam)))

                        if (not "arith" in list(storage["guild"][message.guild.id]["game"].keys())):
                            storage["guild"][message.guild.id]["game"]["arith"] = aridic()
                        storage["guild"][message.guild.id]["game"]["arith"] = aridic()
                        

                    elif msgl[2] in ["참여", "ㅊㅇ"]:
                        if (not "arith" in list(storage["guild"][message.guild.id]["game"].keys())):
                            storage["guild"][message.guild.id]["game"]["arith"] = aridic()
                        if storage["guild"][message.guild.id]["game"]["arith"]["hiring"]:
                            if not (message.author.id in storage["guild"][message.guild.id]["game"]["arith"]["plrs"]):
                                storage["guild"][message.guild.id]["game"]["arith"]["plrs"].append(message.author.id)
                                await message.reply(f"{message.author.mention}, 게임에 참여되었어요!", mention_author=false)

                elif msgl[1] in ["위아래", "업다운"]:
                    x = random.randint(1, 1000)
                    y = 0
                    u = await message.reply(embed = discord.Embed(description = "1부터 1000 사이의 숫자를 골랐어요. 그 숫자는 무엇일까요?").set_footer(text = "기회는 단 10번!"))
                    for t in range(1,11):
                        b = await bot.wait_for("message", check = lambda m : message.author == m.author and m.channel == message.channel and m.content.startswith("<> "))
                        if x == int(b.content.split(" ")[1]):
                            await ctx.send("정답이예요. :)")
                            raise ReturnException
                        else:
                            if x < int(b.content.split(" ")[1]):
                                await u.delete()
                                u = await b.reply("%d보다 작아요." % int(b.content.split(" ")[1]))
                            else:
                                await u.delete()
                                u = await b.reply("%d보다 커요." % int(b.content.split(" ")[1]))
                        await b.delete()
                    await u.delete()
                    await message.reply("안타깝네요. 제가 생각한 수는 %d였답니다." % x)

                elif msgl[1] == "오목":
                    tempstorage["user"][message.author.id] = {"ttt" : {"started" : false}, "omok" : {"started": False}}

                    if tempstorage["user"][message.author.id]["omok"]["started"]:
                        raise ReturnException

                    tempstorage["user"][message.author.id]["omok"]["plrs"] = [message.author]
                    
                    h = await message.reply("> 이 분과 오목을 하실 분을 찾아요!", mention_author = False)
                    await h.add_reaction("🙋")
                    try:
                        rct = await bot.wait_for("reaction_add", check = lambda r, u : r.message.id == h.id and u != message.author and u.id != 902511727147618304 and r.emoji == "🙋", timeout = 10)
                    except asyncio.TimeoutError:
                        await h.delete()
                        await message.reply("타임 오버네요! ;<")
                        tempstorage["user"][message.author.id]["omok"]["started"] = false
                        raise ReturnException

                    async for i in rct[0].users():
                        if i.id == 902511727147618304: continue
                        tempstorage["user"][message.author.id]["omok"]["plrs"].append(i)
                        break

                    siz = 15

                    await h.delete()
                    random.shuffle(tempstorage["user"][message.author.id]["omok"]["plrs"])
                    tempstorage["user"][message.author.id]["omok"]["ed"] = {"🔘" : tempstorage["user"][message.author.id]["omok"]["plrs"][0],
                                                                        "⚪" : tempstorage["user"][message.author.id]["omok"]["plrs"][1]}
                    tempstorage["user"][message.author.id]["omok"]["omk"] = [[None for i in range(siz)] for j in range(siz)]

                    tempstorage["user"][message.author.id]["omok"]["last"] = "None"

                    rvals =  ({i : v for i,v in enumerate([k for k in "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ"])},
                            {i : v for i,v in enumerate([k for k in "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅒㅔㅖ"])})
                    
                    tempstorage["user"][message.author.id]["omok"]["lastd"] = {"vals" : ()}
                    tempstorage["user"][message.author.id]["omok"]["turn"] = 1
                    try:
                        async for whilewhilewhilewhilewhilewhilewhilewhilewhilewhilewhilewhilewhilewhile in awhile():
                            for e in ["🔘", "⚪"]:
                                m = [''.join([v if v in ["🔘", "⚪"] else '<:blank:913408915075657761>' if "⚪" in tempstorage["user"][message.author.id]["omok"]["omk"][i][j:] or "🔘" in tempstorage["user"][message.author.id]["omok"]["omk"][i][j:] else '' for j, v in enumerate(tempstorage["user"][message.author.id]["omok"]["omk"][i])]) for i in range(0,14)]
                                st = await ctx.send(embed = discord.Embed(description = "{mt}({dol})의 턴입니다.\n\n⬛{ㄱ}{ㄴ}{ㄷ}{ㄹ}{ㅁ}{ㅂ}{ㅅ}{ㅇ}{ㅈ}{ㅊ}{ㅋ}{ㅌ}{ㅍ}{ㅎ}\n".format(dol = e, mt = tempstorage["user"][message.author.id]["omok"]["ed"][e].mention, **module['game'].hed) +
                                            '\n'.join([("{%s}" % v).format(**module['game'].hed) + m[i] for i, v in enumerate([i for i in "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅒㅔㅖ"])]))
                                            .add_field(
                                                name = ("상대가 놓은 곳 : {}".format(tempstorage["user"][message.author.id]["omok"]["last"])) if tempstorage["user"][message.author.id]["omok"]["turn"] > 1 else '​', 
                                                value = ("```{}```".format((await module['game'].geturdl(tempstorage["user"][message.author.id]["omok"]["lastd"]["vals"], rvals))) if tempstorage["user"][message.author.id]["omok"]["turn"] > 1 else '​' )
                                            ))
                                msg = (await bot.wait_for("message", check = lambda m: m.author == tempstorage["user"][message.author.id]["omok"]["ed"][e] and message.channel == m.channel and m.content.startswith(("o> ", "ㅇ> ", "% "))))
                                
                                tempstorage["user"][message.author.id]["omok"]["last"] = msg.content.split(" ")[1][0]
                                if "기권" in msg.content:
                                    raise module['game'].오목_기권
                                vals = ({v : i for i,v in enumerate([k for k in "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ"])}[dcp(msg.content.split(" ")[1][0])[0]],
                                        {v : i for i,v in enumerate([k for k in "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅒㅔㅖ"])}[dcp(msg.content.split(" ")[1][0])[1]])
                                
                                tempstorage["user"][message.author.id]["omok"]["lastd"] = {"vals" : vals}
                                if tempstorage["user"][message.author.id]["omok"]["omk"][vals[1]][vals[0]]:
                                    pass
                                else:
                                    tempstorage["user"][message.author.id]["omok"]["omk"][vals[1]][vals[0]] = e
                                await msg.delete(); await st.delete()

                                tempstorage["user"][message.author.id]["omok"]["turn"] += 1
                                if (await module['game'].is_winner(tempstorage["user"][message.author.id]["omok"]["omk"], e)) : break
                            if (await module['game'].is_winner(tempstorage["user"][message.author.id]["omok"]["omk"], e)) : break
                        
                        m = [''.join([v if v in ["🔘", "⚪"] else '<:blank:913408915075657761>' if "⚪" in tempstorage["user"][message.author.id]["omok"]["omk"][i][j:] or "🔘" in tempstorage["user"][message.author.id]["omok"]["omk"][i][j:] else '' for j, v in enumerate(tempstorage["user"][message.author.id]["omok"]["omk"][i])]) for i in range(0,14)]
                        
                        wf = await module['game'].is_winner(tempstorage["user"][message.author.id]["omok"]["omk"],"🔘")
                        st = await ctx.send(embed = discord.Embed(description = 
                        "{mt}({dol})가 이겼습니다.\n\n⬛{ㄱ}{ㄴ}{ㄷ}{ㄹ}{ㅁ}{ㅂ}{ㅅ}{ㅇ}{ㅈ}{ㅊ}{ㅋ}{ㅌ}{ㅍ}{ㅎ}\n".format(
                            dol = "🔘" if wf else "⚪", mt = tempstorage["user"][message.author.id]["omok"]["ed"]["⚪"].mention if not wf else tempstorage["user"][message.author.id]["omok"]["ed"]["🔘"].mention, **module['game'].hed) +
                                '\n'.join([("{%s}" % v).format(**module['game'].hed) + m[i] for i, v in enumerate([i for i in "ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣㅐㅒㅔㅖ"])])))
                    except module['game'].오목_기권:
                        await ctx.send("기권.")

                    tempstorage["user"][message.author.id]["omok"]["started"] = false
                else:
                    await message.reply(random.choice([
                        "ㅔ?",
                        "ㅔ..?",
                        f"`{msgl[1:]}`요?"
                    ]), **maF)
        except Exception as e:
            if type(e) == ReturnException:
                pass
            else:
                raise e
            
    if storage["guild"][message.guild.id]["UserAgreement"] == False and message.content.startswith("&"):
        if message.content == "&이용약관":
            if message.author.top_role.permissions.administrator:
                if not message.author.id == message.guild.owner.id:
                    h = "\n\n**서버 주인이 아닌 다른 관리자가 이용 약관에 대신 동의합니다. 서버 주인은 언제든지 동의를 파기할 권리를 가지고 있습니다.**"
                else:
                    h = ''
                await message.channel.send(embed = discord.Embed(
                title = "사과봇 이용 약관",
                description = f"```아 몰라 나중에 작성할래```\n이용 약관에 동의하신다면 '이용 약관에 동의합니다.'를 입력해주세요.{h}"
                ))
                def check(m):
                    return m.content == '이용 약관에 동의합니다.' and m.channel == message.channel and m.author == message.author
                msg = await bot.wait_for('message', check=check)
                if msg:
                    storage["guild"][message.guild.id]["UserAgreement"] = True
                    await message.channel.send(embed = await complete("동의 처리가 되었습니다!"))
                return
            else:
                await message.channel.send(embed = await warn("관리자 권한이 없습니다!"))
                return
        await message.channel.send(embed = await warn("이용 약관에 동의하지 않으셨습니다.", "`&이용약관 동의`을 입력해서 동의 절차를 밟아주세요."))
        return
    if not ("msgcount" in list(storage["guild"][message.guild.id].keys())):
        storage["guild"][message.guild.id]["msgcount"] = 0
    storage["guild"][message.guild.id]["msgcount"] += 1
    if not (("msgcc" in list(storage["guild"][message.guild.id].keys()))):
        storage["guild"][message.guild.id]["msgcc"] = {}
    if not (message.channel.id in list(storage["guild"][message.guild.id]["msgcc"].keys())):
        storage["guild"][message.guild.id]["msgcc"][message.channel.id] = 0
    if not (message.author.id in list(storage["guild"][message.guild.id]["msgcu"].keys())):
        storage["guild"][message.guild.id]["msgcu"][message.author.id] = 0

    storage["guild"][message.guild.id]["msgcc"][message.channel.id] += 1
    storage["guild"][message.guild.id]["msgcu"][message.author.id] += 1


    if not message.content.startswith("&"):
        async for i in aiter(list(storage["guild"][message.guild.id]["cmr"].keys())):
            if i in message.content:
                for j in storage["guild"][message.guild.id]["cmr"][i]:
                    await message.add_reaction(j)
    if not (message.channel.topic is None):
        if "#포스트" in message.channel.topic and pc:
            a = discord.Embed(
                title = f"{message.author}님의 포스트",
                description = f"{message.content}"
            )
            if message.attachments: a.set_image(url = message.attachments[0])
            await message.channel.send(embed = a)
            await message.delete()
    await bot.process_commands(message)

@bot.is_owner
@bot.command()
async def adddata(ctx, name, value = None):
    for i in list(storage["user"].keys()):
        storage["user"][i][name] = eval(value)
    await ctx.send("done")

@bot.event
async def on_voice_state_update(self, member, after):
    if member.channel is not None:
        voice_state = member.channel.guild.voice_client
        if voice_state is not None and len(voice_state.channel.members) == 1:
            await voice_state.disconnect()

@bot.command()
async def rfc(ctx, *, m):
    g = bot.get_channel(906207770603311144)
    await g.send(m)

@bot.is_owner
@bot.command(name = "eq")
async def oooo(ctx, *, b):
    b = b.replace('+', "%2B")
    await ctx.send(requests.get(f"http://192.168.25.28:5000/soloeq?eq={b}").content.decode("utf-8"))

@bot.command()
async def getp(ctx, id:int):
    x = (await bot.fetch_user(id)).avatar_url
    await ctx.send(x)
@bot.command()
async def prns(ctx, *, s):
    await ctx.send(module["langlib"].prns(s))
@bot.command()
async def rcmd(ctx, name, syntax, alias, desc):
    global cmdl
    c = await cmdd()
    c["syntax"] = syntax
    c["alias"] = alias
    c["desc"] = desc
    cmdl[name] = c
    with open("./cmds.pkl", "wb") as f:
        pickle.dump(cmdl, f)

@bot.is_owner
@bot.command(aliases=["exec"])
async def execute(ctx,*,e):
    try:
        exec(e,globals(),locals())
    except:
        await ctx.send(embed = discord.Embed(
            title = ":warning: 오류 발생!",
            description = traceback.format_exc(),
            color = 0xff0000
        ))
        return
    await ctx.send(embed = discord.Embed(
        title = ":white_check_mark: 오류 없이 성공적으로 실행되었습니다!",
        color = discord.Colour.green()
    ))

@bot.command()
async def lae(ctx):
    x = await ctx.channel.fetch_message(913384616554004491)
    print(x.content)
@bot.command()
async def initguild(ctx):
    storage["guild"][ctx.guild.id] = {"msgcount":0, "msgcc":{}, "game":{}, "cmr":{}, "custom":{"welcome":{}, "bye":{}}}

@bot.command()
async def botg(ctx):
    for i in bot.guilds:
        await ctx.send(i.name)


class Develop(commands.Cog, name="개발"):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name="checkstorage", aliases=["chstrg"])
    async def chstrg(self, ctx):
        if len(f"{storage}") > 4000:
            with open("./storage/strg.txt", "w", encoding = "UTF-8") as f:
                f.write(f"{storage}")
            await ctx.send(file = discord.File("./storage/strg.txt"))
        else:
            await ctx.send(embed = discord.Embed(
                description = f"{storage}"
            ))

class Management(commands.Cog, name="관리"):
    def __init__(self, bot):
        self.bot = bot

    async def wait_until(self, dt):
        now = datetime.datetime.now()
        await asyncio.sleep((dt - now).total_seconds())

    async def save(gid, t, do, obj, *arg):
        global storage
        storage["guild"][gid]["schedules"].append ( {
                    'do' : do,
                    'obj' : obj,
                    'arg' : arg,
                    't' : t.strftime("%m/%d/%Y, %H:%M:%S")
                    } )

    @commands.command(name="schedule", aliases=["sched", "스케줄"])
    async def sched(self, ctx, dt:str, do=None, obj=None, *arg):
        global storage

        if len(storage["guild"][ctx.guild.id]["schedules"]) > 4:
            await ctx.send(embed = await warn("한 서버(길드)당 최대 스케줄 개수는 5개입니다."))
            return
        try:
            t = pt(dt)
        except ParserError:
            await ctx.send(embed = await warn("올바른 시간 형식이 아닙니다."))
            return
        
        n = (t - datetime.datetime.now()).total_seconds()
        if n > 86400:
            await ctx.send(embed = await warn(f"스케줄 기간은 1일이 최대입니다. ( {n} / 86400 [초] )"))
            return
        

        # 이제 채널 삭제 만들기
        if do == "삭제" or do == "delete" or do == "del":
            if obj == "channel" or obj == "채널":
                c = discord.utils.get(ctx.guild.text_channels, id=int(arg[0]))
                if c:
                    #await self.save(ctx.guild.id, t, do, obj, arg)
                    await ctx.send(embed = await complete(f"채널을 찾았습니다! \n\n 채널은 {t}에 삭제됩니다."))
                    await self.wait_until(t)
                    await c.delete()
                else:
                    await ctx.send(embed = await warn(f"아이디가 {arg[0]}인 채널이 없습니다."))
            elif obj == "category" or obj == "카테고리":
                c = discord.utils.get(ctx.guild.categories, id = int(arg[0]))
                if c:
                    if "--keepchannels" in arg or "--kc" in arg or "--채널보존" in arg:
                        await ctx.send(embed = await complete(f"{t}에 카테고리 {c}을(를) 삭제합니다.", "카테고리에 있던 채널들은 삭제되지 않습니다."))
                        await self.wait_until(t)
                        try:
                            await c.delete()
                        except NotFound:
                            await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 실행하지 못했습니다.",
                                description = f"예약된 작업 : `id가 {arg[0]}인 카테고리의 삭제 (채널 보존)`\n시간 : `{t}`\n실패 사유 : `카테고리가 이미 삭제되었습니다.`",
                                color = discord.Colour.red()
                            ))
                        else:
                            await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 성공적으로 실행했습니다.",
                                description = f"예약된 작업 : `id가 {arg[0]}인 카테고리의 삭제 (채널 보존)`\n시간 : `{t}`",
                                color = discord.Colour.green()
                            ))
                    else:
                        await ctx.send(embed = await complete(f"{t}에 카테고리 {c}을(를) 삭제합니다.", "카테고리에 있던 채널들도 함께 삭제됩니다."))
                        await self.wait_until(t)
                        try:
                            for i in c.channels:
                                try:
                                    await i.delete()
                                except AttributeError:
                                    pass
                            await c.delete()
                        except NotFound:
                            await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 실행하지 못했습니다.",
                                description = f"예약된 작업 : `id가 {arg[0]}인 카테고리의 삭제`\n시간 : `{t}`\n실패 사유 : `카테고리가 이미 삭제되었습니다.`",
                                color = discord.Colour.red()
                            ))
                        else:
                            await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 성공적으로 실행했습니다.",
                                description = f"예약된 작업 : `id가 {arg[0]}인 카테고리의 삭제`\n시간 : `{t}`",
                                color = discord.Colour.green()
                            ))
            elif obj == "message" or obj == "msg":
                e = await ctx.send(embed = discord.Embed(
                    title = "<a:load:906221997514706996> 메시지를 찾는 중입니다."
                ))
                for v,i in enumerate(ctx.guild.text_channels):
                    try:
                        m = await bot.http.get_message(i.id, int(arg[0]))
                    except NotFound:
                        m = None
                    if m:
                        c = i
                        break
                    else:
                        if round((v / len(ctx.guild.text_channels)) * 100) % 10 == 0:
                            await e.edit(embed = discord.Embed(
                        title = f"<a:load:906221997514706996> 메시지를 찾는 중입니다.\n\n{round((v / len(ctx.guild.text_channels)) * 100)}% [{i}]"
                ))
                if m:
                    await e.delete()
                    await ctx.send(embed = await complete(f"메시지를 찾았습니다! \n\n 메시지는 {t}에 삭제됩니다."))
                    await self.wait_until(t)
                    try:
                        msg = await c.fetch_message(int(m["id"]))
                    except NotFound:
                        await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 실행하지 못했습니다.",
                                description = f"예약된 작업 : `id가 {arg[0]}인 메시지의 삭제`\n시간 : `{t}`\n실패 사유 : `메시지가 이미 삭제되었습니다.`",
                                color = discord.Colour.red()
                            ))
                        return
                    try:
                        await msg.delete()
                    except NotFound:
                        await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 실행하지 못했습니다.",
                                description = f"예약된 작업 : `id가 {arg[0]}인 메시지의 삭제`\n시간 : `{t}`\n실패 사유 : `메시지가 이미 삭제되었습니다.`",
                                color = discord.Colour.red()
                            ))
                    else:
                        await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 성공적으로 실행했습니다.",
                                description = f"예약된 작업 : `id가 {arg[0]}인 메시지의 삭제`\n시간 : `{t}`",
                                color = discord.Colour.green()
                            ))
                else:
                    await e.delete()
                    await ctx.send(embed = await warn(f"id가 {arg[0]}인 메시지를 찾을 수 없습니다!"))
        elif do == "create" or do == "생성":
            if obj == "channel" or obj == "채널":
                if len(arg) > 1:
                    ct = discord.utils.get(ctx.guild.categories, id=int(arg[0]))
                    if ct:
                        await ctx.send(embed = await complete(f"{t}에 채널 '{arg[1]}'을(를)\n '{ct}' 카테고리에 생성합니다."))
                        await self.wait_until(t)
                        try:
                            await ctx.guild.create_text_channel(f'{arg[1]}', category=ct)
                        except discord.HTTPException:
                             await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 실행하지 못했습니다.",
                                description = f"예약된 작업 : `'{ct}' 카테고리에 채널 '{arg[1]}' 생성`\n시간 : `{t}`\n실패 사유 : `카테고리가 삭제됨`",
                                color = discord.Colour.red()
                            ))
                        else:
                            await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 성공적으로 실행했습니다.",
                                description = f"예약된 작업 : `'{ct}' 카테고리에 채널 '{arg[1]}' 생성`\n시간 : `{t}`",
                                color = discord.Colour.green()
                            ))
                    else:
                        await ctx.send(embed = await warn(f"id가 {arg[1]}인 카테고리를 찾을 수 없습니다."))
                        return
                else:
                    if (1,2):
                        await ctx.send(embed = discord.Embed(
                            title = f"{t}에 채널 {arg[0]}을(를) 생성합니다.",
                            description = "카테고리가 명시되어 있지 않아, 빈 공간에 채널을 생성합니다.\n특정 카테고리에 채널을 생성할려면 카테고리 ID를 인자로 주세요.",
                            color = discord.Colour.green()
                        ))
                        await self.wait_until(t)
                        try:
                            await ctx.guild.create_text_channel(f'{arg[0]}')
                        except discord.HTTPException:
                             await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 실행하지 못했습니다.",
                                description = f"예약된 작업 : `'채널 '{arg[0]}' 생성`\n시간 : `{t}`\n실패 사유 : `길드가 삭제됨`",
                                color = discord.Colour.red()
                            ))
                        else:
                            await ctx.author.send(embed = discord.Embed(
                                title = "예약된 작업을 성공적으로 실행했습니다.",
                                description = f"예약된 작업 : `채널 '{arg[0]}' 생성`\n시간 : `{t}`",
                                color = discord.Colour.green()
                            ))
        elif do == "give" or do == "추가":
            if obj == "role" or obj == "역할":
                if "@" in arg[0]:
                    ri = arg[0][3:-1]
                else:
                    ri = arg[0]
                r = ctx.guild.get_role(int(ri))
                if r:
                    if "@" in arg[1]:
                        ui = arg[1][3:-1]
                    else:
                        ui = arg[1]
                    u = bot.get_user(int(ui))
                    if u:
                        await ctx.send((r,u))

class Custom(commands.Cog, name = "커스텀"):
    def __init__(self, bot):
        self.bot = bot
    
    #개인
    @commands.command(name = "set")
    async def s(self, ctx, it, v):
        if it == "color":
            await ctx.send(f"{v}")

    #서버
    @commands.command(name="config", aliases = ["cfg","구성"])
    async def c(self, ctx, typ, p=None, *, msg = None):
        global storage
        if 1:
            if not typ in ['description','desc',"color",'url','title', '부제목', '색상', '제목', '링크']:
                await isDir(ctx.guild.id)
                a = ctx.message.attachments
                if a:
                    a = a[0]
                    if typ == "Image" or typ == "image" or typ == "사진" or typ == "이미지":
                        if a.filename.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                            p = {"welcome" : "welcome", "bye" : "bye", "환영" : "welcome", "배웅" : "bye"}[p]
                            if p in ["welcome", "bye"]:
                                storage["guild"][ctx.guild.id]["custom"][p]["image"] = a.url
                                await ctx.send(embed = await complete("{} 이미지를 성공적으로 설정했습니다!".format({"welcome":"환영", "bye" : "배웅"}[p])))
                        else:
                            await ctx.send(embed = discord.Embed(
                                title = "이미지의 확장자가 올바르지 않습니다!",
                                description = "```c\n사용 가능한 확장자 : \n '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'```",
                                color = discord.Colour.red()
                            ))
                else:
                    await ctx.send(embed = await warn("파일을 첨부해주셔야 합니다!"))
            else:
                if p in ["welcome","bye", "환영", "배웅"]:
                    p = {"welcome" : "welcome", "bye" : "bye", "환영" : "welcome", "배웅" : "bye"}[p]
                    typ = {"color" : "color", "desc" : "desc", "description": "desc", "title" : "title",
                           "색상" : "color", "부제목" : "desc", "제목": "title"}[typ]
                    if typ == "title":
                        storage["guild"][ctx.guild.id]["custom"][p][typ] = msg
                        await ctx.send(embed = await complete("{} 메시지의 제목을 성공적으로 설정했습니다!".format({"welcome":"환영", "bye" : "배웅"}[p])))
                    elif typ == "description" or typ == "desc":
                        storage["guild"][ctx.guild.id]["custom"][p][typ] = msg
                        await ctx.send(embed = await complete("{} 메시지의 부제목을 성공적으로 설정했습니다!".format({"welcome":"환영", "bye" : "배웅"}[p])))
                    elif typ == "color":
                        try:
                            storage["guild"][ctx.guild.id]["custom"][p][typ] = int(msg, base=16)
                        except ValueError:
                            await ctx.send(embed = warn("색상 값이 올바르지 않습니다!"))
                        else:
                            await ctx.send(embed = await complete("{} 메시지의 색을 성공적으로 설정했습니다!".format({"welcome":"환영", "bye" : "배웅"}[p])))


class Community(commands.Cog, name="커뮤니티"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="custommessagereaction",aliases=["cmr"])
    async def custommessagereaction(self, ctx, name, emoji):
        global storage
        check = lambda r, u: u == ctx.author and str(r.emoji)
        user = ctx.author
        await checkUser(user.id)
        if not ctx.guild.id in list(storage["user"][user.id]["cmr"]):
            storage["user"][user.id]["cmr"][ctx.guild.id] = {}
        
        if not (name in list(storage["guild"][ctx.guild.id]["cmr"].keys())):
            storage["guild"][ctx.guild.id]["cmr"][name] = []
        else:
            if type(storage["guild"][ctx.guild.id]["cmr"][name]) != list:
                storage["guild"][ctx.guild.id]["cmr"][name] = []
        if not (ctx.guild.id in list(storage["user"][user.id]["cmr"].keys())):
            storage["user"][user.id]["cmr"][ctx.guild.id] = {}
        else:
            if not (name in list(storage["user"][user.id]["cmr"][ctx.guild.id].keys())):
                storage["user"][user.id]["cmr"][ctx.guild.id][name] = []
            if type(storage["user"][user.id]["cmr"][ctx.guild.id][name]) != list:
                storage["user"][user.id]["cmr"][ctx.guild.id][name] = []
        if len(storage["guild"][ctx.guild.id]["cmr"][name]) >= 3:
            await ctx.send(embed=await warn(f":warning: '{name}' 단어에 추가된 반응이 3개를 초과합니다."))
            return
        if len(list(storage["user"][user.id]["cmr"][ctx.guild.id].keys())) < 13:
            msg = await ctx.send(embed = discord.Embed(
                title = f"'{name}' 단어에 '{emoji}' 반응을 추가하시겠습니까?",
                description = "이모티콘이 깨져 보이면 정상적으로 등록되지 않을 수도 있습니다.",
                color = discord.Colour.orange()
            ))
            await msg.add_reaction("✅")
            await msg.add_reaction("🚫")
            try:
                reaction, user = await bot.wait_for("reaction_add", check=check, timeout=30)
            except asyncio.TimeoutError:
                await msg.edit(content="Ban cancelled, timed out.")
                return
            if str(reaction.emoji) == "✅":
                await msg.delete()
                try:
                    storage["user"][user.id]["cmr"][ctx.guild.id][name].append(emoji)
                except KeyError:
                    storage["user"][user.id]["cmr"][ctx.guild.id][name] = []
                    storage["user"][user.id]["cmr"][ctx.guild.id][name].append(emoji)
                storage["guild"][ctx.guild.id]["cmr"][name].append(emoji)
                await ctx.send(embed = discord.Embed(
                    title = f"'{name}' 단어에 '{emoji}' 반응을 추가했습니다.",
                    color = discord.Colour.green()
                ))
                return
            elif str(reaction.emoji) == "🚫":
                await msg.delete()
        else:
            await ctx.send("bda")

    @commands.command(name="deletecustommessagereaction",aliases=["dcmr"])
    async def deletecustommessagereaction(self, ctx, name, emoji = None):
        global storage
        check = lambda r, u: u == ctx.author and str(r.emoji)
        user = ctx.author
        await checkUser(user.id)
        if name in list(storage["user"][user.id]['cmr'][ctx.guild.id].keys()):
            if not emoji:
                msg = await ctx.send(embed = discord.Embed(
                    title = f"'{name}' 단어의 반응을 삭제하시겠습니까?",
                    description = "단, 자신이 등록한 반응만 삭제됩니다.",
                    color = discord.Colour.orange()
                ))
                await msg.add_reaction("✅")
                await msg.add_reaction("🚫")
                try:
                    reaction, user = await bot.wait_for("reaction_add", check=check, timeout=30)
                except asyncio.TimeoutError:
                    await msg.edit(content="Ban cancelled, timed out.")
                    return
                e = []
                if str(reaction.emoji) == "✅":
                    for i in storage['guild'][ctx.guild.id]['cmr'][name]:
                        for j in storage["user"][user.id]['cmr'][ctx.guild.id][name]:
                            if i == j:
                                storage['guild'][ctx.guild.id]['cmr'][name].remove(i)
                                storage["user"][user.id]['cmr'][ctx.guild.id][name].remove(i)
                                e.append(i)
                    await msg.delete()
                    await ctx.send(embed = discord.Embed(
                        title = f"✅ {name} 단어의 반응 중 {', '.join(e)} 을(를) 성공적으로 삭제했습니다.",
                        color = discord.Colour.green()
                ))

@bot.command()
@commands.is_owner()
async def tpl(ctx, leng:int):
    if ctx.author.id != 379091348885864450:
        ctx.send(embed=discord.Embed(
            title = ":warning: 이 기능은 개발자만이 실행할 수 있습니다.",
            color = discord.Colour.red()
        ))
    else:
        await botKeyCheck('tpl')
        storage['bot']['tpl'] = leng
        await ctx.send(embed = discord.Embed(
            title = f":white_check_mark: 사과봇의 전체적 ttsplay 글자 제한을 {storage['bot']['tpl']}글자로 설정했습니다.",
            color = discord.Colour.green()
        ))

@bot.command()
@commands.is_owner()
async def addstrg(ctx, o : str, key : str, *, value : str):
    try:
        global storage
        if o == "guild":
            for i in list(storage["guild"].keys()):
                storage["guild"][i][key] = eval(value)
        elif o == "user":
            for i in list(storage["user"].keys()):
                storage["user"][i][key] = eval(value)
        await ctx.send("done")
    except:
        await ctx.send(traceback.format_exc())

@bot.command()
@commands.is_owner()
async def delstrg(ctx, o : str, key : str):
    try:
        global storage
        if o == "guild":
            for i in list(storage["guild"].keys()):
                del storage["guild"][i][key]
        elif o == "user":
            for i in list(storage["user"].keys()):
                del storage["user"][i][key]
        await ctx.send("done")
    except:
        await ctx.send(traceback.format_exc())






    
bot.add_cog(Management(bot))
bot.add_cog(Community(bot))
bot.add_cog(Custom(bot))
bot.add_cog(Develop(bot))

@tasks.loop(seconds = 60)
async def initmsgc():
    global storage
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0:
        async for i in aiter(list(storage["guild"].keys())):
            storage["guild"][i]['msgcount'] = 0
            storage["guild"][i]["msgcc"] = {}
            storage["guild"][i]["msgcu"] = {}

@tasks.loop(seconds = 30)
async def weath():
    now = datetime.datetime.now()
    if now.hour in [6, 18]:
        storage["bot"]["weather"] = await module["weather"].weather()

@tasks.loop(seconds = 20)
async def autosave():
    global storage
    if 1:
        with open("./s.pkl", "wb") as f:
            pickle.dump(storage,f)

statcount = 0

@tasks.loop(seconds = 15)
async def stat(bot):
    global statcount
    await bot.wait_until_ready()
    sl = ["{bg}개의 서버에서 일", "살려달라", "&명령어", f"{len(bot.commands)}개의 명령어"]
    await bot.change_presence(activity = discord.Game(name = sl[statcount % len(sl)].format(bg = len(bot.guilds)-4)))
    statcount += 1

initmsgc.start()
autosave.start()
stat.start(bot)

# 청사과 봇 코드

@bot.command()
async def vt(ctx : commands.context.Context):
    pass

@_bot.event
async def on_ready():
    global ivgd, gd
    ivgd = bot.get_channel(927534804331806800)
    print(f"청사과 - {_bot.user}로 로그인됨.")

    # 채널 청소, 메시지 보내기 
    VerifyChannel = _bot.get_channel(927913185766436885)
    await VerifyChannel.purge(limit = 100)

    Verifyer = discord.ui.View(timeout = None)
    Verifyer.add_item(views.VerifyButton(ivgd, cd))

    await VerifyChannel.send("여기를 눌러 검증하세요.", view = Verifyer)

    BugReportChannel = _bot.get_channel(927153144482377739)
    await BugReportChannel.purge(limit = 100)

    BugReporter = views.BugReport()

    await BugReportChannel.send("버그를 제보하려면 여기를 누르세요.", view = BugReporter)

    _bot.add_view(Verifyer)
    _bot.add_view(BugReporter)

    await GreenStat(_bot)

async def GreenStat(bot : discord.Client):
    while True:
        for i in ["검증", "오류 수집", "버그 수집"]:
            await bot.change_presence(activity = discord.Game(name = i))
            await asyncio.sleep(15)

@_bot.event
async def on_message(m):
    if m.author.id == 927465958665244742: return
    await _bot.process_commands(m)
    if not m.reference and m.guild.id != 893899915305050183:
        if not m.author.id == 927465958665244742:
            try: await m.delete()
            except NotFound: pass

@_bot.event
async def on_member_join(m):
    global ivgd, gd
    if m.guild.id == 927460646008791141:
        cd[m.id] = False
        await m.add_roles(discord.utils.get(m.guild.roles, id = 927461725802987520))
    elif m.guild.id == 893899915305050183:
        try:
            if cd[m.id] == False:
                await m.kick(reason = "미검증 유저")
                try:
                    await m.send("> 검증되지 않은 유저는 이 서버에 출입할 수 없습니다.\n`검증은 1회성이며, 서버를 나가고 재가입하려면 인증을 다시 해야 합니다.`")
                except discord.Forbidden:
                    pass
            else:
                await (await _bot.fetch_guild(927460646008791141)).kick(m, reason="검증 완료됨")
        except KeyError:
            await m.kick(reason = "미검증 유저")
            try:
                await m.send("> 검증되지 않은 유저는 이 서버에 출입할 수 없습니다.\n`검증은 1회성이며, 서버를 나가고 재가입하려면 인증을 다시 해야 합니다.`")
            except discord.Forbidden:
                pass

cd = {}


# 에러 관리
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

@_bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

# 봇 토큰 보안

if os.path.isdir(r"E:\TOKEN"):
    if os.path.isfile(r"E:\CHECK.CHECK"):
        if os.popen("WMIC BIOS GET SERIALNUMBER").read().strip().split("\n")[2] != open(r"E:\CHECK.CHECK", "r").read(): # 디바이스의 시리얼 넘버가 맞는다면
            print("SD카드의 정보가 올바르지 않습니다.")
            sys.exit(1)
        else:
            print("정보가 확인되었습니다. 봇을 시작합니다.")

            with open(r"E:\TOKEN\TOKEN.TOKEN", "r") as f:
                t1, t2 = ccd.decrypt(f.read(), os.popen("WMIC BIOS GET SERIALNUMBER").read().strip().split("\n")[2]).split("\n")
            
            loop = asyncio.get_event_loop()

            loop.create_task(bot.start(t1)) # 다른 토큰이면 이 부분에 토큰을 넣어주세요
            loop.create_task(_bot.start(t2)) # 다른 토큰이면 이 부분에 토큰을 넣어주세요

            try:
                loop.run_forever()
            finally:
                loop.stop()
            
    else:
        print("SD카드에 인증 정보가 포함된 파일이 없습니다.")
        sys.exit(0)
else:
    print("SD카드가 확인되지 않습니다.")
    sys.exit(1)
