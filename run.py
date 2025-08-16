import discord
import asyncio
import os
from dotenv import load_dotenv
from discord.ext import commands
from asset import *
from encrypt_morse import emorse
from decrypt_morse import dmorse
from ceaser_cipher import ceasercipher
from rot13_cipher import rot13cipher
from random import randint

# Load token from .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Configure bot
bot = commands.Bot(command_prefix=',', intents=discord.Intents.all())
bot.remove_command('help')


# EVENTS

@bot.event
async def on_ready():
    """Triggered when bot successfully logs in."""
    print("Bot is running...")


@bot.event
async def on_message(message):
    """Custom listener for keyword triggers."""
    if message.author.bot:
        return

    if "awkward silence" in message.content.lower():
        await message.channel.send(f"{message.author.mention} ...")

    elif "nextupdate" in message.content.lower():
        await message.channel.send(f"{message.author.mention} next update on 02.12.2021")

    await bot.process_commands(message)


# CIPHER COMMANDS

@bot.command(name="e_morse", description="Encrypt plain text to Morse code.")
async def e_morse(ctx, arg: str):
    """Encrypt plain text into Morse code."""
    result = emorse(arg)
    embed = discord.Embed(colour=discord.Colour.red())
    embed.add_field(name=result, value=f"Ciphered text of {arg}", inline=True)
    await ctx.send(embed=embed)


@bot.command(name="d_morse", description="Decrypt Morse code to plain text.")
async def d_morse(ctx, arg: str):
    """Decrypt Morse code back into plain text."""
    result = dmorse(arg)
    embed = discord.Embed(colour=discord.Colour.red())
    embed.add_field(name=result, value=f"Deciphered text of {arg}", inline=True)
    await ctx.send(embed=embed)


@bot.command(name="rot13", description="Encrypt text with Rot13 cipher.")
async def rot13(ctx, arg: str):
    """Apply Rot13 encryption (same function also decrypts)."""
    result = rot13cipher(arg)
    embed = discord.Embed(colour=discord.Colour.red())
    embed.add_field(name=result, value=f"Ciphered text of {arg}", inline=True)
    await ctx.send(embed=embed)


@bot.command(name="ceaser", description="Encrypt text with Caesar cipher. Args: text (quoted), shift (int).")
async def ceaser(ctx, text: str, shift: int):
    """Encrypt plain text using Caesar cipher with given shift."""
    result = ceasercipher(text, shift)
    embed = discord.Embed(colour=discord.Colour.red())
    embed.add_field(
        name=result,
        value=f"Ciphered text of {text} (shift {shift})",
        inline=True
    )
    await ctx.send(embed=embed)


@ceaser.error
async def ceaser_error(ctx, error):
    """Handle wrong Caesar cipher args."""
    if isinstance(error, commands.BadArgument):
        await ctx.send("Usage: ,ceaser \"text\" shift_number")


@bot.command(name="ceaserall", description="Display Caesar cipher results for all shifts (1–25).")
async def ceaserall(ctx, text: str):
    """Show Caesar cipher outputs for every shift (1–25)."""
    embed = discord.Embed(colour=discord.Colour.red(), title=f"Caesar Cipher Variants for: {text}")

    for shift in range(1, 26):
        result = ceasercipher(text, shift)
        embed.add_field(
            name=f"Shift {shift}",
            value=result,
            inline=True
        )

    await ctx.send(embed=embed)


# FUN COMMANDS

async def action_command(ctx, action: str, reason: str, gif_func):
    """Helper to avoid repetition in fun commands (slap, hug, etc)."""
    if reason in ["everyone", "everybody"]:
        msg = f"{ctx.author.mention} {action} everyone"
    else:
        msg = f"{ctx.author.mention} {action} {reason}"

    await ctx.send(msg)
    await ctx.send(gif_func(randint(0, 5)))


@bot.command()
async def slap(ctx, *, reason: str):
    """Slap someone with a random GIF."""
    await action_command(ctx, "slapped", reason, slapgif)


@bot.command()
async def spank(ctx, *, reason: str):
    """Spank someone with a random GIF."""
    await action_command(ctx, "spanked", reason, spankgif)


@bot.command()
async def hug(ctx, *, reason: str):
    """Hug someone with a random GIF."""
    await action_command(ctx, "hugged", reason, huggif)


@bot.command()
async def kiss(ctx, *, reason: str):
    """Kiss someone with a random GIF."""
    await action_command(ctx, "kissed", reason, kissgif)


@bot.command()
async def emoji(ctx, text: str = None):
    """Send a custom emoji."""
    await ctx.send("<:innocat:866885659784249364>")
    if text:
        await ctx.send(text)


# SNIPE COMMANDS 

snipe_message_author = {}
snipe_message_content = {}

@bot.event
async def on_message_delete(message):
    """Save deleted messages for snipe."""
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    await asyncio.sleep(60)
    snipe_message_author.pop(message.channel.id, None)
    snipe_message_content.pop(message.channel.id, None)


@bot.command(name='snipe')
async def snipe(ctx):
    """Retrieve the last deleted message."""
    channel = ctx.channel
    if channel.id in snipe_message_content:
        em = discord.Embed(
            title="Sniped message",
            description=snipe_message_content[channel.id],
            colour=discord.Colour.orange()
        )
        em.set_footer(text=f"~ {snipe_message_author[channel.id]}")
        await ctx.send(embed=em)
    else:
        await ctx.send("There's nothing to snipe.")


# SNIPE EDITTED MESSAGE
edit_snipe_message_author = {}
edit_snipe_message_content = {}

@bot.event
async def on_message_edit(before, after):
    """Save edited messages for edit snipe."""
    edit_snipe_message_author[before.channel.id] = before.author
    edit_snipe_message_content[before.channel.id] = before.content
    await asyncio.sleep(60)
    edit_snipe_message_author.pop(before.channel.id, None)
    edit_snipe_message_content.pop(before.channel.id, None)


@bot.command(name='editsnipe')
async def editsnipe(ctx):
    """Retrieve the last edited message."""
    channel = ctx.channel
    if channel.id in edit_snipe_message_content:
        em = discord.Embed(
            title="Edit Sniped",
            description=edit_snipe_message_content[channel.id],
            colour=discord.Colour.orange()
        )
        em.set_footer(text=f"Text before edit: ~ {edit_snipe_message_author[channel.id]}")
        await ctx.send(embed=em)
    else:
        await ctx.send(f"No recently edited messages in #{channel.name}.")


# UTILS 

@bot.command()
async def avatar(ctx, *, member: discord.Member = None):
    """Display avatar of a user (default: your own)."""
    member = member or ctx.author
    await ctx.send(member.avatar.url)


# HELP MENUS

@bot.command()
async def help(ctx):
    """Show cipher command help menu."""
    embed = discord.Embed(colour=discord.Colour.red())
    embed.set_author(name="Cipher Commands:")
    embed.add_field(name='ceaser', value='Encrypt text with Caesar cipher. Usage: ,ceaser "text" int', inline=False)
    embed.add_field(name='e_morse', value='Encrypt text to Morse. Usage: ,e_morse "text"', inline=False)
    embed.add_field(name='d_morse', value='Decrypt Morse to text. Usage: ,d_morse "morse"', inline=False)
    embed.add_field(name='rot13', value='Encrypt text with Rot13. Usage: ,rot13 "text"', inline=False)
    embed.add_field(name='ceaserall', value='Show Caesar cipher for all shifts.', inline=False)
    embed.add_field(name='help2', value='Show fun commands help.', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def help2(ctx):
    """Show fun command help menu."""
    embed = discord.Embed(colour=discord.Colour.orange())
    embed.set_author(name="Fun Commands:")
    commands_list = [
        "slap", "spank", "hug", "kiss",
        "snipe", "editsnipe", "avatar", "emoji"
    ]
    for cmd in commands_list:
        embed.add_field(name=cmd, value=f"Usage: ,{cmd} [arg]", inline=True)
    embed.add_field(name='help', value='Show cipher commands help.', inline=False)
    await ctx.send(embed=embed)


# RUN

bot.run(TOKEN)
