import discord
import os
import random
import time
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='!', case_insensitive=True,
                   intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following servers: \n')
    for server in bot.guilds:
        print(f'\n\n {server.name} (id:{server.id})')

        members = '\n - ' .join([member.name for member in server.members])
        print(f'Server members: \n - {members}')

    # for guild in bot.guilds:
    #     await guild.system_channel.send("Beep boop")


@bot.event
async def on_member_join(member):
    await member.guild.system_channel.send(f'{member.name} has joined the server!')


@bot.command(name='paid', help='Tells you if you paid your fee this week')
@commands.has_role('Admin')
async def has_user_paid(ctx):
    # Not implemented yet...
    await ctx.send(random.choice(['Yes', 'No']))


@bot.command(name='changeroles', help='Resets your roles, and allows you to assign new ones.')
@commands.has_role('Raider')
async def change_role(ctx):
    # Deleting the user command
    await ctx.message.delete()

    # Clearing all roles on user
    await ctx.author.remove_roles(get(ctx.guild.roles, name='Tank'))
    await ctx.author.remove_roles(get(ctx.guild.roles, name='Healer'))
    await ctx.author.remove_roles(get(ctx.guild.roles, name='DPS'))

    # Creating embed that shows roles
    embed = discord.Embed(
        title=f'Changing roles for **{ctx.author.name}**', 
        description=f'**{ctx.author.name}** currently has roles: '
    )

    # Sends the embed that gets deleted after 60 seconds
    message = await ctx.send(embed=embed, delete_after=60)

    # Adds the three reactions to the message
    await message.add_reaction(bot.get_emoji(784901512882552843))
    await message.add_reaction(bot.get_emoji(784902181857525760))
    await message.add_reaction(bot.get_emoji(784902194704285726))


@bot.event
async def on_reaction_add(reaction, user):
    # If the bot adds reactions, return (ignore them)
    if user.bot:
        return

    # Go through users roles, and add current ones to roles[]
    roles = []
    for role in user.roles:
        if str(role) in ['Tank', 'Healer', 'DPS']:
            roles.append('**'+str(role)+'**')

    # Add the role to roles[] given the reaction type
    if str(reaction) == '<:tank:784901512882552843>':
        await user.add_roles(get(reaction.message.guild.roles, name='Tank'))
        roles.append('**Tank**')
    elif str(reaction) == '<:healer:784902181857525760>':
        await user.add_roles(get(reaction.message.guild.roles, name='Healer'))
        roles.append('**Healer**')
    elif str(reaction) == '<:dps:784902194704285726>':
        await user.add_roles(get(reaction.message.guild.roles, name='DPS'))
        roles.append('**DPS**')
    else:
        # If a user reacts with another emoji, remove it instantly
        await reaction.remove(user)

    roles.sort(reverse=True)

    # Create the embed again, this time with the updated roles. Add a new field for each role
    embed = discord.Embed(
        title=f'Changing roles for **{user.name}**', description=f'{user.name} currently has roles: ')
    if '**Tank**' in roles:
        embed.add_field(
            name='Tank', value='<:tank:784901512882552843>', inline=True)
    if '**Healer**' in roles:
        embed.add_field(
            name='healer', value='<:healer:784902181857525760>', inline=True)
    if '**DPS**' in roles:
        embed.add_field(
            name='dps', value='<:dps:784902194704285726>', inline=True)

    # Edits the current message with the updated embed
    await reaction.message.edit(embed=embed)


@bot.event
async def on_reaction_remove(reaction, user):
    # If the bot removes reactions, return (ignore them)
    if user.bot:
        return

    # Remove the role of user based on reaction removed
    if str(reaction) == '<:tank:784901512882552843>':
        await user.remove_roles(get(reaction.message.guild.roles, name='Tank'))
    elif str(reaction) == '<:healer:784902181857525760>':
        await user.remove_roles(get(reaction.message.guild.roles, name='Healer'))
    elif str(reaction) == '<:dps:784902194704285726>':
        await user.remove_roles(get(reaction.message.guild.roles, name='DPS'))

    # Go through users roles, and add current ones to roles[]
    roles = []
    for role in user.roles:
        if str(role) in ['Tank', 'Healer', 'DPS']:
            roles.append('**'+str(role)+'**')
    roles.sort(reverse=True)

    # Create new embed based on new roles
    embed = discord.Embed(
        title=f'Changing roles for **{user.name}**', description=f'{user.name} currently has roles: ')
    if '**Tank**' in roles:
        embed.add_field(
            name='Tank', value='<:tank:784901512882552843>', inline=True)
    if '**Healer**' in roles:
        embed.add_field(
            name='healer', value='<:healer:784902181857525760>', inline=True)
    if '**DPS**' in roles:
        embed.add_field(
            name='dps', value='<:dps:784902194704285726>', inline=True)

    # Edit the message with newly updated embed
    await reaction.message.edit(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRole):
        await ctx.send('You do not have the correct role for this command')

bot.run(os.getenv('DISCORD_TOKEN'))
