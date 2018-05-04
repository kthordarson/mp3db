import pymysql.cursors
import configparser
import os
import hashlib
import time
import warnings


def db_insert_filename_mutagen(conn, cursor, filename, size, metadata):
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

    tag_list = {'filehash': filehash, 'filename': filename, 'size': str(size)}
    try:
        cursor.execute('INSERT IGNORE INTO Files (filehash,filename,size) VALUES (%s, %s, %s)',
                       (filehash, filename, size))
        file_id = cursor.lastrowid
        conn.commit()
    except:
        file_id = 0
        pass

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
            cursor.execute('ALTER TABLE Files ADD %s varchar (255) ' % (field))
        except:
            pass

        last_row = int(file_id)
        try:
            cursor.execute("UPDATE IGNORE Files set {} = '{}' WHERE file_id = {}".format(field, tag_value, int(
                last_row)))  # conn.commit()
        except Exception as e:
            pass
    # cursor.execute('select album,artist,file_id,title from files ') # update other tables from file_id
    cursor.execute('select album, artist, file_id, title from files WHERE file_id = {}'.format(file_id)) # update other tables from file_id
    # print ("Working on {} ".format(filename))
    escapes = ''.join([chr(char) for char in range(1, 32)])
    for row in cursor.fetchall():
        album, artist, file_id, title = row
        # title = title.translate(None, escapes)
        # cursor.execute('insert into album (album, artist) VALUES (%s,%s)',(row[0], row[1]))
        # print ("INSERT INTO album (album, artist) VALUES '{}','{}'".format(album,artist))
        cursor.execute("INSERT INTO album (title, artist) VALUES ('{}','{}')".format(album, artist))
        album_id = cursor.lastrowid
        cursor.execute("INSERT INTO artist (name) VALUES ('{}')".format(artist))
        artist_id = cursor.lastrowid
        sql_command = "INSERT INTO song (file_id, title, album_id, artist_id) VALUES (%s, %s, %s, %s )"
        try:
            #cursor.execute("INSERT INTO song (file_id, title, album_id, artist_id) VALUES ('{}','{}','{}','{}')".format(file_id, title,  album_id, artist_id))
            cursor.execute(sql_command,(file_id, title,  album_id, artist_id))
        except Exception as e:
            print ("Error processing {} {}".format(filename,e))
    return


def populate_tables(dbconfig):
    cnx = pymysql.connect(**dbconfig)
    cnx.autocommit = True
    cursor = cnx.cursor()
    start_time = time.time()
    start = time.clock()

    # now populate other tables
    # cursor_table1.execute('insert into table2 (part, min, max, unitPrice, date) select part, min, max, unitPrice, now() from table1')
    # cursor_table1.execute('SELECT part, min, max, unitPrice, NOW() from table1')
    # for row in cursor_table1.fetchall():
    #    part, min, max, unitPrice, now = row
    #    cursor_table2.execute("INSERT INTO table2 VALUES (%s,%s,%s,%s,'%s')" % (
    #    part, min, max, unitPrice, now.strftime('%Y-%m-%d %H:%M:%S')))
    print ("Populating tables....")
    cursor.execute('select album,artist,file_id,title from files ')
    for row in cursor.fetchall():
        album, artist, file_id, title = row
        # cursor.execute('insert into album (album, artist) VALUES (%s,%s)',(row[0], row[1]))
        # print ("INSERT INTO album (album, artist) VALUES '{}','{}'".format(album,artist))
        cursor.execute("INSERT INTO album (title, artist) VALUES ('{}','{}')".format(album, artist))
        album_id = cursor.lastrowid
        cursor.execute("INSERT INTO artist (name) VALUES ('{}')".format(artist))
        artist_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO song (file_id,title,album_id, artist_id) VALUES ('{}','{}','{}','{}')".format(file_id, title,
                                                                                                       album_id,
                                                                                                       artist_id))
    cnx.commit()
    end_time = time.time()
    print('Done populating elapsed time {} '.format((end_time - start_time)))



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
    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_database, charset='utf8')
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
