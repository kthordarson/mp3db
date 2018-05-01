# mp3 collection thing

# from mediafile import MediaFile
from pathlib import Path
from database import *
import configparser
import taglib
import time

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
    try:
        cursor.execute(sql_search, filename)
        data = cursor.fetchone()
    except:
        print ("searchfilename failed.. {}".format(filename))
        data = None
        pass
    if data is None:
        #print('There is no file named [{}] in our database'.format(filename))
        return False
    else:
        #print('Component %s found in %s row(s)' % (filename, data))
        return True
    # return True

def update_file_list(conn,mp3list):
    """
    # refresh file list and update db if needed
    :param conn: connection object
    :param mp3list: list of files
    :return:
    """
    for file in sorted(mp3list):
        with conn:
            file = os.path.realpath(file)
            file = file.replace('\\', '/')
            if searchfilename(conn=conn, filename=file) == False:  # Search db, insert if file not already in db
                meta = getmetadata_taglib(file)
                filesize = os.path.getsize(file)
                try:
                    result = db_insert_filename_taglib(conn=conn, size=filesize, filename=file, metadata=meta)
                    # result = db_insert_filename(conn=conn, size=filesize, filename=file, metadata=meta)
                except KeyError as e:
                    print ("KeyError in update_file_list {} {} ".format(e, file))
                    pass

    return

if __name__ == "__main__":
    start_time = time.time()
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    db_host = config['DEFAULT']['server']
    db_user = config['DEFAULT']['user']
    db_pass = config['DEFAULT']['pass']
    db_database = config['DEFAULT']['db_database']

    mp3_root = config['DEFAULT']['mp3_root_path']
    conn = pymsql_connect(db_host, db_user, db_pass, db_database)

#    create_new_db()
    mp3list = scanfolder_glob(mp3_root)
    update_file_list(conn,mp3list)
    end_time = time.time()

    print('Scanned {0:} elapsed time {1:8.2f} '.format(mp3_root, (end_time - start_time)))
