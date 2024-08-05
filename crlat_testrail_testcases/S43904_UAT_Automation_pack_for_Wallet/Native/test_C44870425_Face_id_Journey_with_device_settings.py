import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.
@vtest
class Test_C44870425_Face_id_Journey_with_device_settings(Common):
    """
    TR_ID: C44870425
    NAME: Face id Journey with device settings
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
