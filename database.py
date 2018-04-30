import sqlite3
import mysql.connector as mariadb
import pymysql.cursors
import configparser
import os


def pymsql_connect(db_host, db_user, db_pass, db_database):
    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_database)
    cursor = conn.cursor()
    return conn
def mariadb_connect():
    mariadb_connection = mariadb.connect(host='192.168.0.20', user='root', password='newpwd', database='mp3db')
    cursor = mariadb_connection.cursor()
    return cursor

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
    """ delete """
    # clear file list for debugging
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM Files')
        cursor.execute('DELETE FROM Album')
        cursor.execute('DELETE FROM Albumartist')
    except:
        print("Could not delete...")
    return cursor.lastrowid



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        print('Connection status {}'.format(e))

    return None


def db_insert_filename(conn, filename, size, metadata):
    """ insert data into database
    :param conn: connection
    :param filename: filename to insert
    :param hash md5 hash of file
    :param metadata object
    """
    # insert data into database
    # sql = 'INSERT OR REPLACE INTO Files(filename) VALUES(?) '
    # cur = conn.cursor()
    cursor = conn.cursor()
    # cursor.execute(sql, data)
    #filename = str(filename)
    filename = os.path.realpath(filename)
    filename =filename.replace('\\', '/')

    album = metadata.album
    artist = metadata.artist
    title = metadata.title
    # album = metadata.tags["ALBUM"][0]
    # title = metadata.tags["TITLE"][0]
    # artist = metadata.tags["ARTIST"][0]
    # cursor.execute('INSERT IGNORE INTO Files (hash,filename, album, artist, title) VALUES (%s,%s,%s,%s,%s)', (hash, filename, album, artist, title))
    cursor.execute('INSERT IGNORE INTO Files (filename, size, album, artist, title) VALUES (%s,%s,%s,%s,%s)', (filename, size,album, artist, title))
    print ("Insert {}".format(filename))
    file_idx = cursor.lastrowid

    # populate album table
    cursor.execute("SELECT * FROM Album WHERE title LIKE %s", (album))  # look for existing album
    if cursor.fetchone() is None: # if not found, insert new artist
        cursor.execute('INSERT  IGNORE INTO Album (title,albumartist) VALUES (%s, %s)', (album,artist))
        artist_idx = cursor.lastrowid
    else:
        print ("Found album at {}".format(cursor.fetchall)) # don't insert new artists
        res = cursor.fetchall()
        for k in res:
            print ("k ",k)
        artist_idx = cursor.lastrowid

    #cursor.execute('INSERT IGNORE INTO Album (title,albumartist) VALUES (%s,%s)', (album, artist))
    album_idx = cursor.lastrowid

    # populate Albumartist table
    try:
        cursor.execute("SELECT * FROM Albumartist WHERE Name LIKE %s", (artist)) # look for existing artist
    except:
        print ("Some error with {} ".format(filename))
        pass
    if cursor.fetchone() is None: # if not found, insert new artist
        cursor.execute('INSERT  IGNORE INTO Albumartist (name) VALUES (%s)', (artist,))
        artist_idx = cursor.lastrowid
    else:
        print ("Found artist at {}".format(cursor.fetchall)) # don't insert new artists
        res = cursor.fetchall()
        for k in res:
            print ("k ",k)
        artist_idx = cursor.lastrowid


    cursor.execute('INSERT  IGNORE INTO Song (title,artist,album,filename) VALUES (%s,%s,%s,%s)', (title,artist_idx,album_idx,file_idx))
    song_idx = cursor.lastrowid
    #print ("results: {} {} {} {} ".format(file_idx, album_idx, artist_idx,song_idx))
    # print ("DB insert result {}".format(result))
    conn.commit()
    return

def db_insert_filename_taglib(conn, filename, size, metadata):
    """ insert data into database
    :param conn: connection
    :param filename: filename to insert
    :param hash md5 hash of file
    :param metadata object
    """
    # insert data into database
    # sql = 'INSERT OR REPLACE INTO Files(filename) VALUES(?) '
    # cur = conn.cursor()
    cursor = conn.cursor()
    # cursor.execute(sql, data)
    #filename = str(filename)
    filename = os.path.realpath(filename)
    filename =filename.replace('\\', '/')

    # album = metadata.album
    # artist = metadata.artist
    # title = metadata.title
    album = metadata.tags["ALBUM"][0]
    title = metadata.tags["TITLE"][0]
    artist = metadata.tags["ARTIST"][0]
    # cursor.execute('INSERT IGNORE INTO Files (hash,filename, album, artist, title) VALUES (%s,%s,%s,%s,%s)', (hash, filename, album, artist, title))
    cursor.execute('INSERT IGNORE INTO Files (filename, size, album, artist, title) VALUES (%s,%s,%s,%s,%s)', (filename, size,album, artist, title))
    print ("Insert {}".format(filename))
    file_idx = cursor.lastrowid

    # populate album table
    cursor.execute("SELECT * FROM Album WHERE title LIKE %s", (album))  # look for existing album
    if cursor.fetchone() is None: # if not found, insert new artist
        cursor.execute('INSERT  IGNORE INTO Album (title,albumartist) VALUES (%s, %s)', (album,artist))
        artist_idx = cursor.lastrowid
    else:
        print ("Found album at {}".format(cursor.fetchall)) # don't insert new artists
        res = cursor.fetchall()
        for k in res:
            print ("k ",k)
        artist_idx = cursor.lastrowid

    #cursor.execute('INSERT IGNORE INTO Album (title,albumartist) VALUES (%s,%s)', (album, artist))
    album_idx = cursor.lastrowid

    # populate Albumartist table
    try:
        cursor.execute("SELECT * FROM Albumartist WHERE Name LIKE %s", (artist)) # look for existing artist
    except:
        print ("Some error with {} ".format(filename))
        pass
    if cursor.fetchone() is None: # if not found, insert new artist
        cursor.execute('INSERT  IGNORE INTO Albumartist (name) VALUES (%s)', (artist,))
        artist_idx = cursor.lastrowid
    else:
        print ("Found artist at {}".format(cursor.fetchall)) # don't insert new artists
        res = cursor.fetchall()
        for k in res:
            print ("k ",k)
        artist_idx = cursor.lastrowid


    cursor.execute('INSERT  IGNORE INTO Song (title,artist,album,filename) VALUES (%s,%s,%s,%s)', (title,artist_idx,album_idx,file_idx))
    song_idx = cursor.lastrowid
    #print ("results: {} {} {} {} ".format(file_idx, album_idx, artist_idx,song_idx))
    # print ("DB insert result {}".format(result))
    conn.commit()
    return

def db_insert_album(conn, title, albumartist):
    cursor = conn.cursor()
    cursor.execute('INSERT  IGNORE INTO Album (title,albumartist) VALUES (%s,%s)', (title, albumartist))
    conn.commit()

    return cursor.lastrowid


def db_getfilelist(conn):
    """ read some mp3 tags and print"""
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Files')
    return cursor

def create_new_db():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    db_host = config['DEFAULT']['server']
    db_user = config['DEFAULT']['user']
    db_pass = config['DEFAULT']['pass']
    db_database = config['DEFAULT']['db_database']
    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_database)

    PATH_TO_FILE = "mp3db.sql"
    fullLine = ''
    for line in open(PATH_TO_FILE):
      tempLine = line.strip()
      # Skip empty lines.
      # However, it seems "strip" doesn't remove every sort of whitespace.
      # So, we also catch the "Query was empty" error below.
      if len(tempLine) == 0:
        continue
      # Skip comments
      if tempLine[0] == '#':
        continue
      fullLine += line
      if not ';' in line:
        continue
      # You can remove this. It's for debugging purposes.
      # print "[line] ", fullLine, "[/line]"
      with conn.cursor() as cur:
          try:
            cur.execute(fullLine)
          except MySQLdb.OperationalError as e:
            if e[1] == 'Query was empty':
              continue
      fullLine = ''

   # db.close()   #conn.commit()