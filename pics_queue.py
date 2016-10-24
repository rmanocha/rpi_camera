from boto.s3.connection import S3Connection
from boto.s3.key import Key

import records

from settings import S3_BUCKET, AWS_ACCESS_KEY, AWS_SECRET_KEY, DB_NAME

from time import sleep

SELECT_STATEMENT = "select * from rpi_camera where uploaded = 0"

MARK_UPLOADED_STATEMENT = "update rpi_camera set uploaded = 1 where rid = %s"

def log_info(statement):
    print statement

def send_to_s3(filename):
    log_info("Uploading %s" % filename)

    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    bucket = conn.get_bucket(S3_BUCKET)

    key = bucket.get_key(filename, validate=False)
    key.set_contents_from_filename(filename)

    log_info("done")

def mark_uploaded(db, row_id):
    db.query(MARK_UPLOADED_STATEMENT % row_id)

    log_info("Marked row %d as uploaded" % row_id)

if __name__=="__main__":
    db = records.Database("sqlite:///" + DB_NAME)

    while True:
        rows = db.query("select * from rpi_camera where uploaded = 0")
        for row in rows:
            filename = row["filename"]
            row_id = row["rid"]

            log_info("Uploading %s with id %d" % (filename, row_id))

            try:
                send_to_s3(filename)
                mark_uploaded(db, row_id)
            except Exception as e:
                log_info("error uploading and marking the file")
                log_info(e)
        else:
            log_info("no rows found")
            sleep(.5)
