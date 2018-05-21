# Create your views here.
from django.shortcuts import render
import pymysql.cursors
import pymysql
from .scandb import run_scan
from .wordcloud import makecloud
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from base64 import b64encode
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
    select DISTINCT genre as "genre", count( genre) as "count" from files
    where genre != ''
    group by genre
    order by count(genre) DESC limit 10

    """
    cursor.execute(sql_command)
    genres_stats = cursor.fetchall()

    # get genres word cloud
    sql_command = """
    select genre as "genre" from files
    where genre != ''
    """
    cursor.execute(sql_command)
    genres_wordcloud = cursor.fetchall()
    makecloud(genres_wordcloud)

    #get top artists
    sql_command = """
    select song.artist_id as "Artist id", count(song.artist_id) AS "Count", artist.artistname as "artistname" from song,artist
    where song.artist_id = artist.artist_id
    group by song.artist_id
    order by count(song.artist_id) DESC limit 20
    """
    cursor.execute(sql_command)
    artist_stats = cursor.fetchall()
    return render(request,'index.html', {'results':results, 'genres_stats':genres_stats, 'artist_stats':artist_stats})


def artist_list(request):
    # get list of all artist
    # db = MySQLdb.connect(**dbconfig)
    page = request.GET.get('page', 1)
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
    sql_command = """
        SELECT artist.artist_id, artist.artistname,
        (SELECT COUNT(*) from album WHERE artist.artist_id = album.artist_id) as "albumcount"
        FROM artist    
    """
    cursor.execute(sql_command)
    #result = cursor.fetchall()
    results = cursor.fetchall()
    paginator = Paginator(results, 100)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    return render(request,'artist_list.html', {'result': results})



def song_list(request):
    page = request.GET.get('page', 1)
    # get list of all songs
    #db = MySQLdb.connect(**dbconfig)
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
#    cursor.execute("SELECT * FROM song LIMIT 100")
    sql_command = """
    select song.*, files.APIC
    from song
    inner join files
    on song.file_id = files.file_id
    """
    cursor.execute(sql_command)
    results = cursor.fetchall()
#    results[1]['APIC'] = b64encode(results[1]['APIC'])
    paginator = Paginator(results, 50)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    return render(request, 'song_list.html', {'results': results})
#    return render(request,'song_list.html', {'results': results})
#    return artist

def artist(request):
    cnx = pymysql.connect(**dbconfig,cursorclass=pymysql.cursors.DictCursor)
    cursor = cnx.cursor()
    if 'id' in request.GET:
        id = request.GET['id']
        if not id:
            error = True
        else:
            sql_command = "select * from artist where artist_id = %s"
            cursor.execute(sql_command,[id])
            results = cursor.fetchall()
            cursor.execute('SELECT COUNT(*) as Count from album where artist_id=%s', [id])
            albumcount = cursor.fetchall()
            albumcount = albumcount[0]['Count']
            return render(request,'artist.html', {'results': results, 'albumcount':albumcount})
    else:
        cursor.execute("SELECT * from artist")
        results = cursor.fetchall()
        return render(request, 'artist.html', {'results': results})
    return artist


def getalbums(request):
    page = request.GET.get('page', 1)
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
            results = cursor.fetchall()
            paginator = Paginator(results, 100)
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
            return render(request, 'getalbums.html', {'result': results, 'artist_name':artist_name})

#            return render(request, 'getalbums.html', {'result': result, 'artist_name':artist_name})
    else:
#            sql_command = "SELECT * from album"
            sql_command = """
            select album.*,count(song.song_id) as count 
            from album
            inner join song
            on album.album_id = song.album_id
            group by album.album_id
            """
            cursor.execute(sql_command)
            results = cursor.fetchall()
            paginator = Paginator(results, 100)
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
            return render(request, 'getalbums.html', {'result': results})


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
