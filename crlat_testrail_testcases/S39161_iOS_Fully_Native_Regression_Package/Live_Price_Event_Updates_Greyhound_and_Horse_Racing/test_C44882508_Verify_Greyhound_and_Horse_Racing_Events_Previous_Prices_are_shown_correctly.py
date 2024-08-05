import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C44882508_Verify_Greyhound_and_Horse_Racing_Events_Previous_Prices_are_shown_correctly(Common):
    """
    TR_ID: C44882508
    NAME: Verify Greyhound and Horse Racing Events Previous Prices are shown correctly
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
