import os
from urllib.parse import urlparse
from urllib3 import PoolManager
from .exceptions import (FileTooLargeError, 
                         InvalidImageExtensionError, 
                         ImageExtensionNotFoundException)
import filetype


class Validator:
    """
        Standard Validator for reSmushit
    """
    def __init__(self, path, max_file_size, _type):
        self.path = path
        self._type = _type
        self.max_file_size = max_file_size
        self.max_file_size_kb = max_file_size // 1024
        self.__ALLOWED_FILETYPES = ("png", "jpg", "jpeg", "gif", "bmp", "tiff", "tiff")

    def __check_url_validity(self):
        if urlparse(self.path).scheme in ["http", "https", "ftp"]:
            return True
        else:
            raise ValueError(f"URL scheme required: {self.path}")

    def __file_exists(self):
        if os.path.exists(self.path):
            return True
        raise FileNotFoundError(f"{self.path}")

    def _open_image_from_url(self):
        http = PoolManager()
        r = http.request("GET", url=self.path)
        return r.data

    def _open_image_from_path(self):
        data = ""
        with open(self.path, "rb") as f:
            data = f.read()
        return data

    def _find_image_extension(self, imagebytes):
        kind = filetype.guess(obj=imagebytes)
        if kind.extension:
            self.extension = kind.extension
            return kind.extension
        raise ImageExtensionNotFoundException(f"'{kind.extension}' image extension found")


    def __check_file_size(self, imagebytes):

        if len(imagebytes) > self.max_file_size:
            raise FileTooLargeError(
                f"Max allowed file size: {self.max_file_size_kb}KB."
            )

    def __get_file_name(self):
        filename, _ = os.path.splitext(os.path.basename(urlparse(self.path).path))
        return filename

    # def __get_file_extension(self):
    #     _, extension = os.path.splitext(os.path.basename(urlparse(self.path).path))
    #     return extension

    def __check_allowed_filetypes(self, imagebytes):
        
        if not self.extension in self.__ALLOWED_FILETYPES:
            raise InvalidImageExtensionError(
                f"'{self.extension}' extension type is not allowed.\nAllowed types: {self.__ALLOWED_FILETYPES}"
            )

    def validate(self):
        if self._type == "url":
            self.__check_url_validity()
            imagebytes = self._open_image_from_url()
            self._find_image_extension(imagebytes=imagebytes)
            self.__check_allowed_filetypes(imagebytes=imagebytes)
            self.__check_file_size(imagebytes=imagebytes)
            filename = self.__get_file_name()
            # fileext = self.__get_file_extension()
            return  imagebytes, filename, self.extension

        if self._type == "file":
            self.__file_exists()
            imagebytes = self._open_image_from_path()
            self._find_image_extension(imagebytes=imagebytes)
            self.__check_allowed_filetypes(imagebytes=imagebytes)
            filename = self.__get_file_name()
            # fileext = self.__get_file_extension()
            self.__check_file_size(imagebytes=imagebytes)
            return imagebytes, filename, self.extension
