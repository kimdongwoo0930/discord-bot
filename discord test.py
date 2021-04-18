import asyncio
import discord 
from discord.ext import commands
from discord.utils import get
import youtube_dl
from selenium import webdriver
import bs4
import lxml
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import os




youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'song.mp4',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.2):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

file =  './song.mp4'
크롬드라이브경로 = r"C:\Users\qaz25\Documents\chromedriver_win32\chromedriver.exe"
Numlist = 0
bookmc=[]
entireNum={}
searchyoutube={}
client = commands.Bot(command_prefix='#')
queue = []
Song_Title =[]
request_title = {}



def play(ctx):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    url = bookmc[0]
    vc2 = get(client.voice_clients, guild=ctx.guild)
    del bookmc[0]
    if not vc2.is_playing():
        vc2.play(discord.FFmpegPCMAudio(url,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
def play_next(ctx):
    vc2 = get(client.voice_clients, guild=ctx.guild)
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if not vc2.is_playing():
        if not bookmc:
            print("예약된 곡이 없습니다")
            
        else:
            if os.path.isfile(file):
                os.remove(file)
            url = bookmc[0]
            del bookmc[0]
            del Song_Title[0]
            song_info = ytdl.extract_info(url, download=True)
            filename = ytdl.prepare_filename(song_info)
            player = discord.FFmpegPCMAudio(filename)
            vc2.play(player, after=lambda e: play_next(ctx))
    






token = "ODIxMjQ4Mzc3Mzg2OTU4ODYw.YFA9Jw.Rpx_k1w6V_uUG9ATeOHl7IBj5Oc"
#토큰 = 디스코드 봇코드
log_channel_id="821249456086188062"

musiclist={}
queues={}
def check_queue(id):
    if queues[id]!=[]:
        player = queues[id].pop(0)
        players[id] = player
        del musiclist[0]

@client.event
async def on_ready():
    print("연결중")
    print(client.user.name)
    print(client.user.id)
    print("연결완료")
    print("================")
    game = discord.Game("#도움말/작동")
    await client.change_presence(status = discord.Status.online, activity = game) 


@client.command(name="도움말",pass_context=True)
async def _help(ctx):
    embed=discord.Embed(title="도움말",color=0x00ff56)                     #정보/도움말
    embed.set_thumbnail(url="https://miro.medium.com/max/1033/1*MAsNORFL89roPfIFMBnA4A.jpeg")
    embed.add_field(name="테스트봇", value ="테스트봇을 사용시 사용전 #연결로 통화방에 봇을 넣어주세요",inline =False)
    embed.add_field(name="명령어", value = "#도움말 \n#연결  \n#연결끊기  \n#검색 (노래제목)  \n#다음 /스킵 /skip \n 노래 선택시 ## (숫자)\n#채팅제거 (채팅수)\n #정지\n #재생\n #취소 (대기열번호)\n현재 듣고있는 노래확인은 #확인",inline =False)
    embed.add_field(name="정보", value ="이봇의 검색 기능은 유튜브를 기준으로 만들어졌습니다",inline =False)
    await ctx.channel.send(embed=embed)


@client.command(name="채팅제거",pass_context =True)          #채팅청소
async def _clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)


@client.command(name="연결",pass_context = True)
async def _join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("채널에 접속되어있지않습니다")

@client.command(name="연결끊기",pass_context = True)
async def _exit(ctx):
    server = ctx.guild
    vs2 = server.voice_client
    if vs2.is_playing():
        vs2.stop()
    if os.path.isfile(file):
        os.remove(file)
    await client.voice_clients[0].disconnect()


@client.command(name="검색",pass_context = True)
async def _music(ctx,encText):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    '''Text = ""
    learn = message.split(" ")
    vrsize = len(learn)                                    #배열 크기
    vrsize = int(vrsize)
    for i in range(1, vrsize):                             # 띄어쓰기 한글자한글자 인식함
        Text = Text + " " + learn[i]
    encText = Text
    print(Text)'''

    driver = webdriver.Chrome(크롬드라이브경로 , options= options)
    driver.get("https://www.youtube.com/results?search_query="+encText)
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all("a", {"id" : 'video-title'})

    embed = discord.Embed(
        title = "검색결과",
        description = "재생목록",
        color=0x049e46
    )

    for i in range(0,5):
        entireNum = entire[i]
        영상제목 = entireNum.text.strip()
        hyper = entireNum.get('href')
        link = "https://www.youtube.com"+hyper

        embed.add_field(name=str(i + 1) + "번쨰 영상", value = "\n" + "[%s](<%s>)" % (영상제목, link),inline=False)
        searchyoutube[i] = link
        request_title[i]=(영상제목)

    driver.quit()
    
    await ctx.channel.send(embed=embed)








@client.command(name='#',pass_context = True)
async def choose(ctx,num : int):
    server = ctx.guild
    vs2 = server.voice_client
    if vs2.is_playing():
        if not searchyoutube:
            embed = discord.Embed(title="검색한 영상이 없습니다", color=0x049e46)
        else:
            Song_Title.append(request_title[num -1])
            bookmc.append(searchyoutube[num-1])
            embed = discord.Embed(title="현재 재생중이어서 대기열목록에 추가되었습니다 \n대기열은 #목록에서 확인하세요.", color=0x049e46)
    else:
        if os.path.isfile(file):
            os.remove(file)
        if not searchyoutube:
            await  ctx.channel.send("검색한 영상이 없습니다")
        else:
            server = ctx.guild
            vs2 = server.voice_client
            url = searchyoutube[num - 1]
            player = await YTDLSource.from_url(url)
            Song_Title.append(player.title)
            vs2.play(player, after = lambda e: play_next(ctx))
            embed = discord.Embed(description=f"현재 재생중인 곡: \n{player.title}" + "\n[" + "<@" + str(ctx.author.id) + ">" + "]", color=0x049e46)

    for i in range(0,5):
        del searchyoutube[i]
        del request_title[i]
    await ctx.channel.send(embed=embed)

@client.command(name = '정지', pass_context = True)
async def pause(ctx):
    server = ctx.guild
    vs2 = server.voice_client
    if vs2.is_playing():
        vs2.pause()
    else:
        await ctx.send("재생중인 노래가 없습니다")

@client.command(name = '재생', pass_context = True)
async def resume(ctx):
    server = ctx.guild
    vs2 = server.voice_client
    if vs2.is_paused():
        vs2.resume()
    else:
        await ctx.send("일시정지중인 노래가 없습니다")

@client.command(aliases = ['다음','스킵','skip'], pass_context = True)
async def song_next(ctx):
    server = ctx.guild
    vs2 = server.voice_client
    if vs2.is_playing():
        vs2.stop()
        play_next(ctx)
    else:
        embed = discord.Embed(description="현재 재생중인 노래가 없습니다.")
    await ctx.channel.send(embed=embed)

    
@client.command(name = '목록', pass_entext = True)
async def Blist(ctx):
    Numlist = len(bookmc)
    embed = discord.Embed(
        title = "대기열목록",
        description = "재생목록",
        color=0x049e46
    )
    for i in range(0,Numlist):
        embed.add_field(name=str(i + 1) + "번쨰 영상", value = "\n" + "(<%s>)" % (Song_Title[i+1]),inline=False)
    await ctx.channel.send(embed=embed)

@client.command(name = "취소", pass_entext = True)
async def sakze(ctx,num : int):
    del bookmc[num -1]
    del Song_Title[num]
    embed = discord.Embed(title=str(num) + "번째 대기영상이 삭제되었습니다.", color=0x049e46)
    await ctx.channel.send(embed=embed)

@client.command(name = "확인",pass_entext = True)
async def song_title(ctx):
    server = ctx.guild
    vs2 = server.voice_client
    if not vs2.is_playing():
        embed = discord.Embed(title="현재 재생중인 곡이 없습니다.", color=0x049e46)
    else:
        if len(Song_Title) == 1:
            embed = discord.Embed(title="현재 재생중인 곡: \n(<%s>) \n 다음 곡: \n없습니다."%(Song_Title[0]), color=0x049e46)
        else:
            embed = discord.Embed(title="현재 재생중인 곡: \n(<%s>) \n 다음 곡: \n(<%s>)"%(Song_Title[0],Song_Title[1]), color=0x049e46)
        
    await ctx.channel.send(embed=embed)
    
    


'''@client.event
async def on_message(message):
    if message.author.bot:
        return None

    if message.author == client.user:
        return

    if message.content.startswith("#help"):
        embed=discord.Embed(title="Example Embed", description="이것은 Embed입니다.", color=0x00ff56)
        embed.set_thumbnail(url="https://miro.medium.com/max/1033/1*MAsNORFL89roPfIFMBnA4A.jpeg")
        await message.channel.send(embed=embed)
    
    if message.content.startswith("안녕"):
        channel = message.channel
        await channel.send("반가워")
'''
client.run(token)