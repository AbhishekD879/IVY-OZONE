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
class Test_C29041_Successful_Bet_Placement_on_Multiples(Common):
    """
    TR_ID: C29041
    NAME: Successful Bet Placement on Multiples
    DESCRIPTION: This test case verifies placing a bet on Multiples
    DESCRIPTION: NOTE: For checking information in IMS system  navigate by link
    DESCRIPTION: http://backoffice-tst2.coral.co.uk/ti/bet
    DESCRIPTION: and set up fields 'Placed At'(date of placing bet) and 'Receipt' (ex.  "O/0123364/0000141" from bet receipt of placed bet) with proper values
    DESCRIPTION: AUTOTEST [C527796]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_applicationlogin_with_user_with_positive_balance(self):
        """
        DESCRIPTION: Load Invictus application
        DESCRIPTION: Login with user with positive balance
        EXPECTED: 
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

    def test_004_open_betslip_multiplessection(self):
        """
        DESCRIPTION: Open Betslip->'Multiples' section
        EXPECTED: Multiples are displayed
        """
        pass

    def test_005_enter_stake_for_one_of_available_multiples(self):
        """
        DESCRIPTION: Enter Stake for one of available Multiples
        EXPECTED: Est. Returns, Total Stake and Total Est. Returns fields are calculated
        """
        pass

    def test_006_tap_bet_now_buttonfrom_ox99_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        DESCRIPTION: From OX99 'PLACE BET' button
        EXPECTED: Multiple Bet is placed successfully (the one which had entered Stake, the rest Multiples are ignored)
        EXPECTED: User balance is decreased by Total Stake
        EXPECTED: Bet Receipt page is shown with the correct information about placed bet
        """
        pass

    def test_007_tap_done_buttonfrom_ox99_go_betting_button(self):
        """
        DESCRIPTION: Tap 'Done' button
        DESCRIPTION: From OX99 'GO BETTING' button
        EXPECTED: User is returned to the main view she/he was before placing the bet (Sport / Race Landing page, Homepage)
        """
        pass

    def test_008_check_placed_bet_correctness_in_openbet_system(self):
        """
        DESCRIPTION: Check placed bet correctness in Openbet system
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

    def test_011_tap_bet_now_buttonfrom_ox99_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        DESCRIPTION: From OX99 'PLACE BET' button
        EXPECTED: Multiple Bets is placed successfully
        EXPECTED: User balance is decreased by Total Stake
        EXPECTED: Bet Receipt page is shown with the correct information about placed bet
        """
        pass

    def test_012_check_placed_bet_correctness_in_openbet_system(self):
        """
        DESCRIPTION: Check placed bet correctness in Openbet system
        EXPECTED: Information should be correct in Openbet system
        """
        pass
