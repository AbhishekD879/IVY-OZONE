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
class Test_C62799665_Verify_edit_my_acca_deactivate_during_self_exclusion_period_for_login(Common):
    """
    TR_ID: C62799665
    NAME: Verify edit my acca deactivate during self-exclusion period for login
    DESCRIPTION: This test case verifies deactivate of edit my acca during self-exclusion
    PRECONDITIONS: User should be 'Self Exclusion'
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_login(self):
        """
        DESCRIPTION: Load Oxygen application and login
        EXPECTED: User should login successfully
        """
        pass

    def test_002_add_multiple_selection_to_betslip_and_tab_on_place_betacca_bet(self):
        """
        DESCRIPTION: Add multiple selection to betslip and tab on place bet(ACCA bet)
        EXPECTED: Bet is placed successfully as for logged in user
        """
        pass

    def test_003_navigate_to_my_bets_open_bets_and_check_the_bet_placed(self):
        """
        DESCRIPTION: Navigate to my bets->open bets and check the bet placed
        EXPECTED: Coral:
        """
        pass

    def test_004_(self):
        """
        DESCRIPTION: 
        EXPECTED: Acca bet should be there with Edit my bet
        """
        pass

    def test_005_(self):
        """
        DESCRIPTION: 
        EXPECTED: Ladbrokes:
        """
        pass

    def test_006_(self):
        """
        DESCRIPTION: 
        EXPECTED: Acca bet should be there with Edit my Acca button
        """
        pass

    def test_007_tap_right_menu_icon(self):
        """
        DESCRIPTION: Tap Right Menu Icon
        EXPECTED: Right Menu slides in from the right
        """
        pass

    def test_008_tap_my_account_item(self):
        """
        DESCRIPTION: Tap 'My account' item
        EXPECTED: My account' page is opened with full list of items
        """
        pass

    def test_009_tap_responsible_gambling(self):
        """
        DESCRIPTION: Tap 'Responsible Gambling'
        EXPECTED: The 'Responsible Gambling' page is opened
        """
        pass

    def test_010_navigate_to_account_closer_reopen(self):
        """
        DESCRIPTION: Navigate to 'Account closer& reopen
        EXPECTED: Check 'Account closer& reopen' is available
        """
        pass

    def test_011_click_on__account_closer_reopen__link(self):
        """
        DESCRIPTION: Click on  'Account closer& reopen'  link
        EXPECTED: Account closer& reopen page opens
        """
        pass

    def test_012_click_on_sports_close_button(self):
        """
        DESCRIPTION: Click on sports close button
        EXPECTED: Pop up appears click on continue button
        """
        pass

    def test_013_enter_the_duration_from_the_drop_down_and_press_continue(self):
        """
        DESCRIPTION: Enter the duration from the drop down and press continue
        EXPECTED: Account closed successfully
        """
        pass

    def test_014_navigate_to_my_bets__open_bets(self):
        """
        DESCRIPTION: Navigate to my bets -Open bets
        EXPECTED: open bet screen displayed
        """
        pass

    def test_015_check_the_bet_place_which_after_self_exclusion(self):
        """
        DESCRIPTION: Check the bet place which after self-exclusion
        EXPECTED: Edit my acca button is disactivate
        """
        pass
