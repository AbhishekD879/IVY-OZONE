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
class Test_C44882504_Verify_Greyhound_and_Horse_Racing_Events_Updates_when_Events_are_Non_Displayed(Common):
    """
    TR_ID: C44882504
    NAME: Verify Greyhound and Horse Racing Events Updates when  Events are Non-Displayed
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
