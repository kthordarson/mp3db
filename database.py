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
    print ("- {}".format(filename))
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
    cursor.execute('INSERT INTO Files (filename,size, filehash) VALUES (%s, %s, %s)',(filename, size, filehash))
    file_id = cursor.lastrowid
    conn.commit()
    cursor.execute("INSERT INTO Song (file_id, filename) VALUES (%s, %s)",(file_id,filename))
    song_id = cursor.lastrowid

    tag_list = {}
    # insert all found fields into DB
    if metadata is None:
        metadata = {'filename': filename}
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
            cursor.execute("ALTER TABLE Files ADD {} VARCHAR (255) NULL DEFAULT ''".format(field))
            # cnx.commit()
        except Exception as e:
            # print ("Error in alter table column: Filename: {} Field: {} Tag_value: {} ERROR {}".format(filename, field, tag_value, e))
            pass

        last_row = int(file_id)
        try: # add all new columns found in id3 tag ot our db
            sql_command = """UPDATE IGNORE files SET {} = %s WHERE file_id = %s""".format(field)
            cursor.execute(sql_command, (tag_value,file_id,))
        except Exception as e:
            #print ("Error UPDATE file DB: {} {}".format(filename, e))
            pass

        try:
            cursor.execute("ALTER TABLE Song ADD {} VARCHAR (255)".format(field))
        except Exception as e:
            # print ("Error in ALTER table song FILE {} FIELD {} ERROR {} ".format(filename, field, e))
            pass

    return


def populate_tables2(dbconfig):
    # GET ALBUM / ALBUMARTIST / ARTIST TABLES
    connection = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    connection.autocommit = True


    with connection.cursor() as cursor:
        # lets populate album, artist and albumartist tables from files
        sql_command = "SELECT album,artist,albumartist, file_id FROM files"
        cursor.execute(sql_command)
        result = cursor.fetchall()
        for row in result:
            artist = row.get('artist')  ### look in []
            albumtitle = row.get('album')
            albumartist = row.get('albumartist')
            title = row.get('title')
            file_id = row.get('file_id')

            # album populate
            sql_command = "SELECT album_id FROM album WHERE (Artist = %s OR albumartist = %s) AND albumtitle = %s"
            cursor.execute(sql_command, [artist,albumartist,albumtitle])
            result = cursor.fetchall()
            if len(result) == 0:
                #sql_command = """UPDATE IGNORE album  SET ({},{},{}) VALUES ('{}','{}','{}') """.format(album,artist,albumartist)
                sql_command = """INSERT INTO album (albumtitle,artist,albumartist) VALUES ("%s","%s","%s")""" % (albumtitle,artist,albumartist)
                try:
                    print ("Running: {} ".format(sql_command))
                    cursor.execute(sql_command)
                    connection.commit()
                except Exception as e:
                    print ("INSERT INTO album error. ".format(e))

            # artist populate
            sql_command = "SELECT artist_id FROM artist WHERE name = %s"
            cursor.execute(sql_command, [artist])
            result = cursor.fetchall()
            if len(result) == 0:
                sql_command = """INSERT INTO artist (name) VALUES ("%s")""" % (artist)
                try:
                    print ("Running: {} ".format(sql_command))
                    cursor.execute(sql_command)
                    connection.commit()
                except Exception as e:
                    print ("INSERT INTO artist error. ".format(e))


            # albumartist populate
            sql_command = "SELECT albumartist_id FROM albumartist WHERE name = %s"
            cursor.execute(sql_command, [albumartist])
            result = cursor.fetchall()
            if len(result) == 0:
                sql_command = """INSERT INTO albumartist (name) VALUES ("%s")""" % (albumartist)
                try:
                    print("Running: {} ".format(sql_command))
                    cursor.execute(sql_command)
                    connection.commit()
                except Exception as e:
                    print("INSERT INTO albumartist error. ".format(e))
            
            
def create_new_db():
    """
    this will delete the database and recreate all tables
    :return:
    """
    print("Create new DB..")
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    db_host = config['DEFAULT']['server']
    db_user = config['DEFAULT']['user']
    db_pass = config['DEFAULT']['pass']
    db_database = config['DEFAULT']['db_database']
    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass, charset='utf8')
    # conn.cursor().set_character_set('utf8')
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
