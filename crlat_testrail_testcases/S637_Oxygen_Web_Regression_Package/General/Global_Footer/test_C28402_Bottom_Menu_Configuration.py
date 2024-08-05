import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C28402_Bottom_Menu_Configuration(Common):
    """
    TR_ID: C28402
    NAME: Bottom Menu Configuration
    DESCRIPTION: This test case verifies Quick Links section configuration
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: *   BMA-10479 V2 - Footer
    PRECONDITIONS: Link Title - Target URI
    PRECONDITIONS: Sports Bettings/Bet in Play in-play
    PRECONDITIONS: Coral News - http://news.coral.co.uk/
    PRECONDITIONS: Online Casino - http://www.coral.co.uk/casino/top-games
    PRECONDITIONS: Live Casino - http://www.coral.co.uk/live-casino
    PRECONDITIONS: Online Poker - http://www.coral.co.uk/poker
    PRECONDITIONS: Online Games - http://www.coral.co.uk/games/top-games
    PRECONDITIONS: Online Slots - http://www.coral.co.uk/slots/top-games
    PRECONDITIONS: Online Bingo - http://www.coral.co.uk/bingo
    PRECONDITIONS: Lotto - lotto
    PRECONDITIONS: Mobile Betting - http://www.coral.co.uk/mobile
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: http://endpoints/keystone/bottom-menus, where **endpoints** can be found by using ***devlog*** function
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_bottom_menu_items_order(self):
        """
        DESCRIPTION: Verify Bottom Menu items order
        EXPECTED: Quick Links items order corresponds to the set in CMS by drag-n-drop order on 'Bottom Menus' page
        """
        pass

    def test_003_verify_menu_item_names(self):
        """
        DESCRIPTION: Verify Menu item names
        EXPECTED: *   Menu item names correspond to the names set in CMS
        EXPECTED: *   Menu item names must not be null or empty.
        """
        pass

    def test_004_verify_menu_items_visibility(self):
        """
        DESCRIPTION: Verify Menu items visibility
        EXPECTED: Disabled (active/inactive) - determines whether the menu item should be visible in the Quick Link menu (default - active)
        """
        pass

    def test_005_verify_end_point_after_tapping_menu_items(self):
        """
        DESCRIPTION: Verify end point after tapping Menu items
        EXPECTED: *   Clicking / tapping Menu items redirect to the pages, path for which were set in 'Target Uri' field in CMS
        EXPECTED: *   'Target Uri' supports internal (e.g. football/today) and external (begins with http/https) Uri's
        """
        pass

    def test_006_verify_in_app_checkbox(self):
        """
        DESCRIPTION: Verify 'In App' checkbox
        EXPECTED: *   'In App' attribute (selected / unselected) determaines that menu item is opened in new or the same browser tab
        EXPECTED: *    'In App' attribute is selected by default
        """
        pass
