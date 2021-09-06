import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def insertDataframe(cur, insertquery, dataframe):
    """Inserts a dataframe to a database

    Args:
        cur (connection.Cursor): the cursorobject
        insertquery (string): an insertionquery
        dataframe (Dataframe): the dataframe which should be inserted
    """
    for i, row in dataframe.iterrows(): 
        try:       
            rowdata = row[["song_id", "title", "artist_id", "year", "duration"]]
            cur.execute(insertquery, rowdata)
        except:
            print("error while inserting", rowdata)


def process_song_file(cur, filepath):
    """processes a song file, by reading and inserting it into the song table and the artist table

    Args:
        cur (connection.Cursor): the cursorobject
        filepath (string): filepath of the file which should be processed
    """    
    df = pd.read_json(filepath, lines=True)

    # insert song record
    insertDataframe(cur, song_table_insert, df[["song_id", "title", "artist_id", "year", "duration"]])    
    
    # insert artist record
    artist_data = df[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].to_numpy()[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """processes a log file, by reading and inserting, transforming and writing the information to the database 

    Args:
        cur (connection.cursor): the cursorobject
        filepath ([type]): filepath of the file which should be processed
    """    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"]=="NextSong"]

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = (df["ts"], df["ts"].dt.hour, df["ts"].dt.week, df["ts"].dt.month, df["ts"].dt.year, df["ts"].dt.weekday)

    column_labels = ("datetime", "hour", "week", "month", "year", "weekday")
    time_df = pd.concat(time_data, axis=1, keys=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row["ts"], row["userId"], row["level"], songid, artistid, row["sessionId"], row["location"], row["userAgent"])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """iterating over all jsonfiles(datafiles) to process these

    Args:
        cur (connection.cursor): the cursorobject
        conn (connection): the connection object pointing to the database
        filepath (string): the directory of the files which should be processed
        func (function): the function which should be executed on the files
    """    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=admin")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()