from discord.ext import commands
from discord import File as send_file
from discord import utils, RawReactionActionEvent, Colour
from .KTSHelper import KTSHelper
from datetime import date
import logging

FORMAT = "[%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
logging.basicConfig(filename='bot.log', level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class TournamentCog(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command(name='teilnehmer', help="Exportiere alle Teilnehmer für KTS")
    async def participants(self, ctx, ):
        """
        Reads all users reacted to the most recent message in #anmeldung
        Constructs a list of these users in form of "lastname, first name"
        Let build an xml-Tournament file and sends it
        """
        if not any(role.name in ['Judge', 'Content Creator'] for role in ctx.message.author.roles):
            return None
        channel = utils.get(ctx.guild.channels, name="📝anmeldung")
        message = await channel.fetch_message(967204036271013939)
        participants = []
        for reaction in message.reactions:
            async for user in reaction.users():
                u = await self.bot.fetch_user(user.id)
                if not u.name == "YGOTournamentBot":
                    participants.append(
                        str(u.name) + "," + str(u.discriminator))
        tourney_name = "Muri-locals-" + date.today().strftime("%Y-%m-%d")
        kts = KTSHelper(name=tourney_name, players=participants)
        tournament_file = kts.get_xml()
        with open(tournament_file, "rb") as f:
            await ctx.channel.send("Hier die Tournament-Datei:", file=send_file(f, tournament_file))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """
        grants the Event Role on reacting to the latest message in #anmeldung
        """
        guild = self.bot.get_guild(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)
        role = utils.get(guild.roles, name="Event")
        user = utils.get(guild.members, id=payload.user_id)
        if channel.name == "anmeldung":
            await user.add_roles(role, reason="Tournament SignUp")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        """
        removes the Event role from a user when he is withdrawing his reaction to the most recent message in #anmeldung
        """
        guild = self.bot.get_guild(payload.guild_id)
        channel = self.bot.get_channel(payload.channel_id)
        role = utils.get(guild.roles, name="Event")
        user = utils.get(guild.members, id=payload.user_id)
        if channel.name == "anmeldung":
            await user.aremove_roles(role, reason="Tournament SignUp")


def setup(bot):
    bot.add_cog(TournamentCog(bot))
