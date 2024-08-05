import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2  # Ladbrokes Only test functionality
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.low
@pytest.mark.homepage_featured
@pytest.mark.gaming
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C58419485_Gaming_overlay_behaviour_for_logged_in_user_on_iOS_130_and_Android_any_version(Common):
    """
    TR_ID: C58419485
    VOL_ID: C58446746
    NAME: "Gaming" overlay behaviour for logged in user on iOS >= 13.0 and Android (any version)
    DESCRIPTION: This test case verifies opening and closing "Gaming" overlay.
    DESCRIPTION: Test case should only be run on mobile/tablet browsers (Safari, Chrome)
    PRECONDITIONS: Design: https://app.zeplin.io/project/5c6ac2bc1c25679a7c64f730?seid=5e26bf41f308cd9894fd184e
    PRECONDITIONS: Gaming Overlay Enabled in CMS :
    PRECONDITIONS: System Configuration -> Config -> GamingEnabled > enabled=true
    PRECONDITIONS: System Configuration -> Config -> GamingEnabled > overlayUrl > set url(below).
    PRECONDITIONS: overlayUrls: for BETA -  https://beta-www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BINGO
    PRECONDITIONS: for QA   -  https://qa2.www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BINGO
    PRECONDITIONS: The iOS version should be higher than 13.0
    PRECONDITIONS: The user should be logged in.
    """
    keep_browser_open = True
    device_name = 'iPhone XR' if not tests.use_browser_stack else tests.mobile_safari_default
    sport_name = vec.siteserve.FOOTBALL_TAB

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check if GamingEnabled > enabled=true in CMS
        DESCRIPTION: User is logged in
        """
        system_configuration = self.get_initial_data_system_configuration()
        gaming_overlay = system_configuration.get('GamingEnabled', {})
        if not gaming_overlay:
            gaming_overlay = self.cms_config.get_system_configuration_item('GamingEnabled')
        if not gaming_overlay.get('enabled'):
            raise CmsClientException('"Gaming Overlay" is not Enabled in CMS')
        if not gaming_overlay.get('overlayUrl'):
            raise CmsClientException('"Gaming Overlay" URL is not configured in CMS')

        self.site.login()

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch Application.
        EXPECTED: Application is launched and user is navigated to the "Home" page.
        """
        # covered in preconditions

    def test_002_tap_on_the_gaming_button_on_the_tap_bar(self):
        """
        DESCRIPTION: Tap on the "Gaming" button on the tap bar.
        EXPECTED: "Gaming" overlay should be shown as per design.
        EXPECTED: ![](index.php?/attachments/get/101705294)
        """
        self.site.navigation_menu.click_item(vec.sb.GAMING_FOOTER_ITEM)
        self.site.wait_splash_to_hide()
        result = self.site.gaming_overlay.wait_for_gaming_spinner_to_hide(timeout=20)
        self.assertTrue(result, msg='"Gaming" spinner is not hidden')
        self.assertTrue(self.site.gaming_overlay.is_displayed(), msg='"Gaming" overlay is not shown')
        self.__class__.gaming_overlay = self.site.gaming_overlay.stick_to_iframe()
        self.assertEqual(self.gaming_overlay.header.title, vec.gvc.GAMING_OVERLAY_TITLE,
                         msg=f'Actual Gaming Overlay title "{self.gaming_overlay.header.title}" is not as expected '
                         f'"{vec.gvc.GAMING_OVERLAY_TITLE}"')

    def test_003_tap_on_x_button(self, page_default='Homepage'):
        """
        DESCRIPTION: Tap on "X" button.
        EXPECTED: "Gaming" overlay should be closed.
        EXPECTED: User should be on the page he was before opening "Gaming" overlay.
        """
        self.gaming_overlay.header.close_button.click()
        self.site.gaming_overlay.switch_to_main_page()
        self.site.wait_content_state(page_default)

    def test_004_navigate_to_any_sports_page_and_repeat_steps_1_3_above(self):
        """
        DESCRIPTION: Navigate to any Sports page and repeat Steps 1-3 above.
        """
        if self.site.cookie_banner:
            self.site.cookie_banner.ok_button.click()
        self.site.open_sport(name=self.sport_name)
        self.test_002_tap_on_the_gaming_button_on_the_tap_bar()
        self.test_003_tap_on_x_button(page_default=self.sport_name)
