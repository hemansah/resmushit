import pytest
from resmushit import Resmushit
import os
from resmushit.exceptions import InvalidImageExtensionError
from resmushit.validator import Validator

FIXTURES = os.path.dirname(os.path.abspath(__file__)) + "/fixtures"


def test_webp_extension():
    with pytest.raises(InvalidImageExtensionError):
        Resmushit(image_path=FIXTURES + "/sample.webp", _type="file").optimize()


def test_jpg_extension():
    imagebytes = Validator(path=FIXTURES + "/sample.jpg", _type='file', max_file_size=Resmushit._filesize_limit())._open_image_from_path()
    ext = Validator(path=FIXTURES + "/sample.jpg", _type='file', max_file_size=Resmushit._filesize_limit())._find_image_extension(imagebytes=imagebytes)
    assert ext == 'jpg'
 