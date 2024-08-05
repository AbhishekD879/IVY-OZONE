import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_014_Module_Selector_Ribbon.Private_Markets.BasePrivateMarketsTest import BasePrivateMarketsTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import cleanhtml


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.private_markets
@pytest.mark.homepage
@pytest.mark.promotions_banners_offers
@pytest.mark.static_block
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C29433_Private_Markets_Terms_and_Conditions_page(BasePrivateMarketsTest, BaseUserAccountTest):
    """
    TR_ID: C29433
    NAME: 'Private Markets Terms and Conditions' page
    DESCRIPTION: This test case verifies 'Private Markets Terms and Conditions' page
    DESCRIPTION: 'Private Markets Terms and Conditions' page is CMS configurable
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User should be eligible for one or more private enhanced market offers
    PRECONDITIONS: Private market offers should be active (not expired)
    PRECONDITIONS: To load CMS for Private Markets use Static Block "Private Markets Terms And Conditions"
    PRECONDITIONS: (https://CMS_endpoint/keystone/static-blocks)accountFreebets?freebetTokenType=ACCESS
    PRECONDITIONS: request is used in order to get a private market for particular user after a page refresh or
    PRECONDITIONS: navigating to Homepage from any other page and user request is used to get private market after
    PRECONDITIONS: login(open Dev tools -> Network ->XHR tab) CMS_endpoint can be found using devlog
    """
    keep_browser_open = True
    is_enabled = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if not cls.is_enabled and tests.settings.cms_env != 'prd0':
            cms = cls.get_cms_config()
            cms.enable_static_block(uri=cms.constants.PRIVATE_MARKETS_TC_STATIC_BLOCK_URI, enable=False)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Places a bet again on the event which triggers Private Market appearance
        EXPECTED: Bet is placed successfully and Bet Receipt is shown
        """
        self.__class__.is_enabled = self.cms_config.is_static_block_enabled(
            uri=self.cms_config.constants.PRIVATE_MARKETS_TC_STATIC_BLOCK_URI)
        if not self.is_enabled:
            if tests.settings.cms_env != 'prd0':
                self.cms_config.enable_static_block(uri=self.cms_config.constants.PRIVATE_MARKETS_TC_STATIC_BLOCK_URI)
            else:
                raise CmsClientException(f'Static block with uri "{self.cms_config.constants.PRIVATE_MARKETS_TC_STATIC_BLOCK_URI}" '
                                         f'is disabled, cannot execute the test on prod endpoints')
        static_block = self.cms_config.get_static_block(uri=self.cms_config.constants.PRIVATE_MARKETS_TC_STATIC_BLOCK_URI)
        self.__class__.cms_static_block_description = \
            cleanhtml(static_block['htmlMarkup']).replace('\r\n', '\n').replace('\n\n\n', '\n').rstrip().strip()
        username = tests.settings.user_with_private_market
        self.site.login(username=username, async_close_dialogs=False)
        self.trigger_private_market_appearance(user=username,
                                               expected_market_name=self.private_market_name)

    def test_001_open_oxygen_application(self):
        """
        DESCRIPTION: Open Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='HomePage')

    def test_002_click_on_terms_and_conditions_link_on_your_enhanced_markets_tab_section(self):
        """
        DESCRIPTION: Click/Tap on 'Terms and Conditions' link on 'Your Enhanced Markets' tab/section
        EXPECTED:  'Private Markets Terms and Conditions' page is opened with
        EXPECTED:  'Private Markets Terms and Conditions' header and 'Back' button
        EXPECTED:  Page content is displayed correctly (according to CMS configurations in 'Static Blocks')
        """
        private_market_section = self.site.home.get_module_content(self.expected_sport_tabs.private_market)
        private_market_section.terms_and_conditions.click()
        self.device.driver.implicitly_wait(5)
        self.site.wait_content_state(state_name='PrivateMarketsTermsAndConditionsPage')
        private_markets_page = self.site.private_markets_terms_and_conditions_page
        header_line = private_markets_page.header_line.page_title.text
        self.assertEqual(header_line.upper(), vec.sb.PRIVATE_MARKETS_TERMS_AND_CONDITIONS.upper(),
                         msg=f'Actual page header: "{header_line.upper()}", '
                             f'expected: "{vec.sb.PRIVATE_MARKETS_TERMS_AND_CONDITIONS.upper()}"')
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.has_back_button, msg='"Back" button not found')
        self.maxDiff = None
        ui_text = private_markets_page.static_block.text.strip()
        self.assertIn(self.cms_static_block_description.replace('&', 'and').upper(),
                      ui_text.replace('&', 'and').upper(),
                      msg=f'UI text: \n"{ui_text}"\n\nis not same as expected from CMS:'
                          f' \n"{self.cms_static_block_description}"\n')

    def test_003_click_tap_on_back_button(self):
        """
        DESCRIPTION: Click/Tap on 'Back' button
        EXPECTED: User navigates back to previous page
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='HomePage')
