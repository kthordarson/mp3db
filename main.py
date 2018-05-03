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
    #if f is not None: return f
    #    album = ''.join(f.tags["ALBUM"])
    #    title = ''.join(f.tags["TITLE"])
    # try:
    #     album = ''.join(f.tags["ALBUM"])
    # except:
    #     f.tags["ALBUM"] = ''
    # try:
    #     title = ''.join(f.tags["TITLE"])
    # except:
    #     f.tags["TITLE"] = ''
    #
    # try:
    #     artist = ''.join(f.tags["ARTIST"])
    # except:
    #     f.tags["ARTIST"] = ''
    #
    # # print (f.tags)
    return None

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

def get_hash(filename):
    #create fake filehash for faster searching...
    size = os.path.getsize(filename)
    filehash = (str(size)+filename)
    filehash = filename.encode('utf-8')
    filehash = hashlib.md5(filehash)
    filehash = filehash.hexdigest()
    return filehash

def update_db(file_list, dbconfig):
    # cnx = mysql.connector.connect(**dbconfig)
    cnx = pymysql.connect(**dbconfig)
    cnx.autocommit = True
#    cursor = cnx.cursor(buffered=True)

    numberofthreads = 4
    threadlist = []
    thread_id = 1
    cursor = cnx.cursor()
    sql_search = ("SELECT * FROM Files WHERE Filename LIKE %s")

    for file in file_list:
        if not shutdown_event.is_set():
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

def update_db_file(file, dbconfig):
    # cnx = mysql.connector.connect(**dbconfig)
    cnx = pymysql.connect(**dbconfig)
    cnx.autocommit = True
    cursor = cnx.cursor()

    file = os.path.realpath(file)
    file = file.replace('\\', '/')
    filehash = get_hash(file)
    # cursor.execute(sql_search, file)
    # cursor.execute("SELECT * FROM Files WHERE Filename LIKE %s ", (file,))
    cursor.execute("SELECT * FROM Files WHERE filehash = %s ", (filehash,))
#    cnx.commit()
    data = cursor.fetchone()
    if data is None:  # Search db, insert if file not already in db
        meta = getmetadata_taglib(file)
        filesize = os.path.getsize(file)
        db_insert_filename_taglib_cursor(cnx, cursor=cursor, size=filesize, filename=file, metadata=meta)
    # else: print (file + " already in db")
    cnx.close()

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

def generate_filename(list):
    for x in list:
        yield x

if __name__ == "__main__":


    # set up the queue to hold all the urls
    # Use many threads (50 max, or one for each url)
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
    # connect to our db
#    conn = pymsql_connect(db_host, db_user, db_pass, db_database)

    # create_new_db()
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
    run_counter = 1
    max_files = len(mp3list_temp)
    mp3list_temp = iter(mp3list_temp)
    for x in range(max_threads):
        while run_counter <= max_files:
            print("Running {} ".format(run_counter))
            files = next(mp3list_temp)
            t = threading.Thread(target=update_db_file, args=(files,dbconfig))
            t.start()
            threads.append(t)
            thread_id += 1
            run_counter += 1
            for i in threads:
                i.join(timeout=0.1)
        #print ('Waiting for threads...')
        # update_db(mp3list_temp,dbconfig=dbconfig)
    end = time.clock()
    print ("The time was {}".format(end - start))
    end_time = time.time()
    print('Scanned {0:} elapsed time {1:8.2f} '.format(mp3_root, (end_time - start_time)))
