import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C44870166_Verify_user_navigation_through_Highlights_tab_on_Home_page(Common):
    """
    TR_ID: C44870166
    NAME: Verify user navigation through Highlights tab on Home page
    DESCRIPTION: Verify user sees 'Highlights' tab in the homepage and user can scroll down the Highlights page
    DESCRIPTION: Verify user can place single and multiple bets using Highlights page selections.
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load Application
        EXPECTED: Application page is loaded and user is landed on Home page with Highlights tab expanded by default
        EXPECTED: For Logged in User : If user has any Private Markets, 'Your Enhanced Markets' tab will be opened by default.
        """
        pass

    def test_002_scroll_up_and_down_through_highlights_page(self):
        """
        DESCRIPTION: Scroll up and down through Highlights Page
        EXPECTED: User is able to view all the events displayed on Highlights page including Surface bets. Quick links and Featured modules which are configured in CMS, In-Play events if there are any.
        """
        pass

    def test_003_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any selection
        EXPECTED: for Mobile : Quick bet window should open
        EXPECTED: Tablet and Desktop : Selection gets added to bet slip
        """
        pass

    def test_004_add_multiple_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add multiple selections to the bet slip
        EXPECTED: Selections get added to the bet slip and bet slip counter updates
        """
        pass

    def test_005_place_bet(self):
        """
        DESCRIPTION: Place bet
        EXPECTED: Mobile : User should be able to place bet from Quick bet window in case of single selection. In case of multiple selections, user should be able to place bet from bet slip.
        EXPECTED: Tablet & Desktop : User should be able to place bet from bet slip.
        """
        pass

    def test_006_repeat_steps_1_4_for_a_logged_out_user(self):
        """
        DESCRIPTION: Repeat steps 1-4 for a logged out user
        EXPECTED: 
        """
        pass
