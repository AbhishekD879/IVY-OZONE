import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C16508303_Vanilla_Successful_Bet_Placement_on_Multiples(Common):
    """
    TR_ID: C16508303
    NAME: [Vanilla] Successful Bet Placement on Multiples
    DESCRIPTION: This test case verifies placing a bet on Multiples
    DESCRIPTION: OXYGEN AUTOTEST [C527796]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: App is opened
        """
        pass

    def test_002_add_several_selections_from_different_events_to_thebetslip(self):
        """
        DESCRIPTION: Add several selections from different events to the betslip
        EXPECTED: 
        """
        pass

    def test_003_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: 
        """
        pass

    def test_004_scroll_to_multiplessection(self):
        """
        DESCRIPTION: Scroll to 'Multiples' section
        EXPECTED: Multiples are displayed
        """
        pass

    def test_005_enter_stake_for_one_of_available_multiples(self):
        """
        DESCRIPTION: Enter Stake for one of available Multiples
        EXPECTED: Est. Returns and Total Stake and Total Est. Returns fields are calculated
        """
        pass

    def test_006_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: Multiple Bet is placed successfully (the one which had entered Stake, the rest Multiples are ignored)
        EXPECTED: User balance is decreased by Total Stake
        EXPECTED: Bet Receipt page is shown with the correct information about placed bet
        """
        pass

    def test_007_tap_go_betting_button(self):
        """
        DESCRIPTION: Tap 'Go betting' button
        EXPECTED: User is returned to the main view she/he was before placing the bet (Sport / Race Landing page, Homepage)
        """
        pass

    def test_008_check_placed_bet_correctness_in_openbet_system_for_test_environments_only_httpsbackoffice_tst2coralcouktibet___enter_username_and_click_enter(self):
        """
        DESCRIPTION: Check placed bet correctness in Openbet system (for test environments ONLY https://backoffice-tst2.coral.co.uk/ti/bet - enter 'Username' and click Enter)
        EXPECTED: Information should be correct in Openbet system
        """
        pass

    def test_009_add_several_selections_from_different_events_to_thebetslip(self):
        """
        DESCRIPTION: Add several selections from different events to the betslip
        EXPECTED: 
        """
        pass

    def test_010_enter_stake_for_all_available_multiples(self):
        """
        DESCRIPTION: Enter Stake for all available Multiples
        EXPECTED: Est. Returns, Total Stake and Total Est. Returns fields are calculated
        """
        pass

    def test_011_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: Multiple Bets is placed successfully
        EXPECTED: User balance is decreased by Total Stake
        EXPECTED: Bet Receipt page is shown with the correct information about placed bet
        """
        pass

    def test_012_check_placed_bet_correctness_in_openbet_system_for_test_environments_only_httpsbackoffice_tst2coralcouktibet___enter_username_and_click_enter(self):
        """
        DESCRIPTION: Check placed bet correctness in Openbet system (for test environments ONLY https://backoffice-tst2.coral.co.uk/ti/bet - enter 'Username' and click Enter)
        EXPECTED: Information should be correct in Openbet system
        """
        pass
