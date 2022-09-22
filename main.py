import os
from dotenv import load_dotenv
import logging
import KTSHelper
from datetime import date
import discord


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
FORMAT = "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
logging.basicConfig(filename='bot.log', level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SCOPE = [int(guild) for guild in os.getenv('GUILD_ID').split(',')]
PERMITTED_ROLES = [int(role) for role in os.getenv('PERMISSIONS').split(',')]
SIGNUP_CHANNEL = int(os.getenv('SIGNUP_CHANNEL'))

bot = discord.Bot(debug_guilds=SCOPE)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.member != bot.user and payload.emoji.name in ['🔵', '🔴']:
        role = None
        guild = await bot.fetch_guild(payload.guild_id)
        for r in guild.roles:
            if r.name == 'Event':
                role = r
                break
        if not role:
            return
        role_object = discord.Object(role.id)
        try:
            await payload.member.add_roles(role_object)
        except Exception as e:
            logger.exception(e)


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    if payload.emoji.name in ['🔵', '🔴']:
        role = None
        guild = await bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)
        for r in guild.roles:
            if r.name == 'Event':
                role = r
                break
        if not role:
            return
        role_object = discord.Object(role.id)
        try:
            await member.remove_roles(role_object)
        except Exception as e:
            logger.exception(e)


@bot.command(
    name="teilnehmer",
    description="creates KTS tournament file with all enrolled players"
)
async def participants(ctx: discord.ApplicationContext, message_id: str, emoji: str):
    """
    Reads all users reacted to the most recent message in #anmeldung
    Constructs a list of these users in form of "lastname, first name"
    Let build a xml-Tournament file and sends it
    """
    if not any(role.id in PERMITTED_ROLES for role in ctx.author.roles):
        await ctx.send("You don't have sufficient permissions!")
        return None
    message_id = int(message_id)
    signup_channel = None
    for channel in ctx.guild.channels:
        if channel.id == SIGNUP_CHANNEL:
            signup_channel = channel
    if not signup_channel:
        await ctx.send("Something went wrong")
        return
    message = await signup_channel.fetch_message(message_id)
    participant_members = []
    for reaction in message.reactions:
        if reaction.emoji == emoji:
            async for user in reaction.users():
                participant_members.append(str(user))
    tourney_name = "Muri-locals-" + date.today().strftime("%Y-%m-%d")
    tournament_file = KTSHelper.get_xml(name=tourney_name, players=participant_members)
    await ctx.channel.send("Hier die Tournament-Datei:", file=discord.File(tournament_file))


@bot.command(
    name='reset',
    description='Setzt alle Anmeldungen zurück'
)
async def reset_signups(ctx: discord.ApplicationContext, message_id: str):
    if not any(role.id in PERMITTED_ROLES for role in ctx.author.roles):
        await ctx.send("You don't have sufficient permissions!")
        return None
    message_id = int(message_id)
    signup_channel = None
    for channel in ctx.guild.channels:
        if channel.id == SIGNUP_CHANNEL:
            signup_channel = channel
    if not signup_channel:
        await ctx.send("Something went wrong")
        return
    message = await signup_channel.fetch_message(message_id)
    await message.clear_reactions()
    await ctx.send("Anmeldungen zurückgesetzt")
    await signup_channel.send("@everyone Anmeldungen sind nun wieder offen :)")


while True:
    try:
        bot.run(TOKEN)
    except Exception as e:
        if e is not RuntimeError:
            logger.error(e)
