import pymysql.cursors
import configparser
import os
import hashlib

def db_insert_filename_mutagen(conn, cursor, filename, size, metadata):
    """ insert data into database
    :param conn: connection
    :param filename: filename to insert
    :param size of file
    :param metadata object
    """
    # insert data into database
    filename = os.path.realpath(filename)
    filename = filename.replace('\\', '/')

    #create fake filehash for faster searching...
    filehash = (str(size)+filename)
    filehash = filename.encode('utf-8')
    filehash = hashlib.md5(filehash)
    filehash = filehash.hexdigest()

    tag_list = {'filehash':filehash, 'filename':filename, 'size': str(size)}
    try:
        cursor.execute('INSERT IGNORE INTO Files (filehash,filename,size) VALUES (%s, %s, %s)', (filehash,filename,size))
        last_row = cursor.lastrowid
        conn.commit()
    except:
        last_row = 0
        pass


    # insert all found fields into DB
    create_column = False
    if metadata is None:
        metadata = {'filename':filename}
    index = 0
    try: # populate a valid tag_list with all available metadata from file
        for index, element in enumerate(metadata):
            tag_list[element[0]] =  element[1]
            index += 1
    except AttributeError as e:
        print ("meta tag read error {} in file {} ".format(e, filename))

    for field,tag_value in tag_list.items():
        tag_value = ''.join(tag_value)
        try:
            # exception, try to add column "field" to table
            cursor.execute('ALTER TABLE Files ADD %s varchar (255) ' % (field))
            create_column = False
        except: pass

        last_row = int(last_row)
        try:
            cursor.execute("UPDATE IGNORE Files set {} = '{}' WHERE file_id = {}".format(field, tag_value, int(last_row)))            # conn.commit()
        except Exception as e:
            pass

        result = cursor.fetchone()
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
    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass, database=db_database,charset='utf8')
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
    conn.commit()
    # db.close()
