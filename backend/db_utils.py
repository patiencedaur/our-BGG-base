import sqlite3
import gameinfo
import bggapi_get
from settings import *

class DatabaseInit:

    def create_db(self):
        '''
        Create an SQLite3 database.
        '''
        conn = sqlite3.connect(DB_PATH)
        with conn.cursor() as cur:
            cur.execute('DROP TABLE IF EXISTS Games')
            cur.execute('CREATE TABLE Games (title TEXT, id INTEGER, player_num_min INTEGER, player_num_max INTEGER,\
                        playing_minutes INTEGER, coco TEXT, mechanics TEXT, url TEXT)')
                        #coco = cooperative or competitive

    def fill_db(self):
        '''
        Fill the DB with all our games, using data from gameinfo.
        '''

        def get_tuple(gd): # make tuple from game dict to feed it to the db easily. mechanics is a string
            return (gd['title'], gd['id'], gd['player_num_min'], gd['player_num_max'],\
                    gd['playing_minutes'], gd['coco'], '; '.join(gd['mechanics'])[:-2], gd['url'],)

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        all_games_dict = bggapi_get.get_game_dict() # ids and titles
        data_to_fill = []

        for game_id in all_games_dict.keys(): #collect all data from all games to feed it to db
            one_game_dict = gameinfo.get_game_info(game_id)
            data_to_fill.append(get_tuple(one_game_dict))

        stmt = '''
        INSERT OR REPLACE INTO Games (title, id, player_num_min, player_num_max,
        playing_minutes, coco, mechanics, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cur.executemany(stmt, data_to_fill) #fill in all games

        conn.commit()
        cur.close()

    def print_db(self):

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        print('Games:')
        cur.execute('SELECT title, id, player_num_min, player_num_max, playing_minutes, coco, mechanics, url FROM Games')
        for row in cur:
            print(row)
        cur.close()

class GetGames:
    def __init__(self):
        self.attrs = ('title', 'id', 'player_num_min', 'player_num_max', 'playing_minutes', 'coco', 'mechanics', 'url')
        # self.title = self.attrs[0]
        # self.id = self.attrs[1]
        # self.player_num_min = self.attrs[2]
        # self.player_num_max = self.attrs[3]
        # self.playing_minutes = self.attrs[4]
        # self.coco = self.attrs[5]
        # self.mechanics = self.attrs[6]
        # self.url = self.attrs[7]

    def get_by_title(self, game_title):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        stmt = '''
        SELECT title, id, player_num_min, player_num_max, playing_minutes, coco, mechanics, url FROM Games
            WHERE title = ?
        '''
        cur.execute(stmt, game_title)
        for row in cur:
            print(row)
        cur.close()