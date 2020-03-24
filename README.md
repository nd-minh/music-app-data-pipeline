# Data Pipeline for a Music Streaming App

In this project, our aim is to design a data pipeline on AWS for a music streaming app. Our tasks are listed as follows:
1. Stage into Redshift two sources of data stored on Amazon S3: logs of user activities on the app and song metadata
2. Fill the datawarehouse with a set of dimensional tables
3. Check the results to ensure a coherent and sensible data flow within the pipeline

The two sources of data are described below.

- Source 1: Logs of user activity on the app, available in JSON format.
Example:

![alt text](/images/log-data.png "log-ex")

- Source 2: Metadata of available songs in the app, available also in JSON format.

Example:

```JSON
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

#### Staging Tables:
We will first stage data from source 1 and source 2 into 2 staging tables: `staging_events` and `staging_songs`, respectively. The staging tables have all the columns as in the data sources, with datatype of each column matches the content of that column. For more details on the datatypes of the columns, please refer to `create_tables.sql`.

### Schema Design:
We design a fact table and dimension tables so that it is optimized for queries on song play analysis. To that end, we propose a star schema and an ETL pipeline to transfer the data from the two staging tables into one fact tables and four dimension tables. The descriptions of the tables and their relationship is as follows.

#### Dimension Tables:
- Table `Artists`: contains information about artists in the app. *Columns:* artist_id, name, location, latitude, longitude. 
- Table `Songs`: contains information about songs in the app. *Columns:* song_id, title, artist_id, year, duration. 
- Table `Users`: contains information about users in the app. *Columns:* user_id, first_name, last_name, gender, level. 
- Table `Time`: contains information about timestamps of records broken down into specific units. *Columns:* start_time, hour, day, week, month, year, weekday. 

#### Fact Table:
- Tables `SongPlays`: contains records in log data associated with page `NextSong`. *Columns:* songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent. 

With this design, the analytics team can easily query songs that users are listening to, as well as related information about the users, artists, and temporal information of the listening sessions.

Our data pipeline can be represented with a directed acyclic graph (DAG) as follows:

![alt text](/images/dag.png "dag")

The detailed DAG structure is in the `main_dag.py` file. All the operators are defined in the `operator` folder. All the SQL queries are available in the `sql_queries.py` file. 

### Build Instruction

- Run Airflow and then run the DAG.

