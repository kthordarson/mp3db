import pymysql.cursors
import configparser
import os


def pymsql_connect(db_host, db_user, db_pass, db_database):
    """ Connect to mysql database
    :param db_host: server name or ip
    :param db_user: username
    :param db_pass: password
    :param db_database: name of database
    :return:
    """
    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_database, charset='utf8')
    # cursor = conn.cursor()
    return conn


def db_insert_filename_taglib(conn, filename, size, metadata):
    """ insert data into database
    :param conn: connection
    :param filename: filename to insert
    :param size of file
    :param metadata object
    """
    # insert data into database
    cursor = conn.cursor()
    filename = os.path.realpath(filename)
    filename = filename.replace('\\', '/')

    album = ''.join(metadata.tags["ALBUM"])
    title = ''.join(metadata.tags["TITLE"])
    artist = ''.join(metadata.tags["ARTIST"])
    # print ("Processing {} found fields: ALBUM {} ARTIST {} TITLE {}".format(filename, album, artist, title))
    cursor.execute('INSERT INTO Files (filename, size, album, artist, title) VALUES (%s,%s,%s,%s,%s)',
                   (filename, size, album, artist, title))
    # SET @last_id_in_table1 = LAST_INSERT_ID();
    filename_id = cursor.lastrowid
    cursor.execute('SELECT LAST_INSERT_ID()')
    conn.commit()

    # populate album table
    res = cursor.execute('SELECT * FROM album where Title like (%s)', (album,)) # search for existing album
    data = cursor.fetchone() # store search results
    if not data: # if nothing found...
        cursor.execute('INSERT IGNORE INTO Album (title,artist) VALUES (%s, %s)', (album, artist)) # insert into db
        album_id = cursor.lastrowid
    else: album_id = data[0] # else get id of album
#    cursor.execute('SELECT LAST_INSERT_ID()')
    conn.commit()

    # populate artist table
    res = cursor.execute('SELECT * FROM artist where Name like (%s)', (artist,)) # search for existing artis)
    data = cursor.fetchone()
    if not data:
        cursor.execute('INSERT IGNORE INTO artist (name) VALUES (%s)', (artist,))
        artist_id = cursor.lastrowid
    else: artist_id = data[0]
    # cursor.execute('SELECT LAST_INSERT_ID()')
    conn.commit()

    # populate song table
#    print ("artist_id {} is {} album_id {} is {} title is {} filename_id {} is filename {} "
#           .format(artist_id, artist, album_id, album, title , filename_id, os.path.basename(filename)))
    cursor.execute('INSERT INTO Song (title,artist_id,album_id,filename_id) VALUES (%s,%s,%s,%s)',
                   (title, artist_id, album_id, filename_id))
    song_id = cursor.lastrowid
    conn.commit()
    return

def db_insert_filename_taglib_cursor(cursor, filename, size, metadata):
    """ insert data into database
    :param conn: connection
    :param filename: filename to insert
    :param size of file
    :param metadata object
    """
    # insert data into database
    # cursor = conn.cursor()
    filename = os.path.realpath(filename)
    filename = filename.replace('\\', '/')

    album = ''.join(metadata.tags["ALBUM"])
    title = ''.join(metadata.tags["TITLE"])
    artist = ''.join(metadata.tags["ARTIST"])
    # print ("Processing {} found fields: ALBUM {} ARTIST {} TITLE {}".format(filename, album, artist, title))
    cursor.execute('INSERT INTO Files (filename, size, album, artist, title) VALUES (%s,%s,%s,%s,%s)',
                   (filename, size, album, artist, title))
    # SET @last_id_in_table1 = LAST_INSERT_ID();
    filename_id = cursor.lastrowid
    cursor.execute('SELECT LAST_INSERT_ID()')
    # conn.commit()

    # populate album table
    res = cursor.execute('SELECT * FROM album where Title like (%s)', (album,)) # search for existing album
    data = cursor.fetchone() # store search results
    if not data: # if nothing found...
        cursor.execute('INSERT IGNORE INTO Album (title,artist) VALUES (%s, %s)', (album, artist)) # insert into db
        album_id = cursor.lastrowid
    else: album_id = data[0] # else get id of album
#    cursor.execute('SELECT LAST_INSERT_ID()')
    # conn.commit()

    # populate artist table
    res = cursor.execute('SELECT * FROM artist where Name like (%s)', (artist,)) # search for existing artis)
    data = cursor.fetchone()
    if not data:
        cursor.execute('INSERT IGNORE INTO artist (name) VALUES (%s)', (artist,))
        artist_id = cursor.lastrowid
    else: artist_id = data[0]
    # cursor.execute('SELECT LAST_INSERT_ID()')
    # conn.commit()

    # populate song table
 #   print ("artist_id {} is {} album_id {} is {} title is {} filename_id {} is filename {} "
 #          .format(artist_id, artist, album_id, album, title , filename_id, os.path.basename(filename)))
    cursor.execute('INSERT INTO Song (title,artist_id,album_id,filename_id) VALUES (%s,%s,%s,%s)',
                   (title, artist_id, album_id, filename_id))
    song_id = cursor.lastrowid
    # conn.commit()
    return

def create_new_db():
    """
    this will delete the database and recreate all tables
    :return:
    """
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    db_host = config['DEFAULT']['server']
    db_user = config['DEFAULT']['user']
    db_pass = config['DEFAULT']['pass']
    db_database = config['DEFAULT']['db_database']
    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_database)
    # conn.cursor().set_character_set('utf8')
    conn.set_charset('utf8')
    conn.cursor().execute('SET NAMES utf8;')
    conn.cursor().execute('SET CHARACTER SET utf8;')
    conn.cursor().execute('SET character_set_connection=utf8;')
    PATH_TO_FILE = "mp3db.sql"
    fullLine = ''
    print ("Create new DB..")
    for line in open(PATH_TO_FILE):
        tempLine = line.strip()
        if len(tempLine) == 0:
            continue
        # Skip comments
        if tempLine[0] == '#':
            continue
        fullLine += line
        if ';' not in line:
            continue
        # You can remove this. It's for debugging purposes.
        # print ("[line] ", fullLine, "[/line]")
        with conn.cursor() as cur:
            try:
                cur.execute(fullLine)
            except Exception as e:
                print ("Error with create new db {} ".format(e))
                continue
        fullLine = ''
    print ("Done creating new DB")
# db.close()   #conn.commit()
