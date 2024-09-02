import os

from task_manager.config.base import Config
import uuid
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

class FileOperator:

    def save(self, image, file_size):
        self.check_file_size(file_size)
        self.check_file_type(image.content_type)
        unique_filename = secure_filename(f"{uuid.uuid4()}_{image.filename}")
        filepath = os.path.join(Config.FILEPATH, unique_filename)
        image.save(filepath)
        return {'filepath': filepath, 'unique_filename': unique_filename}

    def check_file_size(self, file_size):
        max_file_size = int(Config.MAX_FILE_SIZE_MB) * 1024 * 1024
        if file_size > max_file_size:
            raise RequestEntityTooLarge('file is very large')

    def check_file_type(self, file_type):
        if file_type not in ['image/jpeg']:
            raise TypeError('change type file')
