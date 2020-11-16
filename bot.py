#모듈 임포트

from discord import *
from random import randint
import asyncio
from discord.ext import commands
from os.path import isdir
import time
import os
from os.path import isfile
import datetime
from pytz import timezone
from datetime import timedelta
import ast

#기본 변수 설정

prefix ="''"

app = commands.Bot(command_prefix=["''", '"'])

a = open('token.txt', 'r')
token = a.read()
a.close()

category_list = [
    '지원',
    '일반',
    '관리자',
    '수학',
    '포인트'
]

category_explain = [
    '`도움`, `봇정보`, `핑`',
    '`정보`, `출석`, `소개설정`, `파일생성`, `찬반투표`, `공지설정`, `공지취소`, `서버정보`',
    '`밴`, `언밴`, `관리자송금`, `공지`, `실행`',
    '`사칙연산`, `일차풀기`, `소수`',
    '`도박`, `송금`'
]

func_list = [
    '도움',
    '봇정보',
    '출석',
    '정보',
    '소개설정',
    '밴',
    '언밴',
    '파일생성',
    '사칙연산',
    '일차풀기',
    '도박',
    '핑',
    '송금',
    '관리자송금',
    '공지',
    '찬반투표',
    '공지설정',
    '공지취소',
    '실행',
    '서버정보',
    '소수'
]

func_footer = [
    '도움',
    '봇정보',
    '출석',
    '정보 (멤버 멘션/None)',
    '소개설정 (소개말)',
    '밴 (멤버 멘션)',
    '언밴 (멤버 멘션)',
    '파일생성 (제목) (내용)',
    '사칙연산 (수) (연산자) (수)',
    '일차풀기 (미지수 단위) (a) (b) (c)',
    '도박 (걸 포인트 / 올인)',
    '핑',
    '송금 (멤버 멘션) (송금할 포인트)',
    '관리자송금 (멤버 멘션) (송금할 포인트)',
    '공지 (내용)',
    '찬반투표 (내용)',
    '공지설정',
    '공지취소',
    '실행 (파이썬 스크립트)',
    '서버정보',
    '소수 (첫번째 값) (두번째 값)'
]

func_explain = [
    '쓸 수 있는 명령어 확인',
    '봇 정보 확인',
    '출석하기',
    '포인트 및 정보 확인',
    '소개말 설정',
    '봇 사용 금지 (관리자 전용)',
    '봇 사용 금지 해제 (관리자 전용)',
    '파일 만들어서 올려줌 (파일명 한글은 미적용)',
    '사칙연산 수행(+, -, *, /)',
    '일차방정식의 해 구하기 (ax+b=c)',
    '50% 확률로 건 돈을 더 얻음 (아니면 건돈 × -1배)',
    '핑을 측정',
    '돈을 송금함',
    '돈 송금 - 관리자용',
    '공지하기',
    '찬성/반대 투표 생성',
    '공지설정',
    '공지채널 설정 취소',
    '입력한 코드 실행 (관리자 전용)',
    '서버 정보 확인',
    '첫번째 값과 두번째 값 사이의 소수들을 구함'
]

embedcolor = 0x00ffff
errorcolor = 0xff0000

KST = timezone('Asia/Seoul')

#함수 처리

def is_owner():
    async def predicate(ctx):
        return ctx.author.id in [745848200195473490, 557119176590884864, 594183416266752000, 441202161481809922]
    return commands.check(predicate)

def can_use():
    async def predicate(ctx):
        return not isbanned(ctx.author.id)
    return commands.check(predicate) 

def isbanned(id):
    if isfile('ban.txt'):
        return (str(id) in open('ban.txt', 'r').read())
    open('ban.txt', 'x')
    return False

def readpoint(id):
    pointroute = f'{id}.txt'
    try:
        a = open(pointroute, 'r')
        b = a.read()
    except FileNotFoundError:
        a = open(pointroute, 'w')
        a.write('0')
        b = 0
    a.close()
    b = int(b)
    return b

def writepoint(id, addpoint):
    pointroute = f'{id}.txt'
    a = open(pointroute, 'w')
    a.write(str(addpoint))
    a.close()

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

def get_prime(start, end):
    # 에라토스테네스의 체 초기화: end개 요소에 True 설정(소수로 간주)
    sieve = [True] * end
    # end의 최대 약수가 sqrt(end) 이하이므로 i=sqrt(end)까지 검사
    m = int(end ** 0.5)
    for i in range(start, m + 1):
        if sieve[i] == True:           # i가 소수인 경우
            for j in range(i+i, end, i): # i이후 i의 배수들을 False 판정
                sieve[j] = False
    # 소수 목록 산출
    return [i for i in range(2, end) if sieve[i] == True]

#이벤트 처리

@app.event
async def on_ready():
    print('구동 시작')
    game = Game(f'{prefix}도움')
    await app.change_presence(status=Status.online, activity=game)
    

@app.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        pass

#커맨드 처리

#일반 카테고리

@app.command(name='출석')
@can_use()
async def _chulseok(ctx):
    utcnow= datetime.datetime.utcnow()
    time_gap= datetime.timedelta(hours=9)
    kor_time= utcnow+ time_gap
    date = str(kor_time.strftime('%Y%m%d'))
    ifyouchulseoked = f'{date}/{ctx.author.id}.txt'
    b = True
    if not isdir(f'{date}/'):
        os.makedirs(f'{date}/')
    try:
        a = open(ifyouchulseoked, 'r')
    except FileNotFoundError:
        b = False
        a = open(ifyouchulseoked, 'w')
        point = readpoint(ctx.author.id)
        writepoint(ctx.author.id, 100+point)
        point += 1
        msgembed = Embed(title='출석 완료', description=f'출석이 완료되었습니다. \n 현재 포인트: {point}', color=embedcolor)
    a.close()
    if b:
        msgembed = Embed(title='🚫에러🚫', description='이미 출석했습니다', color=errorcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='소개설정')
@can_use()
async def _setInfo(ctx, *, content):
    pointroute = f'{ctx.author.id}_info.txt'
    a = open(pointroute, 'w', encoding='utf-8')
    a.write(content)
    a.close()
    msgembed = Embed(title='변경 완료', description=f'소개말이 {content} (으)로 변경되었습니다', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(Embed=msgembed)
    
@app.command(name='정보')
@can_use()
async def _info(ctx, member : Member):
    id = member.id
    pointroute = f'{id}_info.txt'
    b = True
    try:
        a = open(pointroute, 'r')
    except FileNotFoundError:
        b = False
        userinfo = f'내용이 없습니다. `{prefix}소개설정` 명령어로 소개말을 설정하세요.'
    if b:
        a.close()
        a = open(pointroute, 'r', encoding='utf-8')
        userinfo = a.read()
        a.close()
    pointroute = f'{id}.txt'
    msgembed = Embed(title=str(member), description=userinfo, color=embedcolor)
    msgembed.set_thumbnail(url=str(member.avatar_url))
    msgembed.add_field(name='유저 ID', value=f'{id}')
    point = readpoint(id)
    msgembed.add_field(name='💵유저 포인트💵', value=point)
    msgembed.set_footer(text=f'{member} | {prefix}도움', icon_url=member.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='파일생성')
@can_use()
async def _makefile(ctx, filename, *, content):
    a = open(filename, 'w')
    a.write(content)
    a.close()
    file1 = File(filename)
    await ctx.send(file=file1)
    os.remove(filename)

@app.command(name='찬반투표')
@can_use()
async def _devote_tof(ctx, *, content):
    msgembed = Embed(title='투표', description=content, color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    a = await ctx.send(embed=msgembed)
    await a.add_reaction('❌')
    await a.add_reaction('✅')

@app.command('공지설정')
@can_use()
async def _공지설정(ctx):
    try:
        a = open('notice.txt', 'r')
        b = a.read()
    except FileNotFoundError:
        a = open('notice.txt', 'w')
        b = ''
    a.close()
    if str(ctx.channel.id) in b:
        msgembed = Embed(title='🚫에러🚫', description='이미 등록되어 있음', color=errorcolor)
    else:
        os.remove('notice.txt')
        a = open('notice.txt', 'w')
        a.write(b + f'\n{ctx.channel.id}')
        a.close()
        msgembed = Embed(title='🔔공지설정🔔', description='완료', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command('공지취소')
@can_use()
async def _공지취소(ctx):
    try:
        a = open('notice.txt', 'r')
        b = a.read()
    except FileNotFoundError:
        a = open('notice.txt', 'w')
        b = ''
    a.close()
    if not str(ctx.channel.id) in b:
        msgembed = Embed(title='🚫에러🚫', description='등록되어 있지 않음', color=errorcolor)
    else:
        os.remove('notice.txt')
        a = open('notice.txt', 'w')
        a.write(b.replace(f'\n{ctx.channel.id}', ''))
        a.close()
        msgembed = Embed(title='🔕공지취소🔕', description='완료', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='서버정보')
@can_use()
async def _serverinfo(ctx):
    msgembed = Embed(title='서버정보', description='', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    msgembed.set_thumbnail(url=ctx.guild.icon_url)
    server = ctx.guild
    msgembed.add_field(name='서버이름', value=server, inline=True)
    msgembed.add_field(name='서버 id', value=str(server.id), inline=True)
    msgembed.add_field(name='서버 오너', value=f'<@{server.owner_id}>', inline=True)
    msgembed.add_field(name='서버 인원수', value=server.member_count, inline=True)
    msgembed.add_field(name='서버 생성일', value=str(server.created_at)[:19], inline=True)
    msgembed.add_field(name='서버 부스트', value=f'{server.premium_tier}티어, {server.premium_subscription_count}개', inline=True)
    if len(server.emojis) == 0:
        emojis = '커스텀 이모지 없음'
    else:
        emojis = ''
        for i in range(len(server.emojis)):
            emojis = emojis + ', ' + str(server.emojis[i])
        emojis = emojis[2:len(emojis)]
    msgembed.add_field(name='이모지 목록', value=emojis, inline=True)
    await ctx.send(embed=msgembed)

#수학 카테고리

@app.command(name='사칙연산')
@can_use()
async def _calcul(ctx, n1, operator, n2):
    b = True
    msgembed = Embed(title='사칙연산', description='', color=embedcolor)
    msgembed.add_field(name='**Input**', value=f'```{n1}{operator}{n2}```', inline=False)
    if operator == '+':
        a = float(n1)+float(n2)
    elif operator == '-':
        a = float(n1)-float(n2)
    elif operator == '/' or operator == '÷':
        a = float(n1)/float(n2)
    elif operator == '*' or operator == '×':
        a = float(n1)*float(n2)
    else:
        b = False
    if float(int(a)) == a:
        a = int(a)
    msgembed.add_field(name='**Output**', value=f'```{a}```', inline='True')
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    if b:
        await ctx.send(embed=msgembed)

@app.command(name='일차풀기')
@can_use()
async def _calcul(ctx, operator, a, b, c):
    msgembed = Embed(title='일차풀기', description='', color=embedcolor)
    if b[0] == '-':
        msgembed.add_field(name='**Input**', value=f'```{a}{operator}{b}={c}```', inline=False)
    else:
        msgembed.add_field(name='**Input**', value=f'```{a}{operator}+{b}={c}```', inline=False)
    answer = (float(c)-float(b)) / float(a)
    if float(int(answer)) == answer:
        answer = int(answer)
    msgembed.add_field(name='**Output**', value=f'```{answer}```', inline=False)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='소수')
@can_use()
async def _prime(ctx, start, end):
    if int(start) >= int(end):
        msgembed = Embed(title='에러', description='첫번째 값은 두번째 값보다 작아야 합니다', color=errorcolor)
    elif int(start) < 2:
        msgembed = Embed(title='에러', description='첫번째 값은 최소 2입니다', color=errorcolor)
    else:
        primes = get_prime(int(start), int(end))
        if len(primes) == 0:
            prime_str == '없음'
        else:
            prime_str = ''
            for i in range(len(primes)):
                prime_str = prime_str + ', ' + str(primes[i])
            prime_str = prime_str[2:len(prime_str)]
        msgembed = Embed(title='소수', description=f'**{start} ~ {end} 사이의 소수:**\n{prime_str}', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

#지원 카테고리

@app.command(name='봇정보')
@can_use()
async def _botinfo(ctx):
    msgembed = Embed(title='ThinkingBot Beta#7894',description='', color=embedcolor)
    msgembed.add_field(name='개발자', value='Team ThinkingBot')
    msgembed.add_field(name='도움을 주신 분들', value='`huntingbear21#4317`님, `Decave#9999`님, `koder_ko#8504`님, `Scott7777#5575`님, `Minibox#3332`님 등 많은 분들께 감사드립니다.', inline=False)
    msgembed.add_field (name='상세정보', value='다른 봇에서는 볼 수 없는 독특한 기능들이 많이 있음', inline=False)
    msgembed.add_field(name='버전', value='1.4.1 - 20201113 릴리즈', inline=False)
    msgembed.add_field(name='개발언어 및 라이브러리', value='파이썬, discord.py', inline=False)
    msgembed.add_field(name='링크', value='[깃허브 바로가기](https://github.com/sw08/thinkingbot)\n[봇 초대 링크](https://discord.com/api/oauth2/authorize?client_id=750557247842549871&permissions=0&scope=bot)\n[공식 서포트 서버](https://discord.gg/ASvgRjX)\n[공식 홈페이지](http://thinkingbot.kro.kr)', inline=False)
    msgembed.set_thumbnail(url="https://sw08.github.io/cloud/profile.png")
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='도움')
@can_use()
async def _help(ctx, what_you_look_for):
    if what_you_look_for in func_list:
        msgembed = Embed(title=f'도움 - {what_you_look_for}', description=func_explain[func_list.index(what_you_look_for)], color=embedcolor)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}{func_footer[func_list.index(what_you_look_for)]}', icon_url=ctx.author.avatar_url)

    elif what_you_look_for in category_list:
        msgembed = Embed(title=f'도움 - {what_you_look_for}', description=category_explain[category_list.index(what_you_look_for)], color=embedcolor)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}도움 {what_you_look_for}', icon_url=ctx.author.avatar_url)
    
    else:
        msgembed = Embed(title='🚫에러🚫', description='음.... 아직 그런 카테고리/명령어는 없습니다.', color=errorcolor)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='핑')
@can_use()
async def _ping(ctx):
    la = app.latency
    msgembed = Embed(title='핑', description=f'{str(round(la * 1000))}ms', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

#관리자 카테고리

@app.command(name='밴')
@can_use()
@is_owner()
async def _ban(ctx, member: Member):
    if isbanned(member.id):
        msgembed = Embed(title='에러', description='이미 차단되었습니다', color=embedcolor)
    else:
        b = True
        try:
            a = open('ban.txt', 'r')
        except FileNotFoundError:
            a = open('ban.txt', 'w')
            a.write(str(member.id))
            b = False
        a.close()
        if b:
            a = open('ban.txt', 'r')
            banned_members = a.read()
            a.close()
            a = open('ban.txt', 'w')
            a.write(f'{banned_members}\n{member.id}')
            a.close()
            msgembed = Embed(title='밴', description=f'{member.mention} 님은 ThinkingBot에게서 차단되었습니다. 이의는 ThinkingBot 관리자에게 제출해 주십시오.', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)
    await ctx.send(member.mention + ' <:Ban:776014153860513814>')

@app.command(name='언밴')
@can_use()
@is_owner()
async def _ban(ctx, member: Member):
    if isbanned(member.id):
        b = True
        try:
            a = open('ban.txt', 'r')
        except FileNotFoundError:
            a = open('ban.txt', 'w')
            a.write('')
            b = False
        a.close()
        if b:
            a = open('ban.txt', 'r')
            banned_members = a.read().replace(f'\n{member.id}', '')
            a.close()
            a = open('ban.txt', 'w')
            a.write(banned_members)
            a.close()
            msgembed = Embed(title='밴', description=f'{member.mention} 님은 ThinkingBot에게서 차단이 풀렸습니다.', color=embedcolor)
    else:
        msgembed = Embed(title='에러', description='차단된 적이 없습니다', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='관리자송금')
@can_use()
@is_owner()
async def _sendmoney(ctx, member: Member, money):
    point = readpoint(member.id)
    writepoint(member.id, point+int(money))
    msgembed = Embed(title='관리자송금', description=f'{member.mention}님께 {money}원이 송금되었습니다', color=embedcolor)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='공지')
@can_use()
@is_owner()
async def _공지(ctx, *, msg):
    utcnow= datetime.datetime.utcnow()
    time_gap= datetime.timedelta(hours=9)
    kor_time= utcnow+ time_gap
    time1 = kor_time.strftime('%Y/%m/%d %H:%M')
    a = True
    msgembed = Embed(title='📢봇공지📢', description='', color=embedcolor)
    msgembed.add_field(name='ㅤ', value=f'{msg}\n\n-------------\n\n[공식 서포트 서버](https://discord.gg/ASvgRjX)\n[공식 홈페이지](http://thinkingbot.kro.kr)', inline=False)
    msgembed.set_footer(text=f'{ctx.author} | {time1}', icon_url=ctx.author.avatar_url)
    msgembed.set_thumbnail(url="https://sw08.github.io/cloud/profile.png")
    try:
        b = open('notice.txt', 'r')
    except FileNotFoundError:
        b = open('notice.txt', 'w').close()
        a = False
        await ctx.send('공지채널없음')
    if a:
        c = b.read().split('\n')
        c.remove('')
        for i in range(len(c)):
            await app.get_channel(int(c[i].replace('\n', ''))).send(embed=msgembed)
    b.close()

@app.command(name='실행')
@can_use()
@is_owner()
async def eval_fn(ctx, *, cmd):
    msgembed = Embed(title='실행', description='', color=embedcolor)
    msgembed.add_field(name='**INPUT**', value=f'```py\n{cmd}```', inline=False)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    try:
        fn_name = "_eval_expr"
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        insert_returns(body)
        env = {
            'app': app,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
            }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        
    except Exception as a:
        result = a
    msgembed.add_field(name="**OUTPUT**", value=f'```{result}```', inline=False)    
    await ctx.send(embed=msgembed)

#포인트 카테고리

@app.command(name='도박')
@can_use()
async def _dobac(ctx, don1):
    point = readpoint(ctx.author.id)
    if don1 == '올인':
        don = point
    else:
        don = don1
    if float(don) > point:
        msgembed = Embed(title='🚫에러🚫', description='돈이 부족합니다', color=errorcolor)
    elif float(don) <= 0:
        msgembed = Embed(title='🚫에러🚫', description='돈은 1 이상부터 걸 수 있습니다', color=errorcolor)
    else:
        if randint(0,1):
            writepoint(ctx.author.id, point+int(don))
            msgembed = Embed(title='와아아', description='이겼습니다!', color=embedcolor)
            msgembed.add_field(name='원래 있던 돈', value=str(point), inline=False)
            msgembed.add_field(name='번 돈', value=don, inline=False)
            msgembed.add_field(name='현재 가진 돈', value=str(point+int(don)), inline=False)
        else:
            writepoint(ctx.author.id, point-int(don))
            msgembed = Embed(title='으아악', description='졌습니다...', color=errorcolor)
            msgembed.add_field(name='원래 있던 돈', value=str(point), inline=False)
            msgembed.add_field(name='잃은 돈', value=don, inline=False)
            msgembed.add_field(name='현재 가진 돈', value=str(point-int(don)), inline=False)
    msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

@app.command(name='송금')
@can_use()
async def _sendmoney(ctx, member: Member, money):
    point = readpoint(ctx.author.id)
    if point < int(money):
        msgembed = Embed(title='에러', description=f'돈이 부족합니다\n현재 있는 돈은 {readpoint(ctx.author.id)}입니다', color=errorcolor)
    elif int(money) < 1:
        msgembed = Embed(title='에러', description='1 이상부터 보낼 수 있습니다', color=errorcolor)
    elif int(money) != float(money):
        msgembed = Embed(title='에러', description='정수만 보낼 수 있습니다', color=errorcolor)
    else:
        writepoint(ctx.author.id, point-int(money))
        point = readpoint(member.id)
        writepoint(member.id, point+int(money))
        msgembed = Embed(title='송금', description=f'{member.mention}님께 {money}원이 송금되었습니다', color=embedcolor)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=msgembed)

#에러 처리

@_help.error
async def _help_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        msgembed = Embed(title='도움', description='도움말', color=embedcolor)
        msgembed.set_thumbnail(url='https://thinkingbot.kro.kr/profile.png')
        msgembed.add_field(name='일반', value='`일반 명령어들`', inline=False)
        msgembed.add_field(name='포인트', value='`포인트 관련 명령어들`', inline=False)
        msgembed.add_field(name='수학', value='`수학 관련 명령어들`', inline=False)
        msgembed.add_field(name='지원', value='`봇 관련 지원 명령어들`', inline=False)
        msgembed.add_field(name='관리자', value='`관리자 전용 명령어들`', inline=False)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}도움 (명령어/카테고리)', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=msgembed)


@_info.error
async def _info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        pointroute = f'{ctx.author.id}_info.txt'
        b = True
        try:
            a = open(pointroute, 'r')
        except FileNotFoundError:
            b = False
            userinfo = f'내용이 없습니다. `{prefix}소개설정` 명령어로 소개말을 설정하세요.'
        if b:
            a.close()
            a = open(pointroute, 'r', encoding='utf-8')
            userinfo = a.read()
            a.close()
        pointroute = f'{ctx.author.id}.txt'
        msgembed = Embed(title=str(ctx.author), description=userinfo, color=embedcolor)
        msgembed.set_thumbnail(url=str(ctx.author.avatar_url))
        msgembed.add_field(name='유저 ID', value=f'{ctx.author.id}')
        point = readpoint(ctx.author.id)
        msgembed.add_field(name='💵유저 포인트💵', value=point)
        msgembed.set_footer(text=f'{ctx.author} | {prefix}도움', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=msgembed)

app.remove_command("help")
app.run(token)
