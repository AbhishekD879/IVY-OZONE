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
class Test_C44870406_Verify_quick_link_navigation(Common):
    """
    TR_ID: C44870406
    NAME: Verify quick link navigation
    DESCRIPTION: Verify user can navigate to relevant pages by clicking on 'Hit a Quick Link'  menu items in the site page bottom
    DESCRIPTION: Verify on the all pages at the bottom
    PRECONDITIONS: Quick Link items are displayed on all pages at the bottom in logged in and logged out status.
    """
    keep_browser_open = True

    def test_001_open_httpsbeta_sportscoralcouk_on_chrome_browser(self):
        """
        DESCRIPTION: Open https://beta-sports.coral.co.uk/ on Chrome browser.
        EXPECTED: https://beta-sports.coral.co.uk/ displayed on Chrome browser.
        """
        pass

    def test_002_scroll_to_bottom_of_page(self):
        """
        DESCRIPTION: Scroll to bottom of page.
        EXPECTED: Page displays
        EXPECTED: "NOT FOUND WHAT YOU ARE LOOKING FOR? HIT A QUICK LINK"
        EXPECTED: Play 1-2 Free to win £1
        EXPECTED: Homepage
        EXPECTED: In-Play Betting
        EXPECTED: Horse Racing
        EXPECTED: etc
        """
        pass

    def test_003_click_on_horse_racing_quick_link(self):
        """
        DESCRIPTION: Click on Horse Racing Quick Link.
        EXPECTED: User directed to Horse Racing landing page.
        """
        pass

    def test_004_scroll_to_bottom_of_page(self):
        """
        DESCRIPTION: Scroll to bottom of page.
        EXPECTED: Page displays
        EXPECTED: "NOT FOUND WHAT YOU ARE LOOKING FOR? HIT A QUICK LINK"
        EXPECTED: Play 1-2 Free to win £1
        EXPECTED: Homepage
        EXPECTED: In-Play Betting
        EXPECTED: Horse Racing
        EXPECTED: etc
        """
        pass

    def test_005_click_on_horse_promotions_link(self):
        """
        DESCRIPTION: Click on Horse Promotions Link.
        EXPECTED: User directed to Horse Racing landing page.
        """
        pass

    def test_006_repeat_the_above_step_for_a_range_of_quick_links_available(self):
        """
        DESCRIPTION: Repeat the above step for a range of quick links available
        EXPECTED: User is directed to those respective quick links and is able to see the respective quick links at the bottom of the page.
        """
        pass
