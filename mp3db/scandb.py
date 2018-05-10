# mp3 collection thing
from pathlib import Path
from .database import *
import configparser
import time
import threading
import pymysql.cursors
import pymysql
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

# For use in signaling
shutdown_event = threading.Event()

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
        print("Error reading tag from {} {}".format(mp3file, e))
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
    # create fake filehash for faster searching...
    size = os.path.getsize(filename)
    filehash = filename.encode('utf-8')
    filehash = hashlib.md5(filehash)
    filehash = filehash.hexdigest()
    return filehash


def update_db(mp3list_temp, dbconfig,time_diff):
    start_time = time.time()
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    cnx.autocommit = True
    # cursor = cnx.cursor()
    print ("Starting file scan....")
    with cnx.cursor() as cursor:
        if not shutdown_event.is_set():
            for file in mp3list_temp:
                file = os.path.realpath(file)
                file = file.replace('\\', '/')
                filehash = get_hash(file)
                # cursor.execute("SELECT * FROM Files WHERE Filename LIKE %s ", (file,))
                cursor.execute("SELECT filehash FROM Files WHERE filehash = %s ", (filehash,))
                data = cursor.fetchone()
                #                connector.commit()
                if data is None:  # Search db, insert if file not already in db
                    meta = getmetadata_mutagen(file)
                    filesize = os.path.getsize(file)
                    file_id = db_insert_filename_mutagen(cnx, cursor=cursor, size=filesize, filename=file, metadata=meta, filehash=filehash)
                    if file_id:
                        print ("Inserted {} ".format(file))
                        db_process_filename2(cnx, cursor, file_id)
                    else:
                        print ("Error reading file {} ".format(filename))
    cnx.close() #
    end_time = time.time()
    time_diff += (end_time - start_time)
    print('Scanned THREAD  elapsed time {} '.format(time_diff))


# with cnx.cursor() as cursor:
#     if not shutdown_event.is_set():
#         # cursor.execute("SELECT * FROM Files WHERE Filename LIKE %s ", (file,))
#         cursor.execute("SELECT filehash FROM Files WHERE filehash = %s ", (filehash,))
#         data = cursor.fetchone()
#         #                connector.commit()
#         if data is None:  # Search db, insert if file not already in db
#             meta = getmetadata_mutagen(file)
#             filesize = os.path.getsize(file)
#             file_id = db_insert_filename_mutagen(cnx, cursor=cursor, size=filesize, filename=file, metadata=meta,
#                                                  filehash=filehash)
#             if file_id:
#                 print("Inserted {} ".format(file))
#                 db_process_filename2(cnx, cursor, file_id)
#             else:
#                 print("Error reading file {} ".format(filename))


def run_scan(dbconfig,mp3_root):
    thread_id = 1
    threads = []
    max_threads = 4
    time_diff = 0
    start_time = time.time()

    create_new_db(dbconfig)
    truncate_db(dbconfig)
    # build file list
    mp3list = scanfolder_glob(mp3_root)

    filenumber = 0
    mp3list_temp = []
    for k in mp3list:
        filenumber += 1
        mp3list_temp.append(k)

    slice_size = int(len(mp3list_temp) / 4)
    path_list_1 = mp3list_temp[0:slice_size]
    path_list_2 = mp3list_temp[slice_size:slice_size * 2]
    path_list_3 = mp3list_temp[slice_size * 2: slice_size * 3]
    path_list_4 = mp3list_temp[slice_size * 3: len(mp3list_temp)]

    t1 = threading.Thread(target=update_db, args=(path_list_1, dbconfig, time_diff))
    t1.start()
    threads.append(t1)

    t2 = threading.Thread(target=update_db, args=(path_list_2, dbconfig, time_diff))
    t2.start()
    threads.append(t2)

    t3 = threading.Thread(target=update_db, args=(path_list_3, dbconfig, time_diff))
    t3.start()
    threads.append(t3)

    t3 = threading.Thread(target=update_db, args=(path_list_4, dbconfig, time_diff))
    t3.start()
    threads.append(t3)

    end = time.clock()
    for i in threads:
        i.join(timeout=0.1)
        #print ("Thread {} terminating".format(i))
        end_time = time.time()
        #print('Scanned {0:} elapsed time {1:8.2f} '.format(mp3_root, (end_time - start_time)))

if __name__ == "__main__":
    run_scan(dbconfig,path)