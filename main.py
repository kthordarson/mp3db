# mp3 collection thing

from mediafile import MediaFile
import os
from pathlib import Path
from hashing import get_hash
from database import *


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

def read_metadata(mp3file):
    """
    scan mp3 file for metadata and return it
    """
    metadata = None
    f = MediaFile(mp3file)
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
    filename = os.path.normpath(filename)
    cursor.execute("SELECT * FROM `Files` WHERE `Filename` LIKE %s", [filename] )
    data = cursor.fetchone()

    if data is None:
        #print('There is no file named [{}] in our database'.format(filename))
        return False
    else:
        # print('Component %s found in %s row(s)' % (filename, data))
        return True

def update_file_list(conn,mp3list):
    # refresh file list and update db if needed
    for file in sorted(mp3list):
        with conn:
            if not searchfilename(conn=conn, filename=file):  # Search db, insert if file not already in db
                # md5 = get_hash(file)
                md5 = get_hash(file)
                hash = md5.hexdigest()
                meta = read_metadata(file)
                #print ('Update DB {} '.format(meta))
                result = db_insert_filename(conn=conn, hash=hash, filename=file.absolute(), metadata=meta)
    return

if __name__ == "__main__":
    database = 'mydb.db'
    #    unlock_db(database)
    mp3_root = 'f:/mp3dev/'
    conn = pymsql_connect()
    create_new_db()
    mp3list = scanfolder_glob(mp3_root)

    update_file_list(conn,mp3list)

    # read some tags and print
    files = db_getfilelist(conn=conn)
    for file in files:
        getmetadata(file)
