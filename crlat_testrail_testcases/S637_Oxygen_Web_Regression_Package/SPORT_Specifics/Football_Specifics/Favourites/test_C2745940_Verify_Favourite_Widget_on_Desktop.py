import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2745940_Verify_Favourite_Widget_on_Desktop(Common):
    """
    TR_ID: C2745940
    NAME: Verify ‘Favourite’ Widget on Desktop
    DESCRIPTION: This Test Case verified ‘Favourite Matches’ Widget on Desktop for both logged out and logged in users
    DESCRIPTION: TESTCASE [C2746163]
    PRECONDITIONS: User is NOT logged in
    """
    keep_browser_open = True

    def test_001_navigate_to_homepage(self):
        """
        DESCRIPTION: Navigate to Homepage
        EXPECTED: 'Favourite Matches' page/widget is displayed below Betslip widget
        """
        pass

    def test_002_verify_favourite_matches_widget_elements(self):
        """
        DESCRIPTION: Verify 'Favourite Matches' widget elements
        EXPECTED: *   Collapsible/Expandable accordion with title 'FAVOURITES'
        EXPECTED: *   Introductory text is displayed as follows: **"To view and add matches into your favourites, please log in into your account." ** (taken from CMS->System config->favoritesText)
        EXPECTED: *   'Log In' button (taken from CMS->System config->favoritesText)
        """
        pass

    def test_003_log_in_and_verify_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Log In and verify 'Favourite Matches' page/widget
        EXPECTED: Introductory text is displayed as follows: **"You currently have no favourites added. Browse through the matches currently available and add them to your favourite list."** (text is hardcoded)
        """
        pass

    def test_004_add_football_event_to_favourites_and_verify_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Add Football event to Favourites and verify 'Favourite Matches' page/widget
        EXPECTED: *  Added event is displayed on 'Favourite Matches' page/widge
        """
        pass

    def test_005_add_4_football_events_to_favourites_widget_and_verify_show_all_link_displaying(self):
        """
        DESCRIPTION: Add 4 football events to Favourites widget and verify 'Show All' link displaying
        EXPECTED: * The first three events are displayed in the widget
        EXPECTED: * 'Show All' button appears below event cards
        """
        pass

    def test_006_click_on_show_all_button(self):
        """
        DESCRIPTION: Click on 'Show All' button
        EXPECTED: * Widget expands downwards to show the full list of events
        EXPECTED: * 'Show All' changes to 'Show Less'
        """
        pass

    def test_007_click_on_show_less_button(self):
        """
        DESCRIPTION: Click on 'Show Less' button
        EXPECTED: * Widget collapses to show first 3 events
        EXPECTED: * 'Show Less' changes to 'Show All'
        """
        pass
