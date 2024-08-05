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
class Test_C57731989_Verify_scores_switchers_limits(Common):
    """
    TR_ID: C57731989
    NAME: Verify scores switchers limits
    DESCRIPTION: This test case verifies scores switchers limits
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage or Football landing page
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link_and_open_current_tab(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link and open 'Current Tab'
        EXPECTED: Score block is successfully displayed
        """
        pass

    def test_002_switch_scores_for_both_teams_to_9(self):
        """
        DESCRIPTION: Switch scores for both teams to 9
        EXPECTED: - Score switchers unable to use **UP** arrows
        EXPECTED: - **UP** arrows icon become gray
        """
        pass

    def test_003_switch_scores_for_both_teams_to_0(self):
        """
        DESCRIPTION: Switch scores for both teams to 0
        EXPECTED: - Score switchers unable to use **DOWN** arrows
        EXPECTED: - **DOWN** arrows icon become gray
        """
        pass
