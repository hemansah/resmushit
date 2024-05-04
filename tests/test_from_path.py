import resmushit
import pytest
from resmushit import Resmushit
import os
from resmushit.exceptions import InvalidImageExtensionError

FIXTURES = os.path.dirname(os.path.abspath(__file__)) + "/fixtures"


def test_from_path():
    assert (
        resmushit.from_path(
            image_path=FIXTURES+"/sample.jpg",
            output_dir=FIXTURES+"/optimized"
        )
        == None
    )


def test_from_path_without_path():
    with pytest.raises(ValueError):
        resmushit.from_path()



def test_from_path_bytes_output():
    assert isinstance(
        resmushit.from_path(
            image_path=FIXTURES+"/sample.jpg",
            save=False
        ),
        bytes,
    )