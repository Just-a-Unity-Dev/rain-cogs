import discord
from redbot.core import commands, Config, checks

class RainCogs(commands.Cog):
	"""multipurpose cog"""

	def __init__(self, bot) -> None:
		self.bot = bot
		self.config = Config.get_conf(self, 23975432657)
		default_guild = {
			"bless_role": None
		}
		self.config.register_guild(**default_guild)

	@commands.group()
	async def rain(self) -> None:
		"""
		rain cogs - it's a cold cog
		"""
		pass

	@rain.group()
	@checks.admin_or_permissions(manage_guild=True)
	async def config(self) -> None:
		"""
		configuration for rain cogs
		"""
		pass

	@config.command()
	async def blessrole(self, ctx: commands.Context, blessRole) -> None:
		"""set the bless role (role id)"""
		await self.config.guild(ctx.guild)["bless_role"].set(int(blessRole))
		await ctx.reply(f"Set the value of `bless_role` to f{str(int(blessRole))}")

	@rain.command()
	@checks.admin_or_permissions(manage_roles=True)
	async def bless(self, ctx: commands.Context, target: discord.Member) -> None:
		"""
		verifies a user
		"""
		if not target:
			return await ctx.send_help()
		if ctx.me is target:
			return await ctx.send("you cant bless me, i'm already blessed!")
		if ctx.author is target:
			return await ctx.send("you cant bless yourself!")

		blessed_role = await self.config.guild(ctx.guild).bless_role()
		if not blessed_role:
			return await ctx.send("the server admin didn't set up bless roles correctly, uh oh!\n\n*just so you know, this is not your fault. ping a server admin to fix this.*")
		guild = ctx.guild
		role = guild.get_role(blessed_role)

		try:
			await target.add_roles(role, reason="blessed")
		except discord.errors.Forbidden:
			return await ctx.send("the server admin didn't set up roles correctly, uh oh!\n\n*just so you know, this is not your fault. ping a server admin to fix this.*")