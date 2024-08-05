import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.lotto
@vtest
class Test_C29596_Error_Handling(Common):
    """
    TR_ID: C29596
    NAME: Error Handling
    DESCRIPTION: This test case verifies error handling for Lottery - Bet Placement page
    DESCRIPTION: JIRA tickets:
    DESCRIPTION: BMA-2363 Lottery - Bet placement error messages
    PRECONDITIONS: 1. Launch Invictus application
    PRECONDITIONS: 2. Go to Lotto section
    """
    keep_browser_open = True

    def test_001_user_balance_is_positivetry_to_place_a_bet_with_no_draw_selected(self):
        """
        DESCRIPTION: User balance is positive.
        DESCRIPTION: Try to place a bet with no draw selected.
        EXPECTED: *   Bet is not placed as button to place bet becomes inactive
        """
        pass

    def test_002_as_logged_in_user_enter_bet_value_for_the_lotteryopen_invictus_app_in_another_browser_tab_and_log_out_from_the_appback_to_the_first_tabtap_place_a_bet_button(self):
        """
        DESCRIPTION: As Logged in user enter bet value for the lottery.
        DESCRIPTION: Open invictus app in another browser tab and log out from the app.
        DESCRIPTION: Back to the first tab.
        DESCRIPTION: Tap 'Place a bet' button
        EXPECTED: *   Info message about logged out by server user is displayed
        EXPECTED: *   User is redirected to the Homepage
        """
        pass
