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
class Test_C57732123_Verify_error_handling_when_user_has_wrong_date(Common):
    """
    TR_ID: C57732123
    NAME: Verify error handling when user has wrong date
    DESCRIPTION: This test case verifies error handling when user has wrong date
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User Do not have prediction yet
    PRECONDITIONS: 3. User set date in Future/Past on device
    """
    keep_browser_open = True

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: 'Submit' button **displayed**
        """
        pass

    def test_002_tap_on_submit_button(self):
        """
        DESCRIPTION: Tap on 'Submit' button
        EXPECTED: 'Submit' button changes to **'PLEASE CORRECT YOUR DATE/TIME SETTINGS
        EXPECTED: '**
        """
        pass
