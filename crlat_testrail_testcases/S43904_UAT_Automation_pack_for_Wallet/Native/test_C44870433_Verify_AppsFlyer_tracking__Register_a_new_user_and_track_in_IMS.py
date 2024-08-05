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
class Test_C44870433_Verify_AppsFlyer_tracking__Register_a_new_user_and_track_in_IMS(Common):
    """
    TR_ID: C44870433
    NAME: "Verify AppsFlyer tracking - Register a new user and track in IMS"
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
