import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870192_Verify_user_can_add_FB_favourites__Verify_user_can_select_Deselect_favourite_icon_Verify_favourite_icon_count_Verify_user_can_navigate_to_the_favourite_matches_page_and_verify_the_page_links_and_details_(Common):
    """
    TR_ID: C44870192
    NAME: "Verify user can add FB favourites, - Verify user can select/Deselect favourite icon -Verify favourite icon count -Verify user can navigate to the favourite matches page and verify the page links and details  "
    DESCRIPTION: "Verify user can add FB favourites,
    DESCRIPTION: - Verify user can select/Deselect favourite icon
    DESCRIPTION: -Verify favourite icon count
    DESCRIPTION: -Verify user can navigate to the favourite matches page and verify the page links and details
    DESCRIPTION: "
    PRECONDITIONS: "Site is loaded & the user is logged in.
    PRECONDITIONS: There are inPlay/Upcoming events under Football League competitions"
    """
    keep_browser_open = True

    def test_001_load_appsite__log_in(self):
        """
        DESCRIPTION: Load app/site & Log in
        EXPECTED: User is logged in and on the Homepage
        """
        pass

    def test_002_navigate_to_football(self):
        """
        DESCRIPTION: Navigate to Football
        EXPECTED: User is on the Football page with Matches displayed
        """
        pass

    def test_003_add_football_event_to_favourites(self):
        """
        DESCRIPTION: Add Football Event to Favourites
        EXPECTED: Event is displayed on Favourite widget
        """
        pass

    def test_004_verify_the_user_is_able_to_select__deselect_the_favourites(self):
        """
        DESCRIPTION: Verify the user is able to select & deselect the Favourites
        EXPECTED: User is able to select & deselect the Favourites.
        """
        pass

    def test_005_go_to_favourite_matchesdesktop_favourites_widgetmobile_star_fav_on_the_header__football_pageand_verify_user_can_navigate_to_the_favourite_matches_page_and_verify_the_page_links_and_details(self):
        """
        DESCRIPTION: Go to Favourite Matches
        DESCRIPTION: Desktop: Favourites Widget
        DESCRIPTION: Mobile: Star (Fav) on the Header > Football page
        DESCRIPTION: and verify user can navigate to the favourite matches page and verify the page links and details
        EXPECTED: All the selected Favourites are displayed and the user is able to navigate to the favourite matches page and verify the page links and details.
        """
        pass

    def test_006_verify_the_user_is_able_to_deselect_previous_added_event_from_favourite_widget(self):
        """
        DESCRIPTION: Verify the user is able to Deselect previous added Event from Favourite widget
        EXPECTED: Event are deselected from Favourite widget
        """
        pass
