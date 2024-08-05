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
class Test_C57732013_Verify_view_of_Previous_week_tab(Common):
    """
    TR_ID: C57732013
    NAME: Verify view of 'Previous week tab'
    DESCRIPTION: This test case verifies 'Previous week tab' view
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on home page
    PRECONDITIONS: 4. User made predictions previous week
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
        EXPECTED: https://app.zeplin.io/project/5c471d82d6094838624e7232/screen/5c4af6681386a637a91d183d
        EXPECTED: - Close button
        EXPECTED: - Expanded/Collapsed text from CMS (Static text-> Previous page-> pageText1)
        EXPECTED: - Previous week events with results:
        EXPECTED: - Event number: *e.g. Match 1*
        EXPECTED: - Match result: *e.g. Result 2-2*
        EXPECTED: - Team names *Liverpool*
        EXPECTED: - Team kits
        """
        pass
