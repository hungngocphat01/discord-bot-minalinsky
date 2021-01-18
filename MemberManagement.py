# This fine defines the MemberManagement module. It contains the following functions:

# premium
# allroles
# whois

import discord
from discord.ext import commands
from Administration import *
from Logging import *

class MemberManagement(commands.Cog):
    def __init__(self, bot):
        log("Module loaded: MemberManagement")
        self.bot = bot
                   
    @commands.command()
    async def whois(self, ctx, arg = None):
        command_log(ctx)

        mentions = ctx.message.mentions
        if len(mentions) > 0:
            mem = mentions[0]
        elif arg == "me":
            mem = ctx.message.author
        else:
            await ctx.send("```No such member.```")
            return

        if (mem is not None):
            embed = discord.Embed(color=mem.color)
            embed.title = "Member information"
            embed.set_image(url = mem.avatar_url)
            embed.add_field(
                name = "Name",
                value = str(mem),
                inline = True
            )
            embed.add_field(
                name = "Display name",
                value = mem.display_name,
                inline = True
            )
            embed.add_field(
                name = "Joined on",
                value = mem.joined_at.strftime("%d-%m-%Y"),
                inline = False

            )
            embed.add_field(
                name = "Booster",
                value = mem.premium_since.strftime("%d-%m-%Y") if mem.premium_since is not None else "No",
                inline = True
            )
            embed.add_field(
                name = "Status",
                value = "Offine" if mem.status is discord.Status.offline else "Online",
                inline = True
            )

            role_lst = [role.mention for role in mem.roles if role.name != "@everyone"]
            role_str = ""
            for role_span in role_lst:
                role_str += role_span + " "

            embed.add_field(
                name = "Roles",
                value = role_str,
                inline = False
            )

            special_perms = ""
            if mem.guild_permissions.administrator:
                special_perms += "Administrator" + ", "
            else:
                if mem.guild_permissions.ban_members:
                    special_perms += "Ban members" + ", "
                if mem.guild_permissions.kick_members:
                    special_perms += "Kick members" + ", "
                if mem.guild_permissions.manage_channels:
                    special_perms += "Manage channels" + ", "
                if mem.guild_permissions.manage_guild:
                    special_perms += "Manage guild" + ", "
                if mem.guild_permissions.view_audit_log:
                    special_perms += "View audit log" + ", "
                if mem.guild_permissions.manage_messages:
                    special_perms += "Manage messages" + ", "
                if mem.guild_permissions.mute_members:
                    special_perms += "Mute members" + ", "
                if mem.guild_permissions.deafen_members:
                    special_perms += "Deafen members" + ", "
                if mem.guild_permissions.manage_nicknames:
                    special_perms += "Manage nicknames" + ", "
                if mem.guild_permissions.manage_roles:
                    special_perms += "Manage roles" + ", "
                if mem.guild_permissions.manage_permissions:
                    special_perms += "Manage permissions" + ", "
                if mem.guild_permissions.manage_emojis:
                    special_perms += "Manage emojis" + ", "
            
            embed.add_field(
                name = "Special permissions",
                value = special_perms[None:-2] if len(special_perms) > 0 else "None"
            )

            if (mem.activity is not None):
                embed.add_field(
                    name = "Currently " + \
                    ("playing" if mem.activity.type == discord.ActivityType.playing \
                    else "watching" if mem.activity.type == discord.ActivityType.watching \
                    else "listening" if mem.activity.type == discord.ActivityType.listening \
                    else "watching" if mem.activity.type == discord.ActivityType.watching \
                    else "playing" if mem.activity.type == discord.ActivityType.playing \
                    else "streaming" if mem.activity.type == discord.ActivityType.streaming \
                    else "doing something with") + " " + mem.activity.name,
                    value = mem.activity.details if "details" in dir(mem.activity) else "No details",
                    inline = False
                )
            await ctx.send(embed=embed)
        else:
            await ctx.send("```Error: Cannot get member from mention```")

    @commands.command()
    async def role(self, ctx, cmd, mention, rolename):
        command_log(ctx)
        mem = ctx.message.mentions[0]
        # LLMFVN exclusive feature
        if (str(ctx.guild.id) != "694173494052651020"):
            await ctx.send("```This is a Love Live µ'sic Forever VN exclusive feature.```")
            return
        if (not is_admin(ctx.author.top_role.id)):
            await ctx.send("```Only admins can issue this command.```")
            return
        if (cmd not in ["give", "delete"]):
            await ctx.send("```Parameter is missing or wrongly specified.```")
            return
        if (mem is None):
            await ctx.send(f"```No such member.```")
            return

        if (cmd == "give"):
            # Get the role
            role = None
            for r in ctx.guild.roles:
                if (r.name ==  rolename):
                    role = r
                    break
            if (role is None):
                await ctx.send(f"```No such role: {rolename}.```")
                return
            # elif (is_admin(role.id)):
            #     await ctx.send(f"```Permission denied: {rolename} must be given manually.```")
            #     return
            await mem.add_roles(role)
            await ctx.send(f"```Role \"{rolename}\" gave to {mem.display_name}```")
        elif (cmd == "delete"):
            removed = False
            roles = mem.roles
            for r in roles:
                if r.name == rolename:
                    roles.remove(r)
                    await mem.edit(roles = roles)
                    removed = True
                    break
            if not removed:
                await ctx.send(f"```No such role: {rolename}.```")
            else:
                await ctx.send(f"```Role \"{rolename}\" deleted from {mem.display_name}```")
