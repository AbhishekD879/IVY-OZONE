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
class Test_C64256392_Verify_betslip_by_using_Oddboosts_freebets_to_the_selections(Common):
    """
    TR_ID: C64256392
    NAME: Verify betslip by using Oddboosts & freebets to the selections.
    DESCRIPTION: Verify betslip by using Oddboosts & freebets to the selections.
    PRECONDITIONS: * At least 5 preplay & inplay events should be available in Front End.
    PRECONDITIONS: * Oddboosts &  Freebets should be available in Front End.
    """
    keep_browser_open = True

    def test_001_add_four_selections_to_the_betslip_from_same_preplay_event(self):
        """
        DESCRIPTION: Add four selections to the betslip from same preplay event
        EXPECTED: * Four selections are added to the betslip
        EXPECTED: * Betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        """
        pass

    def test_002_use_oddboost__freebet(self):
        """
        DESCRIPTION: Use oddboost & freebet
        EXPECTED: * All Odds are boosted & boost button turns to boosted.
        EXPECTED: * Freebet option turns to Remove freebet for selected selections.
        EXPECTED: Ladbrokes:-
        EXPECTED: * 'You have Freebets available' message is shown initially at top of betslip
        """
        pass

    def test_003_add_four_selections_to_the_betslip_from_different_preplay_events(self):
        """
        DESCRIPTION: Add four selections to the betslip from different preplay events
        EXPECTED: * Four selections are added to the betslip
        EXPECTED: * Betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        """
        pass

    def test_004_use_oddboost__freebet_for_any_one_single_selection_as_well_as_for_any_one_multiple_bets_selection(self):
        """
        DESCRIPTION: Use oddboost & freebet for any one single selection as well as for any one multiple bets selection.
        EXPECTED: * All Odds are boosted & boost button turns to boosted.
        EXPECTED: * Freebet option turns to Remove freebet for selected selections.
        """
        pass

    def test_005_add_four_selections_to_the_betslip_from_same_inplay_event(self):
        """
        DESCRIPTION: Add four selections to the betslip from same inplay event
        EXPECTED: * Four selections are added to the betslip
        EXPECTED: * Betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        """
        pass

    def test_006_use_oddboost__freebet(self):
        """
        DESCRIPTION: Use oddboost & freebet
        EXPECTED: * All Odds are boosted & boost button turns to boosted.
        EXPECTED: * Freebet option turns to Remove freebet for selected selections.
        EXPECTED: Ladbrokes:
        EXPECTED: * 'You have Freebets available' message is shown initially at top of betslip
        """
        pass

    def test_007_trigger_price_change_for_the_selections_which_has_used_freebets__oddboost_in_the_enhanced_betslip(self):
        """
        DESCRIPTION: Trigger price change for the selections which has used freebets & oddboost in the enhanced betslip
        EXPECTED: * Corresponding 'Price/Odds' immediately displays new price
        EXPECTED: * On top of selection 'Price changes from 2/3 to 4/5' for example message is shown.
        EXPECTED: * Betslip size is going to increase dynamically without scrollbar irrespective of price changes/messages.
        EXPECTED: Ladbrokes:
        EXPECTED: * 'Some of your prices have changed' message shown at top of betslip for 5s as well as at bottom of betslip.
        EXPECTED: Coral:
        EXPECTED: * 'Some of your prices have changed' message shown above total stake.
        """
        pass

    def test_008_trigger_suspension_for_any_one_of_the_selections_in_the_enhanced_betslip(self):
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

    def test_009_add_four_selections_to_the_betslip_from_different_inplay_events(self):
        """
        DESCRIPTION: Add four selections to the betslip from different inplay events
        EXPECTED: * Four selections are added to the betslip
        EXPECTED: * Betslip size is going to increase dynamically without scrollbar irrespective of lengthy selection names.
        """
        pass

    def test_010_use_oddboost__freebet_for_any_one_single_selection_as_well_as_for_any_one_multiple_bets_selection(self):
        """
        DESCRIPTION: Use oddboost & freebet for any one single selection as well as for any one multiple bets selection.
        EXPECTED: * All Odds are boosted & boost button turns to boosted.
        EXPECTED: * Freebet option turns to Remove freebet for selected selections.
        """
        pass

    def test_011_repeat_step_7_step_8(self):
        """
        DESCRIPTION: Repeat step-7, step-8
        EXPECTED: 
        """
        pass
