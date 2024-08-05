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
class Test_C57732015_Verify_displaying_of_You_didnt_play_1_2_Free_last_week_messages(Common):
    """
    TR_ID: C57732015
    NAME: Verify displaying of 'You didn't play 1-2-Free last week' messages
    DESCRIPTION: This test case verifies displaying of 'You didn't play 1-2-Free last week' messages
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on home page
    PRECONDITIONS: 4. User didn't make predictions previous week
    """
    keep_browser_open = True

    def test_001_tap_on_play_now_button_on_splash_screen(self):
        """
        DESCRIPTION: Tap on 'Play Now' button on Splash screen
        EXPECTED: 'Current tab' is successfully opened
        """
        pass

    def test_002_tap_on_last_week_results(self):
        """
        DESCRIPTION: Tap on 'Last week results'
        EXPECTED: 'Previous week tab' is successfully opened and designed according to:
        EXPECTED: https://app.zeplin.io/project/5c471d82d6094838624e7232/screen/5c4af66866e3b3bee96d62f0
        EXPECTED: - 'You didn't play 1-2-Free last week' messages displayed
        """
        pass
