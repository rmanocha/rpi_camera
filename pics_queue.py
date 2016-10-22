from boto.s3.connection import S3Connection
from boto.s3.key import Key

import records

from time import sleep

S3_BUCKET = "pi-photos-test"

def log_info(statement):
    print statement

def send_to_s3(filename):
    log_info("Uploading %s" % filename)
    conn = S3Connection()
    bucket = conn.get_bucket(S3_BUCKET)
    #key = Key(bucket)
    key = bucket.get_key(filename, validate=False)
    key.set_contents_from_filename(filename)
    log_info("done")

def mark_uploaded(db, row_id):
    pass

if __name__=="__main__":
    db = records.Database("sqlite:///rpi_camera.db")

    while True:
        rows = db.query("select * from rpi_camera where uploaded = 0")
        import ipdb; ipdb.set_trace()
        if rows:
            log_info("found %d not uploaded files" % len(rows))

            filename = rows[0]["filename"]
            row_id = rows[0]["id"]

            log_info("Uploading %s with id %d" % (filename, row_id))

            send_to_s3(filename)
            mark_uploaded(db, row_id)
        else:
            sleep(.5)
