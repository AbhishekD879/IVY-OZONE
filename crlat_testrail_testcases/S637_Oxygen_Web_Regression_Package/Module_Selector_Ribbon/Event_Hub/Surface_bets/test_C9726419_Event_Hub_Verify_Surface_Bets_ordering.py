import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C9726419_Event_Hub_Verify_Surface_Bets_ordering(Common):
    """
    TR_ID: C9726419
    NAME: Event Hub: Verify Surface Bets ordering
    DESCRIPTION: Test case verifies proper Surface Bets ordering on Event Hub
    PRECONDITIONS: 1. There are a few Surface Bet added to the Event Hub in the CMS
    PRECONDITIONS: 2. Open this Event Hub page in the application
    PRECONDITIONS: CMS path for the Event Hub: Sport Pages > Event Hub > Edit Event hub > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_cms_edit_a_surface_bet_add_a_selection_of_the_live_eventin_the_application_refresh_the_event_hub_page_verify_the_surface_bet_with_live_event_is_first(self):
        """
        DESCRIPTION: In the CMS edit a Surface Bet: add a selection of the Live event
        DESCRIPTION: In the application refresh the Event Hub page. Verify the Surface Bet with Live event is first
        EXPECTED: Selection from the Live event is shown first
        """
        pass

    def test_002_in_the_ti_change_events_disporder_of_the_the_selection_from_the_surface_betsin_the_application_refresh_the_event_hub_page_verify_the_selection_from_the_event_with_the_disporder_is_shown_first(self):
        """
        DESCRIPTION: In the TI change events Disporder of the the selection from the Surface Bets
        DESCRIPTION: In the application refresh the Event Hub page. Verify the selection from the event with the Disporder is shown first
        EXPECTED: Selection from the event with less Disporder is shown first
        """
        pass

    def test_003_in_the_cms_edit_the_surface_bets_use_selections_with_different_start_datetimein_the_application_refresh_the_event_hub_page_verify_the_soonest_selection_is_shown_first(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bets: use selections with different Start date/time.
        DESCRIPTION: In the application refresh the Event Hub page. Verify the soonest selection is shown first.
        EXPECTED: The soonest selection is shown first
        """
        pass

    def test_004_in_the_cms_edit_the_surface_bets_use_selections_with_the_same_start_datetimein_the_application_refresh_the_event_hub_page_verify_surface_bets_are_ordered_by_selection_name_in_alphabetical_order(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bets: use selections with the same Start date/time.
        DESCRIPTION: In the application refresh the Event Hub page. Verify Surface Bets are ordered by selection name in alphabetical order.
        EXPECTED: Surface bets are ordered in alphabetical order
        """
        pass
