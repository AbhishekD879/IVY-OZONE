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
class Test_C57732010_Verify_UpSell_Match_Result_displayed_based_on_prediction(Common):
    """
    TR_ID: C57732010
    NAME: Verify UpSell 'Match Result' displayed based on prediction
    DESCRIPTION: This test case verifies UpSell 'Match Result' displayed based on prediction
    PRECONDITIONS: Please look for some insights on a page as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Zeplin
    PRECONDITIONS: 1. Market with name |Match Result| configured on Openbet https://tst2-backoffice-lcm.ladbrokes.com/ti
    PRECONDITIONS: 2. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 3. User on 'Current Tab'
    """
    keep_browser_open = True

    def test_001_set_scores_and_tap_on_submit_button_on_current_tab(self):
        """
        DESCRIPTION: Set scores and Tap on 'Submit' button on 'Current Tab'
        EXPECTED: 'You are in' page is successfully opened and designed according to:
        EXPECTED: https://app.zeplin.io/project/5c471d82d6094838624e7232/screen/5c5053d087c26e79e46e6c30
        EXPECTED: Three UpSell 'Treble - Match Betting' are displayed based on their prediction:
        EXPECTED: - 'Draw' - if user select same scores for teams
        EXPECTED: - Home team name - if user select Home team to Win
        EXPECTED: - Away team name - if user select Away team to Win
        """
        pass
