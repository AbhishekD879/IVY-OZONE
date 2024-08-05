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
class Test_C57732132_Verify_navigation_to_Splash_screen_from_different_pages(Common):
    """
    TR_ID: C57732132
    NAME: Verify navigation to 'Splash screen' from different pages
    DESCRIPTION: This test case verifies navigation to 'Splash screen' from Homepage and Football landing page
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage and Football landing page
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link_on_homepage(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link on Homepage
        EXPECTED: 'Splash screen' is successfully opened
        """
        pass

    def test_002_tap_on_play_1_2_free_predictor_and_win_150_quick_link_on_football_landing_page(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link on Football landing page
        EXPECTED: 'Splash screen' is successfully opened
        """
        pass
