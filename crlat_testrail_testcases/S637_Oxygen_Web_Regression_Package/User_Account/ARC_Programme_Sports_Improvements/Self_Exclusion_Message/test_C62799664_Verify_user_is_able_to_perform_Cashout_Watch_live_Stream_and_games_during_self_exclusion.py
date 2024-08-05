import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C62799664_Verify_user_is_able_to_perform_Cashout_Watch_live_Stream_and_games_during_self_exclusion(Common):
    """
    TR_ID: C62799664
    NAME: Verify user is able to perform Cashout, Watch live Stream and games during self-exclusion
    DESCRIPTION: This test cases verifies user is able to perform Cashout, Watch live Stream and games during self-exclusion
    PRECONDITIONS: User should be 'Self Exclusion'
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_login(self):
        """
        DESCRIPTION: Load Oxygen application and login
        EXPECTED: User should login successfully
        """
        pass

    def test_002_add_selection_to_betslip_and_tab_on_place_bet(self):
        """
        DESCRIPTION: Add selection to betslip and tab on place bet
        EXPECTED: Bet is placed successfully as for logged in user
        """
        pass

    def test_003_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right Menu Icon
        EXPECTED: Right Menu slides in from the right
        """
        pass

    def test_004_tap_my_account_item(self):
        """
        DESCRIPTION: Tap 'My account' item
        EXPECTED: My account' page is opened with full list of items
        """
        pass

    def test_005_tap_responsible_gambling(self):
        """
        DESCRIPTION: Tap 'Responsible Gambling'
        EXPECTED: The 'Responsible Gambling' page is opened
        """
        pass

    def test_006_navigate_to_account_closer_reopen(self):
        """
        DESCRIPTION: Navigate to 'Account closer& reopen
        EXPECTED: Check 'Account closer& reopen' is available
        """
        pass

    def test_007_click_on__account_closer_reopen__link(self):
        """
        DESCRIPTION: Click on  'Account closer& reopen'  link
        EXPECTED: Account closer& reopen page opens
        """
        pass

    def test_008_click_on_sports_close_button(self):
        """
        DESCRIPTION: Click on sports close button
        EXPECTED: Pop up appears click on continue button
        """
        pass

    def test_009_enter_the_duration_from_the_drop_down_and_press_continue(self):
        """
        DESCRIPTION: Enter the duration from the drop down and press continue
        EXPECTED: Account closed successfully
        """
        pass

    def test_010_navigate_to_my_bets__open_bets(self):
        """
        DESCRIPTION: Navigate to my bets -Open bets
        EXPECTED: open bet screen displayed
        """
        pass

    def test_011_during_that_self_exclusionwhat_user_perform(self):
        """
        DESCRIPTION: During that self-exclusionwhat user perform
        EXPECTED: user can perform all the mention can do cashout ,watch live streaming, play free-to-play games
        """
        pass
