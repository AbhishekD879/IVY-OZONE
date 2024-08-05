import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C9607562_Verify_Surface_Bets_ordering(Common):
    """
    TR_ID: C9607562
    NAME: Verify Surface Bets ordering
    DESCRIPTION: Test case verifies proper Surface Bets ordering
    PRECONDITIONS: 1. There are a few Surface Bet added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_cms_edit_a_surface_bet_add_a_selection_of_the_live_eventin_the_application_refresh_the_slphomepage_verify_the_surface_bet_with_live_event_is_first(self):
        """
        DESCRIPTION: In the CMS edit a Surface Bet: add a selection of the Live event
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify the Surface Bet with Live event is first
        EXPECTED: Selection from the Live event is shown first
        """
        pass

    def test_002_in_the_ti_change_events_disporder_of_the_the_selection_from_the_surface_betsin_the_application_refresh_the_slphomepage_verify_the_selection_from_the_event_with_the_disporder_is_shown_first(self):
        """
        DESCRIPTION: In the TI change events Disporder of the the selection from the Surface Bets
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify the selection from the event with the Disporder is shown first
        EXPECTED: Selection from the event with less Disporder is shown first
        """
        pass

    def test_003_setup_following_4_surface_bets_selections1_live_event_disporder12_live_event_disporder23_not_live_event_disporder14_not_live_event_disporder2in_the_application_refresh_the_slphomepage_verify_the_order_of_selections(self):
        """
        DESCRIPTION: Setup following 4 Surface Bets selections:
        DESCRIPTION: 1 Live event, Disporder=1
        DESCRIPTION: 2 Live event, Disporder=2
        DESCRIPTION: 3 Not Live event, Disporder=1
        DESCRIPTION: 4 Not Live event, Disporder=2
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify the order of selections
        EXPECTED: Selections from Live events are shown first. Events with less Disporder are shown first within Live and Not Live events separately.
        EXPECTED: Correct Order is:
        EXPECTED: 1 Live event, Disporder=1
        EXPECTED: 2 Live event, Disporder=2
        EXPECTED: 3 Not Live event, Disporder=1
        EXPECTED: 4 Not Live event, Disporder=2
        """
        pass

    def test_004_in_the_cms_edit_the_surface_bets_use_selections_from_events_with_different_start_datetimein_the_application_refresh_the_slphomepage_verify_the_selection_from_the_soonest_event_is_shown_first(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bets: use selections from events with different Start date/time.
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify the selection from the soonest event is shown first.
        EXPECTED: The selection from the soonest event is shown first
        """
        pass

    def test_005_setup_following_4_not_live_surface_bets_selections_from_events1_disporder1_and_sooner_start_time_ex_15002_disporder1_and_later_start_time_ex_19003_disporder2_and_sooner_start_time_ex_15004_disporder2_and_later_start_time_ex_1900in_the_application_refresh_the_slphomepage_verify_the_order_of_selections(self):
        """
        DESCRIPTION: Setup following 4 Not Live Surface Bets selections from events:
        DESCRIPTION: 1 Disporder=1 and sooner start time (ex. 15:00)
        DESCRIPTION: 2 Disporder=1 and later start time (ex. 19:00)
        DESCRIPTION: 3 Disporder=2 and sooner start time (ex. 15:00)
        DESCRIPTION: 4 Disporder=2 and later start time (ex. 19:00)
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify the order of selections
        EXPECTED: Selections from the events with less Disporder are shown first.
        EXPECTED: Start time defines order after Disporder.
        EXPECTED: Correct order is:
        EXPECTED: 1 Disporder=1 and sooner start time (ex. 15:00)
        EXPECTED: 2 Disporder=1 and later start time (ex. 19:00)
        EXPECTED: 3 Disporder=2 and sooner start time (ex. 15:00)
        EXPECTED: 4 Disporder=2 and later start time (ex. 19:00)
        """
        pass

    def test_006_in_the_cms_edit_the_surface_bets_use_selections_from_events_with_the_same_start_datetimein_the_application_refresh_the_slphomepage_verify_surface_bets_are_ordered_by_event_name_in_alphabetical_order(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bets: use selections from events with the same Start date/time.
        DESCRIPTION: In the application refresh the SLP/Homepage. Verify Surface Bets are ordered by event name in alphabetical order.
        EXPECTED: Surface bets are ordered in alphabetical order
        """
        pass
