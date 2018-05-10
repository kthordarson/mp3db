import pymysql.cursors
import pymysql.connections
import configparser
import os
import hashlib
import time
import warnings
import itertools
# import pymysql.cursors.DictCursor
import pymysql
import os
from mymp3thing.settings import BASE_DIR
# from django.conf.settings import PROJECT_ROOT


def db_insert_filename_mutagen(conn, cursor, filename, size, metadata, filehash):
    # print ("Scanning file {}".format(filename))
    """ insert data into database
    :param conn: connection
    :param filename: filename to insert
    :param size of file
    :param metadata object
    :param cursor name of cursor connectorator
    """
    # insert data into database
    filename = os.path.realpath(filename)
    filename = filename.replace('\\', '/')

    try:
        # cursor.execute('INSERT INTO Files (filename,size, filehash) VALUES (%s, %s, %s)',(filename, size, filehash))
        sql_command = "INSERT INTO Files (filename,size, filehash) VALUES (%s, %s, %s)"
        cursor.execute(sql_command,[filename, size, filehash])
        last_fileid = cursor.lastrowid
    except pymysql.err.InternalError as e:
        if e.args[0] == 1213:                   # DEADLOCK, try again after sleep
            print ("DEADLOCK {} ".format(e))
            time.sleep(0.1)                     # Wait and retry
            sql_command = "INSERT INTO Files (filename,size, filehash) VALUES (%s, %s, %s)"
            cursor.execute(sql_command, [filename, size, filehash])
            last_fileid = cursor.lastrowid
    except Exception as e:
        print ("ERR {} ".format(e))

    file_id = cursor.lastrowid
    # conn.commit()
    tag_list = {}

    # insert all found fields into DB
    if metadata is None:
        metadata = {'filename': filename}
        metadata = {'title': os.path.basename(filename)}
    index = 0

    try:  # populate a valid tag_list with all available metadata from file
        for index, element in enumerate(metadata):
            tag_list[element[0]] = element[1]
            index += 1
    except AttributeError as e:
        print("meta tag read error {} in file {} ".format(e, filename))

    for field, tag_value in tag_list.items():
        tag_value = ''.join(tag_value)
        try:
            # exception, try to add column "field" to table
            #cursor.execute("ALTER TABLE Files ADD %s varchar (255) NULL DEFAULT ''" % (field))
            # sql_command = "ALTER TABLE Files ADD %s VARCHAR (255) NULL DEFAULT ''"
            sql_command= "ALTER TABLE Files ADD {} VARCHAR (255) NULL DEFAULT ''".format(field)
            cursor.execute(sql_command)
            # conn.commit()
        except pymysql.err.InternalError as e:
            if e.args[0] == 1060: pass # error 1060 is duplicate warning
        try: # add all new columns found in id3 tag ot our db
            sql_command = """UPDATE IGNORE files SET {} = %s WHERE file_id = %s""".format(field)
            cursor.execute(sql_command, (tag_value,file_id,))
            # conn.commit()
        except TypeError as e:
            print ("Error UPDATE file DB: {} {}".format(filename, e))
            pass
    return last_fileid


def db_process_filename2(connection, cursor, file_id):
    #innerconn = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)

    inner_cursor = connection.cursor()
    # get all unique artist
    sql_command = """SELECT * FROM files WHERE file_id=%s"""
    cursor.execute(sql_command, [file_id])
    # connection.commit()
    for row in cursor.fetchall():
        artistname = row.get('artist')
        file_id = row.get('file_id')
        album = row.get('album')
        albumartistname = row.get('albumartist')
        title = row.get('title')
        filename = row.get('filename')

# TODO fix duplicate entries

        # first look in artist table for existing artist
        sql_command = """SELECT artist_id, artistname FROM artist WHERE artistname = (%s)"""
        cursor.execute(sql_command,[artistname])
        res = cursor.fetchone()
        if res is None:
            # insert
            sql_command = """INSERT INTO artist (artistname) VALUES (%s)"""
            cursor.execute(sql_command,[artistname])
            artist_id = cursor.lastrowid
            # connection.commit()
        else:
            artist_id= res.get('artist_id')
#            print ("no insert", res)

        # first look in albumartist table for existing albumartist
        sql_command = """SELECT albumartist_id, albumartistname FROM albumartist WHERE albumartistname = (%s)"""
        cursor.execute(sql_command,[albumartistname])
        res = cursor.fetchone()
        if res is None:
            # insert
 #           print ("Insert")
            sql_command = """INSERT INTO albumartist (albumartistname) VALUES (%s)"""
            cursor.execute(sql_command,[albumartistname])
            albumartist_id = cursor.lastrowid
            # connection.commit()
        else:
            albumartist_id = res.get('albumartist_id')

        # first look in album table for existing album
        sql_command = """SELECT album_id FROM album WHERE name = (%s) AND (artist_id = %s OR albumartist_id = %s)"""
        cursor.execute(sql_command,[album, artist_id, albumartist_id])
        res = cursor.fetchone()
        if res is None:
            # insert
            sql_command = """INSERT INTO album (name, artist_id, albumartist_id) VALUES (%s, %s, %s)"""
            cursor.execute(sql_command,[album, artist_id, albumartist_id])
            album_id = cursor.lastrowid
            # # connection.commit()
        else:
            album_id = res.get('album_id')
        # get all unique songs
        # get artist_id and albumartist_id from tables...
        sql_command = """INSERT INTO song (file_id,title, album_id, artist_id, albumartist_id) VALUES (%s, %s, %s, %s, %s) """  # .format(file_id, filename)
        cursor.execute(sql_command, [file_id, title, album_id, artist_id, albumartist_id])
        song_id = cursor.lastrowid
        print ("Last insert file_id {} song_id {}".format(file_id, song_id))
        # connection.commit()


def truncate_db(dbconfig):

    sql_command ="""
        TRUNCATE album;
        TRUNCATE albumartist;
        TRUNCATE artist;
        TRUNCATE files;
        TRUNCATE song;
"""
    conn = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit = True
    conn.set_charset('utf8')

    with conn.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute("TRUNCATE album")
        # conn.commit()
        cursor.execute("TRUNCATE albumartist")
        # conn.commit()
        cursor.execute("TRUNCATE artist")
        # conn.commit()
        cursor.execute("TRUNCATE files")
        # conn.commit()
        cursor.execute("TRUNCATE song")
        # conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

    return

def create_new_db(dbconfig):
    """
    this will delete the database and recreate all tables
    :return:
    """
    print("Create new DB..")
    conn = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit = True
    conn.cursor().execute("SET FOREIGN_KEY_CHECKS=0;")
    conn.set_charset('utf8')
    conn.cursor().execute('SET NAMES utf8;')
    conn.cursor().execute('SET CHARACTER SET utf8;')
    conn.cursor().execute('SET character_set_connection=utf8;')
    file = os.path.realpath(BASE_DIR)
    file = file.replace('\\', '/')
    path_to_file= os.path.join(BASE_DIR,'mp3db.sql')
    #path_to_file = "mp3db.sql"
    full_line = ''
    for line in open(path_to_file):
        temp_line = line.strip()
        if len(temp_line) == 0:
            continue
        # Skip comments
        if temp_line[0] == '#':
            continue
        full_line += line
        if ';' not in line:
            continue
        # You can remove this. It's for debugging purposes.
        # print ("[line] ", full_line, "[/line]")
        with conn.cursor() as cur:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    # Put here your query raising a warning
                    cur.execute(full_line)
            except Exception as e:
                print("Error with create new db {} ".format(e))
                continue
        full_line = ''
    conn.cursor().execute("SET FOREIGN_KEY_CHECKS=1;")
    # conn.commit()
    print("Done creating new DB")
    # db.close()
#
# SELECT album.album_id as 'ID', album.name as 'Tite', artist.artistname as 'Artist', albumartist.albumartistname as 'Album artist'
# FROM album
# INNER JOIN artist ON artist.artist_id = album.artist_id
# INNER JOIN albumartist ON albumartist.albumartist_id = album.artist_id
