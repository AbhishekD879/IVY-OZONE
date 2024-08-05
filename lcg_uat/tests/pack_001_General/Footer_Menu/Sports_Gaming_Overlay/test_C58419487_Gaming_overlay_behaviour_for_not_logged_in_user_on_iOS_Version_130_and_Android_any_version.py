import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.low
@pytest.mark.reg157_fix
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@vtest
class Test_C58419487_Gaming_overlay_behaviour_for_not_logged_in_user_on_iOS_Version_130_and_Android_any_version(Common):
    """
    TR_ID: C58419487
    NAME: "Gaming" overlay behaviour for not logged in user on iOS Version >= 13.0 and Android (any version)
    DESCRIPTION: This test case verifies "Gaming" overlay behaviour for not logged in user on iOS Version >= 13.0 and all Android versions
    DESCRIPTION: Test case should only be run on mobile/tablet browsers (Safari, Chrome)
    DESCRIPTION: AUTOTEST [C58626054]
    PRECONDITIONS: User is not logged in
    PRECONDITIONS: iOS version is >= 13.0
    PRECONDITIONS: Android - all versions
    PRECONDITIONS: Design: https://app.zeplin.io/project/5c6ac2bc1c25679a7c64f730?seid=5e26bf41f308cd9894fd184e
    PRECONDITIONS: Gaming Overlay Enabled in CMS :
    PRECONDITIONS: System Configuration -> Structure -> GamingEnabled > enabled=true
    PRECONDITIONS: System Configuration -> Structure -> GamingEnabled > overlayUrl > set url
    PRECONDITIONS: ![](index.php?/attachments/get/101693960)
    PRECONDITIONS: overlayUrls:
    PRECONDITIONS: Ladbrokes: https://www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BETTING&_disableFeature=GlobalSearch
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://qa2.www.coral.co.uk/en/sportsoverlay?.box=1&invokerProduct=BETTING&_disableFeature=GlobalSearch
    """
    keep_browser_open = True
    device_name = 'iPhone XS' if not tests.use_browser_stack else tests.mobile_safari_default

    def test_000_open_the_application_and_scroll_down_to_the_tab_bar(self):
        """
        DESCRIPTION: Open the application and scroll down to the Tab bar
        EXPECTED: Application is opened and the Tab bar is visible
        """
        self.site.wait_content_state("homepage")
        footer_menu = self.site.navigation_menu
        self.assertTrue(footer_menu, msg='Footer menu is not displayed')

    def test_001_tap_on_the_gaming_icon_on_the_tab_bar(self):
        """
        DESCRIPTION: Tap on the "Gaming" icon on the Tab bar
        EXPECTED: - User is taken to the "Casino" landing page
        EXPECTED: - Login overlay or Face/ Touch ID is NOT shown
        """
        footer_items = self.site.navigation_menu.items_as_ordered_dict
        gaming_button = footer_items.get(vec.sb.GAMING_FOOTER_ITEM) if vec.sb.GAMING_FOOTER_ITEM in footer_items else footer_items.get(vec.sb.CASINO_FOOTER_ITEM)
        gaming_button.click()
        self.site.wait_content_state_changed()
        current_url = self.device.get_current_url()
        self.assertIn('games', current_url, msg=current_url)
