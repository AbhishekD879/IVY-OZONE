import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28598_Verify_Session_Storage(Common):
    """
    TR_ID: C28598
    NAME: Verify Session Storage
    DESCRIPTION: This Test Case verified Session Storage
    DESCRIPTION: Favourites are stored in localStorage of the browser. Thus, they can be shared only between different tabs of the same browser.
    PRECONDITIONS: **JIRA Ticket** :
    PRECONDITIONS: BMA-7791 'Match Favorites Storage Solution: Session Storage'
    PRECONDITIONS: **NOTE **:
    PRECONDITIONS: *   User is logged in
    """
    keep_browser_open = True

    def test_001_login_oxygen_application(self):
        """
        DESCRIPTION: Login Oxygen application
        EXPECTED: Home page is opened
        """
        pass

    def test_002_tap_football_icon_from_the_sports_menu(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports menu
        EXPECTED: 
        """
        pass

    def test_003_tap_on_the_favourite_maches_icon_star_iconnear_matchevent(self):
        """
        DESCRIPTION: Tap on the 'Favourite Maches' icon (star icon) near match/event
        EXPECTED: 
        """
        pass

    def test_004_tap_on_the_add_favourite_match_button(self):
        """
        DESCRIPTION: Tap on the 'Add Favourite Match' button
        EXPECTED: -User has navigated to the 'Favourite Matches' page
        EXPECTED: -Match/event displayed on the 'Favourite Matches' page
        """
        pass

    def test_005_match_with_favourite_matches_selection_has_started(self):
        """
        DESCRIPTION: Match with 'Favourite Matches' selection has started
        EXPECTED: Match with 'Favourite Matches' selection available, on the ‘Favourite Matches’ page until 12 hours after the match has started
        """
        pass

    def test_006_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: 
        """
        pass

    def test_007_login_by_the_same_user(self):
        """
        DESCRIPTION: Login by the same user
        EXPECTED: 
        """
        pass

    def test_008_go_to_the_favourite_matches_page(self):
        """
        DESCRIPTION: Go to the 'Favourite Matches' page
        EXPECTED: Selections within the ‘favourite matches’ page is still displayed
        """
        pass
