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
class Test_C28599_Verify_Redirection_to_Event_Page_from_Favourite_Matches_Page(Common):
    """
    TR_ID: C28599
    NAME: Verify Redirection to Event Page from 'Favourite Matches' Page
    DESCRIPTION: This test case verifies redirection to Event page from 'Favourite Matches' page
    PRECONDITIONS: **JIRA Ticket **:
    PRECONDITIONS: BMA-7792 'Match Favourites Event Linking'
    PRECONDITIONS: **NOTE **:
    PRECONDITIONS: *   Match Center Functionality is available for logged in users only
    PRECONDITIONS: **NOTE:** 'Favourites' page is available only for mobile and tablet. For desktop, there is a 'Favourites' widget available.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_to_the_application(self):
        """
        DESCRIPTION: Log in to the application
        EXPECTED: The user is logged in successfully
        """
        pass

    def test_003_tap_football_icon_on_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on Sports Menu Ribbon
        EXPECTED: 
        """
        pass

    def test_004_add_several_events_to_favourite_matches_from_football_details_pages(self):
        """
        DESCRIPTION: Add several events to 'Favourite Matches' from Football Details pages
        EXPECTED: 
        """
        pass

    def test_005_tap_favourite_icon_from_match_centre_header_of_football_pages(self):
        """
        DESCRIPTION: Tap Favourite icon from Match Centre header of Football pages
        EXPECTED: 'Favourite Matches' page is opened
        """
        pass

    def test_006_click_on_any_event_name_displayed_on_favourite_matches_page(self):
        """
        DESCRIPTION: Click on any Event name displayed on 'Favourite Matches' page
        EXPECTED: The user is redirected to the appropriate Event Details page
        EXPECTED: **For desktop:**
        EXPECTED: - Favourite icon is located before event name in header
        EXPECTED: - Favourite icon is filled with yellow color (selected state)
        EXPECTED: **For mobile/table:**
        EXPECTED: - Favourite icon is located within user tabs area (above market tabs)
        EXPECTED: - Favourite icon is filled with yellow color (selected state)
        """
        pass
