import sqlite3
from sqlite3 import Error

database = "./pokernow_sqlite.db"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, relation):
    try:
        c = conn.cursor()
        c.execute(relation)
    except Error as e:
        print(e)


def build_sql_database_framework():

    player_relation = """ CREATE TABLE IF NOT EXISTS Player (
                                id integer PRIMARY KEY,
                                username nvarchar(14),
                                avgplace float,
                                vpip integer,
                                cf integer,
                                bf integer,
                                numhands integer
                            ); """

    playerlist_relation = """CREATE TABLE IF NOT EXISTS PlayerList (
                                id integer PRIMARY KEY,
                                p1 integer,
                                p2 integer,
                                p3 integer,
                                p4 integer,
                                p5 integer,
                                p6 integer,
                                p7 integer,
                                p8 integer,
                                FOREIGN KEY (p1) REFERENCES Player (id),
                                FOREIGN KEY (p2) REFERENCES Player (id),
                                FOREIGN KEY (p3) REFERENCES Player (id),
                                FOREIGN KEY (p4) REFERENCES Player (id),
                                FOREIGN KEY (p5) REFERENCES Player (id),
                                FOREIGN KEY (p6) REFERENCES Player (id),
                                FOREIGN KEY (p7) REFERENCES Player (id),
                                FOREIGN KEY (p8) REFERENCES Player (id)
                            )"""
    
    hand_relation = """CREATE TABLE IF NOT EXISTS Hand (
                            id integer PRIMARY KEY,
                            hand nvarchar(8),
                            numplayers integer,
                            bblevel integer,
                            netgain integer,
                            action ntext,
                            dateplayed date,
                            playerID integer,
                            playerListID integer,
                            FOREIGN KEY (playerID) REFERENCES Player (id),
                            FOREIGN KEY (playerListID) REFERENCES PlayerList (id)
                        );"""



    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, player_relation)
        create_table(conn, hand_relation)
        create_table(conn, playerlist_relation)
    else:
        print("Error! cannot create the database connection.")

        
    conn.close()

