import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29023_Bet_is_not_placed_for_selections_without_entered_Stakes(Common):
    """
    TR_ID: C29023
    NAME: Bet is not placed for selections without entered Stakes
    DESCRIPTION: This test case verifies handling when Stake fields for some of several selections are empty
    DESCRIPTION: AUTOTEST: [C2604527]
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  User has sufficient funds for placing a bet
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_a_few_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add a few selections to the betslip
        EXPECTED: 
        """
        pass

    def test_003_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Betslip is opened, selections are displayed on the Betslip
        """
        pass

    def test_004_enter_valid_stake_for_some_of_added_selections_the_other_selections_leave_without_stakes(self):
        """
        DESCRIPTION: Enter valid 'Stake' for some of added selections, the other selections leave without Stakes
        EXPECTED: 
        """
        pass

    def test_005_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - 'Place Bet' button is enabled and it is possible to start bet placement process as soon as stake is entered at least for one selection
        EXPECTED: - Bet is successfully placed for the selections with entered Stake, other selections are ignored and cleared from the Betslip
        EXPECTED: - Bet Receipt is shown and contains information about placed bets (only selections with entered Stakes, selections without Stakes are not displayed on Bet Receipt)
        """
        pass
