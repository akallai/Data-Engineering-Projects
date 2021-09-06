# Project: Data Modeling with Postgres
## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.


## Files 

The project consists of the following files:<br /> 
[config.py](config.py) is the configfile which contains connection details to the database. <br /> 
[create_tables.py](create_tables.py) is (re)creating the database for setup and testing purposes.<br />  
[etl.ipynb](etl.ipynb) is a notebook for thesting and developing the etl-pipeline. <br /> 
[etl.py](etl.py)  is the pipeline script. It iterates over all data files and ingests it into the database **star schema**.<br /> 
[sql_queries.py](sql_queries) contains the sql queries.<br /> 
[test.ipynb](test.ipynb) is notebook for testing the etl pipeline. It shows if the ingestion worked.<br /> 

## Setup and run
1. For this project a Postgres Database is needed. Install a database if non is existent.
2. Edit the [config.py-file](config.py) to connect with the database.
3. Run ```python sql_queries.py``` to create the database tables.
4. Run ```python etl.py``` to run the pipeline.



## Database Schema
### Fact table

```
songplays
	- songplay_id 	PRIMARY KEY
	- start_time 	REFERENCES time (start_time)
	- user_id	REFERENCES users (user_id)
	- level
	- song_id 	REFERENCES songs (song_id)
	- artist_id 	REFERENCES artists (artist_id)
	- session_id
	- location
	- user_agent
```

### Dimension tables

```
users
	- user_id 	PRIMARY KEY
	- first_name
	- last_name
	- gender
	- level

songs
	- song_id 	PRIMARY KEY
	- title
	- artist_id
	- year
	- duration

artists
	- artist_id 	PRIMARY KEY
	- name
	- location
	- latitude
	- longitude

time
	- start_time 	PRIMARY KEY
	- hour
	- day
	- week
	- month
	- year
	- weekday
```
