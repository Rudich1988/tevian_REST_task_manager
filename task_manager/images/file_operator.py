import os
import uuid

from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from task_manager.config.base import Config
from task_manager.exceptions.custom_exceptions import FileTypeError


class FileOperator:

    def save(self, image, filepath):
        image.seek(0)
        image.save(filepath)

    def check_file(self, image, file_size):
        self.check_file_size(file_size)
        self.check_file_type(image.content_type)
        unique_filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
        filepath = os.path.join(Config.FILEPATH, unique_filename)
        return {'filepath': filepath, 'unique_filename': unique_filename}

    def check_file_size(self, file_size):
        max_file_size = int(Config.MAX_FILE_SIZE_MB) * 1024 * 1024
        if file_size > max_file_size:
            raise RequestEntityTooLarge('file is very large')

    def check_file_type(self, file_type):
        if file_type not in ['image/jpeg']:
            raise FileTypeError(message='change file type', status_code=400)

    def delete(self, files):
        if not files:
            return
        for file in files:
            try:
                os.remove(file)
            except:
                continue
