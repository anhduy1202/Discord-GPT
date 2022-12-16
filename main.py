import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import openai
import requests


load_dotenv()
BOT_TOKEN = os.getenv('ACCESS_TOKEN')
openai.api_key = os.getenv("OA_TOKEN")
OA_TOKEN = openai.api_key
openai.Model.list()
ROOT = "https://api.openai.com/v1"
HEADERS = {"Authorization": f"Bearer {OA_TOKEN}"}

intents = discord.Intents(messages=True, message_content=True)
client = commands.Bot(command_prefix="gpt!", intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} is ready")

# GET ALL MODELS


@client.command()
async def models(ctx):
    res = requests.get(f"{ROOT}/models",  headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        print("GET request was successful. Response data:", data)
    else:
        print("GET request failed with status code:", res.status_code)
    await ctx.send("hello")


# CREATE IMAGES
@client.command()
async def images(ctx, arg):
    payload = {"prompt": f"{arg}"}
    res = requests.post(f"{ROOT}/images/generations",
                        json=payload, headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        url = data['data'][0]['url']
        embed = discord.Embed()
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    else:
        print("POST request failed with status code:", res.status_code)

client.run(BOT_TOKEN)
