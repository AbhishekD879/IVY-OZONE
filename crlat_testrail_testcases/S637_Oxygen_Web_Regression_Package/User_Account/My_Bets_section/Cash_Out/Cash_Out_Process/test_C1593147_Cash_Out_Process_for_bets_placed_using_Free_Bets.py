import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C1593147_Cash_Out_Process_for_bets_placed_using_Free_Bets(Common):
    """
    TR_ID: C1593147
    NAME: Cash Out Process for bets placed using Free Bets
    DESCRIPTION: This test case verifies Cashout process for bets placed using Free Bets
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. User has Free Bets in account
    PRECONDITIONS: NOTE: Should be run on:
    PRECONDITIONS: - Cash Out tab;
    PRECONDITIONS: - Open Bets tab;
    PRECONDITIONS: - Bet History;
    """
    keep_browser_open = True

    def test_001_1_select_an_event_with_available_cashout1_add_selection__from_this_event_to_the_betslip_and_select_free_bet_from_free_bets_available_drop_down(self):
        """
        DESCRIPTION: 1. Select an event with available Cashout
        DESCRIPTION: 1. Add selection  from this event to the Betslip and select Free Bet from 'Free Bets Available' drop-down
        EXPECTED: Free bet offer is selected
        """
        pass

    def test_002_place_bet_using_selected_free_bet(self):
        """
        DESCRIPTION: Place Bet using selected Free Bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_003_go_to_cashout_section_and_verify_placed_bet_displaying(self):
        """
        DESCRIPTION: Go to Cashout section and verify placed bet displaying
        EXPECTED: 1. Placed Bet is displayed in Cashout section
        EXPECTED: 2. Only full Cashout is available for the Bet
        """
        pass

    def test_004_tap_cashout_buttonverify_that_cashout_proccess_is_successfully_completed(self):
        """
        DESCRIPTION: Tap 'Cashout' button.
        DESCRIPTION: Verify that cashout proccess is successfully completed
        EXPECTED: Cashout proccess is successfully completed
        """
        pass
