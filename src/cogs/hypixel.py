import discord
from discord.ext import commands
from src.func.General import General
from src.func.String import String
from src.func.Union import Union
from src.utils.discord_utils import name_grabber


class Hypixel(commands.Cog, name="hypixel"):
    """
    All non-guild related Hypixel commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx, name: str, tag: str = None):
        """Update your discord nick, tag and roles!"""
        res = await Union(user=ctx.author).sync(ctx, name, tag)
        if isinstance(res, discord.Embed):
            await ctx.send(embed=res)
        elif isinstance(res, str):
            await ctx.send(res)

    @commands.command(aliases=['i'])
    async def info(self, ctx, name: str = None):
        """View Hypixel stats of the given user!"""
        if not name:
            name = await name_grabber(ctx.author)
        await ctx.send(embed=await String(string=name).info())

    @commands.command(aliases=['dnkladd'])
    @commands.has_permissions(manage_messages=True)
    async def Dnkl_Add(self, ctx, name: str):
        """Add a user to the do-not-kick-list!"""
        res = await String(string=name).dnkladd(ctx)
        if isinstance(res, str):
            await ctx.send(res)
        elif isinstance(res, discord.Embed):
            await ctx.send(embed=res)

    @commands.command(aliases=['dnklrmv'])
    @commands.has_permissions(manage_messages=True)
    async def DNKL_Remove(self, ctx, name: str):
        """Remove a player from the do-not-kick-list"""
        await ctx.send(await String(string=name).dnklremove())

    @commands.command(aliases=['dnkllist'])
    async def DNKL_List(self, ctx):
        """View all users on the do-not-kick-list!"""
        await ctx.send(embed=await General.dnkllist(ctx))

    @commands.command(aliases=['dnklchk'])
    async def DNKL_Check(self, ctx, name: str = None):
        """Check whether you are eligible for the do-not-kick-list!"""
        if not name:
            name = await name_grabber(ctx.author)

        res = await String(string=name).dnklcheck()
        if isinstance(res, discord.Embed):
            await ctx.send(embed=res)
        elif isinstance(res, str):
            await ctx.send(res)


def setup(bot):
    bot.add_cog(Hypixel(bot))
