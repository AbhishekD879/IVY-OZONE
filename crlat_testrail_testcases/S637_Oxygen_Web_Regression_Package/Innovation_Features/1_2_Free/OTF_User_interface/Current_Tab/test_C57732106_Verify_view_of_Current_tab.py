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
class Test_C57732106_Verify_view_of_Current_tab(Common):
    """
    TR_ID: C57732106
    NAME: Verify view of 'Current tab'
    DESCRIPTION: This test case verifies 'Current tab' view
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on home page
    """
    keep_browser_open = True

    def test_001_tap_on_play_now_button_on_splash_screen(self):
        """
        DESCRIPTION: Tap on 'Play Now' button on Splash screen
        EXPECTED: 'Current tab' is successfully opened and designed according to:
        EXPECTED: https://app.zeplin.io/project/5b5f6d56008921750a2b9a82/screen/5c17957a7501c0242a0b9ddc
        EXPECTED: - Close button
        EXPECTED: - Expanded/Collapsed text from CMS (Static text-> Current page->pageText1)
        EXPECTED: - Green button with 'SUBMIT' text (Static text-> Current page->ctaText1)
        EXPECTED: - Events CMS->Active game):
        EXPECTED: - Event number: *e.g. Match 1*
        EXPECTED: - Date of event: *e.g. 15:00 MON*
        EXPECTED: - Team name *Liverpool*
        EXPECTED: - Team kits
        EXPECTED: - Event TV icon *BBC*
        """
        pass
