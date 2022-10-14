from io import BytesIO
import aiohttp
import asyncio
import base64
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
		default_guild = {
			"servers": {}
		}
		self.config.register_guild(**default_guild)

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
		numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
		emojinumbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
		output = []
		answers = ranswers.split(",")
		output.append(f"Question: **{question}** *by {ctx.author.mention}*")
		for i, answer in enumerate(answers):
			output.append(f":{numbers[i]}: - {answer}")
		message = await ctx.send('\n'.join(output))
		for i, answer in enumerate(answers):
			await message.add_reaction(emojinumbers[i])

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
					if r.status == 200:
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

	@config.command(name="addserver")
	async def config_addserver(self, ctx: commands.Context, name, server_url, instance, api_key) -> None:
		"""USE THIS COMMAND IN A DM. THIS MAY RESULT IN LEAKING YOUR WATCHDOG API KEY."""
		if name is None:
			return await ctx.reply("Lacking a `name`.")
		if instance is None:
			return await ctx.reply("Lacking an `instance`.")
		if server_url is None:
			return await ctx.reply("Lacking a `server_url`.")
		if api_key is None:
			return await ctx.reply("Lacking a `api_key`.")
		async with self.config.guild(ctx.guild).servers() as servers:
			servers[name] = {
				"url": server_url,
				"key": instance,
				"token": api_key
			}
		return await ctx.reply(f"Created new server {name}.")
	
	@config.command("removeserver")
	async def config_removeserver(self, ctx: commands.Context, name):
		if name is None:
			return await ctx.reply("Lacking a `name`.")
		
		async with self.config.guild(ctx.guild).servers() as servers:
			if name not in servers:
				await ctx.send("That server did not exist.")
				return

			del servers[name]

		return await ctx.reply(f"Removed server {name}.")

	@rainutil.command(name="restart")
	@checks.admin_or_permissions(manage_guild=True)
	async def restart(self, ctx: commands.Context, name):
		if name is None:
			return await ctx.reply("Lacking a `name`.")
		
		await ctx.message.add_reaction("⏰")

		async with self.config.guild(ctx.guild).servers() as servers:
			if name not in servers:
				return await ctx.send("That server did not exist.")
			config = servers[name]
			if config is None:
				return await ctx.reply("That isn't a valid server.")
			try:
				base_url = config["url"]
				instance = config["key"]
				token = config["token"]

				url = base_url + f"/instances/{instance}/restart"
				auth_header = "Basic " + base64.b64encode(f"{instance}:{token}".encode("ASCII")).decode("ASCII")

				await ctx.reply(f"{url}, {auth_header}")

				async with aiohttp.ClientSession() as session:
					async def load():
						async with session.post(url, headers={"Authorization": auth_header}) as resp:
							if resp.status != 200:
								await ctx.reply(f"Wrong status code: {resp.status}")
							else:
								return await ctx.reply(f"Restarted `{name}`")
					await asyncio.wait_for(load(), timeout=5)
			except asyncio.TimeoutError:
				return await ctx.reply("Server timed out.")
			except Exception as err:
				# wtf
				return await ctx.reply(f"Unexpected error occurred: {repr(err)}")
