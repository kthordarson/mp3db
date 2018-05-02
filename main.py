# mp3 collection thing

# from mediafile import MediaFile
from pathlib import Path
from database import *
import configparser
import taglib
import time
from threading import Thread
import fnmatch
from multiprocessing import Pool
from queue import Queue
import sys
# import MySQLdb
import mysql.connector
from mysql.connector import errorcode
from mysql.connector.errors import Error
import threading
# For use in signaling
shutdown_event = threading.Event()


def getmetadata_taglib(mp3file):
    """
    scan mp3 file with pytaglib
    :param mp3file: full path of filename to scan
    :return: metadata
    """
    # metadata = None
    f = taglib.File(mp3file)
    try:
        album = ''.join(f.tags["ALBUM"])
    except:
        f.tags["ALBUM"] = ''

    try:
        title = ''.join(f.tags["TITLE"])
    except:
        f.tags["TITLE"] = ''

    try:
        artist = ''.join(f.tags["ARTIST"])
    except:
        f.tags["ARTIST"] = ''

    # print (f.tags)
    return f

def scanfolder_glob(folder):
    """
    scan folder for mp3 files
    :param folder: root folder of mp3 files
    :return: list of mp3 files
    """
    found_files = Path(folder).glob('**/*.mp3')
    return found_files

def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename



def searchfilename(conn, filename):
    """
    search database for filename. Returns True if found, otherwise False
    :param conn: connection object
    :param filename: file to search for
    :return: true or false
    """
    cursor = conn.cursor()
    filename = os.path.realpath(filename)
    filename = filename.replace('\\', '/')
    sql_search = "SELECT * FROM Files WHERE Filename LIKE %s"
    cursor.execute(sql_search, filename)
    data = cursor.fetchone()
    cursor.close()
    if data is None:
        #print('There is no file named [{}] in our database'.format(filename))
        return False
    else:
        #print('Component %s found in %s row(s)' % (filename, data))
        return True
    # return True

def update_db(file_list, dbconfig):
    cnx = mysql.connector.connect(**dbconfig)
    cnx.autocommit = True
    cursor = cnx.cursor(buffered=True)

    numberofthreads = 4
    threadlist = []
    thread_id = 1
    # cursor = conn.cursor()
    sql_search = ("SELECT * FROM Files WHERE Filename LIKE %s")

    for file in file_list:
        if not shutdown_event.is_set():
            file = os.path.realpath(file)
            file = file.replace('\\', '/')
            #cursor.execute(sql_search, file)
            cursor.execute("SELECT * FROM Files WHERE Filename LIKE %s ", (file,))
            data = cursor.fetchone()
            if data is None:  # Search db, insert if file not already in db
                meta = getmetadata_taglib(file)
                filesize = os.path.getsize(file)
                db_insert_filename_taglib_cursor(cursor=cursor, size=filesize, filename=file, metadata=meta)
            #else: print (file + " already in db")
    cnx.close()

def update_db_file(conn,file):
    #cursor = conn.cursor()
    sql_search = "SELECT * FROM Files WHERE Filename LIKE %s"
    file = os.path.realpath(file)
    file = file.replace('\\', '/')
    cursor.execute(sql_search, file)
    data = cursor.fetchone()
    cursor.close()
    #print ("fff")
    if data is None:  # Search db, insert if file not already in db
        meta = getmetadata_taglib(file)
        filesize = os.path.getsize(file)
        db_insert_filename_taglib_cursor(conn=conn, size=filesize, filename=file, metadata=meta)
    else: print (file + " already in db")
    conn.commit()

def update_file_list(conn,mp3list, thread_id=1):
    """
    # refresh file list and update db if needed
    :param conn: connection object
    :param mp3list: list of files
    :return:
    """

    cursor = conn.cursor()
    sql_search = "uSELECT * FROM Files WHERE Filename LIKE %s"
    print ("Started updating file list")
    for file in sorted(mp3list):
        if not shutdown_event.is_set():
            file = os.path.realpath(file)
            file = file.replace('\\', '/')
            cursor.execute(sql_search,file)
            data = cursor.fetchone()
            if data is None:  # Search db, insert if file not already in db
                meta = getmetadata_taglib(file)
                filesize = os.path.getsize(file)
                db_insert_filename_taglib(conn=conn, size=filesize, filename=file, metadata=meta)
            #else: # print (file + " already in db")

    return

def grab_files(directory):
    for name in os.listdir(directory):
        full_path = os.path.join(directory, name)
        if os.path.isdir(full_path):
            for entry in grab_files(full_path):
                yield entry
        elif os.path.isfile(full_path):#  and Path(full_path).suffix == 'mp3':
            if Path(full_path).suffix == 'mp3':
                yield full_path
        #else:
            #print('Unidentified name %s. It could be a symbolic link' % full_path)

if __name__ == "__main__":

    numberofthreads = 4
    threadlist = []
    thread_id = 1

    # set up the queue to hold all the urls
    q = Queue(maxsize=0)
    # Use many threads (50 max, or one for each url)
    start_time = time.time()

    # read config file
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    db_host = config['DEFAULT']['server']
    db_user = config['DEFAULT']['user']
    db_pass = config['DEFAULT']['pass']
    db_database = config['DEFAULT']['db_database']
    mp3_root = config['DEFAULT']['mp3_root_path']
    dbconfig = {
        "user" : db_user,
        "password" : db_pass,
        "database": db_database,
        "host" : db_host,
    }
    # connect to our db
#    conn = pymsql_connect(db_host, db_user, db_pass, db_database)

    create_new_db()
    # build file list
    mp3list = scanfolder_glob(mp3_root)

    filenumber = 0
    mp3list_temp = []
    for k in mp3list:
        filenumber += 1
        mp3list_temp.append(k)
    update_db(mp3list_temp,dbconfig=dbconfig)

    end_time = time.time()
    print('Scanned {0:} elapsed time {1:8.2f} '.format(mp3_root, (end_time - start_time)))
