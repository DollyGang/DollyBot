import asyncio
import aiosqlite
from aiosqlite import cursor
from aiosqlite.core import connect
DB_PATH = "./database/database.db"
from collections import defaultdict
import os

async def db_connect():                 #Method to establish connection with the database, has to be called in each and every method accessing the Database
    connection = await aiosqlite.connect(DB_PATH)
    return connection

async def update_prefix(guildID, newPrefix):    #Updates the prefix of the specified guild with the given prefix
    connection = await db_connect()             #calls method to establish connection to DB
    cursor = await connection.cursor()          #creates a cursor to execute Queries in the DB
    sql = '''                                   
        UPDATE prefixes
        SET prefix = ?
        WHERE guildID = ?
        '''
    await cursor.execute(sql, (str(newPrefix), str(guildID),))      #Executes the previously specified query with the given parameters, the "," at the end is necessary
    await connection.commit()                                       #Commits the previously created query
    await connection.close()                                        #closes the connection, which is necessary otherwise could cause other methods to fail 
        
async def get_prefix(guildID):              #Returns the prefix of the specified guild
    connection = await db_connect()         
    cursor = await connection.cursor()
    sql = '''
        SELECT prefix 
        FROM prefixes
        WHERE guildID = ?
        '''
    await cursor.execute(sql, str(guildID),)
    fetched = await cursor.fetchone()
    await connection.close()
    return fetched[0]                   #[0] is necessary, otherwise would return as tuple instead of just the prefixes string value
    
    
async def main():                       #Testing out the above methods (working as of now)
    await update_prefix("1","?")
    test = await get_prefix("1");
    print(test)
    
asyncio.run(main())                    #Used to call the main function in async mode
#print(os.getcwd())