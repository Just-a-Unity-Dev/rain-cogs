from io import BytesIO
import aiohttp
import discord
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

	@rainutil.command(name="poll")
	async def poll_command(self, ctx: commands.Context, question: str, ranswers: str):
		"""
		poll command
		this one is fairly advanced so theres that
		syntax: poll "ques tion" "answer1,answer2,answer3,etc"
		the first argument is the question which you can include spaces by "wrapping quotes around them"
		second question are the answers, wrapped around in quotes, only up to 9 are allowed.
		seperate each answer with , so you get "answer1,answer2,answer3" and etc
		"""
		numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
		output = []
		answers = ranswers.split(",")
		output.append(f"Question: **{question}** *by {ctx.author.mention}*\n")
		for i, answer in enumerate(answers):
			output.append(f":{numbers[i]}: - {answer}\n")
		message = await ctx.send(answers)
		for i, answer in enumerate(answers):
			message.add_reaction(numbers[i])

	@rainutil.command(name="steal")
	@checks.admin_or_permissions(manage_emojis=True)
	async def emoji_steal(self, ctx: commands.Context, emoji: discord.PartialEmoji) -> None:
		"""steals an emoji of your choice"""
		guild = ctx.guild
		url = emoji.url
		async with aiohttp.ClientSession() as ses:
			async with ses.get(url) as r:
				try:
					image = BytesIO(await r.read())
					binary = image.getvalue()
					if r.status is 200:
						emote: discord.Emoji = await guild.create_custom_emoji(image=binary,name=emoji.name)
						await ctx.reply(f"emoji `{emote.name}` created")
						return ses.close()
				except discord.HTTPException:
					return await ctx.reply("this emoji is too big!")

	@rainutil.group()
	@checks.admin_or_permissions(manage_guild=True)
	async def config(self, ctx: commands.Context) -> None:
		"""
		configuration for rain util
		"""
		pass

	@rainutil.group()
	async def roblox(self, ctx: commands.Context):
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
