import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C58449372_Verify_Resulted_Events_displaying_on_Slider_Header_on_EDP(Common):
    """
    TR_ID: C58449372
    NAME: Verify Resulted Events displaying on Slider Header on EDP
    DESCRIPTION: This test case verifies how resulted events will be shown on Slider Header on EDP.
    DESCRIPTION: Test case is applicable for HR and GH landing and event detail pages.
    DESCRIPTION: Note: 'Live' and 'Race Off' labels are not shown on Desktop platform for Coral (for Ladbrokes works both on Desktop and Mobile) according to BMA-52890
    PRECONDITIONS: Following meetings should be configured i TI for HR and GH:
    PRECONDITIONS: 1. Meeting with upcoming and two resulted events
    PRECONDITIONS: 2. Meeting with upcoming and two race off events (event that has IsOFF=Yes and BetInRunning=False(unchecked) in TI)
    PRECONDITIONS: 3. Meeting with upcoming, one resulted and one race off event
    PRECONDITIONS: 4. Meeting with upcoming and more than two resulted/race off events
    PRECONDITIONS: Note: navigation between meetings always leads to active race.
    """
    keep_browser_open = True

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: Application is opened.
        """
        pass

    def test_002_tap_race_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon on the sports menu ribbon.
        EXPECTED: <Race> landing page is opened.
        """
        pass

    def test_003_check_meetings_from_preconditions(self):
        """
        DESCRIPTION: Check meetings from preconditions.
        EXPECTED: 2 last resulted/race off races are shown on the far left hand side on slider header on opened EDP.
        """
        pass

    def test_004_tap_on_any_event_from_meeting_from_preconditions_ribbon_with_resulted_events(self):
        """
        DESCRIPTION: Tap on any event from meeting from preconditions ribbon with resulted events.
        EXPECTED: 2 last resulted races (if available) are shown on the far left hand side on slider header on opened EDP.
        EXPECTED: Note: if there are only 1 or 2 active/upcoming races remaining, then more than 2 resulted races will be displayed.
        """
        pass

    def test_005_set_results_in_ti_eg_1_resulted_race_and_1_race_off_or_2_resulted_races_for_some_events_inside_selected_meeting(self):
        """
        DESCRIPTION: Set Results in TI (e.g. 1 resulted race and 1 race off, or 2 resulted races) for some events inside selected meeting.
        EXPECTED: 
        """
        pass

    def test_006_reload_the_page(self):
        """
        DESCRIPTION: Reload the page.
        EXPECTED: The Races ribbon moves to the left and 2 last resulted races are shown.
        """
        pass

    def test_007_swipe_left(self):
        """
        DESCRIPTION: Swipe Left.
        EXPECTED: Previous resulted events are shown.
        """
        pass

    def test_008_select_another_meeting_from_meeting_dropdown(self):
        """
        DESCRIPTION: Select another meeting from Meeting dropdown.
        EXPECTED: Active race is highlighted, 2 last resulted/race off races if available are shown on the far left hand side on slider header.
        """
        pass
