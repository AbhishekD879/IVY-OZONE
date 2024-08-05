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
class Test_C1234459_Verify_Next_Races_Module(Common):
    """
    TR_ID: C1234459
    NAME: Verify 'Next Races' Module
    DESCRIPTION: This test case is checking the UI of  'Next Races' module for Greyhounds.
    PRECONDITIONS: Make sure events are available for current day.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Oxygen application is loaded.
        """
        pass

    def test_002_on_homepage_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: On homepage tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        """
        pass

    def test_003_check_next_races_module(self):
        """
        DESCRIPTION: Check 'Next Races' module
        EXPECTED: For **Mobile and Tablet** , 'Next Races' module is displayed below 'Today's' tab&gt; 'By meeting' switcher
        EXPECTED: For **Desktop** :
        EXPECTED: - for screen width &gt; 970 px, 1025px, Next Races module is shown in line with Races Grids in main display area
        EXPECTED: - for screen width 1280px, 1600px, Next Races module is displayed on the second column of the display area
        """
        pass

    def test_004_check_horizontal_scrolling_through_events(self):
        """
        DESCRIPTION: Check horizontal scrolling through events
        EXPECTED: For **Mobile and Tablet**:
        EXPECTED: 1. It is possible to move between events using swiping on Mobile/Tablet
        EXPECTED: 2. Swiping is fulfilled fluently
        EXPECTED: 3. The previous race is not shown when user swipes across the 'Next Races' module
        EXPECTED: 4. The next race is shown when user swipes across the 'Next Races' module
        EXPECTED: For **Desktop** :
        EXPECTED: 1. Clickable Rollover right arrow which appear on hover is displayed when content is more than one slide
        EXPECTED: 2. Clickable Rollover left arrow (content on both sides) which appear on hover is displayed when viewing slide 2 or more
        EXPECTED: 3. User can click both arrows to move content left and right
        """
        pass

    def test_005_expand_next_races_module_and_check_default_quantity_of_eventsqayntity_of_the_events_sets_in_the_cms_cms__gt_systemconfiguration__gtgreyhoundnextraces__gt_numberofevents(self):
        """
        DESCRIPTION: Expand 'Next Races' module and check default quantity of events
        DESCRIPTION: Qayntity of the events sets in the CMS (CMS -&gt; systemConfiguration -&gt;GreyhoundNextRaces -&gt; numberOfEvents)
        EXPECTED: 1.  The 'Next Races' events to start are shown
        EXPECTED: 2.  Suspended events are not shown in 'Next Races' module
        EXPECTED: 3. Appropriate number of events (which was set in CMS) is displayed within Next Races module/carousel
        EXPECTED: 4.  If number of selections is less than was set in CMS -&gt; display the remaining selections
        EXPECTED: 5.  If there are no events to show -'Next Races' module is absent
        """
        pass

    def test_006_verify_event_sectionsqayntity_of_the_events_sets_in_the_cms_cms__gt_systemconfiguration__gtgreyhoundnextraces__gt_numberofselections(self):
        """
        DESCRIPTION: Verify event sections
        DESCRIPTION: Qayntity of the events sets in the CMS (CMS -&gt; systemConfiguration -&gt;GreyhoundNextRaces -&gt; numberOfSelections)
        EXPECTED: -Appropriate number of selections (which was set in CMS) is displayed within Next Races module/carousel
        EXPECTED: - If number of selections is less than was set in CMS -&gt; display the remaining selections
        EXPECTED: - 'Unnamed Favourite' runner shouldn't be shown on the 'Next Races' module
        """
        pass

    def test_007_verify_full_race_card_link(self):
        """
        DESCRIPTION: Verify 'FULL RACE CARD' link
        EXPECTED: Link is shown under the selections
        """
        pass

    def test_008_click_by_time_switcher(self):
        """
        DESCRIPTION: Click 'By Time' switcher
        EXPECTED: For **Mobile and Tablet** , 'Next Races' module is displayed below 'Today's' tab&gt; 'By Time' switcher
        EXPECTED: For **Desktop** :
        EXPECTED: - for screen width &gt; 970 px, 1025px, Next Races module is shown in line with Races Grids in main display area
        EXPECTED: - for screen width 1280px, 1600px, Next Races module is displayed on the second column of the display area
        """
        pass

    def test_009_repeat_steps_4_7(self):
        """
        DESCRIPTION: Repeat steps #4-7
        EXPECTED: Results are the same
        """
        pass

    def test_010_go_to_tomorrow_tab_and_verify_next_races_module(self):
        """
        DESCRIPTION: Go to 'Tomorrow' tab and verify 'Next Races' module
        EXPECTED: 'Next Races' module is absent
        """
        pass

    def test_011_go_to_the_future_tab_and_verify_next_races_module(self):
        """
        DESCRIPTION: Go to the 'Future' tab and verify 'Next Races' module
        EXPECTED: 'Next Races' module is absent
        """
        pass
