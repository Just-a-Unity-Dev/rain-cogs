from redbot.core import commands, Config, checks
from pathlib import Path
import discord
import random

class RainCogs(commands.Cog):
	"""multipurpose cog"""

	def __init__(self, bot) -> None:
		self.bot = bot
		self.script_location = Path(__file__).absolute().parent
		self.config = Config.get_conf(self, 23975432657)
		with open(self.script_location / "gifs.txt", "r") as f:
			self.gifs = [line.rstrip() for line in f]
		default_guild = {
			"blessrole": None
		}
		self.config.register_guild(**default_guild)

	@commands.group()
	async def rain(self, ctx: commands.Context) -> None:
		"""
		it's a cold cog, afterall.
		"""
		pass

	@rain.group()
	@checks.admin_or_permissions(manage_guild=True)
	async def config(self, ctx: commands.Context) -> None:
		"""
		configuration for rain cogs
		"""
		pass

	@rain.command()
	async def manifest(self, ctx: commands.Context) -> None:
		"""the true manifestation"""
		return await ctx.reply(content="my physical manifestation... a plushie!", file=discord.File(self.script_location / "rain.png"))

	@config.command(name="blessrole")
	async def config_blessrole(self, ctx: commands.Context, blessRole) -> None:
		"""set the bless role (role id)"""
		if blessRole is None:
			await self.config.guild(ctx.guild).blessrole.set(None)
			return await ctx.reply("Reset the value of `blessrole` to `None`")
		await self.config.guild(ctx.guild).blessrole.set(int(blessRole))
		return await ctx.reply(f"Set the value of `blessrole` to `{str(int(blessRole))}`")

	async def blessing(self, ctx: commands.Context, target: discord.Member, roleToggle: bool):
		guild = ctx.guild
		blessed_role = await self.config.guild(guild).blessrole()
		role = guild.get_role(blessed_role)
		try:
			if roleToggle == True:
				await target.add_roles(role, reason="blessed")
				return await ctx.reply(content=f"blessed {target.mention}")
			else:
				await target.remove_roles(role, reason="deblessed")
				return await ctx.reply(content=f"deblessed {target.mention}")
		except discord.errors.Forbidden:
			return await ctx.reply("the server admin didn't set up roles correctly, uh oh!\n\n*just so you know, this is not your fault. ping a server admin to fix this.*")

	@rain.command(aliases=["gif"])
	async def rgif(self, ctx: commands.Context, gif: int = None):
		"""the AI will send you one random gif for free"""
		gifId = gif or random.randint(0, len(self.gifs) - 1)

		if gif is not None:
			try:
				return await ctx.reply(f"<:manifest:1019605971410096250> **#{gifId}**\n{self.gifs[gif + 1]}")
			except IndexError:
				return await ctx.reply(f"there was an error trying to get GIF #{gif + 1}, perhaps it doesn't exist?")

		return await ctx.reply(f"<:manifest:1019605971410096250> **#{gifId}**\n{self.gifs[gifId]}")
	

	@rain.command()
	@checks.admin_or_permissions(manage_roles=True)
	async def bless(self, ctx: commands.Context, target: discord.Member) -> None:
		"""
		verifies a user
		"""
		if not target:
			return await ctx.send_help()
		if ctx.me is target:
			return await ctx.reply("you cant bless me! i'm already blessed internally!")
		if ctx.author is target:
			return await ctx.reply("you cant bless yourself!")

		blessed_role = await self.config.guild(ctx.guild).blessrole()
		if not blessed_role:
			return await ctx.reply("the server admin didn't set up bless roles correctly, uh oh!\n\n*just so you know, this is not your fault. ping a server admin to fix this.*")
		await self.blessing(ctx, target, True)
	
	@rain.command(aliases=["shadowrealm", "debless"])
	@checks.admin_or_permissions(manage_roles=True)
	async def unbless(self, ctx: commands.Context, target: discord.Member) -> None:
		"""
		deverifies a user
		"""
		if not target:
			return await ctx.send_help()
		if ctx.me is target:
			return await ctx.reply("you cant unbless me!")
		if ctx.author is target:
			return await ctx.reply("you cant unbless yourself!")
		blessed_role = await self.config.guild(ctx.guild).blessrole()
		if not blessed_role:
			return await ctx.reply("the server admin didn't set up bless roles correctly, uh oh!\n\n*just so you know, this is not your fault")
		await self.blessing(ctx, target, False)
