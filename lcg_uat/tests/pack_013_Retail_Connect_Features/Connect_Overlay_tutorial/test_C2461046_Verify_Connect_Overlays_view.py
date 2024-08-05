import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import cleanhtml
from voltron.utils.waiters import wait_for_result


#@pytest.mark.crl_prod
@pytest.mark.crl_hl
#@pytest.mark.crl_tst2  # Coral only
#@pytest.mark.crl_stg2
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.local_storage
@pytest.mark.cookies
@pytest.mark.static_block
@pytest.mark.retail
@vtest
@pytest.mark.connect_descoped
class Test_C2461046_Verify_Connect_Overlays_view(BaseUserAccountTest):
    """
    TR_ID: C2461046
    VOL_ID: C9698428
    NAME: Verify Connect Overlays view
    DESCRIPTION: This test case verifies the view of Connect Overlay
    PRECONDITIONS: Make sure Connect Overlay tutorial feature is turned on in CMS: System configuration -> Connect -> overlay
    PRECONDITIONS: * User need to load SB on mobile device where Connect App and/or RCOMB microsite were used
    PRECONDITIONS: * When Connect App and RCOMB microsite were in use they have written following data into browser storage: cookies: field Name 'CONNECT_TRACKER' = 'false' and in Locale storage: OX.connectOverlayRemain = 4
    PRECONDITIONS: * To emulate above situation without using Connect App/ RCOMB   open dev tool -> Application tab -> cookies: field Name 'CONNECT_TRACKER' set with 'false' value and in Locale storage: OX.connectOverlayRemain set with value that is more than 0. Reload the SB app
    PRECONDITIONS: * User can be logged in or logged out
    """
    keep_browser_open = True
    local_storage_cookie_name = 'OX.retailOverlayRemain'
    cookie_name = 'CONNECT_TRACKER'
    background_color = 'rgba(0, 0, 0, 0.8)'
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
        content_config = self.get_initial_data_system_configuration().get('Connect', {})
        if not content_config:
            content_config = self.cms_config.get_system_configuration_item('Connect')
        if not content_config.get('overlay'):
            raise CmsClientException('Connect overlay is not enabled in CMS')

        static_block = self.cms_config.get_static_block(uri=self.cms_config.constants.CONNECT_STATIC_BLOCK_URI)
        self.__class__.cms_static_block_description = cleanhtml(static_block['htmlMarkup'])

        self.set_local_storage_cookie_value(cookie_name=self.local_storage_cookie_name, value=1)
        self.add_cookie(cookie_name=self.cookie_name, value='false')

    def test_001_verify_view_of_connect_overlay(self):
        """
        DESCRIPTION: Verify view of Connect overlay
        EXPECTED: * Black half transparent background
        EXPECTED: * The white close button 'X' (in the top left-hand corner)
        EXPECTED: * An image of the Connect logo (on the header sports ribbon menu)
        EXPECTED: * The arrow on the overlay image is aligned to the Connect logo on the top right (in the header ribbon menu)
        EXPECTED: * 'Scroll right in the menu' text (above the arrow)
        EXPECTED: * 'Bet in-shop & online with Connect' header (in the middle of the page)
        EXPECTED: * 'Collect your winnings instantly in cash and deposit in shop', 'Track and cash out your in-shop bets', 'Get exclusive promotions' texts
        EXPECTED: * Green button 'TAKE ME TO THE CONNECT HUB'
        EXPECTED: * 'Don’t show me this again' link
        """
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_for_connect_overlay(), msg='Connect overlay is not shown')

        self.__class__.connect_overlay = self.site.connect_overlay

        self.assertEqual(self.connect_overlay.css_property_value('background-color'), self.background_color,
                         msg=f'Background color {self.connect_overlay.css_property_value("background-color")} '
                             f'is not the same as expected {self.background_color}')
        self.assertTrue(self.connect_overlay.close_button.is_displayed(), msg='Close button is not displayed')
        self.assertTrue(self.connect_overlay.connect_icon.is_displayed(), msg='Connect logo is not displayed')
        self.assertTrue(wait_for_result(lambda: self.connect_overlay.swipe_arrow.is_displayed(), timeout=10),
                        msg='Swipe arrow is not displayed')
        self.assertEqual(self.connect_overlay.arrow_text, vec.retail.SCROLL_RIGHT_TEXT,
                         msg=f'Arrow text "{self.connect_overlay.arrow_text}" '
                             f'is not the same as expected "{vec.retail.SCROLL_RIGHT_TEXT}"')

        self.assertEqual(self.connect_overlay.navigate_to_connect.name, vec.retail.OVERLAY_BUTTON,
                         msg=f'Navigate to Connect button text "{self.connect_overlay.navigate_to_connect.name}" '
                             f'is not the same as expected "{vec.retail.OVERLAY_BUTTON}"')
        self.assertEqual(self.connect_overlay.do_not_show.name, vec.retail.OVERLAY_CLOSE,
                         msg=f'Do not show link text "{self.connect_overlay.do_not_show.name}" '
                             f'is not the same as expected "{vec.retail.OVERLAY_CLOSE}"')

    def test_002_verify_connect_overlay_text_corresponds_to_cms_configuration(self):
        """
        DESCRIPTION: Verify Connect overlay text corresponds to CMS Configuration
        EXPECTED: Following text itself and text style correspond to Static Block 'Connect Overlay' (Uri = connect-overlay-en-us):
        EXPECTED: Bet in-shop & online with Connect
        EXPECTED: Collect your winnings instantly in cash and deposit in shop', 'Track and cash out your in-shop bets', 'Get exclusive promotions
        """
        self.assertEqual(self.connect_overlay.overlay_text, self.cms_static_block_description.rstrip(),
                         msg=f'Overlay text "{self.connect_overlay.overlay_text}" '
                             f'is no the same as expected "{self.cms_static_block_description}"')
