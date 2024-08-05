import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28981_Verify_Race_Meetings_Order___To_be_archived(Common):
    """
    TR_ID: C28981
    NAME: Verify 'Race Meetings' Order  -  To be archived
    DESCRIPTION: This test case verifies an order of race Meetings when 'By Meeting' filter is selected
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_from_the_sports_menu_ribbon_tap_greyhounds_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon tap 'Greyhounds' icon
        EXPECTED: 'Greyhound' landing page is opened
        """
        pass

    def test_003_tap_results_tab(self):
        """
        DESCRIPTION: Tap 'Results' tab
        EXPECTED: 'Results' tab is opened
        EXPECTED: 'By Latest Results' sorting type is selected
        """
        pass

    def test_004_tap_by_meeting_sorting_type(self):
        """
        DESCRIPTION: Tap **'By Meeting'** sorting type
        EXPECTED: **'By Meeting'** sorting type is selected
        """
        pass

    def test_005_check_order_of_race_meetings_when_by_meeting_filter_is_selected(self):
        """
        DESCRIPTION: Check order of race meetings when 'By Meeting' filter is selected
        EXPECTED: Race meetings are ordered by event type name (**'typeName'** attribute) in ascending alphabetical order (A-Z)
        """
        pass

    def test_006_expand_event_type_section(self):
        """
        DESCRIPTION: Expand event type section
        EXPECTED: Event type section is expanded
        EXPECTED: List of events are shown
        """
        pass

    def test_007_verify_events_ordering_within_one_event_type(self):
        """
        DESCRIPTION: Verify events ordering within one event type
        EXPECTED: Events are ordered chronologically by **'startTime' **attribute (earliest start time -> upwards)
        """
        pass
