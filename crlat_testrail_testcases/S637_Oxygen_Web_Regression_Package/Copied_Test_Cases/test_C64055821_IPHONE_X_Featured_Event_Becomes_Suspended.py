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
class Test_C64055821_IPHONE_X_Featured_Event_Becomes_Suspended(Common):
    """
    TR_ID: C64055821
    NAME: [IPHONE X] Featured Event Becomes Suspended
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
