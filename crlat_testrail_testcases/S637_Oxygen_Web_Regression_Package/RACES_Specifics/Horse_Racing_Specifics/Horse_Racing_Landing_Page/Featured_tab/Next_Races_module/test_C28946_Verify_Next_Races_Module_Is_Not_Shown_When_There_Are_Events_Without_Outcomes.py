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
class Test_C28946_Verify_Next_Races_Module_Is_Not_Shown_When_There_Are_Events_Without_Outcomes(Common):
    """
    TR_ID: C28946
    NAME: Verify 'Next Races' Module Is Not Shown When There Are Events Without Outcomes
    DESCRIPTION: This test case verifies how events which don't contain outcomes will be shown on the 'Next Races' module.
    DESCRIPTION: NOTE, **User Story:** BMA-2878 Events without outcomes should be hidden from 'Next 4 Races' module
    PRECONDITIONS: 1. Make sure there are events for today's day
    PRECONDITIONS: 2. Make sure there are events which don't contain outcomes and those events should appear in the 'Next Races' module after outcomes become available (have 'Next Events' flag checked in TI).
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is opened
        EXPECTED: * 'Next Races' module is shown
        """
        pass

    def test_003_on_thesite_server_find_an_event_without_outcomeswhich_should_appear_in_the_next_races_module(self):
        """
        DESCRIPTION: On the Site Server find an event without outcomes which should appear in the 'Next Races' module
        EXPECTED: Event is shown
        """
        pass

    def test_004_on_oxygen_application_verify_event_withoutoutcomes_in_the_next_races_module(self):
        """
        DESCRIPTION: On Oxygen application verify event without outcomes in the 'Next Races' module
        EXPECTED: Event without outcomes is hidded from the 'Next Races' module
        """
        pass

    def test_005_trigger_the_following_situationselections_become_available_for_the_event_which_didnt_contain_outcomes(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: Selections become available for the event which didn't contain outcomes
        EXPECTED: Event appears in the 'Next Races' module after page refresh
        """
        pass

    def test_006_trigger_the_following_situationall_events_from_the_next_races_module_dont_contain_outcomes(self):
        """
        DESCRIPTION: Trigger the following situation:
        DESCRIPTION: All events from the 'Next Races' module don't contain outcomes
        EXPECTED: 'Next Races' module is absent until events will be updated
        """
        pass

    def test_007_repeat_step_5(self):
        """
        DESCRIPTION: Repeat step #5
        EXPECTED: Events appear in the 'Next Races' module after page refresh
        """
        pass

    def test_008_go_to_the_homepage(self):
        """
        DESCRIPTION: Go to the homepage
        EXPECTED: Homepage is opened
        """
        pass

    def test_009_select_next_races_tabscroll_to_next_races_section(self):
        """
        DESCRIPTION: Select 'Next Races' tab/scroll to 'Next Races' section
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * 'Next Races' tab is opened
        EXPECTED: * 'Next Races' module is shown
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Next Races' module is shown on the Homepage
        """
        pass

    def test_010_repeat_steps__3___7(self):
        """
        DESCRIPTION: Repeat steps # 3 - 7
        EXPECTED: 
        """
        pass
