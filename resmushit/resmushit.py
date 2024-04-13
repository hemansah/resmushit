import json
import os
from urllib3 import PoolManager
from .log import Log
from .validator import Validator


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

    def __init__(
        self,
        image_url: str = None,
        image_path: str = None,
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
            raise ValueError("image_path or image_url is required")

        self.quality = quality
        self.output_dir = output_dir
        self.preserve_exif = preserve_exif
        self.preserve_filename = preserve_filename
        self.quiet_mode = quiet_mode
        self.__API_URL: str = "http://api.resmush.it"
        self._response = None
        self.__logger = Log(quiet_mode=quiet_mode)

    def __call_api(self):
        try:
            self.__logger.log(
                message=f"Initializing image optimization with quality factor: {self.quality}%",
                color="blue",
            )
            self.__logger.log(message=f"Sending picture {self.filename} to api...")

            http = PoolManager()
            r = http.request(
                "POST",
                self.__API_URL + f"/?qlty={self.quality}&exif={self.preserve_exif}",
                fields={"files": ("image.png", self.imagebytes)},
            )
            self._response = json.loads(r.data.decode("utf-8"))
            self.__logger.log(
                message=f"File optimized by {self._response.get('percent',0)}% (from {self._response.get('src_size',0)//1024}KB to {self._response.get('dest_size',0)//1024}KB). Retrieving...",
                color="green",
            )
        except Exception as e:
            raise Exception(f"Error Occurred: {str(e)}")

    def __get_dest_url(self):
        return self._response.get("dest")

    def __download_image(self, dest_url):
        try:
            http = PoolManager()
            r = http.request("GET", dest_url)
            return r.data
        except Exception as e:
            raise Exception(f"{e}")

    def __save_image(self, imagebytes):
        with open(
            os.path.join(
                self.output_dir,
                f"{'' if self.preserve_filename else 'optimized-'}{self.filename}"
                + f"{self.extension}",
            ),
            "wb",
        ) as f:
            f.write(imagebytes)

    def optimize(self, save: bool = True):
        self.path, self.type, self.imagebytes, self.filename, self.extension = (
            Validator(
                path=self.image_url or self.image_path,
                max_file_size=Resmushit.__MAX_FILESIZE,
            ).validate()
        )
        self.__logger.log(f"Processing: {self.filename}")
        self.__call_api()

        dest_url = self.__get_dest_url()
        optimized_imagebytes = self.__download_image(dest_url=dest_url)
        if save:
            self.__save_image(imagebytes=optimized_imagebytes)
        else:
            return optimized_imagebytes
