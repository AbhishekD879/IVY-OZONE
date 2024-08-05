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
class Test_C60079479_Verify_Overlay_for_Football_landing_page(Common):
    """
    TR_ID: C60079479
    NAME: Verify Overlay for Football landing page
    DESCRIPTION: This Test Case verified Overlay for Match Centre.
    PRECONDITIONS: **﻿JIRA Ticket:**
    PRECONDITIONS: - BMA-9271 Overlay for Match Centre: Favourites Functionality Journey
    PRECONDITIONS: - BMA-16264 Cookie Banner :- Football tutorial displaying when cookie banner message is shown
    PRECONDITIONS: - BMA-31881
    PRECONDITIONS: 1) User is logged out
    PRECONDITIONS: 2) All cookies and cash are cleared
    """
    keep_browser_open = True

    def test_001_mobileload_the_application(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Load the application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_on_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on Football icon on the Sports Menu Ribbon
        EXPECTED: - Football landing page is opened
        EXPECTED: - Football tutorial overlay is **NOT** loaded
        """
        pass

    def test_003_log_in_into_the_application(self):
        """
        DESCRIPTION: Log in into the application
        EXPECTED: User is logged in
        """
        pass

    def test_004_tap_on_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on Football icon on the Sports Menu Ribbon
        EXPECTED: - Football landing page is opened
        EXPECTED: - Football tutorial overlay **is** loaded
        """
        pass

    def test_005_tap_on_close_tutorial_button(self):
        """
        DESCRIPTION: Tap on 'Close tutorial' button
        EXPECTED: Overlay is closed
        """
        pass

    def test_006_go_to_the_homepage(self):
        """
        DESCRIPTION: Go to the homepage
        EXPECTED: Homepage is opened
        """
        pass

    def test_007_tap_on_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on Football icon on the Sports Menu Ribbon
        EXPECTED: - Football landing page is opened
        EXPECTED: - Football tutorial overlay is **NOT** loaded
        """
        pass

    def test_008_clear_all_cookies_and_cache(self):
        """
        DESCRIPTION: Clear all cookies and cache
        EXPECTED: 
        """
        pass

    def test_009_log_in_into_the_application_being_on_football_page(self):
        """
        DESCRIPTION: Log in into the application (being on Football page)
        EXPECTED: - User is logged in
        EXPECTED: - Football landing page is opened
        EXPECTED: - Football tutorial overlay **is** loaded
        """
        pass

    def test_010_verify_how_to_overlay_when_cookies_banner_is_present(self):
        """
        DESCRIPTION: Verify 'How to?' overlay when Cookies Banner is present
        EXPECTED: - 'How to?' overlay is displayed under Cookie Banner if its present
        EXPECTED: - 'How to?' overlay is scrollable on devices with small screen resolution when Cookie Banner is present
        """
        pass

    def test_011_repeat_above_steps_on_desktop(self):
        """
        DESCRIPTION: Repeat above steps on **Desktop**
        EXPECTED: Tutorial overlay is not displayed on desktop in any situation.
        """
        pass
