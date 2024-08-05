import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2  # Ladbrokes only feature
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.low
@pytest.mark.homepage_featured
@pytest.mark.gaming
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C58419486_Gaming_overlay_behaviour_for_logged_in_not_logged_in_user_on_iOS_version_130(Common):
    """
    TR_ID: C58419486
    VOL_ID: C58626827
    NAME: "Gaming" overlay behaviour for logged in/not logged in user on iOS version < 13.0
    DESCRIPTION: This test case verifies "Gaming Overlay" behaviour for logged in user on iOS version < 13.0
    DESCRIPTION: Test case should only be run on mobile/tablet browsers (Safari, Chrome)
    PRECONDITIONS: Design: https://app.zeplin.io/project/5c6ac2bc1c25679a7c64f730?seid=5e26bf41f308cd9894fd184e
    PRECONDITIONS: Gaming Overlay Enabled in CMS :
    PRECONDITIONS: System Configuration -> Config -> GamingEnabled > enabled=true
    PRECONDITIONS: System Configuration -> Config -> GamingEnabled > overlayUrl > set url(below).
    PRECONDITIONS: overlayUrls: for BETA -  https://beta-www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BINGO
    PRECONDITIONS: for QA - https://qa2.www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BINGO
    PRECONDITIONS: The iOS version should be lower 13.0
    PRECONDITIONS: User is not logged in
    """
    keep_browser_open = True
    gaming_url = None
    device_name = 'iPhone XS' if not tests.use_browser_stack else tests.mobile_safari_default

    def verify_redirection(self):
        result = wait_for_result(lambda: self.gaming_url.split('//')[-1] in self.device.get_current_url().split('//')[-1],
                                 name=f'User to be redirected to the "{self.gaming_url}"',
                                 expected_result=True,
                                 timeout=5)
        self.assertTrue(result,
                        msg=f'User is not redirected to the "{self.gaming_url}", '
                        f'instead "{self.device.get_current_url()}" is opened')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Check if GamingEnabled > enabled=true in CMS
        """
        gaming_overlay = self.get_initial_data_system_configuration().get('GamingEnabled', {})
        if not gaming_overlay:
            gaming_overlay = self.cms_config.get_system_configuration_item('GamingEnabled')
        if not gaming_overlay.get('enabledGamingOverlay'):
            raise CmsClientException('"Gaming Overlay" is not Enabled in CMS')
        if not gaming_overlay.get('overlayURL'):
            raise CmsClientException('"Gaming Overlay" URL is not configured in CMS')

        cms_footer_menus = self.cms_config.get_cms_menu_items(menu_types='Footer Menus').get('Footer Menus')
        for menu in cms_footer_menus:
            if menu['linkTitle'] == 'Gaming':
                self.__class__.gaming_url = menu['targetUri']
                break
        if not self.gaming_url:
            raise CmsClientException('"Gaming URL" is not configured in CMS')

    def test_001_launch_the_application_and_scroll_down_to_tab_bar(self):
        """
        DESCRIPTION: Launch the application and scroll down to Tab bar.
        EXPECTED: Application is opened and Tab bar is visible.
        """
        self.site.wait_content_state(state_name='Homepage')
        self.assertTrue(self.site.navigation_menu.is_displayed(), msg='Tab bar is not visible')

    def test_002_tap_on_the_gaming_button_on_the_tap_bar(self):
        """
        DESCRIPTION: Tap on the "Gaming" button on the tap bar.
        EXPECTED: User is redirected to the "Casino" landing page.
        """
        self.site.navigation_menu.click_item(vec.sb.GAMING_FOOTER_ITEM)
        self.verify_redirection()

    def test_003_launch_the_application_and_log_in_with_correct_credentials(self):
        """
        DESCRIPTION: Launch the application and log in with correct credentials.
        EXPECTED: User is logged in and sees the "Home" page.
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')

        self.site.login()

    def test_004_tap_on_the_gaming_button_on_the_tab_bar(self):
        """
        DESCRIPTION: Tap on the "Gaming" button on the Tab bar.
        EXPECTED: User is redirected to the "Casino" landing page.
        """
        self.site.navigation_menu.click_item(vec.sb.GAMING_FOOTER_ITEM)
        self.verify_redirection()
