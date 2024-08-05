import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870155_Verify_user_journey_with_valid_credentials(Common):
    """
    TR_ID: C44870155
    NAME: Verify user journey with valid credentials
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_clicktap_log_in_button(self):
        """
        DESCRIPTION: Click/Tap 'Log in' button
        EXPECTED: 'Log in' pop-up is present
        """
        pass

    def test_002_enter_valid_credentials__and_tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials  and tap 'Log in' button
        EXPECTED: User is logged in with permanent session
        """
        pass
