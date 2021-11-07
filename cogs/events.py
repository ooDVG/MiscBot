import discord
from discord.ext import commands
from discord.ext.commands.core import command
from cogs.utils import utilities as utils

class Events(commands.Cog, name="Events"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Staff")
    async def completechallenge(self, ctx, member: discord.Member, challenge_index: int, scaled_challenge_points: int=1):
        name, uuid = await utils.get_dispnameID(await utils.name_grabber(member))
        # Calculate points based on challenge
        if challenge_index == 1:
            points_earned = scaled_challenge_points
        elif challenge_index == 2:
            points_earned = 2
        elif challenge_index == 3:
            points_earned = 1
        else:
            await ctx.send("Invalid challenge number! Please enter a number between 1 and 3!")
            return

        # Check if member is in guild/allied or not
        if await utils.get_guild(name) != "Miscellaneous" and await utils.get_guild(name) not in self.bot.misc_allies:
            points_earned *= 0.75

        # Get data from db
        row = await self.get_player(uuid)

        if row != None:
            uuid, total_points, completed_challenges = row
            total_points += points_earned
            completed_challenges += 1
            await self.update_value(uuid, total_points, completed_challenges)
        else:
            total_points = points_earned
            completed_challenges = 1
            await self.insert_new(uuid, total_points, completed_challenges)
        
        # Send player's overall stats
        embed = discord.Embed(title=f"Event statistics - {name}", description=f"**Scaled points earned:** {points_earned}\n**Total points:** {total_points}\n**Challenges completed:** {completed_challenges}", color=0x8368ff)
        await ctx.send(embed=embed)


    
    @commands.command()
    @commands.has_role("Staff")
    async def addpoints(self, ctx, member: discord.Member, points: int):
        name, uuid = await utils.get_dispnameID(await utils.name_grabber(member))
        row = await self.get_player(uuid)

        if row == None:
            await self.insert_new(uuid, points, 0)
            completed_challenges = 0
        else:
            uuid, total_points, completed_challenges = row
            await self.update_value(uuid, total_points + points, completed_challenges)
            points = total_points

        # Send player's overall stats
        embed = discord.Embed(title=f"Event statistics - {name}", description=f"**Total points:** {points}\n**Challenges completed:** {completed_challenges}", color=0x8368ff)
        await ctx.send(embed=embed)


        
    @commands.command()
    @commands.has_role("Staff")
    async def removepoints(self, ctx, member: discord.Member, points: int):
        name, uuid = await utils.get_dispnameID(await utils.name_grabber(member))
        row = await self.get_player(uuid)

        if row == None:
            await self.insert_new(uuid, points, 0)
            completed_challenges = 0
        else:
            uuid, total_points, completed_challenges = row
            points = total_points - points
            await self.update_value(uuid, points, completed_challenges)

        # Send player's overall stats
        embed = discord.Embed(title=f"Event statistics - {name}", description=f"**Total points:** {points}\n**Challenges completed:** {completed_challenges}", color=0x8368ff)
        await ctx.send(embed=embed)




    async def insert_new(self, uuid, points, challenges):
        await self.bot.db.execute("INSERT INTO event VALUES (?, ?, ?)", (uuid, points, challenges,))
        await self.bot.db.commit()

    async def update_value(self, uuid, points, completed=None):
        if completed == None:
            await self.bot.db.execute("UPDATE event SET points = (?) WHERE uuid = (?)", (points, uuid,))
        else:
            await self.bot.db.execute("UPDATE event SET points = (?), completed = (?) WHERE uuid = (?)", (points, completed, uuid,))
        await self.bot.db.commit()

    async def get_player(self, uuid):
        cursor = await self.bot.db.execute("SELECT * FROM event WHERE uuid = (?)", (uuid,))
        row = await cursor.fetchone()
        await cursor.close()
        return row


def setup(bot):
    bot.add_cog(Events(bot))