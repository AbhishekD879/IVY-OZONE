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
class Test_C57732133_Verify_user_navigation_without_active_entry(Common):
    """
    TR_ID: C57732133
    NAME: Verify user navigation without active entry
    DESCRIPTION: This test case verifies navigation to 'Splash screen' for user without active entry
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage
    PRECONDITIONS: 3. User NOT made prediction during last week
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link_on_homepage(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link on Homepage
        EXPECTED: - User navigated to 'Splash screen'
        EXPECTED: - 'Splash screen' is successfully opened
        """
        pass
