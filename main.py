# mp3 collection thing

# from mediafile import MediaFile
from pathlib import Path
from database import *
import configparser
import taglib
import time
import fnmatch
import threading

# For use in signaling
shutdown_event = threading.Event()
import pymysql.cursors
import pymysql


def getmetadata_taglib(mp3file):
    """
    scan mp3 file with pytaglib
    :param mp3file: full path of filename to scan
    :return: metadata
    """
    # metadata = None
    mp3file = os.path.realpath(mp3file)
    try:
        f = taglib.File(mp3file)
        return f
    except OSError as e:
        print ("Error reading tag from {} ".format(mp3file))
        time.sleep(1)
    return None

def scanfolder_glob(folder):
    """
    scan folder for mp3 files
    :param folder: root folder of mp3 files
    :return: list of mp3 files
    """
    found_files = Path(folder).glob('**/*.mp3')
    return found_files

def get_hash(filename):
    #create fake filehash for faster searching...
    size = os.path.getsize(filename)
    filehash = (str(size)+filename)
    filehash = filename.encode('utf-8')
    filehash = hashlib.md5(filehash)
    filehash = filehash.hexdigest()
    return filehash

def update_db(mp3list_temp, dbconfig):
    # cnx = mysql.connector.connect(**dbconfig)
    cnx = pymysql.connect(**dbconfig)
    cnx.autocommit = True
#    cursor = cnx.cursor(buffered=True)

    numberofthreads = 4
    threadlist = []
    thread_id = 1
    cursor = cnx.cursor()
    sql_search = ("SELECT * FROM Files WHERE Filename LIKE %s")
    run_counter = 1
    max_files = len(mp3list_temp)
    mp3list_temp = iter(mp3list_temp)

    while run_counter < max_files:
        if not shutdown_event.is_set():
            file = next(mp3list_temp)
            file = os.path.realpath(file)
            file = file.replace('\\', '/')
            filehash = get_hash(file)
            #cursor.execute(sql_search, file)
            # cursor.execute("SELECT * FROM Files WHERE Filename LIKE %s ", (file,))
            cursor.execute("SELECT * FROM Files WHERE filehash = %s ", (filehash,))
            cnx.commit()
            data = cursor.fetchone()
            if data is None:  # Search db, insert if file not already in db
                meta = getmetadata_taglib(file)
                filesize = os.path.getsize(file)
                db_insert_filename_taglib_cursor(cnx, cursor=cursor, size=filesize, filename=file, metadata=meta)
            #else: print (file + " already in db")
    cnx.close()



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

    start_time = time.time()
    start = time.clock()

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

    create_new_db()
    # build file list
    mp3list = scanfolder_glob(mp3_root)

    filenumber = 0
    mp3list_temp = []
    for k in mp3list:
        filenumber += 1
        mp3list_temp.append(k)

    threads = []
    thread_id = 1
    max_threads = 4

    for x in range(max_threads):
        t = threading.Thread(target=update_db, args=(mp3list_temp, dbconfig))
        t.start()
        threads.append(t)
    end = time.clock()
    try:
        for i in threads:
            i.join(timeout=1.0)
    except (KeyboardInterrupt, SystemExit):
        print ("Caught Ctrl-C. Cleaning up. Exiting.")
        shutdown_event.set()
    end_time = time.time()

    print('Scanned {0:} elapsed time {1:8.2f} '.format(mp3_root, (end_time - start_time)))

