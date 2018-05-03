import pymysql.cursors
import configparser
import os
import hashlib

def db_insert_filename_taglib_cursor(conn, cursor, filename, size, metadata):
    """ insert data into database
    :param conn: connection
    :param filename: filename to insert
    :param size of file
    :param metadata object
    """
    # insert data into database
    #cursor = conn.cursor()
    filename = os.path.realpath(filename)
    filename = filename.replace('\\', '/')

    #create fake filehash for faster searching...
    filehash = (str(size)+filename)
    filehash = filename.encode('utf-8')
    filehash = hashlib.md5(filehash)
    filehash = filehash.hexdigest()

#    album = ''.join(metadata.tags["ALBUM"])
#    title = ''.join(metadata.tags["TITLE"])
#    artist = ''.join(metadata.tags["ARTIST"])
    tag_list = {'filehash':filehash, 'filename':filename, 'size': str(size)}
    try:
        cursor.execute('INSERT IGNORE INTO Files (filehash,filename,size) VALUES (%s, %s, %s)', (filehash,filename,size))
        last_row = cursor.lastrowid
        conn.commit()
    except:
        last_row = 0
        pass


    # insert all found fields into DB
    #print ("Filename: {} ".format(filename))
    create_column = False
    if metadata is None:
        metadata = {'filename':filename}

    try:
        for tag in metadata.tags:
            tag_list[tag] = metadata.tags[tag]
    except AttributeError as e:
        print ("meta tag read error {} in file {} ".format(e, filename))

    for field,tag_value in tag_list.items():
        try:
            tag_value = ''.join(tag_value)
        except:
            pass
        try:
            result = cursor.execute('select * FROM %s' % (field))
            # conn.commit()
            create_column = True
        except:
            pass
            #print ("select failed for {} ".format(field))
        if create_column:
           try:
                cursor.execute('ALTER TABLE Files ADD %s varchar (255) ' % (field))
                # conn.commit()
           except:
                #print ("Could not create {} ".format(field) )
                pass
        #sql_string ='INSERT INTO Files ( '  + field + ') VALUE ("' + tag_value + '") WHERE file_id = ' + str(last_row) # WHERE filehash='+filehash
        # sql_string = 'UPDATE IGNORE Files SET  ' + field + ' = "' + tag_value + '" WHERE file_id = ' + str(last_row)  # WHERE filehash='+filehash
        #sql_string = 'UPDATE IGNORE Files SET  ' + field + ' = "' + tag_value + '" WHERE file_id = ' + str(last_row)  # WHERE filehash='+filehash
        sql_string = "UPDATE IGNORE Files SET  %s = $s WHERE file_id = %s"
        # print ("inserting from {} ---- {} ".format(filename, sql_string))
        last_row = int(last_row)
        try:
            #cursor.execute(sql_string, (field, tag_value, last_row))
            cursor.execute("UPDATE IGNORE Files set {} = '{}' WHERE file_id = {}".format(field, tag_value, int(last_row)))            # conn.commit()
            #conn.close()
        except Exception as e:
            pass
            #print ("Error in UPDATE {} {}".format(e, sql_string))

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
