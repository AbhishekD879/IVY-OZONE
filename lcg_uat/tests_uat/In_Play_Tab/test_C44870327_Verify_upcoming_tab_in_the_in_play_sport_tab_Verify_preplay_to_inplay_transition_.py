import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870327_Verify_upcoming_tab_in_the_in_play_sport_tab_Verify_preplay_to_inplay_transition_(Common):
    """
    TR_ID: C44870327
    NAME: "Verify upcoming tab in the in-play sport tab -Verify preplay to inplay transition  ."
    DESCRIPTION: -This test case verifies  'Upcoming' filter on In-Play Sports tab
    DESCRIPTION: -Verify pre-play to In-play transition
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk/
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_for_mobiletabletnavigate_to_in_play_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: For Mobile/Tablet:
        DESCRIPTION: Navigate to 'In-Play' page from the Sports Menu Ribbon
        DESCRIPTION: For Desktop:
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: 'In-Play' Landing Page is opened
        EXPECTED: First <Sport> tab is opened by default
        EXPECTED: 'Live Now' and 'Upcoming' are displayed.
        EXPECTED: User is able to see spinning wheel while events are being loaded
        """
        pass

    def test_003_choose_upcoming_switcher(self):
        """
        DESCRIPTION: Choose 'Upcoming' switcher
        EXPECTED: If there are no events in the filter:
        EXPECTED: "There are currently no upcoming Live events available" message is shown
        EXPECTED: If there are events in the filter:
        EXPECTED: Events are loaded
        """
        pass

    def test_004_verify_accordion_headers_titles_within_upcoming_page(self):
        """
        DESCRIPTION: Verify accordion header's titles within 'Upcoming' page
        EXPECTED: The accordion header titles are in the following format and correspond to the following attributes:
        EXPECTED: 'Category Name' - 'Type Name' if section is named Category Name + Type Name on Pre-Match pages
        EXPECTED: 'Class Name' - 'Type Name' if section is named Class Name (sport name should not be displayed) + Type Name on Pre-Match pages
        EXPECTED: 'CASH OUT' label is shown next to Event type name if at least one of it's events has cashoutAvail="Y
        """
        pass

    def test_005_verify_leaguecompetition_accordion_order(self):
        """
        DESCRIPTION: Verify <League/Competition> accordion order
        EXPECTED: Leagues accordions are ordered by:
        EXPECTED: Class 'displayOrder' in ascending where minus ordinals are displayed first;
        EXPECTED: Type 'displayOrder' in ascending
        """
        pass

    def test_006_verify_events_order_in_the_leaguecompetition_accordion(self):
        """
        DESCRIPTION: Verify events order in the <League/Competition> accordion
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 'startTime' - chronological order in the first instance
        EXPECTED: Event 'displayOrder'  in ascending
        EXPECTED: Alphabetical order
        """
        pass

    def test_007_verify_pre_play_to_in_play_transition(self):
        """
        DESCRIPTION: Verify pre-play to In-play transition
        EXPECTED: Events dropping off from pre-play to inplay
        """
        pass

    def test_008_repeat_steps_2_to_7_for_all_available_sports_in_in_play_tab(self):
        """
        DESCRIPTION: Repeat steps #2 to #7 for all available sports in in-play tab
        EXPECTED: 
        """
        pass
