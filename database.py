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
