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
class Test_C28381_Footer_Menu_Configuration_and_Display(Common):
    """
    TR_ID: C28381
    NAME: Footer Menu Configuration and Display
    DESCRIPTION: This test case verifies Footer Menu Configuration in CMS
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-8171 DESKTOP Global Left Navigation
    DESCRIPTION: *   BMA-8172 CMS - Footer Menu - Mobile, Tablet and Desktop Flag
    DESCRIPTION: *   [BMA-14598 V1.5 Footer][1]
    DESCRIPTION: *   [BMA-14721 Add ability to upload svg icons to Footer menu in CMS][2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-14598
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-14721
    PRECONDITIONS: LINK TITLE - TARGET URI
    PRECONDITIONS: Home - /
    PRECONDITIONS: All Sports - /az-sports
    PRECONDITIONS: In Play-  /in-play
    PRECONDITIONS: Cash Out - /cashout
    PRECONDITIONS: Gaming - http://mcasino-tst2.coral.co.uk/?ref=bma
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_on_mobile_and_tablet(self):
        """
        DESCRIPTION: Load Oxygen application on mobile and tablet
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_presence_of_footer_menu(self):
        """
        DESCRIPTION: Verify presence of Footer menu
        EXPECTED: *   Footer menu is present on the bottom of the page
        EXPECTED: *   Footer menu is present on every page across app
        """
        pass

    def test_003_verify_footer_menu_items_order(self):
        """
        DESCRIPTION: Verify Footer menu items order
        EXPECTED: Footer Menu items order corresponds to the set in CMS by drag-n-drop order
        """
        pass

    def test_004_tap_footer_menu_item(self):
        """
        DESCRIPTION: Tap Footer Menu item
        EXPECTED: *   Footer Menu item is selected and highlighted
        EXPECTED: *   User is navigeted to corrisponding page set in CMS
        """
        pass

    def test_005_verify_menu_item_names(self):
        """
        DESCRIPTION: Verify Menu item names
        EXPECTED: *   Menu item names correspond to the names set in CMS
        EXPECTED: *   Menu item names must be unique.
        EXPECTED: *   Menu item names must not be null or empty.
        """
        pass

    def test_006_verify_end_point_after_tapping_menu_items(self):
        """
        DESCRIPTION: Verify end point after tapping Menu items
        EXPECTED: *   Tapping Menu items redirect to the pages, path for which were set in 'Target Uri' field in CMS
        EXPECTED: *   'Target Uri' supports internal (e.g. football/today) and external (begins with http/https) Uri's
        EXPECTED: *   When the Uri is empty and the user taps the menu item in the app then the app should do nothing.
        EXPECTED: *   In-App (selected/unselected) : determines if the end point for the URL should be displayed within the app with the Global Header & Footer or opens in a separate browser window (default - selected)
        EXPECTED: *   Footer Menu is expanded
        EXPECTED: *   'Authentication Required' (selected/unselected): determines if the end point for the URL should be append with session temporary token and username (default - unselected)
        EXPECTED: *   'SystemID' (the value should be numeric): associated SystemID for the application being called from the link. The value is only required if Authentication Required field is enabled
        EXPECTED: *   If  'Authentication Required' is selected and 'SystemID' is defined then after navigation to target URL Oxygen user should be automatically logged in
        """
        pass

    def test_007_verify_menu_items_visibility(self):
        """
        DESCRIPTION: Verify Menu items visibility
        EXPECTED: *   Disabled (selected/unselected) - determines whether the menu item should be visible in the left hand menu (default - unselected)
        EXPECTED: *   Show Item For (Logged In, Logged Out or Both) - determines when to display item (default - Both)
        """
        pass

    def test_008_verify_menu_items_view(self):
        """
        DESCRIPTION: Verify Menu items view
        EXPECTED: *   Menu Item View (Logged In, Logged Out, Both) - determines possibility to set whether the footer menu items display only for logged in, logged out or both users.
        EXPECTED: *   If no menu icon has been set - only menu name is shown
        """
        pass

    def test_009_verify__filename_option_in_cms(self):
        """
        DESCRIPTION: Verify ' Filename' option in CMS
        EXPECTED: *   'Filename' support only PNG or JPEG format
        EXPECTED: *   It is possible not to upload an icon image
        """
        pass

    def test_010_verify_svg_filename_option_in_cms(self):
        """
        DESCRIPTION: Verify 'Svg Filename' option in CMS
        EXPECTED: *   'Svg Filename' option supports only SVG format
        EXPECTED: *   It is possible not to upload an icon image
        """
        pass

    def test_011_verify_menu_items_presence_on_mobile_tablet(self):
        """
        DESCRIPTION: Verify Menu items presence on mobile, tablet
        EXPECTED: *   Menu Item View (Mobile, Tablet) determines possibility to set whether the footer menu items display only for mobile users, tablet users, desktop users or combinations of them
        EXPECTED: *   If all 3 are unselected (Mobile, Tablet, Desktop) then Menu item isn't shown at all.
        """
        pass
