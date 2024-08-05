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
class Test_C64256394_Verify_live_updates_in_enhanced_betslip(Common):
    """
    TR_ID: C64256394
    NAME: Verify live updates in enhanced betslip.
    DESCRIPTION: Verify live updates in enhanced betslip.
    PRECONDITIONS: * At least 5 inplay events should be available in Front End.
    """
    keep_browser_open = True

    def test_001_add_four_selections_to_the_betslip_from_same_inplay_event(self):
        """
        DESCRIPTION: Add four selections to the betslip from same inplay event
        EXPECTED: * Four selections are added to the betslip
        EXPECTED: * Betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        """
        pass

    def test_002_trigger_price_change_for_the_selections__in_the_enhanced_betslip(self):
        """
        DESCRIPTION: Trigger price change for the selections  in the enhanced betslip
        EXPECTED: * Corresponding 'Price/Odds' immediately displays new price
        EXPECTED: * On top of selection 'Price changes from 2/3 to 4/5' for example message is shown.
        EXPECTED: * Betslip size is going to increase dynamically without scrollbar irrespective of price changes/messages.
        EXPECTED: Ladbrokes:
        EXPECTED: * 'Some of your prices have changed' message shown at top of betslip for 5s as well as at bottom of betslip.
        EXPECTED: Coral:
        EXPECTED: * 'Some of your prices have changed' message shown above total stake.
        """
        pass

    def test_003_trigger_suspension_for_any_one_of_the_selections_in_the_enhanced_betslip(self):
        """
        DESCRIPTION: Trigger suspension for any one of the selections in the enhanced betslip
        EXPECTED: * Corresponding selections are immediately suspended
        EXPECTED: * Betslip size is going to increase dynamically without scrollbar irrespective of suspensions/messages.
        EXPECTED: Ladbrokes:
        EXPECTED: * 'One of your selections has been suspended' message shown at top of betslip for 5s as well as at bottom of betslip.
        EXPECTED: Coral:
        EXPECTED: * 'Please beware some of your selections have been suspended' message shown above total stake.
        """
        pass

    def test_004_repeat_step_1_to_step_3_by_adding_selections_to_betslip_from_different_inplay_events(self):
        """
        DESCRIPTION: Repeat step-1 to step-3 by adding selections to betslip from different inplay events
        EXPECTED: 
        """
        pass

    def test_005_add_one_more_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add one more selection to the betslip
        EXPECTED: * Total we will see 5 selections in betslip
        EXPECTED: * Scroll bar is displayed in the FE with the previous selections betslip size.
        """
        pass
