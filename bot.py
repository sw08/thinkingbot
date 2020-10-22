
#2020.10.12/18:56 작성

#모듈 임포트

from discord import *
from time import sleep
from random import randint
import asyncio
from discord.ext import commands
import time
import os
from os.path import isfile

#기본 변수 설정

prefix ="''"

app = commands.Bot(command_prefix=prefix)

token = 'NzY1NDM0MDU1MDE2ODQxMjU4.X4UwAw.Q3L-hir9EVtpjHVrBzDUzTSLxPc'

category_list = [
    '지원',
    '일반',
    '관리자',
    '수학',
    '재미 및 포인트'
]

category_explain = [
    '`도움`, `봇정보`',
    '`정보`, `출석`, `소개설정`, `파일생성`',
    '`밴`, `언밴`',
    '`사칙연산`, `일차풀기`',
    '`도박`'
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
    '도박'
]

func_footer = [
    '도움',
    '봇정보',
    '출석',
    '정보',
    '소개설정 (소개말)',
    '밴 (멤버 멘션)',
    '언밴 (멤버 멘션)',
    '파일생성 (제목) (내용)',
    '사칙연산 (수) (연산자) (수)',
    '일차풀기 (미지수 단위) (a) (b) (c)',
    '도박 (걸 포인트)'
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
    '50% 확률로 2배의 돈을 얻음 (아니면 건돈×-2배)'
]

embedcolor = 0x00ffff
errorcolor = 0xff0000

#함수 처리

def isbanned(id):
    if isfile('ban.txt'):
        return (str(id) in open('ban.txt', 'r').read())
    open('ban.txt', 'x')
    return False

def is_owner():
    async def predicate(ctx):
        return ctx.author.id == 745848200195473490
    return commands.check(predicate)

def readpoint(id):
    pointroute = f'{id}.txt'
    try:
        a = open(pointroute, 'r').read()
    except FileNotFoundError:
        a = open(pointroute, 'w').close()
        a = 0
    return a

def writepoint(id, addpoint):
    pointroute = f'{id}.txt'
    try:
        a = open(pointroute, 'r').read().close()
    except FileNotFoundError:
        a = open(pointroute, 'w').write('0').close()
        a = '0'
    b = open(pointroute, 'w')
    b.write(str(int(a)+int(addpoint))).close()

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
async def _chulseok(ctx):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:
        date = time.strftime('%Y%m%d', time.localtime(time.time()))
        check = False
        ifyouchulseoked = f'{date}/{ctx.author.id}.txt'
        if not os.path.isdir(f'{date}/'):
            os.makedirs(f'{date}')
        try:
            b = open(ifyouchulseoked, 'r')
        except FileNotFoundError:
            b = open(ifyouchulseoked, 'w')
            b.write('1')
            b.close()
            check = True
            pointroute = f'{ctx.author.id}.txt'
            try:
                a = open(pointroute, 'r')
            except FileNotFoundError:
                a = open(pointroute, 'w')
                a.write('0')
            a.close()
            a = open(pointroute, 'r')
            point = int(a.read())
            a.close()
            a = open(pointroute, 'w')
            a.write(str(point+1))
            a.close()
            await ctx.send('정상적으로 출석되었습니다')
        if not check:
            await ctx.send('이미 출석하셨습니다 내일 다시 오세요')

@app.command(name='소개설정')
async def _setInfo(ctx, *, content):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:
        pointroute = f'{ctx.author.id}_info.txt'
        a = open(pointroute, 'w', encoding='utf-8')
        a.write(content)
        a.close()
        await ctx.send(f'소개말이 {content} (으)로 변경되었습니다'  )
    
@app.command(name='정보')
async def _info(ctx):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:
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
        msgembed = Embed(title=str(ctx.author), description=userinfo, color=0x00ffff)
        msgembed.set_thumbnail(url=str(ctx.author.avatar_url))
        msgembed.add_field(name='유저 ID', value=f'{ctx.author.id}')
        point = readpoint(f'{ctx.author.id}')
        msgembed.add_field(name='유저 포인트', value=point)
        msgembed.set_footer(text=f'{prefix}도움 | {ctx.author}')
        await ctx.send(embed=msgembed)

@app.command(name='파일생성')
async def _makefile(ctx, filename, *, content):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:
        a = open(filename, 'w')
        a.write(content)
        a.close()
        file1 = File(filename)
        await ctx.send(file=file1)
        os.remove(filename)

#수학 카테고리

@app.command(name='사칙연산')
async def _calcul(ctx, n1, operator, n2):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:
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
        msgembed.set_footer(text=f'{prefix}도움 | {ctx.author}')
        if b:
            await ctx.send(embed=msgembed)

@app.command(name='일차풀기')
async def _calcul(ctx, operator, a, b, c):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:
        msgembed = Embed(title='일차풀기', description='', color=embedcolor)
        if b[0] == '-':
            msgembed.add_field(name='**Input**', value=f'```{a}{operator}{b}={c}```', inline=False)
        else:
            msgembed.add_field(name='**Input**', value=f'```{a}{operator}+{b}={c}```', inline=False)
        answer = (float(c)-float(b)) / float(a)
        if float(int(answer)) == answer:
            answer = int(answer)
        msgembed.add_field(name='**Output**', value=f'```{answer}```', inline=False)
        msgembed.set_footer(text=f'{prefix}도움 | {ctx.author}')
        await ctx.send(embed=msgembed)

#지원 카테고리

@app.command(name='봇정보')
async def _botinfo(ctx):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:
        msgembed = Embed(title='ThinkingBot Beta#7894',description='', color=embedcolor)
        msgembed.add_field(name='개발자', value='yswysw#9328')
        msgembed.add_field(name='도움을 주신 분들', value='`huntingbear21#4317`님, `Decave#9999`님, `koder_ko#8504`님 등 많은 분들께 감사드립니다.', inline=False)
        msgembed.add_field (name='상세정보', value='2020년에 만들어진 봇이며, 수학과 다른 봇에서는 볼 수 없는 독특한 기능들이 많이 있음', inline=False)
        msgembed.add_field(name='버전', value='Beta 0.4 - 20201022 릴리즈', inline=False)
        msgembed.add_field(name='개발언어 및 라이브러리', value='파이썬, discord.py', inline=False)
        msgembed.add_field(name='개발환경', value='윈도우10, Visual Studio Code', inline=False)
        msgembed.add_field(name='공식 서포트 서버', value='https://discord.gg/ASvgRjX', inline=False)
        msgembed.add_field(name='봇 초대 링크', value='https://discord.com/api/oauth2/authorize?client_id=750557247842549871&permissions=0&scope=bot', inline=False)
        msgembed.set_thumbnail(url="https://sw08.github.io/cloud/profile.png")
        msgembed.set_footer(text=f'{prefix}도움 | {ctx.author}')
        await ctx.send(embed=msgembed)

@app.command(name='도움')
async def _help(ctx, what_you_look_for):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:
        if what_you_look_for in func_list:
            msgembed = Embed(title=f'도움 - {what_you_look_for}', description=func_explain[func_list.index(what_you_look_for)], color=embedcolor)
            msgembed.set_footer(text=f'{prefix}{func_footer[func_list.index(what_you_look_for)]} | {ctx.author}')

        elif what_you_look_for in category_list:
            msgembed = Embed(title=f'도움 - {what_you_look_for}', description=category_explain[category_list.index(what_you_look_for)], color=embedcolor)
            msgembed.set_footer(text=f'{prefix}도움 {what_you_look_for} | {ctx.author}')
        
        else:
            msgembed = Embed(title='에러', description='음.... 아직 그런 카테고리는 없습니다.', color=errorcolor)
            msgembed.set_footer(text=f'{prefix}도움 커맨드 써보라고 | {ctx.author}')
        await ctx.send(embed=msgembed)

#관리자 카테고리

@app.command(name='밴')
async def _ban(ctx, member: Member):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:
        if ctx.author.id == 745848200195473490:
            if isbanned(member.id):
                await ctx.send('이미 차단당했습니다')
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
                    await ctx.send(f'{member.mention} 님은 ThinkingBot에게서 차단되었습니다. 이의는 ThinkingBot 관리자에게 제출해 주십시오.')
        else:
            await ctx.send('권한이 없습니다')

@app.command(name='언밴')
async def _ban(ctx, member: Member):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:
        if ctx.author.id == 745848200195473490:
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
                    await ctx.send(f'{member.mention} 님은 ThinkingBot에게서 차단이 풀렸습니다.')
            else:
                await ctx.send('차단당한적이 없습니다')
        else:
            await ctx.send('권한이 없습니다')

#재미 및 포인트 카테고리
'''
@app.command(name='도박')
async def _dobac(ctx, don):
    if isbanned(ctx.author.id):
        await ctx.send('명령어 사용 불가')
    else:'''
#에러 처리

@_help.error
async def _help_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        msgembed = Embed(title='도움', description='도움말', color=embedcolor)
        msgembed.add_field(name='일반', value='`일반 명령어들`', inline=False)
        msgembed.add_field(name='재미 및 포인트', value='`포인트 관련 명령어들`')
        msgembed.add_field(name='수학', value='`수학 관련 명령어들`', inline=False)
        msgembed.add_field(name='지원', value='`봇 관련 지원 명령어들`', inline=False)
        msgembed.add_field(name='관리자', value='`관리자 전용 명령어들`', inline=False)
        await ctx.send(embed=msgembed)

app.remove_command("help")
app.run(token)