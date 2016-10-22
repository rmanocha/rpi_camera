#!/bin/bash
#echo "create table last_motion (rid integer primary key, start_time datetime, end_time datetime); insert into last_motion SELECT 1, datetime('now', '-5 seconds');" | sqlite3 last_motion.db
echo "create table rpi_camera (rid integer primary key, created_ts datetime, updated_ts datetime, filename text, uploaded boolean); CREATE INDEX rpi_camera_uploaded_index ON rpi_camera (uploaded);" | sqlite3 rpi_camera.db

