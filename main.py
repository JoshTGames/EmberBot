import os, random, datetime;
import aiocron, asyncio;
from num2words import num2words;

#FILE MANAGEMENT
from dotenv import load_dotenv;
from pathlib import Path;
"""THIS GRABS ALL THE SETTINGS FROM THE SETTINGS.ENV FILE"""
envPath = str(Path(__file__).parent.absolute()) + '\settings.env'
load_dotenv(dotenv_path= envPath);
#/


import discord;
from discord.ext import commands, tasks;
from pretty_help import DefaultMenu, PrettyHelp;

#/ MY MODULES
import myutils, json_management;
#/

intents = discord.Intents.default()
intents.members = True

"""SETTINGS"""
TOKEN = os.getenv('DISCORD_TOKEN');
ADMIN_ROLE = os.getenv('ADMIN_ROLE');
OWNER_ID = os.getenv('OWNER_ID');
READ_CHANNEL = os.getenv('READ_CHANNEL').split(',');
READ_REACTION_MESSAGES = os.getenv('READ_REACTION_MESSAGES').split(',');
HELP_MENU = DefaultMenu('◀️', '▶️', '❌');

FUN_STATUS = os.getenv('FUN_STATUS').split(',');

#/ FEEDBACK - EFFECTIVE TEAMWORKER
WORK_ETHIC = os.getenv('WORK_ETHIC').split(',');
WORK_QUALITY = os.getenv('WORK_QUALITY').split(',');
COMMUNICATION = os.getenv('COMMUNICATION').split(',');
ATTENDANCE = os.getenv('ATTENDANCE').split(',');
EFFECTIVE_TEAMWORKER = [WORK_ETHIC, WORK_QUALITY, COMMUNICATION, ATTENDANCE]; # ITERATE THROUGH EACH OF THESE
#/ FEEDBACK - AGILE PRACTITIONER
TRELLO_FEEDBACK = os.getenv('TRELLO_FEEDBACK').split(',');
DAILY_SCRUM = os.getenv('DAILY_SCRUM').split(',');
GIT_COMMITS = os.getenv('GIT_COMMITS').split(',');
GIT_BRANCHES = os.getenv('GIT_BRANCHES').split(',');
AGILE_PRACTITIONER = [TRELLO_FEEDBACK, DAILY_SCRUM, GIT_COMMITS, GIT_BRANCHES]; # ITERATE THROUGH EACH OF THESE

#/ DAILY SCRUM
SCRUM_CHANNEL = os.getenv('SCRUM_CHANNEL');
#template = open('thread_template.txt', 'r').read();

"""--------"""

#/ EVENTS
bot = commands.Bot(command_prefix= commands.when_mentioned, intents = intents);


"""BOOT UP"""
@bot.event
async def on_ready():     
    print("|| BOT ONLINE! ||");
    bot.loop.create_task(change_status());      
    #bot.help_command = PrettyHelp(dm_help= True, navigation=HELP_MENU, color=discord.Colour.red(), index_title= 'Help', show_index= False, no_category= 'Help');

@bot.event
async def on_message(msg):
    msgContent = msg.content;
    msgArray = msgContent.lower().split();
    if("birthday" in msgArray):
        await msg.reply("Whose ");
    await bot.process_commands(msg);

"""RANDOM STATUS"""
curStatus = None;
async def change_status():
    global curStatus;
    while True:
        possibleStatus = FUN_STATUS;
        if(curStatus != None): possibleStatus.pop(possibleStatus.index(curStatus)) # ENSURES IT CANT BE SELECTED AGAIN

        curStatus = FUN_STATUS[random.randint(0, len(possibleStatus)-1)];    
        print(f"|| Changing status to: '{curStatus}' ||")
        await bot.change_presence(activity= discord.Game(curStatus));
        await asyncio.sleep(60*10); #WAIT 10 MINUTES
    
"""REACTION ROLES"""
async def manage_reactions(msg, isAddReaction):
    guild = await bot.fetch_guild(msg.guild_id);    
    member = await guild.fetch_member(msg.user_id);
    emoji = msg.emoji;    
    await myutils.manage_reactions(isAddReaction, msg, guild, member, emoji)

@bot.event
async def on_raw_reaction_add(msg):
    if(not (str(msg.message_id) in READ_REACTION_MESSAGES)): return; # ENSURES ITS READING THE RIGHT MESSAGES
    await manage_reactions(msg, True);    
@bot.event
async def on_raw_reaction_remove(msg):
    if(not (str(msg.message_id) in READ_REACTION_MESSAGES)): return; # ENSURES ITS READING THE RIGHT MESSAGES
    await manage_reactions(msg, False);
"""--------------"""


"""CHAT COMMANDS"""
@bot.command(name = "ping", help='Check to see if im alive!', pass_context = True)
@commands.has_role(ADMIN_ROLE)
async def ping(ctx):   
    if(not myutils.is_in_channel(ctx.channel.id, READ_CHANNEL)): return # GENERAL COMMANDS REQUIRE TO BE IN A CHANNEL    
    await ctx.reply("Pong!");


@bot.command(name = "promote", help='promote ~UserName ~RoleName', pass_context = True)
@commands.has_role(ADMIN_ROLE)
async def promote(ctx, user_name, role_name):
    if(not myutils.is_in_channel(ctx.channel.id, READ_CHANNEL)): return # GENERAL COMMANDS REQUIRE TO BE IN A CHANNEL    
    msgsToRemove = [];
    msgsToRemove.append(ctx.message);

    content = ctx.message.content.split();
    user = content[2] if((len(content) >=3)) else None; #attempt to get discord user from message
    role = content[3] if((len(content) >=4)) else None; #attempt to get role from message   

    member = await ctx.guild.fetch_member(int(user.strip('<@!>')));    
    roleId = discord.utils.get(ctx.guild.roles, name=role);    
    if(len(content) < 4):
        await ctx.send(f"{ctx.author.mention}, Error executing command: Please format it {bot.user.mention} promote @usernameHere roleNameHere");
    elif(member == None):
        await ctx.send(f"{ctx.author.mention}, Error executing command: User not found...");    
    elif(roleId == None):
        await ctx.send(f"{ctx.author.mention}, Error executing command: Role not found...");  
    
    if(member and roleId):
        await myutils.set_role(ctx, member, roleId, True, True);   
    await myutils.delete_msgs(msgsToRemove);    

"""BIRTHDAY COMMANDS"""
@bot.command(name = "setbirthday")
async def setbirthday(ctx): #SAVES THE USER TO A CSV DATABASE
    birthdates = csv_management.ReadFile("Birthdays.csv");
    #LOAD CSV
    #QUERY THE CSV FOR THE USER SHOULD THEY ALREADY EXIST...
    #CREATE/UPDATE THE USER ONTO THE CSV WITH THE DATE OF BIRTH
### CREATE AN AIOCRON FUNCTION WHICH RUNS EVERY DAY AT 7AM. IF IT LANDS ON PEOPLES B-DAY ANNOUNCE IT IN THE BDAYS CHAT! 

"""FEEDBACK FRUITS GENERATOR"""
def get_name(s): return s.encode('ascii', 'namereplace');
async def create_feedback(ctx, title, index, user, emojis, colour):    
    options = "";            
    for y in range(1, len(index)): options += f'{index[y]}\n';          
    

    embed = discord.Embed(
        title= title, 
        description= f"**{index[0]}**\n{options}", 
        color= colour
    ) 
    embed.set_footer(text=f'REACT TO OPTIONS\nFeedback for {user}');       
            
    newMsg = await ctx.send(embed=embed);
    for e in emojis: await newMsg.add_reaction(e); #POPULATES ALL POSSIBLE OPTIONS TO MESSAGE            
    return newMsg;
async def wait_for_input(ctx, index, emojis, reactMsgId):
    reaction, _ = await bot.wait_for('reaction_add', timeout=30, check=lambda r, u: str(r.emoji) in emojis and u == ctx.author and r.message.id == reactMsgId);
    if(reaction):                
        split_msg = index[emojis.index(reaction.emoji)+1].strip(f':{num2words(emojis.index(reaction.emoji)+1)}:');        
        return (f'\n{index[0]}: {split_msg}')            
        

@bot.command(name = "feedback", help='feedback ~addresseeName ~(Optional)referenceName', pass_context = True)
async def generate_feedback(ctx, name, yourName = ""):    
    if(not myutils.is_in_channel(ctx.channel.id, READ_CHANNEL) and not myutils.is_in_dm_channel(ctx.channel)): return; # IF IT IS NOT A DM OR IN THE RIGHT SERVER CHANNEL, RETURN
    print(f'#- {ctx.author} is creating feedback -#')
    msgsToRemove = [];
    if(not myutils.is_in_dm_channel(ctx.channel)): msgsToRemove.append(ctx.message); #ADDS MAIN DM MESSAGE TO REMOVAL LIST

    content = ctx.message.content.split();
    user = content[2] if ((len(content) >=3)) else None;    
    yourName = content[3] if ((len(content) >=4)) else None;    
    if(len(content) < 3):
        await ctx.reply(f"Error executing command: Please format it {bot.user.mention} feedback nameHere");

    teamworker_output = "";
    for x in EFFECTIVE_TEAMWORKER:
        emojis = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(1, len(x))] # FILLS UP THE EMOJI LIST TO THE NUMBER OF OPTIONS
        reactMsg = await create_feedback(ctx, "**EFFECTIVE TEAMWORKER FEEDBACK**", x, user, emojis, discord.Colour.blue());  
        msgsToRemove.append(reactMsg);     
        try:                          
            teamworker_output += await wait_for_input(ctx, x, emojis, reactMsg.id); 
            msgsToRemove = await myutils.delete_msgs(msgsToRemove); 
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} **Feedback Cancelled:** (Timeout)");    
            print(f'#- {ctx.author} has timed out -#') 
            return await myutils.delete_msgs(msgsToRemove);
    agile_output = "";
    for x in AGILE_PRACTITIONER: 
        emojis = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(1, len(x))] # FILLS UP THE EMOJI LIST TO THE NUMBER OF OPTIONS
        reactMsg = await create_feedback(ctx, "**AGILE PRACTITIONER FEEDBACK**", x, user, emojis, discord.Colour.purple());  
        msgsToRemove.append(reactMsg);     
        try:                          
            agile_output += await wait_for_input(ctx, x, emojis, reactMsg.id); 
            msgsToRemove = await myutils.delete_msgs(msgsToRemove); 
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} **Feedback Cancelled:** (Timeout)");  
            print(f'#- {ctx.author} has timed out -#')  
            return await myutils.delete_msgs(msgsToRemove);      
        
    await ctx.author.send(f"```During the last sprint, {user} has performed as follows: \n{teamworker_output} \n\n{f'--'+yourName if(yourName != None) else ''}```"); 
    await ctx.author.send(f"```During the last sprint, {user} has performed as follows: \n{agile_output} \n\n{f'--'+yourName if(yourName != None) else ''}```"); 
    print(f'#- {ctx.author} has finished their feedback -#')
    msgsToRemove = await myutils.delete_msgs(msgsToRemove); 
   
"""-------------"""

#//-- DAILY SCRUM EVENTS 

"""HIDES THE THREAD FROM THE SERVER"""
def generate_thread_name(date): return f'{date.day}.{date.month}.{date.year} Update';

async def archive_thread(id):
    thread = bot.get_channel(int(id));    
    await thread.edit(archived = True);

"""CREATES A NEW THREAD UNDER THE PARENT CHANNEL"""
async def create_new_thread(date):            
    threadParent = bot.get_channel(int(SCRUM_CHANNEL));    
    startMsg = await threadParent.send(template);    
    thread = await threadParent.create_thread(name= generate_thread_name(date), message= startMsg);
    await thread.send(discord.utils.get(thread.guild.roles, name= ADMIN_ROLE).mention);
    return thread;

"""CREATES A DAILY THREAD 9AM EVERY WEEK-DAY"""
@aiocron.crontab('* * * * *')
async def create_daily_thread():    
    print("running");
    if(bot == None):
        print("Client doesn't exist!");
        return;
    #/ GET OLD THREAD 
    f = open('previous_thread_id.txt', 'r');
    previousThreadId = f.read();
    f.close();
    #/ ARCHIVE OLDER THREAD
    if(previousThreadId != ""): await archive_thread(previousThreadId); 
    
    #/ CHECK IF ITS THE WEEKEND
    date = datetime.date.today();
    #if(date.weekday() in [5, 6]): return;

    #/ CREATE NEW THREAD
    thread = await create_new_thread(date);    
    print(f"Building Thread: {thread.name}")    
    
    #/ CACHE NEW THREAD
    f = open('previous_thread_id.txt', 'w');
    f.write(str(thread.id));
    f.close();

bot.run(TOKEN);