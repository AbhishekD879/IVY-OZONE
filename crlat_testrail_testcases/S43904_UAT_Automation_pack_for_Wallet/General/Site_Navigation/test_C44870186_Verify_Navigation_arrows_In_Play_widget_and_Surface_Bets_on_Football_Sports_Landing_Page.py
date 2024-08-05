import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C44870186_Verify_Navigation_arrows_In_Play_widget_and_Surface_Bets_on_Football_Sports_Landing_Page(Common):
    """
    TR_ID: C44870186
    NAME: "Verify Navigation arrows, In-Play widget and Surface Bets on Football Sports Landing Page.
    DESCRIPTION: "Verify Navigation arrows, In-Play widget and Surface Bets on Football Sports Landing Page.
    PRECONDITIONS: BETA app is loaded and User is on Home page
    PRECONDITIONS: Surface bets are configured on Football Sports Landing Page
    PRECONDITIONS: In order to place bets the user must be logged in.
    """
    keep_browser_open = True

    def test_001_from_home_page_tap_on_footballfrom_header_menu_or_from_all_sports_menu(self):
        """
        DESCRIPTION: From home page tap on Football
        DESCRIPTION: (From header Menu or from All sports menu)
        EXPECTED: User lands on Football sports landing page
        """
        pass

    def test_002_mobile__tablet_only__verify_surface_bets_on_football_landing_page(self):
        """
        DESCRIPTION: Mobile & Tablet only : Verify Surface bets on Football Landing Page
        EXPECTED: User should see Surface bets.
        EXPECTED: User should be able to scroll across the surface bet if more than one are available.
        EXPECTED: User should be able to add and place bets from SurfaceBets.
        """
        pass

    def test_003_desktop_only__verify_in_play_widget_on_foot_ball_landing_page(self):
        """
        DESCRIPTION: Desktop only : Verify In-Play Widget on Foot ball Landing Page
        EXPECTED: On Football Landing Page, User should see In-Play widget.
        EXPECTED: User should be able to scroll across the events if more than one event available.
        EXPECTED: User should navigate to the respective event when tapped on any In-Play event
        """
        pass
