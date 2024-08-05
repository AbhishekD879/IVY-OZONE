import pytest
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from time import sleep


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2  # yourcall not in the scope of roxane release
@pytest.mark.crl_hl
# @pytest.mark.crl_prod
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.your_call
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C1107936_YourCall_tab_static_block(BaseRacing):
    """
    TR_ID: C1107936
    NAME: YourCall tab static block
    DESCRIPTION: This test case verifies YourCall tab with static block and twitter button
    PRECONDITIONS: * The user is on Coral homepage
    PRECONDITIONS: * CMS contains configuration for the static block of YOURCALL tab (Your Call > Your Call Static Block > select "yourcall-racing" from the grid): html markup for text and "TWEET NOW" button with link
    """
    keep_browser_open = True

    change_html_markup = "<ul>\n<li>With <span style=\"color: #ff0000;\">#YourCall</span>, you call the shots." \
                         "</li>\n<li>Tweet your bet <strong>@Coral</strong> with " \
                         "<span style=\"color: #0abfa1;\">#YourCall</span>, and get your price.</li>\n" \
                         "</ul>\n<p><a class=\"btn full-width\" href=\"https://twitter.com/CoralAUTOMATION\" " \
                         "target=\"_blank\">TWEET NOW</a></p>"
    # TODO VOL-1120
    your_call_static_default_html = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.your_call_static_default_html:
            cms_config = cls.get_cms_config()
            cms_config.horse_racing_your_call_static_block(htmlMarkup=cls.your_call_static_default_html)
            cls.wait_block_to_change(cls.your_call_static_default_html)

    @classmethod
    def wait_block_to_change(cls, block_to_change, timeout: int = 120):
        """
        Wait current block to change using public api
        :param block_to_change: block that should be changed
        :param timeout: time to wait block to change
        """
        wait_for_result(lambda: next((block for block in cls.get_cms_config().get_your_call_static_block()
                                      if block['title'] == 'yourcall-racing'), None)['htmlMarkup'] == block_to_change,
                        name=f'Static block to change',
                        timeout=timeout)
        # We should have this sleep, because we have not one CDN and they are not updated in the same time
        sleep(60)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get Static Block parameters from CMS
        """
        static_block_params = self.cms_config.get_your_call_static_block()
        yc_racing_block = next((block for block in static_block_params if block['title'] == 'yourcall-racing'), None)
        if not yc_racing_block:
            raise CmsClientException('Your Call racing block is not present')
        if not yc_racing_block['htmlMarkup']:
            raise CmsClientException('Your Call racing block is not configured')
        if 'twitter' not in yc_racing_block['htmlMarkup']:
            raise CmsClientException('Your Call racing block is not configured to show twitter button')
        self.__class__.your_call_static_default_html = yc_racing_block['htmlMarkup']

    def test_001_navigate_on_the_horse_racing_tab(self):
        """
        DESCRIPTION: Navigate on the Horse racing tab
        EXPECTED: When the page is loaded YOURCALL tab is present
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        self.site.horse_racing.tabs_menu.click_button('YOURCALL')

    def test_002_click_on_the_yourcall_tab(self):
        """
        DESCRIPTION: Click on the YOURCALL tab
        EXPECTED: The tab is shown as per design:
        EXPECTED: * configurable (on CMS) static text ('#YourCall' is highlighted with different color)
        EXPECTED: * "TWEET NOW" button
        EXPECTED: https://mobile.twitter.com/Coral (configured on CMS)
        """
        selected_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(selected_tab, 'YOURCALL',
                         msg=f'Selected tab is "{selected_tab}" instead of "YOURCALL" tab')
        static_block = self.site.horse_racing.tab_content.accordions_list.static_block
        self.assertTrue(static_block, msg='Can not find Static Block')
        self.__class__.default_text_color = static_block.static_text.text_color_value
        # TODO VOL-2514 Default text color is configurable via CMS, remove hardcoded rgba text from settings.
        self.assertEqual(self.default_text_color, vec.colors.YOUR_CALL_DEFAULT_TEXT_COLOR,
                         msg=f'Default text color "{self.default_text_color}" is not equal to expected '
                             f'"{vec.colors.YOUR_CALL_DEFAULT_TEXT_COLOR}"')

        self.assertTrue(static_block.tweet_now_button, msg='Can not find "Tweet Now" button')
        self.assertEqual(static_block.tweet_now_button.href, 'https://twitter.com/Coral')

    def test_003_change_default_cms_config(self):
        """
        DESCRIPTION: Change default cms config and reload page
        """
        self.cms_config.horse_racing_your_call_static_block(htmlMarkup=self.change_html_markup)
        self.wait_block_to_change(self.change_html_markup)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

    def test_004_verify_that_changes_were_applied(self):
        """
        DESCRIPTION: Verify that changes were applied
        EXPECTED: The tab is shown as per design:
        EXPECTED: * configurable (on CMS) static text ('#YourCall' is highlighted with different color)
        EXPECTED: * "TWEET NOW" button
        EXPECTED: https://mobile.twitter.com/CoralAUTOMATION (configured on CMS)
        """
        self.__class__.static_block = self.site.horse_racing.tab_content.accordions_list.static_block
        self.assertTrue(self.static_block, msg='Can not find Static Block')
        changed_text_color = self.static_block.static_text.css_property_value
        self.assertNotEqual(changed_text_color, self.default_text_color)
        self.assertEqual(self.static_block.tweet_now_button.href, 'https://twitter.com/CoralAUTOMATION')
