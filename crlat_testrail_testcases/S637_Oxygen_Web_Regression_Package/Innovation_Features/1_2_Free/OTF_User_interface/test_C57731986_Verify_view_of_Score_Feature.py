import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C57731986_Verify_view_of_Score_Feature(Common):
    """
    TR_ID: C57731986
    NAME: Verify view of 'Score Feature'
    DESCRIPTION: This test case verifies 'Score Feature' view
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage or Football landing page
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link_and_open_current_tab(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link and open 'Current Tab'
        EXPECTED: 'Score Feature' is successfully displayed for each event and designed according to:
        EXPECTED: https://app.zeplin.io/project/5b5f6d56008921750a2b9a82/screen/5c17962b9057185090e7536e
        EXPECTED: Scores block consist:
        EXPECTED: - Score predictions arrows
        EXPECTED: - Score predictions numbers from 0 to 9 (format "1 - 2")
        """
        pass
