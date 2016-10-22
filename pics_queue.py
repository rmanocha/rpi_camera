import records

from time import sleep

def send_to_s3(filename):
    pass

def mark_uploaded(db, row_id):
    pass

if __name__=="__main__":
    db = records.Database("sqlite:///rpi_camera.db")

    while True:
        rows = db.query("select * from rpi_camera where uploaded is false order by created_date")
        if rows:
            filename = rows[0]["filename"]
            row_id = rows[0]["id"]

            send_to_s3(filename)
            mark_uploaded(db, row_id)
        else:
            sleep(.5)
