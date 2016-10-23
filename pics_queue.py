from boto.s3.connection import S3Connection
from boto.s3.key import Key

import records

from time import sleep

S3_BUCKET = "" # bucket to upload the photos to
AWS_ACCESS_KEY = "" # aws_access_key_id
AWS_SECRET_KEY = "" # aws_secret_access_key

SELECT_STATEMENT = "select * from rpi_camera where uploaded = 0"

MARK_UPLOADED_STATEMENT = "update rpi_camera set uploaded = 1 where row_id = %s"

def log_info(statement):
    print statement

def send_to_s3(filename):
    log_info("Uploading %s" % filename)

    conn = S3Connection()

    bucket = conn.get_bucket(S3_BUCKET)

    key = bucket.get_key(filename, validate=False)
    key.set_contents_from_filename(filename)

    log_info("done")

def mark_uploaded(db, row_id):
    db.query(MARK_UPLOADED_STATEMENT % row_id)

    log_info("Marked row %d as uploaded" % row_id)

if __name__=="__main__":
    db = records.Database("sqlite:///rpi_camera.db")

    while True:
        rows = db.query("select * from rpi_camera where uploaded = 0")
        if rows:
            log_info("found %d not uploaded files" % len(rows))

            filename = rows[0]["filename"]
            row_id = rows[0]["id"]

            log_info("Uploading %s with id %d" % (filename, row_id))

            send_to_s3(filename)
            mark_uploaded(db, row_id)
        else:
            sleep(.5)
