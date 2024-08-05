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
class Test_C28596_Verify_Favourite_Matches_Page_Widget_on_Mobile_Tablet(Common):
    """
    TR_ID: C28596
    NAME: Verify ‘Favourite Matches’ Page/Widget on Mobile/Tablet
    DESCRIPTION: This Test Case verified ‘Favourite Matches’ page for both logged out and logged in users
    DESCRIPTION: AUTOTEST [C2745999]
    PRECONDITIONS: User is NOT logged in
    PRECONDITIONS: User can navigate to 'Favourite Matches' page by:
    PRECONDITIONS: - direct link /favourites
    PRECONDITIONS: - Favourites icon on Football Landing page
    PRECONDITIONS: - Favourites widget on tablet and desktop
    """
    keep_browser_open = True

    def test_001_navigate_to_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Navigate to 'Favourite Matches' page/widget
        EXPECTED: 'Favourite Matches' page/widget is displayed
        """
        pass

    def test_002_verify_favourite_matches_page_elements(self):
        """
        DESCRIPTION: Verify 'Favourite Matches' page elements
        EXPECTED: *   Introductory text is displayed as follows: **"To view and add matches into your favourites, please log in into your account." ** (taken from CMS->System config->favoritesText)
        EXPECTED: *   'Log In' button (taken from CMS->System config->favoritesText)
        """
        pass

    def test_003_log_in_and_verify_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Log In and verify 'Favourite Matches' page/widget
        EXPECTED: *  Introductory text is displayed as follows: **"You currently have no favourites added. Browse through the matches currently available and add them to your favourite list."** (text is hardcoded)
        EXPECTED: *  'Go to Matches' button (text is hardcoded)
        EXPECTED: *  'Go to In-Play Matches' button (text is hardcoded)
        """
        pass

    def test_004_add_football_event_to_favourites_and_verify_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Add Football event to Favourites and verify 'Favourite Matches' page/widget
        EXPECTED: *  'Clear All Favourites' button
        EXPECTED: *  Added event is displayed on 'Favourite Matches' page/widge
        EXPECTED: *   Information text is displayed as follows: **"Browse through the matches currently available and add them to your favourite list."** (text is hardcoded)
        EXPECTED: *  'Go to Matches' button
        EXPECTED: *  'Go to In-Play Matches' button
        """
        pass

    def test_005_click_clear_all_favourites_button(self):
        """
        DESCRIPTION: Click 'Clear All Favourites' button
        EXPECTED: No events are displayed on 'Favourite Matches' page/widget
        """
        pass

    def test_006_click_go_to_matches_button_on_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Click 'Go to Matches' button on 'Favourite Matches' page/widget
        EXPECTED: User is navigated to Football->Matches (Mobile)
        """
        pass

    def test_007_go_back_to_favourite_matches_pagewidget_and_click_go_to_in_play_matches_button(self):
        """
        DESCRIPTION: Go back to 'Favourite Matches' page/widget and click 'Go to In-Play Matches' button
        EXPECTED: User is navigated to Football->In-Play
        """
        pass
