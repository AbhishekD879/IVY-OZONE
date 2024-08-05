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
class Test_C16268968_Vanilla_Accessing_Log_In_popup_in_Quick_Bet_Betslip_view_BYB_tab(Common):
    """
    TR_ID: C16268968
    NAME: [Vanilla] Accessing Log In popup in Quick Bet, Betslip view, BYB tab
    DESCRIPTION: This test case verifies accessing Log In popup from different places of the application
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Home page (with Vanilla) is opened
    PRECONDITIONS: User is logged out
    """
    keep_browser_open = True

    def test_001_add_selection_from_football_to_quick_betadd_a_stake_to_selectiontap_loginplace_bet_button(self):
        """
        DESCRIPTION: Add selection from Football to Quick Bet
        DESCRIPTION: Add a Stake to selection
        DESCRIPTION: Tap 'Login&Place Bet' button
        EXPECTED: Log in pop-up appears
        """
        pass

    def test_002_close_log_in_pop_uptap_add_to_betslip_button(self):
        """
        DESCRIPTION: Close Log in pop-up
        DESCRIPTION: Tap 'Add to betslip' button
        EXPECTED: One selection is added to Betslip
        """
        pass

    def test_003_tap_betslip_iconadd_a_stake_to_selectiontap_loginplace_bet_button(self):
        """
        DESCRIPTION: Tap Betslip icon
        DESCRIPTION: Add a Stake to selection
        DESCRIPTION: Tap 'Login&Place Bet' button
        EXPECTED: Log in pop-up appears
        """
        pass

    def test_004_close_log_in_pop_upnavigate_to_promotion_with_opt_in_button(self):
        """
        DESCRIPTION: Close Log in pop-up
        DESCRIPTION: Navigate to Promotion with Opt In button
        EXPECTED: Opt In button is enabled
        """
        pass

    def test_005_tap_on_opt_in_button(self):
        """
        DESCRIPTION: Tap on Opt In button
        EXPECTED: Log in pop-up appears
        """
        pass

    def test_006_close_log_in_pop_uptap_on_the_build_your_bet_tabadd_at_least_two_selectionstap_place_bet_button_in_the_right_bottom_corner(self):
        """
        DESCRIPTION: Close Log in pop-up
        DESCRIPTION: Tap on the 'Build Your Bet' tab
        DESCRIPTION: Add at least two selections
        DESCRIPTION: Tap Place Bet button in the right bottom corner
        EXPECTED: Log in pop-up appears
        """
        pass

    def test_007_enter_valid_username_and_password_tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid username and password. Tap Log in button
        EXPECTED: User is logged in and stays at the same page
        """
        pass
