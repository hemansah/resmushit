import os
from io import BytesIO
from urllib.parse import urlparse
from urllib3 import PoolManager
import imghdr
from .exceptions import FileTooLargeError, InvalidImageExtensionError


class Validator:
    """
        Standard Validator for reSmushit
    """
    def __init__(self, path, max_file_size):
        self.path = path
        self.type = None
        self.max_file_size = max_file_size
        self.max_file_size_kb = max_file_size // 1024
        self.__ALLOWED_FILETYPES = ("png", "jpg", "jpeg", "gif", "bmp", "tiff", "tiff")

    def __check_path_type(self):
        parsed_url = urlparse(self.path)

        if all([parsed_url.scheme, parsed_url.netloc, parsed_url.path]):
            self.type = "url"
            return "url"

        if os.path.isfile(self.path) and os.path.exists(self.path):
            self.type = "file"
            return "file"
        else:
            raise FileNotFoundError(f"File {self.path} does not exist.")

    def __check_url_validity(self):
        if urlparse(self.path).scheme in ["http", "https", "ftp"]:
            return True
        else:
            raise ValueError(f"URL scheme required: {self.path}")

    def __file_exists(self):
        if os.path.exists(self.path):
            return True
        raise FileNotFoundError(f"{self.path}")

    def __open_image_from_url(self):
        http = PoolManager()
        r = http.request("GET", url=self.path)
        return r.data

    def __open_image_from_path(self):
        data = ""
        with open(self.path, "rb") as f:
            data = f.read()
        return data

    def __find_image_extension(self, imagebytes):
        return imghdr.what(None, h=imagebytes)

    def __check_file_size(self, imagebytes):

        if len(imagebytes) > self.max_file_size:
            raise FileTooLargeError(
                f"Max allowed file size: {self.max_file_size_kb}KB."
            )

    def __get_file_name(self):
        filename, _ = os.path.splitext(os.path.basename(urlparse(self.path).path))
        return filename

    def __get_file_extension(self):
        _, extension = os.path.splitext(os.path.basename(urlparse(self.path).path))
        if extension == ".jpeg":
            extension = ".jpg"
        return extension

    def __check_allowed_filetypes(self, imagebytes):
        extension = self.__find_image_extension(imagebytes=imagebytes)
        if not extension in self.__ALLOWED_FILETYPES:
            raise InvalidImageExtensionError(
                f"'{extension}' extension type is not allowed.\nAllowed types: {self.__ALLOWED_FILETYPES}"
            )

    def validate(self):
        _type = self.__check_path_type()

        if _type == "url":
            self.__check_url_validity()
            imagebytes = self.__open_image_from_url()
            self.__check_allowed_filetypes(imagebytes=imagebytes)
            self.__check_file_size(imagebytes=imagebytes)
            filename = self.__get_file_name()
            fileext = self.__get_file_extension()

            return self.path, _type, imagebytes, filename, fileext

        if _type == "file":
            self.__file_exists()
            imagebytes = self.__open_image_from_path()
            self.__check_allowed_filetypes(imagebytes=imagebytes)
            filename = self.__get_file_name()
            fileext = self.__get_file_extension()
            self.__check_file_size(imagebytes=imagebytes)
            return self.path, _type, imagebytes, filename, fileext
