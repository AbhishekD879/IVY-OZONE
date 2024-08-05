import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64055811_IPHONE_X_Featured_Verify_Event_Data_of_Pre_Match_Events(Common):
    """
    TR_ID: C64055811
    NAME: [IPHONE X] Featured: Verify Event Data of Pre-Match Events
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
