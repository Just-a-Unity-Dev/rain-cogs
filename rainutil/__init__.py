from .rainutil import RainUtils

def setup(bot):
    bot.add_cog(RainUtils(bot))