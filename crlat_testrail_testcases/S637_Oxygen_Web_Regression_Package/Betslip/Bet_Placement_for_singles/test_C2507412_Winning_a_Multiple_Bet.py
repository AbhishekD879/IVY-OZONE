import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C2507412_Winning_a_Multiple_Bet(Common):
    """
    TR_ID: C2507412
    NAME: Winning a Multiple Bet
    DESCRIPTION: This test case verifies Winning a Bet for multiple selections
    DESCRIPTION: AUTOTEST C2552956
    PRECONDITIONS: 1. User should be Log in
    PRECONDITIONS: 2. User should have sufficient funds to place a bet
    PRECONDITIONS: 3. How to trigger the situation when user wins a bet https://confluence.egalacoral.com/pages/viewpage.action?pageId=96150627
    """
    keep_browser_open = True

    def test_001_add_couple_selections_from_different_events_to_the_betlsip(self):
        """
        DESCRIPTION: Add couple selections from different events to the Betlsip
        EXPECTED: 
        """
        pass

    def test_002_open_betslip_multiples_section(self):
        """
        DESCRIPTION: Open Betslip, 'Multiples' section
        EXPECTED: 'Mupliples' section is opened
        """
        pass

    def test_003_enter_correct_stake_in_stake_field_and_tap_place_bet(self):
        """
        DESCRIPTION: Enter correct Stake in 'Stake' field and tap 'Place Bet'
        EXPECTED: *  Bet is placed successfully
        EXPECTED: *  User 'Balance' is decreased by value entered in 'Stake' field
        EXPECTED: *  Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_004_trigger_the_situation_when_user_wins_multiple_bet_each_of_selections_is_won(self):
        """
        DESCRIPTION: Trigger the situation when user wins Multiple bet (each of selections is won)
        EXPECTED: User balance is increased on bet win amount immediately
        """
        pass

    def test_005_go_to_bet_history(self):
        """
        DESCRIPTION: Go to Bet History
        EXPECTED: * 'Won' label is present on the Multiples header
        EXPECTED: * 'You won <currency sign and value>' label right under header, on top of event card is shown
        EXPECTED: * Green tick is shown on the left of the each bet that won
        """
        pass
