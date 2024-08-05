import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException


#@pytest.mark.crl_tst2  # Coral only
#@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.local_storage
@pytest.mark.cookies
@pytest.mark.retail
@pytest.mark.static_block
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1008')
@pytest.mark.na
@vtest
@pytest.mark.connect_descoped
class Test_C2461981_Verify_Connect_Overlays_displaying(BaseUserAccountTest):
    """
    TR_ID: C2461981
    VOL_ID: C9697860
    NAME: Verify Connect Overlays displaying
    DESCRIPTION: This test case verifies that Connect Overlay will be shown for the user, who had Connect app on his device earlier
    PRECONDITIONS: Make sure Connect Overlay tutorial feature is turned on in CMS: System configuration -> Connect -> overlay
    PRECONDITIONS: * If no overlay appears, ensure that in dev tool -> Application tab -> cookies: field Name 'CONNECT_TRACKER' = 'false' and in Locale storage: OX.connectOverlayRemain is = 4.
    PRECONDITIONS: * Reload the SB app
    PRECONDITIONS: * Connect overlay tutorial is shown
    """
    keep_browser_open = True
    local_storage_cookie_name = 'OX.retailOverlayRemain'
    local_storage_tutorial_cookie = 'OX.tutorial'
    cookie_name = 'CONNECT_TRACKER'
    is_enabled = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if not cls.is_enabled and tests.settings.cms_env != 'prd0':
            cms = cls.get_cms_config()
            cms.enable_static_block(uri=cms.constants.CONNECT_STATIC_BLOCK_URI, enable=False)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify CMS settings ans set cookies
        """
        self.__class__.is_enabled = self.cms_config.is_static_block_enabled(uri=self.cms_config.constants.CONNECT_STATIC_BLOCK_URI)
        if not self.is_enabled:
            if tests.settings.cms_env != 'prd0':
                self.cms_config.enable_static_block(uri=self.cms_config.constants.CONNECT_STATIC_BLOCK_URI)
            else:
                raise CmsClientException(f'Static block with uri "{self.cms_config.constants.CONNECT_STATIC_BLOCK_URI}" is disabled, '
                                         f'cannot execute the test on prod endpoints')
        self.set_local_storage_cookie_value(cookie_name=self.local_storage_cookie_name, value=4)
        self.set_local_storage_cookie_value(cookie_name=self.local_storage_tutorial_cookie, value=False)
        self.add_cookie(cookie_name=self.cookie_name, value='false')

    def test_001_close_the_overlay_shown_for_the_first_time_with_a_close_button_x(self):
        """
        DESCRIPTION: Close the overlay (shown for the first time) with a close button (X)
        EXPECTED: * The overlay is closed
        EXPECTED: * Home page is shown
        EXPECTED: * Locale storage: OX.connectOverlayRemain shows value 3
        """
        self.device.navigate_to(url=tests.HOSTNAME)
        self.assertTrue(self.site.wait_for_connect_overlay(), msg='Connect overlay is not shown')

        self.site.connect_overlay.close_button.click()

        self.assertFalse(self.site.wait_for_connect_overlay(expected_result=False, timeout=5),
                         msg='Connect overlay is still shown')
        self.site.wait_content_state('Homepage')

        value = self.get_local_storage_cookie_value(cookie_name=self.local_storage_cookie_name)
        self.assertEqual(value, '3', msg=f'Local storage cookie value {value} is not the same as expected "3"')

    def test_002_reload_the_homepage(self):
        """
        DESCRIPTION: Reload the Homepage
        EXPECTED: * A user is left on the Homepage
        EXPECTED: * Connect overlay is displayed for the second time
        EXPECTED: * Locale storage: OX.connectOverlayRemain shows value 2
        """
        self.device.refresh_page()
        self.site.wait_content_state('Homepage')
        self.assertTrue(self.site.wait_for_connect_overlay(), msg='Connect overlay is not shown')

        value = self.get_local_storage_cookie_value(cookie_name=self.local_storage_cookie_name)
        self.assertEqual(value, '2', msg=f'Local storage cookie value {value} is not the same as expected "2"')

    def test_003_tap_an_image_of_the_connect_logo(self):
        """
        DESCRIPTION: Tap an image of the Connect logo
        EXPECTED: Connect landing page is opened
        """
        self.site.connect_overlay.connect_icon.click()
        self.site.wait_content_state('Connect')

    def test_004_make_sure_connect_overlay_is_not_shown_on_any_other_page_except_home_page_go_to_any_any_sports_landing_page_reload_the_page(self):
        """
        DESCRIPTION: Make sure Connect Overlay is not shown on any other page except Home page:
        DESCRIPTION: * Go to any (any) Sports landing page
        DESCRIPTION: * Reload the page
        EXPECTED: Connect Overlay does not appear
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        self.assertFalse(self.site.wait_for_connect_overlay(expected_result=False, timeout=5),
                         msg='Connect overlay is shown')

        self.device.refresh_page()
        self.site.wait_content_state('football')
        self.assertFalse(self.site.wait_for_connect_overlay(expected_result=False, timeout=5),
                         msg='Connect overlay is shown')

    def test_005_tap_homepage_button(self):
        """
        DESCRIPTION: Tap Homepage button
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('Homepage')

    def test_006_verify_log_in_does_not_influence_connect_overlay_displaying_log_in_with_existing_user(self):
        """
        DESCRIPTION: Verify Log in does not influence Connect Overlay displaying:
        DESCRIPTION: * Log in with existing user
        EXPECTED: * User is logged in successfully
        EXPECTED: * default Sportsbook overlay is displayed if user is logged in for the first
        EXPECTED: * Dialogs pop ups are displayed if required
        """
        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg='Login dialog is not present on page')
        if tests.settings.backend_env != 'prod':
            dialog.username = tests.settings.freebet_user
        else:
            dialog.username = tests.settings.betplacement_user
        dialog.password = tests.settings.default_password
        dialog.click_login()
        dialog_closed = dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')

        tac_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_TERMS_AND_CONDITIONS, timeout=3)
        if tac_dialog:
            tac_dialog.default_action()
            tac_dialog.wait_dialog_closed()

        self.assertTrue(self.site.wait_for_tutorial_overlay(), msg='Tutorial overlay is not shown')
        self.site.tutorial_overlay.text_panel.close_button.click()

        if tests.settings.backend_env != 'prod':
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_TOKEN_DESCRIPTION, timeout=3)
            self.assertTrue(dialog, msg='FREE BETS TOKEN DESCRIPTION dialog is not shown')
            dialog.close_dialog()

    def test_007_reload_the_homepage(self):
        """
        DESCRIPTION: Reload the Homepage
        EXPECTED: * A user is left on the Homepage
        EXPECTED: * Connect overlay is displayed for the third time
        EXPECTED: * Locale storage: OX.connectOverlayRemain shows value 1
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')
        self.assertTrue(self.site.wait_for_connect_overlay(), msg='Connect overlay is not shown')

        value = self.get_local_storage_cookie_value(cookie_name=self.local_storage_cookie_name)
        self.assertEqual(value, '1', msg=f'Local storage cookie value {value} is not the same as expected "1"')

    def test_008_tap_take_me_to_the_connect_hub_button(self):
        """
        DESCRIPTION: Tap 'TAKE ME TO THE CONNECT HUB' button
        EXPECTED: Connect landing page is opened
        """
        self.site.connect_overlay.navigate_to_connect.click()
        self.site.wait_content_state('Connect')

    def test_009_tap_homepage_button(self):
        """
        DESCRIPTION: Tap Homepage button
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('Homepage')

    def test_010_reload_the_homepage(self):
        """
        DESCRIPTION: Reload the Homepage
        EXPECTED: * A user is left on the Homepage
        EXPECTED: * Connect overlay is displayed for the las time
        EXPECTED: * Locale storage: OX.connectOverlayRemain shows value 0
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')
        self.assertTrue(self.site.wait_for_connect_overlay(), msg='Connect overlay is not shown')

        value = self.get_local_storage_cookie_value(cookie_name=self.local_storage_cookie_name)
        self.assertEqual(value, '0', msg=f'Local storage cookie value {value} is not the same as expected "0"')

    def test_011_reload_the_homepage_again(self):
        """
        DESCRIPTION: Reload the Homepage again
        EXPECTED: * A user is left on the Homepage
        EXPECTED: * Connect overlay is not shown any more
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')
        self.assertFalse(self.site.wait_for_connect_overlay(expected_result=False, timeout=5),
                         msg='Connect overlay is shown')
