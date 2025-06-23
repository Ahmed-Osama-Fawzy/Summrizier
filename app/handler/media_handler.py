import os
from werkzeug.utils import secure_filename

class MediaHandler:
    def __init__(self, file, upload_dir="static/uploads", allowed_extensions=None):
        self.file = file
        self.upload_dir = upload_dir
        self.allowed_extensions = allowed_extensions or {"png", "jpg", "jpeg", "gif", "mp4"}
        self.filename = secure_filename(file.filename) if file else None

        # Ensure the upload directory exists
        os.makedirs(upload_dir, exist_ok=True)

    def is_allowed(self):
        if not self.filename:
            return False
        ext = self.filename.rsplit('.', 1)[-1].lower()
        return '.' in self.filename and ext in self.allowed_extensions

    def save(self, custom_name=None):
        if not self.is_allowed():
            raise ValueError("File type not allowed")

        name = custom_name or self.filename
        save_path = os.path.join(self.upload_dir, name)
        self.file.save(save_path)
        self.filename = name  # update filename if custom name used
        return save_path, name

    def get_url(self, app_root=""):
        return os.path.join(app_root, self.upload_dir, self.filename).replace("\\", "/")

    def remove(self, filename=None, filepath=None):
        """
        Removes a file by name or the last saved file if no name is provided.
        """
        name = filename or self.filename
        gpath = filepath or self.upload_dir
        if not name:
            raise ValueError("No filename specified for removal")

        path = os.path.join(gpath, name)
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False
