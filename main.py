# mp3 collection thing

from mediafile import MediaFile
import os
from pathlib import Path
from hashing import get_hash
from database import *
import configparser
import taglib
import time

def getmetadata(mp3file):
    """
    scan mp3 file for metadata and return it
    """
    metadata = None
    f = MediaFile(mp3file[2])
    if f.title is None:
        f.title = ''

    if f.album is None:
        f.album = ''
    if f.albumartist is None:
        f.albumartist = ''
    print("[getmetadata] [Album] {} [Artist] {} [Title] {}".format(f.album, f.albumartist, f.title))
#    db_insert_album(conn, f.album, f.albumartist)
    return metadata
def getmetadata_taglib(mp3file):
    """
    scan mp3 file with pytaglib
    :param mp3file: full path of filename to scan
    :return: metadata
    """
    metadata = None
    f = taglib.File(mp3file)
    print (f.tags)
    return f
def read_metadata(mp3file):
    """
    scan mp3 file for metadata and return it
    """
    metadata = None
    try:
        f = MediaFile(mp3file)
    except:
        print ("Could not read metadata from {} ".format(f))
    if f.title is None:
        f.title = ''

    if f.album is None:
        f.album = ''
    if f.albumartist is None:
        f.albumartist = ''
    return f

def scanfolder_glob(folder):
    """ return list of mp3 files """
    found_images = Path(folder).glob('**/*.mp3')
    return found_images


def searchfilename(conn, filename):
    """ search database for filename. Returns True if found, otherwise False """
    cursor = conn.cursor()
    filename = os.path.realpath(filename)
    filename = filename.replace('\\', '/')
    sql_search = "SELECT * FROM Files WHERE Filename LIKE %s"
    try:
        cursor.execute(sql_search, filename)
        data = cursor.fetchone()
    except:
        print ("Err search failed..")
        data = None
        pass
    #cursor.execute("SELECT * FROM Files WHERE Filename LIKE %s", ('%'+filename+'%') )
    #print ("Searching for {} ".format(filename))
    #print ("res {}".format(data))
    if data is None:
        #print('There is no file named [{}] in our database'.format(filename))
        return False
    else:
        #print('Component %s found in %s row(s)' % (filename, data))
        return True
    return True

def search_file_hash(conn, hash):
    """ search database for filename. Returns True if found, otherwise False """
    cursor = conn.cursor()
    filename = os.path.realpath(filename)
    filename.file.replace('\\', '/')
    cursor.execute("SELECT * FROM Files WHERE Hash LIKE %s", ('%'+hash+'%') )
    data = cursor.fetchone()
    if data is None:
        #print('There is no file named [{}] in our database'.format(filename))
        return False
    else:
        #print('Component %s found in %s row(s)' % (filename, data))
        return True

def update_file_list(conn,mp3list):
    # refresh file list and update db if needed
    for file in sorted(mp3list):
        with conn:
            file = os.path.realpath(file)
            file = file.replace('\\', '/')
            if searchfilename(conn=conn, filename=file) == False:  # Search db, insert if file not already in db
                # md5 = get_hash(file)
                # md5 = get_hash(file)
                # hash = md5.hexdigest()
                #meta = read_metadata(file)
                meta = getmetadata_taglib(file)
                filesize = os.path.getsize(file)
                #print ('Update DB {} '.format(meta))
                try:
                    result = db_insert_filename_taglib(conn=conn, size=filesize, filename=file, metadata=meta)
                    # result = db_insert_filename(conn=conn, hash=hash, filename=file, metadata=meta)
                except:
                    print ("Error in update_file_list {} ".format(file))
                    pass
    return

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    db_host = config['DEFAULT']['server']
    db_user = config['DEFAULT']['user']
    db_pass = config['DEFAULT']['pass']
    db_database = config['DEFAULT']['db_database']
    database = 'mydb.db'
    #    unlock_db(database)
    mp3_root = config['DEFAULT']['mp3_root_path']
    conn = pymsql_connect(db_host, db_user, db_pass, db_database)
    create_new_db()
    start_time = time.time()
    mp3list = scanfolder_glob(mp3_root)
    update_file_list(conn,mp3list)
    end_time = time.time()
    print('Scanned {0:} elapsed time {1:8.2f} '.format(mp3_root, (end_time - start_time)))

    # read some tags and print
#    files = db_getfilelist(conn=conn)
#    for file in files:
#        getmetadata(file)
