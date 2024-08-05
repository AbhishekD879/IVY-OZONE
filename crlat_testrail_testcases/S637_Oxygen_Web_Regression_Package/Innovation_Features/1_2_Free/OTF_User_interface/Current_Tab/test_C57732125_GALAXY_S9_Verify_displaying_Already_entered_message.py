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
class Test_C57732125_GALAXY_S9_Verify_displaying_Already_entered_message(Common):
    """
    TR_ID: C57732125
    NAME: [GALAXY S9] Verify displaying 'Already entered' message
    DESCRIPTION: This test case verifies displaying 'Already entered' message
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User made prediction for the current game
    """
    keep_browser_open = True

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: - 'Already Played' message displayed on 'Current Tab'
        EXPECTED: - Message retrieved from CMS
        EXPECTED: - Designed according to screen:
        """
        pass
