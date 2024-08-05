import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870187_Recently_Played_Gaming_Module(Common):
    """
    TR_ID: C44870187
    NAME: Recently Played Gaming Module
    DESCRIPTION: 1)Verify user navigates to gaming site by clicking on 'Gaming' tab bar menu and quick carousel menu.
    DESCRIPTION: 2)Verify if the Recently played games Portlet is displayed once scrolled down on roxanne site
    DESCRIPTION: 3)Verify user is navigated to the game info page with the Play Now button when clicks on the thumbnail of the game in the container
    DESCRIPTION: 4)Verify game is launched when user clicks on Play now button
    DESCRIPTION: 5)Check slides are scrollable when number of games to be displayed are more than 3
    PRECONDITIONS: Roxanne app is loaded
    PRECONDITIONS: User should be logged in,
    PRECONDITIONS: User should have played one or more games.
    """
    keep_browser_open = True

    def test_001_tap_on_gaming_icon_from_footer_menu(self):
        """
        DESCRIPTION: Tap on 'Gaming' icon from Footer menu
        EXPECTED: User should navigate to the Gaming page.
        """
        pass

    def test_002_verify_recently_played_games_portlet_on_home_page(self):
        """
        DESCRIPTION: Verify Recently Played Games portlet on home page
        EXPECTED: When user is on Roxanne home page and scrolls down , user should see Recently Played games.
        """
        pass

    def test_003_click_on_recently_played_accordion(self):
        """
        DESCRIPTION: Click on 'Recently played' accordion
        EXPECTED: All the recently played games are displayed.
        """
        pass

    def test_004_verify_rpg_carousel(self):
        """
        DESCRIPTION: verify RPG carousel
        EXPECTED: User should be able to scroll across the RPGs if more than 3 recently played games are listed.
        """
        pass
