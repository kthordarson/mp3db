from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime
from django.shortcuts import render
import pymysql.cursors
import pymysql
from .scandb import run_scan

dbconfig = {
    "user": 'mp3db',
    "password": 'mp3db',
    "database": 'mp3dbweb',
    "host": 'localhost',
    "charset": 'utf8',
}


def hello(request):
    return render(request,'index.html')

def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'current_datetime.html', {'current_date': now})

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]


def artist_list(request):
    #db = MySQLdb.connect(**dbconfig)
    cnx = pymysql.connect(**dbconfig)
    cursor = cnx.cursor()
    sql_command = """
        SELECT artist.artist_id, artist.artistname,
        (SELECT COUNT(*) from album WHERE artist.artist_id = album.artist_id) as "albumcount"
        FROM artist    
    """
    cursor.execute(sql_command)
    result = dictfetchall(cursor)
    return render(request,'artist_list.html', {'result': result})
    return artist

def artist(request):
    cnx = pymysql.connect(**dbconfig)
    cursor = cnx.cursor()
#    sql_command = """SELECT artist_id, artistname FROM artist artist_id = %s"""
    if 'id' in request.GET:
        id = request.GET['id']
        if not id:
            error = True
        else:
            sql_command = """select * from artist where artist_id = %s"""
            cursor.execute(sql_command,[id])
            results = dictfetchall(cursor)
            cursor.execute("SELECT COUNT(*) from album where artist_id=%s",[id])
            albumcount = cursor.fetchone()
            albumcount = albumcount[0]
            return render(request,'artist.html', {'results': results, 'albumcount':albumcount})
    else:
        cursor.execute("SELECT * from artist")
        # cursor.execute(sql_command)
        results = dictfetchall(cursor)
        return render(request, 'artist.html', {'results': results})
    return artist


def getalbums(request):
    cnx = pymysql.connect(**dbconfig)
    cursor = cnx.cursor()
    if 'id' in request.GET:
        id = request.GET['id']
        if not id:
            error = True
        else:
            sql_command = "SELECT artistname FROM artist WHERE artist_id = %s"
            cursor.execute(sql_command,[id])
            result = cursor.fetchone()
            artist_name = str(result)
            sql_command ="SELECT * from album where artist_id = %s"
            cursor.execute(sql_command,[id])
            result = dictfetchall(cursor)
            return render(request, 'getalbums.html', {'result': result, 'artist_name':artist_name})
    else:
            sql_command = "SELECT * from album"
            cursor.execute(sql_command)
            result = dictfetchall(cursor)
            return render(request, 'getalbums.html', {'result': result})


def getalbum_tracks(request):
    cnx = pymysql.connect(**dbconfig)
    cursor = cnx.cursor()
    if 'id' in request.GET:
        id = request.GET['id']
        if not id:
            error = True
        else:
            cursor.execute("SELECT name from album where album_id = %s",[id])
            results = cursor.fetchall()
            albumname = results[0][0]
            sql_command ="SELECT * from song where album_id = %s"
            # sql_command = "select song.song_id, song.title, song.artist_id,artist.artistname from song join artist on song.artist_id = artist.artist_id"
            cursor.execute(sql_command,[id])
            results = dictfetchall(cursor)
            #results = cursor.fetchall()
            cursor.execute("SELECT artistname FROM artist WHERE artist_id=%s",[id])
            aname = dictfetchall(cursor)
            artistname = aname[0]['artistname']
            #aname = cursor.fetchall()
            #results += aname
            #z = {**results, **aname}
            #z = dict(results.items() + aname.items())
            return render(request, 'getalbum_tracks.html', {'results': results, 'artistname':artistname, 'albumname':albumname})
    else:
        return render(request, 'index.html')

def search(request):
    cnx = pymysql.connect(**dbconfig)
    cursor = cnx.cursor()
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            sql_command ='SELECT * FROM files WHERE album REGEXP "^{}" '.format(q)
            cursor.execute(sql_command)
            results = dictfetchall(cursor)
            # results = cursor.fetchall()
            return render(request, 'search_results.html', {'results':results, 'query':q})
    return render(request, 'search_results.html', {'query':q, 'error': error})

def rescan_db(request):
    error = False
    if 'path' in request.GET:
        path = request.GET['path']
        if not path:
            error = True
        else:
            run_scan(dbconfig,path)
            render(request, 'index.html')
    return render(request,'index.html')
