import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil


class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, src_dir, dest_dir):
        self.src_dir = src_dir
        self.dest_dir = dest_dir

    def copy_file(self, src_path, relative_path):
        dest_path = os.path.join(self.dest_dir, relative_path)

        # Ensure the target directory exists
        dest_directory = os.path.dirname(dest_path)
        os.makedirs(dest_directory, exist_ok=True)

        shutil.copy(src_path, dest_path)
        print(f"File '{src_path}' copied to '{dest_path}'")

    def on_created(self, event):
        if event.is_directory:
            return

        src_path = os.path.join(self.src_dir, event.src_path)
        relative_path = os.path.relpath(src_path, self.src_dir)
        self.copy_file(src_path, relative_path)

    def on_modified(self, event):
        if event.is_directory:
            return

        src_path = os.path.join(self.src_dir, event.src_path)
        relative_path = os.path.relpath(src_path, self.src_dir)
        self.copy_file(src_path, relative_path)


def main():
    model_path = "model_clasifier/"
    cwd = os.getcwd()
    src_directory = os.path.join(cwd, model_path)
    des_abs_path_partial = '/home/fulp/clasificador_ofertas_empleo/backend/app/'
    des_abs_path = os.path.join(des_abs_path_partial, model_path)

    event_handler = FileModifiedHandler(src_directory, des_abs_path)
    observer = Observer()
    observer.schedule(event_handler, src_directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
