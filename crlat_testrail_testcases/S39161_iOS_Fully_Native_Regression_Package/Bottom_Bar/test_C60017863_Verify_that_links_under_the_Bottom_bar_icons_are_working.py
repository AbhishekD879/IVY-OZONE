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
class Test_C60017863_Verify_that_links_under_the_Bottom_bar_icons_are_working(Common):
    """
    TR_ID: C60017863
    NAME: Verify that links under the Bottom bar icons are working.
    DESCRIPTION: This test case verifies that links under the Bottom bar icons are working.
    PRECONDITIONS: Coral/Ladbrokes app is installed.
    """
    keep_browser_open = True

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app.
        EXPECTED: * User is on the homepage.
        EXPECTED: * Page is loaded.
        EXPECTED: * "Homepage" icon is highlighted.
        """
        pass

    def test_002_tap_on_in_play_icon(self):
        """
        DESCRIPTION: Tap on "In-Play" icon.
        EXPECTED: * User is on In-Play page.
        EXPECTED: * Page is loaded.
        EXPECTED: * "In-Play" icon is highlighted.
        """
        pass

    def test_003_tap_on_the_menu_icon(self):
        """
        DESCRIPTION: Tap on the "Menu" icon.
        EXPECTED: * User is on the Menu page.
        EXPECTED: * Page is loaded.
        EXPECTED: * "Menu" icon is highlighted.
        """
        pass

    def test_004_tap_on_my_bets_icon(self):
        """
        DESCRIPTION: Tap on "My Bets" icon.
        EXPECTED: * User is on My Bets page.
        EXPECTED: * Page is loaded.
        EXPECTED: * "My Bets" icon is highlighted.
        """
        pass

    def test_005_tap_on_account_icon(self):
        """
        DESCRIPTION: Tap on "Account" icon.
        EXPECTED: * User is on Account page.
        EXPECTED: * Page is loaded.
        EXPECTED: * "Account" icon is highlighted.
        """
        pass

    def test_006_tap_on_gaming_icon(self):
        """
        DESCRIPTION: Tap on "Gaming" icon.
        EXPECTED: * User is on Gaming page.
        EXPECTED: * Page is loaded.
        EXPECTED: * "Gaming" icon is highlighted.
        """
        pass
