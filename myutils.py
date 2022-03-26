import os, discord, random;

#FILE MANAGEMENT
from dotenv import load_dotenv;
from pathlib import Path;
"""THIS GRABS ALL THE SETTINGS FROM THE SETTINGS.ENV FILE"""
envPath = str(Path(__file__).parent.absolute()) + '\settings.env'
load_dotenv(dotenv_path= envPath);
#/

"""SETTINGS"""
FUN_QUOTES = os.getenv('FUN_QUOTES').split(',');
"""--------"""

# THIS SCRIPT SHOULD BE POPULATED WITH VARIOUS FUNCTIONS TO BE CALLED, THIS ULTIMATELY WILL HELP REDUCE THE CODE SIZE OF THE MAIN SCRIPT
"""DELETES ALL MESSAGES PASSED INTO THIS FUNCTION"""
async def delete_msgs(msgs):
    for x in msgs: 
        await x.delete();        
    return [];

"""GIVES A USER A ROLE -- |'doNotify'- Perform an embedded notification| 'isPublic'- If false, will notify user of changes, else will announce it"""
async def set_role(ctx, member, role, doNotify= True, hasReceipt= True, guild = None):
    await member.add_roles(role);
    if(not doNotify): return; # NO POINT CONTINUING ON IF NO NOTIFICATION IS REQUIRED...


    #/ GET A DESCRIPTION
    embedDesc = "";
    if(role.name == 'ScrumMaster'):
        embedDesc = '**Your role for this sprint is to:** \nCheck-in with other developers and make sure tasks are achievable. \nEnsure the Trello board is updated. \nEnforce the daily standups in the threads and make note of whats being done.';
    else:
        embedDesc = 'And the responsibilities that come with it 😝'
    #/

    #/ CREATE EMBED
    embed = discord.Embed(
        title=f"🥰 You acquired the '{role.name}' role! 🥰 \n\t**In server: {ctx.guild.name if(guild == None) else guild.name}**", 
        description= embedDesc, 
        color= role.colour
    )
    embed.set_author(name= member.display_name, icon_url= member.avatar_url, url= f"https://www.discordapp.com/users/{member.id}"); 
    embed.set_footer(text= FUN_QUOTES[random.randint(0, len(FUN_QUOTES)-1)]); # RANDOM GOOFY MESSAGE
    #/

    
    if(hasReceipt):
        await member.send(f"**NOTIFICATION FROM '{ctx.guild.name}'**\n{ctx.channel.mention}");
        receipt = discord.Embed(
            title="Role Grant", 
            description= f"Role '{role.name}' successfully given to **{member.name}**", 
            color= role.colour
        )
        receipt.set_author(name= member.display_name, icon_url= member.avatar_url, url= f"https://www.discordapp.com/users/{member.id}"); 
        await ctx.send(ctx.author.mention, embed= receipt);
    else:
        await member.send(embed= embed);
"""REMOVES A ROLE FROM A USER"""
async def remove_role(member, role):
    await member.remove_roles(role);





"""THIS FUNCTION RETURNS WHETHER OR NOT A GIVEN CHANNEL IS WITHIN THE READING LIST OF CHANNELS"""
def is_in_channel(channelId, channels):    
    return True if(str(channelId) in channels or len(channels) <= 0) else False # IF ID IS ID IS FOUND IN ARRAY OR THE ARRAY IS EMPTY, RETURN TRUE
"""RETURNS TRUE IF A MESSAGE IS A DM"""
def is_in_dm_channel(channel): return True if(type(channel) == discord.channel.DMChannel) else False;
    


"""ITERATES THROUGH ALL THE TEAM ROLES, IF THE EMOJI MATCHES, THEN IT WILL RETURN A GIVEN ROLE"""
def check_team_roles(guild, emoji, role):
    if(role != None): return role;
    
    if(emoji.name == '⌨️'):        
        role = discord.utils.get(guild.roles, name= 'Programmer');
    elif(emoji.name == '👷'):
        role = discord.utils.get(guild.roles, name= 'Designer');
    elif(emoji.name == '🎨'):
        role = discord.utils.get(guild.roles, name= 'Artist');
    elif(emoji.name == '🕺'):
        role = discord.utils.get(guild.roles, name= 'Animator');
    elif(emoji.name == '🎶'):
        role = discord.utils.get(guild.roles, name= 'Audio Dev');
    elif(emoji.name == '📝'):
        role = discord.utils.get(guild.roles, name= 'Writer');
    elif(emoji.name == '🔥'):
        role = discord.utils.get(guild.roles, name= 'Artist(Gart)');
    elif(emoji.name == '❄️'):
        role = discord.utils.get(guild.roles, name= 'Artist(Dart)');
    
    return role;

"""THIS FUNCTION HANDLES ROLE GRANTS/REMOVAL"""
async def manage_reactions(isAddReaction, msg, guild, member, emoji):
    role = None;
    role = check_team_roles(guild, emoji, role); #CHECK TEAMROLES    
    if(role == None): return;

    if(isAddReaction): 
        await set_role(msg, member, role, True, False, guild);
    else: 
        await remove_role(member, role);