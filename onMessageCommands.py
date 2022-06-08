import discord
from discord.ext import commands
from datetime import date
import calendar

#ctx is context
async def league(ctx):
    await ctx.channel.send(f"Ew League :poop: {ctx.author.mention}")

#joke event
async def devourQuote(ctx):
    msg = calendar.day_name[date.today().weekday()]
    await ctx.channel.send(f"Today is Devour {msg} :smiling_imp: {ctx.author.mention}!")
