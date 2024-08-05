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
class Test_C145996_Verify_ACCA_Odds_Notification_message_displaying_depend_on_Multiples_availability_in_the_Betslip(Common):
    """
    TR_ID: C145996
    NAME: Verify ACCA Odds Notification message displaying depend on Multiples availability in the Betslip
    DESCRIPTION: This test case verifies ACCA Odds Notification message displaying depend on Multiples availability in the Betslip
    DESCRIPTION: AUTOTEST [C9698710]
    PRECONDITIONS: Check potential payout parameter in DevTools->Network->All->buildBet
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_go_to_any_sports_landing_page(self):
        """
        DESCRIPTION: Go to any Sports Landing page
        EXPECTED: Sports Landing page is opened
        """
        pass

    def test_003_add_one_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add one selection to the Betslip
        EXPECTED: * Multiples are NOT available in the Betslip
        EXPECTED: * ACCA Odds Notification message doesn't appear
        """
        pass

    def test_004_add_two_selections_from_the_same_event_to_the_betslip(self):
        """
        DESCRIPTION: Add two selections from the same event to the Betslip
        EXPECTED: * Multiples are NOT available in the Betslip
        EXPECTED: * ACCA Odds Notification message doesn't appear
        """
        pass

    def test_005_add_at_least_two_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add at least two selections from different events to the Betslip
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message appears
        """
        pass

    def test_006_add_one_more_selection_from_another_event(self):
        """
        DESCRIPTION: Add one more selection from another event
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message is still displayed
        EXPECTED: * Multiples name on ACCA Odds Notification message is updated properly
        EXPECTED: * Odds is recalculated and new price is displayed
        """
        pass

    def test_007_add_one_more_selection_from_the_same_event(self):
        """
        DESCRIPTION: Add one more selection from the same event
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message is NOT displayed
        """
        pass

    def test_008_remove_selection_added_in_the_previous_step(self):
        """
        DESCRIPTION: Remove selection added in the previous step
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message appears again
        EXPECTED: * Multiples name is appropriate to the name in the Betslip
        EXPECTED: * Odds is displayed next to the Multiples name
        """
        pass

    def test_009_remove_one_more_selection_added_to_the_betslip_by_clicking_on_priceodds_buttons(self):
        """
        DESCRIPTION: Remove one more selection added to the Betslip by clicking on Price/Odds buttons
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message is still displayed
        EXPECTED: * Multiples name on ACCA Odds Notification message is updated properly
        EXPECTED: * Odds is recalculated and new price is displayed
        """
        pass

    def test_010_remove_selections_added_to_the_betslip_by_clicking_on_cross_buttons(self):
        """
        DESCRIPTION: Remove selections added to the Betslip by clicking on 'Cross' buttons
        EXPECTED: * Multiples are available in the Betslip
        EXPECTED: * ACCA Odds Notification message is still displayed
        EXPECTED: * Multiples name on ACCA Odds Notification message is updated properly
        EXPECTED: * Odds is recalculated and new price is displayed
        """
        pass

    def test_011_remove_selections_added_to_the_betslip_by_clicking_on_clear_betslip_button(self):
        """
        DESCRIPTION: Remove selections added to the Betslip by clicking on 'Clear Betslip' button
        EXPECTED: * All selections are removed from the Betslip
        EXPECTED: * ACCA Odds Notification message disappears
        """
        pass

    def test_012_repeat_steps_2_11_for_races_lp_price_type_only(self):
        """
        DESCRIPTION: Repeat steps 2-11 for Races (LP price type only)
        EXPECTED: 
        """
        pass
