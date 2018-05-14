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
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
    # counters
    sql_command = """
    SELECT 
        COUNT(*) AS "Files", 
        COUNT(distinct artist) AS "Artists",
        COUNT(distinct albumartist) AS "Albumartists",
        COUNT(DISTINCT album) AS "Albums",
        COUNT(distinct genre) AS "Genres"
    FROM files
"""
    cursor.execute(sql_command)
#    result = cursor.fetchall()
    results = cursor.fetchall()
    results = results[0]

    # get top genres
    sql_command = """
    select genre as "genre", count( genre) as "count" from files
    where genre != ''
    group by genre
    order by count(genre) DESC limit 10

    """
    cursor.execute(sql_command)
    genres_stats = cursor.fetchall()

    #get top artists
    sql_command = """
    select artist_id as "Artist id", artistname, count(artist_id) as "Count" from artist
    group by artistname
    order by count(artist_id) DESC limit 10
    """
    cursor.execute(sql_command)
    artist_stats = cursor.fetchall()
    return render(request,'index.html', {'results':results, 'genres_stats':genres_stats, 'artist_stats':artist_stats})

def dictfetchall():
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]


def artist_list(request):
    # get list of all artist
    # db = MySQLdb.connect(**dbconfig)
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
    sql_command = """
        SELECT artist.artist_id, artist.artistname,
        (SELECT COUNT(*) from album WHERE artist.artist_id = album.artist_id) as "albumcount"
        FROM artist    
    """
    cursor.execute(sql_command)
    #result = cursor.fetchall()
    result = cursor.fetchall()
    return render(request,'artist_list.html', {'result': result})
    return artist

def song_list(request):
    # get list of all songs
    #db = MySQLdb.connect(**dbconfig)
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM song")
    results = cursor.fetchall()
    return render(request,'song_list.html', {'results': results})
    return artist

def artist(request):
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
    if 'id' in request.GET:
        id = request.GET['id']
        if not id:
            error = True
        else:
            sql_command = """select * from artist where artist_id = %s"""
            cursor.execute(sql_command,[id])
            results = cursor.fetchall()
            cursor.execute("SELECT COUNT(*) as Count from album where artist_id=%s",[id])
            albumcount = cursor.fetchall()
            albumcount = albumcount[0]['Count']
            return render(request,'artist.html', {'results': results, 'albumcount':albumcount})
    else:
        cursor.execute("SELECT * from artist")
        results = cursor.fetchall()
        return render(request, 'artist.html', {'results': results})
    return artist


def getalbums(request):
    # get list of all albums in database
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
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
            result = cursor.fetchall()
            return render(request, 'getalbums.html', {'result': result, 'artist_name':artist_name})
    else:
            sql_command = "SELECT * from album"
            cursor.execute(sql_command)
            result = cursor.fetchall()
            return render(request, 'getalbums.html', {'result': result})


def getalbum_tracks(request):
    # get all track from given album_id
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
    if 'id' in request.GET:
        id = request.GET['id']
        if not id:
            error = True
        else:
            sql_command= """
                SELECT 
                song.song_id,
                song.title,
                song.artist_id,
                artist.artistname
                FROM song 
                INNER JOIN artist
                    ON song.artist_id = artist.artist_id
                WHERE album_id = %s
            """
            cursor.execute(sql_command,[id])
            album_info = cursor.fetchall()
            # #make this one sql command
            cursor.execute("SELECT name from album where album_id = %s",[id])
            results = cursor.fetchall()
            albumname = results[0]['name']
            # sql_command ="SELECT * from song where album_id = %s"
            # cursor.execute(sql_command,[id])
            # results = cursor.fetchall()
            # cursor.execute("SELECT artistname FROM artist WHERE artist_id=%s",[id])
            # aname = cursor.fetchall()
            # artistname = aname[0]['artistname']
            return render(request, 'getalbum_tracks.html', {'results': album_info,'albumname':albumname})
    else:
        return render(request, 'index.html')

def search(request):
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            sql_command ='SELECT * FROM files WHERE artist REGEXP "^{}" '.format(q)
            cursor.execute(sql_command)
            results = cursor.fetchall()
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
