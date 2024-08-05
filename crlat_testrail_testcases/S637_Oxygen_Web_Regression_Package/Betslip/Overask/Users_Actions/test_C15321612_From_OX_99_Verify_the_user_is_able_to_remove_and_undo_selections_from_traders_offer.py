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
class Test_C15321612_From_OX_99_Verify_the_user_is_able_to_remove_and_undo_selections_from_traders_offer(Common):
    """
    TR_ID: C15321612
    NAME: [From OX 99] Verify the user is able to remove and undo selections from trader's offer
    DESCRIPTION: This test case verifies removing and undo for selections by a user for trader's offer by overask functionality
    PRECONDITIONS: User is logged in
    PRECONDITIONS: ======
    PRECONDITIONS: [How to accept/decline/make an Offer with Overask functionality](https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955)
    PRECONDITIONS: [How to disable/enable Overask functionality for User or Event Type](https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983)
    """
    keep_browser_open = True

    def test_001_add_a_few_selections_and_go_betslip_singles_section(self):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Singles' section
        EXPECTED: 
        """
        pass

    def test_002_enter_the_value_in_stake_fields_that_do_not_exceed_max_allowed_bet_limit_for_all_of_the_added_selections(self):
        """
        DESCRIPTION: Enter the value in 'Stake' fields that do not exceed max allowed bet limit for all of the added selections
        EXPECTED: The bet is sent to Openbet system for review
        """
        pass

    def test_003_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *  Overask overlay appears
        """
        pass

    def test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger offer with the max bet by a trader in OpenBet system
        EXPECTED: Confirmation is sent and received in Oxygen app
        """
        pass

    def test_005_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   Selection with the maximum bet offer is expanded
        EXPECTED: *   The maximum bet offer for selected on step #3 bet and [X] remove buttons are shown to the user
        EXPECTED: *   Message 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' appears on the grey background below the checked selection
        EXPECTED: *   'Place Bet  and 'Cancel' buttons are present
        EXPECTED: *   'Place Bet  and 'Cancel' buttons are enabled
        """
        pass

    def test_006_tap_the_remove_button_x(self):
        """
        DESCRIPTION: Tap the remove button [X]
        EXPECTED: Selection is changed in the betslip:
        EXPECTED: * selection name is grayed out
        EXPECTED: * market name is grayed out
        EXPECTED: * event name is grayed out
        EXPECTED: * price disappears
        EXPECTED: * stake box disappears
        EXPECTED: * Est. Returns for that individual bet (Available for accas (double, trixie, etc))
        EXPECTED: * Remove [X] button disappears
        EXPECTED: * [REMOVED] text appears
        EXPECTED: * [UNDO] button appears
        """
        pass

    def test_007_tap_undo_button(self):
        """
        DESCRIPTION: Tap [UNDO] button
        EXPECTED: Selection is changed to the previous state:
        EXPECTED: * selection name isn't grayed out
        EXPECTED: * market name isn't grayed out
        EXPECTED: * event name isn't grayed out
        EXPECTED: * price appears
        EXPECTED: * stake box appears
        EXPECTED: * Est. Returns for that individual bet (Available for accas (double, trixie, etc))
        EXPECTED: * Remove [X] button appears
        EXPECTED: * [REMOVED] text disappears
        EXPECTED: * [UNDO] button disappears
        """
        pass

    def test_008_repeat_steps_2_7_for_double(self):
        """
        DESCRIPTION: Repeat steps 2-7 for Double
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_2_7_for_multiple(self):
        """
        DESCRIPTION: Repeat steps 2-7 for Multiple
        EXPECTED: 
        """
        pass
