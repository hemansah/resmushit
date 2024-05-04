import resmushit
import pytest
from resmushit import Resmushit
import os
from resmushit.exceptions import InvalidImageExtensionError, FileTooLargeError

FIXTURES = os.path.dirname(os.path.abspath(__file__)) + "/fixtures"


def test_max_file_size():
    with pytest.raises(FileTooLargeError):
        resmushit.from_path(
            image_path=FIXTURES + "/sample_gt_5_mb.jpg", output_dir=FIXTURES + "/optimized"
        )
