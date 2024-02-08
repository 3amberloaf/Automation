import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pyheif
from PIL import Image

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class HEICConverterHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.lower().endswith(".heic"):
            try:
                jpg_path = event.src_path.rsplit('.', 1)[0] + '.jpg'
                if not os.path.exists(jpg_path):  # Check if JPG version already exists
                    convert_heic_to_jpg(event.src_path, jpg_path)
                    logging.info(f"Converted {event.src_path} to JPG.")
                else:
                    logging.info(f"JPG version of {event.src_path} already exists. Skipping conversion.")
            except Exception as e:
                logging.error(f"Error converting {event.src_path} to JPG: {e}")

def convert_heic_to_jpg(heic_path, jpg_path):
    try:
        heif_file = pyheif.read(heic_path)
        image = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw", heif_file.mode, heif_file.stride)
        image.save(jpg_path, "JPEG")
    except Exception as e:
        logging.error(f"Failed to convert {heic_path} to JPG: {e}")

if __name__ == "__main__":
    path = "/Users/ambersautner/Downloads"  # Update this to your directory
    event_handler = HEICConverterHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    logging.info(f"Watching for HEIC files in {path}...")

    try:
        while True:
            time.sleep(10)  # Reduced CPU usage by increasing sleep time
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopped watching for HEIC files.")
    observer.join()
