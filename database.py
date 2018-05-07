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

def db_insert_filename_mutagen(conn, cursor, filename, size, metadata):
    print ("Scanning file {}".format(filename))
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

    # create fake filehash for faster searching...
    filehash = filename.encode('utf-8')
    filehash = hashlib.md5(filehash)
    filehash = filehash.hexdigest()

   # tag_list = {'filehash': filehash, 'filename': filename, 'size': str(size)}
#    sql_command = "INSERT INTO Files (filename,size, filehash) VALUES (%s, %s, %s)"
#    cursor.execute(sql_command, [filename, size, filehash])
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
    conn.commit()
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
            conn.commit()
        except pymysql.err.InternalError as e:
            if e.args[0] == 1060: pass # error 1060 is duplicate warning
        try: # add all new columns found in id3 tag ot our db
            sql_command = """UPDATE IGNORE files SET {} = %s WHERE file_id = %s""".format(field)
            cursor.execute(sql_command, (tag_value,file_id,))
            conn.commit()
        except TypeError as e:
            print ("Error UPDATE file DB: {} {}".format(filename, e))
            pass
    return

def populate_tables3(dbconfig):
    # GET ALBUM / ALBUMARTIST / ARTIST TABLES
    connection = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    connection.autocommit = True
    with connection.cursor() as cursor:

        # get all unique artist
        sql_command = """SELECT  artist FROM files"""
        cursor.execute(sql_command)
        for row in cursor.fetchall():
            artist = row.get('artist')
            sql_command = """INSERT IGNORE INTO artist(name) VALUES (%s) """ # .format(artist)
            # print ("Running {} ".format(sql_command))
            cursor.execute(sql_command,[artist])
            connection.commit()

        # get all unique albumartist
        sql_command = """SELECT  albumartist FROM files"""
        cursor.execute(sql_command)
        for row in cursor.fetchall():
            albumartist = row.get('albumartist')
            # sql_command = """INSERT INTO albumartist(name) VALUES ("{}") """.format(albumartist)
            sql_command = """INSERT IGNORE INTO albumartist(name) VALUES (%s) """
            # print ("Running {} ".format(sql_command))
            cursor.execute(sql_command,[albumartist])
            connection.commit()

        # get all unique albums
        sql_command = """SELECT  album FROM files"""
        cursor.execute(sql_command)
        for row in cursor.fetchall():
            album = row.get('album')
            name = row.get('artist')
            if name is None: name = ''
            # look in db for values
            # artist = row.get('artist')
            # albumartist = row.get('albumartist')
            sql_command = """SELECT artist_id FROM artist WHERE name = (%s)"""
            cursor.execute(sql_command,[name])
            res = cursor.fetchone()
            artist_id = res['artist_id']

            sql_command = """SELECT albumartist_id FROM albumartist WHERE name = (%s)"""
            cursor.execute(sql_command,[name])
            res = cursor.fetchone()
            albumartist_id = res['albumartist_id']
            try:
                sql_command = """INSERT INTO album (name,artist_id,albumartist_id) VALUES (%s, %s, %s) """
                cursor.execute(sql_command, [album, artist_id, albumartist_id])
                connection.commit()
            except pymysql.err.IntegrityError as e:
                pass

        # get all unique songs
        sql_command = """SELECT file_id, filename,album,artist,albumartist,title FROM files"""
        cursor.execute(sql_command)
        for row in cursor.fetchall():
            file_id = row.get('file_id')
            album = row.get('album')
            artist = row.get('artist')
            albumartist = row.get('albumartist')
            title = row.get('title')
            filename = row.get('filename')

            # get artist_id and albumartist_id from tables...
            # TODO BROKEN!!!!

            # Find artist_id
            # sql_command = """SELECT """

            sql_command = """SELECT album_id FROM album where name= %s """ #.format(artist,albumartist,album)
            cursor.execute(sql_command,[album])
            for k in cursor.fetchall():
                album_id = k.get('album_id')
                
            sql_command = """SELECT artist_id FROM artist where (name = %s) """ #.format(artist,albumartist,album)
            cursor.execute(sql_command,[artist])
            for k in cursor.fetchall():
                artist_id = k.get('artist_id')
                
            sql_command = """SELECT albumartist_id FROM albumartist where (name = %s) """ #.format(albumartist,albumalbumartist,album)
            cursor.execute(sql_command,[albumartist])
            for k in cursor.fetchall():
                albumartist_id = k.get('albumartist_id')

            # sql_command = """INSERT INTO song (file_id, filename) VALUES ("{}","{}") """.format(file_id, filename)
            try:
                sql_command = """INSERT INTO song (file_id,title, album_id, artist_id, albumartist_id) VALUES (%s, %s, %s, %s, %s) """ #.format(file_id, filename)
                cursor.execute(sql_command, [file_id, title, album_id, artist_id, albumartist_id])
                connection.commit()
            except pymysql.err.IntegrityError as e:
                pass
            # print ("Running {} ".format(sql_command))
#            sql_command = "SELECT album, artist, albumartist, title FROM `files` WHERE file_id = %s"
#            cursor.execute(sql_command, [file_id])
            # populate song table
#            sql_command = """SELECT file_id, album, artist, albumartist, title FROM files where filename = "{}" """.format(filename)
#            cursor.execute(sql_command)
#            for row in cursor.fetchall():
#                print ("Song populate from: {} \n Result {} ".format(filename, row))

def create_new_db(dbconfig):
    """
    this will delete the database and recreate all tables
    :return:
    """
    print("Create new DB..")
    conn = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    conn.autocommit = True
    conn.set_charset('utf8')
    conn.cursor().execute('SET NAMES utf8;')
    conn.cursor().execute('SET CHARACTER SET utf8;')
    conn.cursor().execute('SET character_set_connection=utf8;')
    path_to_file = "mp3db.sql"
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
    conn.commit()
    print("Done creating new DB")
    # db.close()
