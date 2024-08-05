import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C57732129_Verify_view_of_Splash_screen(Common):
    """
    TR_ID: C57732129
    NAME: Verify view of 'Splash screen'
    DESCRIPTION: This test case verifies 'Splash screen' view
    DESCRIPTION: AUTOTEST [C23820451]
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: >Deprecated: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: Oxygen CMS guide: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: see section Text Configuration - Splash Page
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is NOT logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE' is available on Homepage / Football sports page (configure in CMS quick link and set link to 1-2-free as '{evnURL}/1-2-free')
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link_on_home_page(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link on home page
        EXPECTED: 'Splash screen' is successfully opened and designed according to:
        EXPECTED: https://app.zeplin.io/project/5b5f6d56008921750a2b9a82/screen/5b5f6dcdb01f154b21372d77
        EXPECTED: - Innovation logo
        EXPECTED: - Main text (pull from CMS->static text-> splash page->pageText1)
        EXPECTED: - Play now button (pull from CMS->static text-> splash page->CTA1)
        EXPECTED: - Cancel button (pull from CMS->static text-> splash page->CTA2)
        """
        pass
