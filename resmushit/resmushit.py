import json
import os
from urllib3 import PoolManager
from .log import Log
from .validator import Validator
from typing import Union

class Resmushit:
    """
    Wrapper for Resmush.it API

    Args:
        image_url (str): The url of image.
        image_path (str): The path of image
        quality (int): Quality at which image is going to be optimized.
        output_dir (str): Location for output image.
        preserve_exif (bool): Preserve EXIF data in the file after optimization.
        preserve_filename (bool): Optimized image will prefix 'optimized-' before image name.
        quiet_mode (bool): Run in quiet mode when True

    Returns:
        bytes or None: if save=True, image is saved into mentioned output directory
                       if save=False, image bytes are returned
    ## Usage:
        `import resmushit`

        `resmushit.from_path(image_path='image.png', quality=95)`

        `buffer = resmushit.from_url(image_url="https://ps.w.org/resmushit-image-optimizer/assets/icon-128x128.png", quality=95, save=False)`

    """

    __MAX_FILESIZE = 5 * 1024 * 1024
    __API_URL: str = "http://api.resmush.it"

    def __init__(
        self,
        image_url: str = None,
        image_path: str = None,
        _type: str = None,
        quality: int = 92,
        output_dir: str = ".",
        preserve_exif: bool = False,
        preserve_filename: bool = False,
        quiet_mode: bool = False,
    ) -> None:
        if image_path is not None and image_url is not None:
            raise ValueError("Either image_path or image_url should be passed")
        elif image_url is not None:
            self.image_url = image_url
            self.image_path = None
        elif image_path is not None:
            self.image_path = image_path
            self.image_url = None
        else:
            raise ValueError("image_path or image_url param is required")
        self._type = _type
        self.quality = quality
        self.output_dir = output_dir
        self.preserve_exif = preserve_exif
        self.preserve_filename = preserve_filename
        self.quiet_mode = quiet_mode
        self._response = None
        self.__logger = Log(quiet_mode=quiet_mode)

    @classmethod
    def _filesize_limit(cls):
        return cls.__MAX_FILESIZE

    def __call_api(self) -> None:
        try:
            self.__logger.log(
                message=f"Initializing image optimization with quality factor: {self.quality}%"
            )
            self.__logger.log(
                message=f"Sending picture {self.filename}.{self.extension} to api..."
            )
            http = PoolManager()
            r = http.request(
                "POST",
                Resmushit.__API_URL
                + f"/?qlty={self.quality}&exif={self.preserve_exif}",
                fields={"files": (f"{self.filename}.{self.extension}", self.imagebytes)},
            )
            self._response = json.loads(r.data.decode("utf-8"))
            self.__logger.log(
                message=f"File optimized by {self._response.get('percent',0)}% (from {self._response.get('src_size',0)//1024}KB to {self._response.get('dest_size',0)//1024}KB). Retrieving..."
            )
        except Exception as e:
            raise Exception(f"Error Occurred: {str(e)}")

    def __get_dest_url(self) -> str:
        return self._response.get("dest")

    def __download_image(self, dest_url) -> bytes:
        try:
            http = PoolManager()
            r = http.request("GET", dest_url)
            return r.data
        except Exception as e:
            raise Exception(f"{e}")

    def __save_image(self, imagebytes) -> bytes:
        with open(
            os.path.join(
                self.output_dir,
                f"{'' if self.preserve_filename else 'optimized-'}{self.filename}"
                +"."+ f"{self.extension}",
            ),
            "wb",
        ) as f:
            f.write(imagebytes)

    def optimize(self, save: bool = True) -> Union[None, bytes]:
        self.imagebytes, self.filename, self.extension = Validator(
            path=self.image_url or self.image_path,
            max_file_size=Resmushit.__MAX_FILESIZE,
            _type=self._type,
        ).validate()
        self.__logger.log(f"Processing: {self.filename}")
        self.__call_api()

        dest_url = self.__get_dest_url()
        optimized_imagebytes = self.__download_image(dest_url=dest_url)
        if save:
            self.__save_image(imagebytes=optimized_imagebytes)
        else:
            return optimized_imagebytes
