import sqlite3


def delete_filelist(conn):
    """ delete everythin in filelist """
    # clear file list for debugging
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM Files')
    except:
        print("Could not delete...")
    return cursor.lastrowid

def reset_database(conn):
    """ delete everythin in filelist """
    # clear file list for debugging
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM Files')
        cursor.execute('DELETE FROM Album')
        cursor.execute('DELETE FROM Albumartist')
    except:
        print("Could not delete...")
    return cursor.lastrowid


def unlock_db(db_filename):
    """ unlock database """
    """Replace db_filename with the name of the SQLite database."""
    connection = sqlite.connect(db_filename)
    connection.commit()
    connection.close()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print('Connection status {}'.format(e))

    return None


def db_insert_filename(conn, filename, hash, metadata):
    """ insert data into database
    :param conn: connection
    :param filename: filename to insert
    :param hash md5 hash of file
    """
    # insert data into database
    # sql = 'INSERT OR REPLACE INTO Files(filename) VALUES(?) '
    # cur = conn.cursor()
    cursor = conn.cursor()
    # cursor.execute(sql, data)
    filename = str(filename)
    album = metadata.album
    artist = metadata.artist
    title = metadata.title
    print ('Update database: {} {} {}'.format(album, artist,title))
    cursor.execute('INSERT OR REPLACE INTO Files (hash,filename, album, artist, title) VALUES (?,?,?,?,?)', (hash, filename, album, artist, title))
    cursor.execute('INSERT OR REPLACE INTO Album (title,albumartist) VALUES (?,?)', (title, artist))
    cursor.execute('INSERT OR REPLACE INTO Albumartist (name) VALUES (?)', (artist,))
    # print ("DB insert result {}".format(result))
    conn.commit()
    return cursor.lastrowid


def db_insert_album(conn, title, albumartist):
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO Album (title,albumartist) VALUES (?,?)', (title, albumartist))
    conn.commit()

    return cursor.lastrowid


def db_getfilelist(conn):
    """ read some mp3 tags and print"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Files')
    return cursor

def create_new_db(conn):

    sql_create_album_table = "CREATE TABLE Album ( `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `Title` TEXT NOT NULL, `Albumartist` TEXT NOT NULL );"

    sql_create_artist_table = "CREATE TABLE Albumartist ( `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `Name` TEXT NOT NULL );"
    
    sql_create_files_table = """
    CREATE TABLE Files ( `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `Hash` TEXT, `Filename` TEXT, `Album` TEXT, `Artist` TEXT, `Title` TEXT );
    """

    sql_create_songs_table = """
    CREATE TABLE Song ( `ID` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `Title` TEXT NOT NULL, `Artist` INTEGER NOT NULL, `Album` INTEGER NOT NULL, `Filename` TEXT );
    """

    cursor = conn.cursor()

    # Enable Foreign key constraints

    cursor.execute("PRAGMA foreign_keys = ON;")

    # Execute the DROP Table SQL statement

    cursor.executescript("DROP TABLE if exists Album")
    cursor.executescript("DROP TABLE if exists Albumartist")
    cursor.executescript("DROP TABLE if exists Files")
    cursor.executescript("DROP TABLE if exists Song")

    cursor.executescript(sql_create_album_table)
    cursor.executescript(sql_create_artist_table)
    cursor.executescript(sql_create_files_table)
    cursor.executescript(sql_create_songs_table)

    conn.commit()