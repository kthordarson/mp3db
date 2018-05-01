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

    try:
        cursor.execute('INSERT IGNORE INTO Files (filename, size, album, artist, title) VALUES (%s,%s,%s,%s,%s)',
                       (filename, size, album, artist, title))
        file_idx = cursor.lastrowid
    except Exception as e:
        print("db_insert_filename_taglib error: filename: {} size: {} album: {} artist: {} title: {} error: {}".format(
            filename, size, album, artist, title, e))
        file_idx = None

    # populate album table
    try:
        cursor.execute("SELECT * FROM Album WHERE title LIKE %s", (album))  # look for existing album
        album_idx = cursor.lastrowid
        if cursor.fetchone() is None:  # if not found, insert new artist
            cursor.execute('INSERT  IGNORE INTO Album (title,albumartist) VALUES (%s, %s)', (album, artist))
            artist_idx = cursor.lastrowid
    except UnicodeEncodeError as e:
        print("db_insert_filename_taglib error: {}".format(e))
        album_idx = None
        pass

    # populate Albumartist table
    try:
        cursor.execute("SELECT * FROM Albumartist WHERE Name LIKE %s", (artist))  # look for existing artist
        artist_idx = cursor.lastrowid
    except Exception as e:
        print("db_insert_filename_taglib error: {} ".format(filename))
        artist_idx = cursor.lastrowid
        pass
    if cursor.fetchone() is None:  # if not found, insert new artist
        try:
            cursor.execute('INSERT  IGNORE INTO Albumartist (name) VALUES (%s)', (artist,))
            artist_idx = cursor.lastrowid
        except UnicodeEncodeError as e:
            print("db_insert_filename_taglib error: {}".format(e))
            pass
    else:
        # print ("Found artist at {}".format(cursor.fetchall)) # don't insert new artists
        # res = cursor.fetchall()
        artist_idx = cursor.lastrowid

    try:
        cursor.execute('INSERT  IGNORE INTO Song (title,artist,album,filename) VALUES (%s,%s,%s,%s)',
                       (title, artist_idx, album_idx, file_idx))
    except UnicodeEncodeError as e:
        print("db_insert_filename_taglib error: {}".format(e))
        pass
    song_idx = cursor.lastrowid
    conn.commit()
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
        if ';' not in line:
            continue
        # You can remove this. It's for debugging purposes.
        # print "[line] ", fullLine, "[/line]"
        with conn.cursor() as cur:
            try:
                cur.execute(fullLine)
            except Exception as e:
                # print ("Error with create new db")
                continue
        fullLine = ''

# db.close()   #conn.commit()
