from redbot.core import commands, Config, checks
from pathlib import Path
import requests

class RainUtil(commands.Cog):
	"""multipurpose cog"""

	def __init__(self, bot) -> None:
		self.bot = bot
		self.script_location = Path(__file__).absolute().parent
		self.config = Config.get_conf(self, 635473658356)
		# default_guild = {
		# 	"blessrole": None
		# }
		# self.config.register_guild(**default_guild)

	@commands.group(aliases=["ru"])
	async def rainutil(self, ctx: commands.Context) -> None:
		"""
		rainutil - the utility part of raincogs
		"""
		pass

	@rainutil.group()
	@checks.admin_or_permissions(manage_guild=True)
	async def config(self, ctx: commands.Context) -> None:
		"""
		configuration for rain util
		"""
		pass

	@rainutil.group()
	async def roblox():
		"""roblox utility commands"""
		pass

	@roblox.command(name="get_user")
	async def roblox_getUser(self, ctx: commands.Context, user: str):
		"""gets the user with a userid/username"""
		usernameAPI = f"https://api.roblox.com/users/get-by-username?username={user}"
		request = requests.get(usernameAPI, timeout=5)
		json = request.json()
		if 'errorMessage' in json:
			return await ctx.reply("an error occured while getting that user, are you sure they exist?")
		await ctx.reply(f"**Username**: {json['Username']}\n**UserID**: {json['Id']}\n**Online**: `{json['IsOnline']}`\n")
