import arrow
import records

from picamera import PiCamera

from time import sleep

CAMERA_RESOLUTION = (1024, 768)

DB_LOCATION = "" # current directory

NUM_IMAGES = 10 # number of images to take each time motion is detected

MOTION_PIN = 0 # GPIO pin to use for the motion detector

def get_filename():
    return arrow.utcnow().format("YYYY-MM-DD-HH-mm-ss") + ".jpeg"

def insert_new_row(db, filename):
    db.query("insert into rpi_camera(created_ts, updated_ts, filename, " + 
            "uploaded) values (:created_ts, :updated_ts, :filename, :uploaded)",
            created_ts=arrow.utcnow(), updated_ts=arrow.utcnow(),
            filename=filename, 0)
    log_info("inserted new row for %s" % filename)

def get_camera():
    camera = PiCamera()
    camera.resolution = CAMERA_RESOLUTION

    return camera

def capture_image(camera):
    filename = get_filename()
    camera.capture(filename, use_video_port=True, format="jpeg")
    log_info("Captured file: %s" % filename)

    return filename

def capture_queue_image(db, camera):
    insert_new_row(db, capture_image(camera))

def detect_motion():
    return true

if __name__=="__main__":
    camera = get_camera()

    db = records.Database("sqlite:///rpi_camera.db")

    while True:
        if detect_motion():
            for i in range(0, 10):
                capture_queue_image(db, camera)
        else:
            sleep(.1)