import resmushit
import pytest
from resmushit import Resmushit
import os
from resmushit.exceptions import InvalidImageExtensionError

FIXTURES = os.path.dirname(os.path.abspath(__file__)) + "/fixtures"

def test_from_url():
    assert (
        resmushit.from_url(
            image_url="https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
            output_dir=FIXTURES+"/optimized"
        )
        == None
    )


def test_from_url_without_url():
    with pytest.raises(ValueError):
        resmushit.from_url()



def test_from_url_bytes_output():
    assert isinstance(
        resmushit.from_url(
            "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg",
            save=False,
        ),
        bytes,
    )
