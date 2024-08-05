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
class Test_C62159700_From_OX_99_Verify_the_user_is_able_to_remove_and_undo_selections_from_traders_offer_for_tricast_and_forecast(Common):
    """
    TR_ID: C62159700
    NAME: [From OX 99] Verify the user is able to remove and undo selections from trader's offer for tricast and forecast
    DESCRIPTION: This test case verifies removing and undo for selections by a user for trader's offer by overask functionality for tricast and forecast
    PRECONDITIONS: User is logged in
    PRECONDITIONS: ======
    PRECONDITIONS: How to accept/decline/make an Offer with Overask functionality
    PRECONDITIONS: How to disable/enable Overask functionality for User or Event Type
    """
    keep_browser_open = True

    def test_001_add_tricast_bet_to_betslip(self):
        """
        DESCRIPTION: Add 'tricast' Bet to Betslip
        EXPECTED: 
        """
        pass

    def test_002_enter_the_value_in_stake_fields_that_do_not_exceed_the_max_allowed_bet_limit_for_all_of_the_added_selections(self):
        """
        DESCRIPTION: Enter the value in 'Stake' fields that do not exceed the max allowed bet limit for all of the added selections
        EXPECTED: The bet is sent to the Openbet system for review
        """
        pass

    def test_003_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: Overask overlay appears
        EXPECTED: ![](index.php?/attachments/get/160879433)
        """
        pass

    def test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger offer with the max bet by a trader in OpenBet system
        EXPECTED: Confirmation is sent and received in the Oxygen app
        """
        pass

    def test_005_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: Selection with the maximum bet offer is expanded
        EXPECTED: The maximum bet offer for selected on step #3 bet and [X] remove buttons are shown to the user
        EXPECTED: Message 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' appears on the grey background below the checked selection
        EXPECTED: 'Place Bet and 'Cancel' buttons are present
        EXPECTED: 'Place Bet and 'Cancel' buttons are enabled
        """
        pass

    def test_006_tap_the_remove_button_x(self):
        """
        DESCRIPTION: Tap the remove button [X]
        EXPECTED: Selection is changed in the bet slip:
        EXPECTED: selection name is grayed out
        EXPECTED: market name is grayed out
        EXPECTED: the event name is grayed out
        EXPECTED: price disappears
        EXPECTED: stake box disappears
        EXPECTED: Est. Returns for that individual bet (Available for tricast)
        EXPECTED: Remove [X] button disappears
        EXPECTED: [REMOVED] text appears
        EXPECTED: [UNDO] button appears
        EXPECTED: ![](index.php?/attachments/get/160879434)
        EXPECTED: ![](index.php?/attachments/get/160879435)
        """
        pass

    def test_007_tap_the_undo_button(self):
        """
        DESCRIPTION: Tap the [UNDO] button
        EXPECTED: Selection is changed to the previous state:
        EXPECTED: selection name isn't grayed out
        EXPECTED: market name isn't grayed out
        EXPECTED: the event name isn't grayed out
        EXPECTED: price appears
        EXPECTED: stake box appears
        EXPECTED: Est. Returns for that individual bet (Available for tricast)
        EXPECTED: Remove [X] button appears
        EXPECTED: [REMOVED] text disappears
        EXPECTED: [UNDO] button disappears
        """
        pass

    def test_008_repeat_steps_2_7_for_forecast(self):
        """
        DESCRIPTION: Repeat steps 2-7 for Forecast
        EXPECTED: 
        """
        pass
