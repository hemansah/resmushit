from .resmushit import Resmushit
from typing import Union

def from_url(image_url=None, _type="url", quality=92, output_dir=".", preserve_exif=False, preserve_filename=False, quiet_mode=False, save=True) -> Union[None, bytes]:
    resmushit = Resmushit(image_url=image_url, _type=_type, image_path=None, quality=quality, output_dir=output_dir, preserve_exif=preserve_exif, preserve_filename=preserve_filename, quiet_mode=quiet_mode)
    return resmushit.optimize(save=save)


def from_path(image_path=None, _type="file", quality=92, output_dir=".", preserve_exif=False, preserve_filename=False, quiet_mode=False, save=True) -> Union[None, bytes]:
    resmushit = Resmushit(image_path=image_path, _type=_type, image_url=None, quality=quality, output_dir=output_dir, preserve_exif=preserve_exif, preserve_filename=preserve_filename, quiet_mode=quiet_mode)
    return resmushit.optimize(save=save)
