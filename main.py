# mp3 collection thing
from pathlib import Path
from database import *
import configparser
import time
import threading
import pymysql.cursors
import pymysql
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
# For use in signaling
shutdown_event = threading.Event()


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

def getmetadata_mutagen(mp3file):
    """
    scan mp3 file with pytaglib
    :param mp3file: full path of filename to scan
    :return: metadata
    """
    # metadata = None
    mp3file = os.path.realpath(mp3file)
    try:
        f = MP3(mp3file, ID3=EasyID3)
        klist = []
        metadata = []
        for a, b in f.items():
            klist.append(a)
            # print (a,b)

        for valid_tags in klist:
            metadata.append((valid_tags, f.ID3.get(f, valid_tags)[0]))

        return metadata
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
    cnx = pymysql.connect(**dbconfig)
    cnx.autocommit = True
    cursor = cnx.cursor()
    run_counter = 1
    with cnx as connector:
        for file in mp3list_temp:
            if not shutdown_event.is_set():
                file = os.path.realpath(file)
                file = file.replace('\\', '/')
                filehash = get_hash(file)
                # cursor.execute("SELECT * FROM Files WHERE Filename LIKE %s ", (file,))
                cursor.execute("SELECT * FROM Files WHERE filehash = %s ", (filehash,))
#                connector.commit()
                data = cursor.fetchone()
                if data is None:  # Search db, insert if file not already in db
                    meta = getmetadata_mutagen(file)
                    filesize = os.path.getsize(file)
                    db_insert_filename_mutagen(cnx, cursor=cursor, size=filesize, filename=file, metadata=meta)
                run_counter += 1
    #cnx.close() # TODO use WITH

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

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))
def split_seq(seq, p):
    newseq = []
    n = len(seq) / p    # min items per subsequence
    r = len(seq) % p    # remaindered items
    b,e = 0, n + min(1, r)  # first split
    for i in range(p):
        newseq.append(seq[b:e])
        r = max(0, r-1)  # use up remainders
        b,e = e, e + n + min(1, r)  # min(1,r) is always 0 or 1

    return newseq

if __name__ == "__main__":
    threads = []
    thread_id = 1
    max_threads = 4

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
        "charset":'utf8',
    }

    create_new_db()
    # build file list
    mp3list = scanfolder_glob(mp3_root)

    filenumber = 0
    mp3list_temp = []
    for k in mp3list:
        filenumber += 1
        mp3list_temp.append(k)

    slice_size = int (len(mp3list_temp) / 4)
    path_list_1 = mp3list_temp[0:slice_size]
    path_list_2 = mp3list_temp[slice_size:slice_size * 2 ]
    path_list_3 = mp3list_temp[slice_size * 2 : slice_size * 3]
    path_list_4 = mp3list_temp[slice_size * 3 : len(mp3list_temp)]

    t1 = threading.Thread(target=update_db, args=(path_list_1, dbconfig))
    t1.start()
    threads.append(t1)

    t2 = threading.Thread(target=update_db, args=(path_list_2, dbconfig))
    t2.start()
    threads.append(t2)

    t2 = threading.Thread(target=update_db, args=(path_list_3, dbconfig))
    t2.start()
    threads.append(t2)

    t2 = threading.Thread(target=update_db, args=(path_list_4, dbconfig))
    t2.start()
    threads.append(t2)

    end = time.clock()
    try:
        for i in threads:
            i.join(timeout=1.0)
    except (KeyboardInterrupt, SystemExit):
        print ("Caught Ctrl-C. Cleaning up. Exiting.")
        shutdown_event.set()
    end_time = time.time()

    print('Scanned {0:} elapsed time {1:8.2f} '.format(mp3_root, (end_time - start_time)))

    # done scanning
    # populate tables
    populate_tables(dbconfig)
