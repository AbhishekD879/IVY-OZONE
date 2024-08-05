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
class Test_C1144114_Need_to_update_ER_of_Step_5_and_title_Race_meeting_disappears_if_all_events_are_Finished(Common):
    """
    TR_ID: C1144114
    NAME: [Need to update ER of Step 5 and title] Race meeting disappears if all events are Finished
    DESCRIPTION: This test case verifies that Race Meeting is disappearing if all it's Events are Finished (have attribute: 'isFinished' = true)
    PRECONDITIONS: Look at the attribute:
    PRECONDITIONS: **isFinished='true'** on event level - to check whether event is resulted
    """
    keep_browser_open = True

    def test_001_open_race_landing_page(self):
        """
        DESCRIPTION: Open <Race> Landing page
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_002_select_any_racing_meeting_and_trigger_finish_for_all_nested_events_set_event_attribute_isfinished__true_for_all_events_withinthe_type(self):
        """
        DESCRIPTION: Select any Racing Meeting and trigger finish for all nested events (set event attribute: 'isFinished' = true for ALL events within the Type)
        EXPECTED: 
        """
        pass

    def test_003_reload_race_landing_page(self):
        """
        DESCRIPTION: Reload <Race> Landing page
        EXPECTED: Corresponding Racing Meeting is no more displayed on <Race> Landing page
        EXPECTED: Update: the resulted events should still be displayed on the page (check conversation in BMA-44727)
        """
        pass

    def test_004_tap_any_event_on_the_page(self):
        """
        DESCRIPTION: Tap any event on the page
        EXPECTED: Event Details page is shown
        """
        pass

    def test_005_search_for_the_finished_type_in_the_dropdown_list_with_race_meeting_titles_at_the_top_of_the_page(self):
        """
        DESCRIPTION: Search for the Finished Type in the dropdown list with Race meeting titles at the top of the page
        EXPECTED: Race meeting with all Finished events shouldn't be shown in the list.
        EXPECTED: Update: the resulted events should still be displayed on the page (check conversation in BMA-44727)
        """
        pass
