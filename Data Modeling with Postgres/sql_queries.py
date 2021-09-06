# DROP TABLES

songplay_table_drop = "drop table if exists songplays;"
user_table_drop = "drop table if exists users;"
song_table_drop = "drop table if exists songs;"
artist_table_drop = "drop table if exists artists;"
time_table_drop = "drop table if exists time"

# CREATE TABLES


songplay_table_create = """
--sql
CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL PRIMARY KEY, start_time TIMESTAMP REFERENCES time (start_time), user_id SERIAL REFERENCES users(user_id), level VARCHAR, song_id VARCHAR REFERENCES songs(song_id), artist_id VARCHAR REFERENCES artists(artist_id), session_id INTEGER, location VARCHAR, user_agent VARCHAR)
;
"""

user_table_create = """
--sql
CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, first_name VARCHAR, last_name VARCHAR, gender VARCHAR(1), level VARCHAR)
;
"""

song_table_create = ("""
--sql
CREATE TABLE IF NOT EXISTS songs (song_id VARCHAR PRIMARY KEY, title VARCHAR, artist_id VARCHAR, year INTEGER, duration DECIMAL)
;
""")

artist_table_create = ("""
--sql
CREATE TABLE IF NOT EXISTS artists (artist_id VARCHAR PRIMARY KEY, name VARCHAR, location VARCHAR, latitude DECIMAL, longitude DECIMAL)
;
""")

time_table_create = ("""
--sql
CREATE TABLE IF NOT EXISTS time (start_time TIMESTAMP primary key, hour INTEGER, day INTEGER, week INTEGER, month INTEGER, year INTEGER, weekday INTEGER)
;
""")

# INSERT RECORDS
songplay_table_insert = ("""
--sql
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
;
""")

user_table_insert = ("""
--sql
INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET first_name = EXCLUDED.first_name, last_name = EXCLUDED.last_name, gender = EXCLUDED.gender, level = EXCLUDED.level
;
""")

song_table_insert = ("""
--sql
INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id) DO UPDATE SET title = EXCLUDED.title, artist_id = EXCLUDED.artist_id, year = EXCLUDED.year, duration = EXCLUDED.duration
;
""")

artist_table_insert = ("""
--sql
INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) DO UPDATE SET name = EXCLUDED.name, location = EXCLUDED.location--, latitude = EXCLUDED.latitude, longitude = EXCLUDED.location
;
""")


time_table_insert = ("""
--sql
INSERT INTO time (start_time, hour, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO NOTHING
; 
""")

# FIND SONGS
song_select = ("""
--sql
SELECT S.song_id, A.artist_id FROM songs S 
JOIN artists A ON S.artist_id = A.artist_id
WHERE S.title = %s AND A.name = %s AND S.duration = %s
""")


# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]