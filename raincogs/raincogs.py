from redbot.core import commands, Config, checks
from pathlib import Path
import discord
import random

class RainCogs(commands.Cog):
	"""multipurpose cog"""

	def __init__(self, bot) -> None:
		self.bot = bot
		self.script_location = Path(__file__).absolute().parent
		self.config = Config.get_conf(self, 785463735624)
		with open(self.script_location / "gifs.txt", "r") as f:
			self.gifs = [line.rstrip() for line in f]

	@commands.group(aliases=["rain", "rf"])
	async def rainfun(self, ctx: commands.Context) -> None:
		"""
		rainfun - fun version of raincogs
		"""
		pass

	@rainfun.group()
	@checks.admin_or_permissions(manage_guild=True)
	async def config(self, ctx: commands.Context) -> None:
		"""
		configuration for rain cogs
		"""
		pass

	@rainfun.command()
	async def manifest(self, ctx: commands.Context) -> None:
		"""the true manifestation"""
		return await ctx.reply(content="my physical manifestation... a plushie!", file=discord.File(self.script_location / "rain.png"))

	@rainfun.command(aliases=["gif"])
	async def rgif(self, ctx: commands.Context, gif: int = None):
		"""the AI will send you one random gif for free"""
		gifId = gif or random.randint(0, len(self.gifs) - 1)

		if gif is not None:
			try:
				return await ctx.reply(f"<:manifest:1019605971410096250> **#{gifId}**\n{self.gifs[gifId]}")
			except IndexError:
				return await ctx.reply(f"there was an error trying to get GIF **#{gifId}**, perhaps it doesn't exist?")

		return await ctx.reply(f"<:manifest:1019605971410096250> **#{gifId}**\n{self.gifs[gifId]}")
