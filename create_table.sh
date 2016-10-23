#!/bin/bash
echo "create table rpi_camera (rid integer primary key, created_ts datetime, updated_ts datetime, filename text, uploaded boolean); CREATE INDEX rpi_camera_uploaded_index ON rpi_camera (uploaded);" | sqlite3 rpi_camera.db

