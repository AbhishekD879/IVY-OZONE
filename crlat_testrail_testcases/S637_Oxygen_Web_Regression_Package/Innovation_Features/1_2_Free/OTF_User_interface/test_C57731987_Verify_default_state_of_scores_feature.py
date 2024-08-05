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
class Test_C57731987_Verify_default_state_of_scores_feature(Common):
    """
    TR_ID: C57731987
    NAME: Verify default state of scores feature
    DESCRIPTION: This test case verifies default state of scores feature
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage or Football landing page
    PRECONDITIONS: 3. User NOT made any predictions previously
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link_and_open_current_tab(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link and open 'Current Tab'
        EXPECTED: - Score block is successfully displayed and switches state is '0' when no score has been selected
        EXPECTED: - Score switchers unable to use **DOWN** arrows and able to use **UP** arrows
        """
        pass
