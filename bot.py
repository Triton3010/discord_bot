import discord
from discord.ext import commands
from googlesearch import search
from connector import get_connection
import os 

client = commands.Bot(command_prefix = '!')

''' handler function for when the bot is ready '''
@client.event
async def on_ready():
    print('The bot is ready')


''' handler function handler for !google command '''
@client.command()
async def google(ctx, *args):
    ''' if the user typed something after !google, then return results '''
    if args:
        print('in google handler')
        search_query = ' '.join(args)
        connection = get_connection()
        print(connection)
        ''' sql query to insert the search keyword made by the user in a table '''
        insert_sql = f"INSERT INTO search (user_id, search_keywords) VALUES ('{ctx.author}', '{search_query}')"

        mycursor = connection.cursor()

        ''' google search the query, return the top 5 results '''
        for each_result in search(search_query, lang='en', num = 5, stop = 5, pause = 2):
            await ctx.send(each_result)

        mycursor.execute(insert_sql)
        connection.commit()
        print('inserted in db')

    else:
        await ctx.send('Please type in some keywords')


''' handler function for !recent command '''
@client.command()
async def recent(ctx, *args):
    ''' if the user typed something after !recent, then return results '''
    if args:
        recent_search_keywords = ' '.join(args)
        connection = get_connection()

        ''' sql query to retrieve latest 5 searches made by the user containing the keyword '''
        select_sql = f"select search_keywords from search where user_id = '{ctx.author}'" \
                    f"and search_keywords like '%{recent_search_keywords}%' ORDER BY inserted_at DESC LIMIT 5"

        mycursor = connection.cursor()
        mycursor.execute(select_sql)
        myresult = mycursor.fetchall()

        if myresult:
            ''' return each previous search query found for the user '''
            for each_recent_search in myresult:
                recent_search_string = ' '.join(each_recent_search)
                await ctx.send(recent_search_string)
        else:
           await ctx.send('No such previous search is made by you') 

    else:
        await ctx.send('Please type in some keywords')


''' handler function to return hey to user's hi '''
@client.event
async def on_message(message):
    if message.content.lower() == 'hi':
        await message.channel.send('hey')
    await client.process_commands(message)

client.run(os.environ.get('BOT_TOKEN'))