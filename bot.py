import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils import get_audio, convert
import ffmpeg
import asyncio

# Load env
load_dotenv()
TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')

ffmpeg_options = {
    'options': '-vn -bufsize 512k -af "volume=1"',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

audio_queue = asyncio.Queue()

async def joinVoiceChannel(ctx):
    if ctx.author.voice is None:
        await ctx.send('You need to be in a voice channel to use this command.')
        return

    author_voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        voice_client = await author_voice_channel.connect()
    else:
        await ctx.voice_client.move_to(author_voice_channel)

async def on_audio_finished(ctx):
    # Check if there are pending audio requests in the queue
    if not audio_queue.empty():
        # Dequeue the next audio request
        next_ctx, next_url = await audio_queue.get()
        # Play the next audio
        await sing(next_ctx, next_url)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def sing(ctx, url: str):
    await joinVoiceChannel(ctx)

    if ctx.voice_client.is_playing():
        # If the bot is already playing audio, enqueue the new request
        await audio_queue.put((ctx, url))
        await ctx.send("Added to queue.")
        return

    await joinVoiceChannel(ctx)

    audio_stream_info = get_audio(url)
    if audio_stream_info:
        title, _, audio_stream_url = audio_stream_info
        source = discord.FFmpegPCMAudio(audio_stream_url, **ffmpeg_options)
        await ctx.send(f'Playing: {title}')
        await ctx.send(f'Queue remains: {audio_queue.qsize()}')
        ctx.voice_client.play(source, after=lambda e: on_audio_finished(ctx))
    else:
        await ctx.send('No audio stream found.')

@bot.command()
async def compose(ctx, url: str, transpose: int, speed: float):
    if transpose == 0 and speed == 1.0:
        await ctx.send("Follow this template: >compose 'link' 'transpose' 'speed'")
        return

    await joinVoiceChannel(ctx)

    audio_stream_info = get_audio(url)
    if audio_stream_info:
        _, abr, audio_stream_url = audio_stream_info

        await ctx.send(f'Downloading audio stream with bitrate {abr}...')
        audio_file_path = f'static/modified/audio_{ctx.guild.id}.mp3'
        ffmpeg.input(audio_stream_url).output(audio_file_path).run(overwrite_output=True)
        await ctx.send(f'Transpose {transpose} and speed {int(speed*100)}%...')
        audio_file_path, _ = convert(audio_file_path, transpose=transpose, speed=speed)
        discord_audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(audio_file_path))
        ctx.voice_client.play(discord_audio_source)
        await ctx.send(f'Playing...')
    else:
        await ctx.send('No audio stream found.')

if __name__ == '__main__':
    bot.run(TOKEN)