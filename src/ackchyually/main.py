import re
import sys
import json
from typing import Optional

import nextcord
from nextcord.ext import commands
import click
import openai
from pytube import YouTube

from ackchyually.openai.message_compartmentalizer import OpenAIMessageCompartmentalizer
from ackchyually.prompt import Prompt
from ackchyually.transcription.youtube_video import YouTubeVideoTranscriber
from ackchyually.youtube.pytube_video_id import PyTubeVideoId

def extract_youtube_url(content) -> Optional[str]:
    youtube_url_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    youtube_url = youtube_url_pattern.findall(content)
    if youtube_url:
        youtube_url = youtube_url[0][0] + youtube_url[0][1] + youtube_url[0][2] + '.' + youtube_url[0][3] + '/' + youtube_url[0][4] + youtube_url[0][5]
        return str(youtube_url)
    return None

@click.command()
@click.argument("url")
@click.option("--oa-api-key", "-k", help="OpenAI API key")
def main(url: str, oa_api_key: str) -> None:
    video_id = PyTubeVideoId(url=url)
    if video_id is None:
        sys.stderr.write("Video not found \n")
        sys.exit(1)

    transcript = YouTubeVideoTranscriber().transcribe_video(video_id=video_id)
    if transcript is None:
        sys.stderr.write("Video transcript not available\n")
        sys.exit(1)

    openai.api_key = oa_api_key
    message_compartmentalizer = OpenAIMessageCompartmentalizer(
        max_token_limit=OpenAIMessageCompartmentalizer.MAX_GPT_3_5_TURBO_TOKENS
    )
    parts = message_compartmentalizer.compartmentalize_message(message=transcript)
    messages = [
        {"role": "system", "content": "You are a media critic assistant"},
        {"role": "user", "content": Prompt.VERY_CRITICAL},
    ]
    for part in parts:
        messages.append({"role": "user", "content": part})
        messages.append({"role": "system", "content": "OK"})
    messages.append({"role": "user", "content": "Give me the final result. Only output the JSON and nothing else."})
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    except openai.error.InvalidRequestError:
        sys.stderr.write("Video transcript too long\n")
        sys.exit(1)
    print(response["choices"][0]["message"]["content"])

@click.command()
@click.option("--dc-api-key", "-d", help="Discord API key")
@click.option("--oa-api-key", "-k", help="OpenAI API key")
def runbot(dc_api_key: str, oa_api_key: str) -> None:
    intents = nextcord.Intents.default()
    bot = commands.Bot(intents=intents)

    @bot.event
    async def on_ready() -> None:
        print(f"Logged in as {bot.user}")

    @bot.slash_command(description="Critique YouTube video", guild_ids=[755881283074261022, 572880907682447380])
    async def yt(interaction: nextcord.Interaction, youtube_url: str) -> None:
        try:
            sys.stderr.write(f"User {interaction.user} requested {youtube_url}\n")
            await interaction.response.defer()
            video_id = PyTubeVideoId(url=youtube_url)
            if video_id is None:
                await interaction.followup.send("Video not found")
                return

            transcript = YouTubeVideoTranscriber().transcribe_video(video_id=video_id)
            if transcript is None:
                await interaction.followup.send("Video transcript not available")
                return

            openai.api_key = oa_api_key
            message_compartmentalizer = OpenAIMessageCompartmentalizer(
                max_token_limit=OpenAIMessageCompartmentalizer.MAX_GPT_3_5_TURBO_TOKENS,
            )
            parts = message_compartmentalizer.compartmentalize_message(message=transcript)
            messages = [
                {"role": "system", "content": "You are a media critic assistant"},
                {"role": "user", "content": Prompt.VERY_CRITICAL},
            ]
            for part in parts:
                messages.append({"role": "user", "content": part})
                messages.append({"role": "system", "content": "OK"})
            messages.append({"role": "user", "content": "Give me the final result. Only output the JSON and nothing else."})
            try:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            except openai.error.InvalidRequestError:
                await interaction.followup.send("Video transcript too long")
                return
            vid =YouTube(youtube_url)
            data = json.loads(response["choices"][0]["message"]["content"])
            embed = nextcord.Embed(
                title=vid.title,
                color=nextcord.Color.red()
            )
            embed.set_author(name='YouTube', url='https://www.youtube.com/', icon_url='https://upload.wikimedia.org/wikipedia/commons/7/75/YouTube_social_white_squircle_%282017%29.svg')
            embed.set_image(url=vid.thumbnail_url)
            embed.add_field(name='Watch', value=f'[Click here to watch]({youtube_url})', inline=False)
            embed.add_field(name="Summary", value=data["summary"], inline=False)
            embed.add_field(name="Reliability score", value=data["score"], inline=False)
            embed.add_field(name="False statements", value="\n".join(data["factcheck"]["false"]) or "None", inline=False)
            embed.add_field(name="Misleading statements", value="\n".join(data["factcheck"]["misleading"]) or "None", inline=False)
            embed.add_field(name="Important ommisions", value="\n".join(data["factcheck"]["omission"]) or "None", inline=False)
            embed.add_field(name="Bias instances", value="\n".join(data["factcheck"]["bias"]) or "None", inline=False)

            await interaction.followup.send(embed=embed)
        except Exception as error:
            sys.stderr.write(f"{error}\n");
            await interaction.followup.send("Gah!")


    bot.run(dc_api_key)


if __name__ == "__main__":
    main()
