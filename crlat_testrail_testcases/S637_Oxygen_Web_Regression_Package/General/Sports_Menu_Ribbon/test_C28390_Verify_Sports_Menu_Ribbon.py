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
class Test_C28390_Verify_Sports_Menu_Ribbon(Common):
    """
    TR_ID: C28390
    NAME: Verify Sports Menu Ribbon
    DESCRIPTION: This test case verifies Sports Menu Ribbon
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-12042 CMS - Ability to Hide/Show Mobile Ribbon Tabs on Mobile/Tablet
    DESCRIPTION: BMA-12043 Client - Module Ribbon Tabs
    DESCRIPTION: BMA-16183 Amend Breakpoints on Landscape for Oxygen Mobile
    PRECONDITIONS: CMS: https://cms-api-ui-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/menus/header-submenus
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: *   Homepage is opened
        EXPECTED: *   Sports Menu Ribbon is displayed
        """
        pass

    def test_002_verify_presence_of_sports_menu_ribbon(self):
        """
        DESCRIPTION: Verify presence of Sports Menu Ribbon
        EXPECTED: *   Sports Menu Ribbon is applicable only to Homepage
        EXPECTED: *   Sports Menu Ribbon is applicable to both logged in and logged out customers
        EXPECTED: *   It is left and right scrolling Ribbon
        EXPECTED: *   Every item is tappable icon with label
        """
        pass

    def test_003_verify_height_of_sports_menu_ribbon_on_mobile_tabletin_portrait_and_landscape_modes(self):
        """
        DESCRIPTION: Verify height of Sports Menu Ribbon On Mobile, Tablet in Portrait and Landscape Modes
        EXPECTED: Sports Menu Ribbon height is as following:
        EXPECTED: * Device CSS Screen Width from 360 to 460 px  - Menu height 60 px
        EXPECTED: * Device CSS Screen Width from 461 to 1023 px - Menu height 90 px
        EXPECTED: * Device CSS Screen Width from 1023 px  - Menu is not displayed
        """
        pass

    def test_004_verify_menu_item_names(self):
        """
        DESCRIPTION: Verify Menu item names
        EXPECTED: Menu item names correspond to the names set in CMS
        """
        pass

    def test_005_verify_end_point_after_tapping_menu_items(self):
        """
        DESCRIPTION: Verify end point after tapping Menu items
        EXPECTED: Tapping Menu items redirect to the pages, path for which were set in 'Target Uri' field in CMS (e.g. football/today)
        """
        pass

    def test_006_verify_menu_item_if_there_are_no_events_available_for_particular_sport(self):
        """
        DESCRIPTION: Verify Menu item if there are no events available for particular sport
        EXPECTED: Menu item is still visible in the Sports Menu Ribbon
        EXPECTED: <Sport> landing page is shown after tapping Menu item
        """
        pass

    def test_007_verify_menu_items_visibility(self):
        """
        DESCRIPTION: Verify Menu items' visibility
        EXPECTED: * Show Item On (Home, In-Play, Both) - determines whether the menu item should be shown in Homepage Sport Selector Ribbon, In-Play Sport Selector Ribbon or in both locations
        """
        pass

    def test_008_verify_menu_item_icons_format(self):
        """
        DESCRIPTION: Verify Menu item icons' format
        EXPECTED: *   'Filename' support only PNG format
        EXPECTED: *   It is possible not to upload an icon image
        """
        pass
