from nextcord.ext import tasks, application_checks
from nextcord.ext import commands
from nextcord import Interaction
import nextcord

# from nextcord.ext import Interaction
import os
import sys
import release
import apis as api
import callables as call


allowed_mentions = nextcord.AllowedMentions(roles = True)
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
client = nextcord.Client(intents=intents)
serverID = []
@tasks.loop(seconds=60)
async def setGuilds():
    serverID = []
    await bot.wait_until_ready()
    for guild in bot.guilds:
        serverID.append(int(guild.id))
    print(f"server ids {serverID}")




#serverID = 855860264942829589



# await bot.wait_until_ready()
print("DokjaBot activated - Made by DioForever - dioforever.live")

announced = {}

async def no_perms(interaction, error):
    if isinstance(error, application_checks.ApplicationMissingPermissions):
        embed = nextcord.Embed(title=f"Required Administrator perms!",
                               color=nextcord.Color.from_rgb(255, 0, 0))
        await interaction.response.send_message(embed=embed, delete_after = 5)
    else:
        raise error


@tasks.loop(seconds=60)
async def rich_presence():
    await bot.wait_until_ready()
    guilds = bot.guilds
    number_of_servers = len(guilds)
    await bot.change_presence(status=nextcord.Status.online,
                              activity=nextcord.Game(f'Library of Culture on {number_of_servers} servers'), )

@bot.slash_command(name="library_addrole", description="Adds role ping to specific manga/manhwa.", guild_ids=serverID)
@application_checks.has_permissions(administrator=True)
async def library_addrole(interaction: Interaction, role: str, title: str):
    pass


@library_addrole.error
async def library_addrole(interaction: Interaction, error):
    await no_perms(interaction,error)


@bot.slash_command(name="library_remove_role", description="Removes role ping to specific manga/manhwa.", guild_ids=serverID)
@application_checks.has_permissions(administrator=True)
async def library_remove_role(interaction: Interaction, role: str, title: str):
    pass

@library_remove_role.error
async def library_remove_role(interaction: Interaction, error):
    await no_perms(interaction, error)

@bot.slash_command(name="library_add", description="Adds the manga to the server library", guild_ids=serverID)
@application_checks.has_permissions(administrator=True)
async def library_add(interaction: Interaction, source: str, title_or_url: str):
    pass

@library_add.error
async def no_perms_ladd(interaction: Interaction, error):
    await no_perms(interaction,error)

@bot.slash_command(name="library_remove", description="Removes the manga from the server library", guild_ids=serverID)
@application_checks.has_permissions(administrator=True)
async def library_remove(interaction: Interaction, source: str, title: str):
    pass
@library_remove.error
async def library_remove(interaction: Interaction, error):
    await no_perms(interaction,error)
@bot.slash_command(name="dm", description="Enables/Disables direct messages instead of pings from this server announcements.", guild_ids=serverID)
async def dm_enable_disable(interaction: Interaction):
    pass

@bot.slash_command(name="sub", description="Subscribe to any book in the library of the server.", guild_ids=serverID)
async def sub(interaction: Interaction, title: str):
    pass
@bot.slash_command(name="unsub", description="Unsubscribe any book in the library of the server.", guild_ids=serverID)
async def unsub(interaction: Interaction, title: str):
    pass
@bot.slash_command(name="sources", description="See all the available sources.", guild_ids=serverID)
async def sources(interaction: Interaction):
    pass

@bot.slash_command(name="list", description="See all the manga/manhwa sources.", guild_ids=serverID)
async def list(interaction: Interaction):
    pass

@bot.slash_command(name="help", description="Need help?", guild_ids=serverID)
async def help(interaction: Interaction):
    pass

First = True



i = 0
# @tasks.loop(minutes=30)
# async def periodical_restart(i=i):
#     await bot.wait_until_ready()
#     is_first = getF(First)
#     if i == 1:
#         os.execl(sys.executable, sys.executable, *sys.argv)
#         print('Restarted')
#     else:
#         i += 1
#         print('30min left till reset')
#

@tasks.loop(seconds=60)
async def releaseCheck():
    await release.chapterreleasecheck(bot, announced)

#release_check = await release.chapterreleasecheck(bot, announced)
#setAnnounced(release_check)


# <@401845652541145089>
setGuilds.start()
periodical_restart.start()
releaseCheck.start()
rich_presence.start()
bot.run(open("botToken", "r").read())
