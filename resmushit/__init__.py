from .resmushit import Resmushit
from .exceptions import ImageURLNotFoundException, ImagePathNotFoundException

def from_url(image_url=None, quality=92, output_dir=".", preserve_exif=False, preserve_filename=False, quiet_mode=False, notime=True, save=True):
    if image_url:
        resmushit = Resmushit(image_url=image_url, image_path=None, quality=quality, output_dir=output_dir, preserve_exif=preserve_exif, preserve_filename=preserve_filename, quiet_mode=quiet_mode)
        return resmushit.optimize(save)
    raise ImageURLNotFoundException("Please provide an image url")

def from_path(image_path=None, quality=92, output_dir=".", preserve_exif=False, preserve_filename=False, quiet_mode=False, notime=True, save=True):
    if image_path:
        resmushit = Resmushit(image_path=image_path, image_url=None, quality=quality, output_dir=output_dir, preserve_exif=preserve_exif, preserve_filename=preserve_filename, quiet_mode=quiet_mode)
        return resmushit.optimize(save)
    raise ImagePathNotFoundException("Please provide an image path")
