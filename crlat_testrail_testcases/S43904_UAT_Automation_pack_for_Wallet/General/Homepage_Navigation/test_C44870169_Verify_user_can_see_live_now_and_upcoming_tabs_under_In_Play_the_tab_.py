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
class Test_C44870169_Verify_user_can_see_live_now_and_upcoming_tabs_under_In_Play_the_tab_(Common):
    """
    TR_ID: C44870169
    NAME: "Verify user can see  'live now' and 'upcoming' tabs under  In-Play the tab.` "
    DESCRIPTION: -This test case verifies 'Live Now' section on 'In-Play' page
    DESCRIPTION: -This test case verifies  'Upcoming' filter on 'In-Play Sports' page.
    PRECONDITIONS: 1.Load https://beta-sports.coral.co.uk/
    PRECONDITIONS: Navigate to 'In-Play' page from the Sports Menu Ribbon for mobile/tablet/Desktop
    PRECONDITIONS: Make sure that Live events are present in 'Live Now' section for mobile/tablet/ Desktop
    PRECONDITIONS: Make sure that upcoming events are present in 'upcoming' section for mobile/tablet/Desktop
    """
    keep_browser_open = True

    def test_001_load_httpsbeta_sportscoralcouk__log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk & log in with valid credentials.
        EXPECTED: App is loaded and user is on Home page
        """
        pass

    def test_002_for_mobiletabletnavigate_to_in_play_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_in_play_page_from_the_main_navigation_menu_at_the_universal_header(self):
        """
        DESCRIPTION: For Mobile/Tablet:
        DESCRIPTION: Navigate to 'In-Play' page from the Sports Menu Ribbon
        DESCRIPTION: For Desktop:
        DESCRIPTION: Navigate to 'In-Play' page from the 'Main Navigation' menu at the 'Universal Header'
        EXPECTED: In-Play page is loaded with 'Live Now' section is displayed with top 4 events expanded in the list followed by 'UPCOMING EVENTS' on mobile.
        EXPECTED: For Desktop: The 'UPCOMING' switcher is available next to 'LIVE NOW'
        """
        pass

    def test_003_choose_upcoming_switcher(self):
        """
        DESCRIPTION: Choose 'Upcoming' switcher
        EXPECTED: If there are no events in the filter:
        EXPECTED: "There are currently no upcoming Live events available" message is shown
        EXPECTED: If there are events in the filter: Events are loaded.
        """
        pass

    def test_004_click_on_each_sport_icon_and_verify_all_the_live__upcoming_events_for_the_corresponding_sport__competition_are_displayed(self):
        """
        DESCRIPTION: Click on each Sport icon and verify All the live & upcoming events for the corresponding sport / competition are displayed.
        EXPECTED: All the live & upcoming events for the corresponding sport / competition are displayed.
        """
        pass
