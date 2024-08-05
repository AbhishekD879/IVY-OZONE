import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.Common import Common
from json import JSONDecodeError


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.frequent_blocker
@vtest
class Test_C59549195_Verify_error_handling_for_failed_EventToOutcomeForClass_request_on_SLP_for_Tier_2_Sports(Common):
    """
    TR_ID: C59549195
    NAME: Verify error handling for failed /EventToOutcomeForClass request on SLP for Tier 2 Sports
    DESCRIPTION: This test case verifies error handling for failed /EventToOutcomeForClass request on on 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs for different Sports
    PRECONDITIONS: 1. https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs - list of Tier 1 and Tier 2 sports.
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 2 and Tier 2 sport Outright(Golf, Cycling, Hurling, Motorbikes).
    PRECONDITIONS: 3. Go to Dev Tools > Network > enter 'simpleFilter' in search field > EventToOutcomeForClass.
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    coral_tabs_list = [vec.sb.TABS_NAME_TODAY.upper(), vec.sb.TABS_NAME_TOMORROW.upper(),
                       vec.sb.TABS_NAME_FUTURE.upper()]
    lads_tabs_list = [vec.sb.TABS_NAME_TODAY.title(), vec.sb.TABS_NAME_TOMORROW.title(),
                      vec.sb.TABS_NAME_FUTURE.title()]
    lads_domain_url = vec.sb.LADS_PROD_ENV_DOMAIN_URL if tests.settings.backend_env == 'prod' else vec.sb.LADS_TST_ENV_DOMAIN_URL
    coral_domain_url = vec.sb.CORAL_PROD_ENV_DOMAIN_URL if tests.settings.backend_env == 'prod' else vec.sb.CORAL_TST_ENV_DOMAIN_URL

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_001_navigate_to_to_matchesmobile_todaytomorrowfuturedesktop_tabs_on_any_sport_landing_page_with_tier_2_sport_configuration(self):
        """
        DESCRIPTION: Navigate to to 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs on any Sport Landing page with Tier 2 Sport configuration
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_boxing_event()
            self.ob_config.add_volleyball_event_to_austrian_league()
        self.navigate_to_page('sport/boxing')
        self.site.wait_content_state_changed()
        tabs_menu = self.site.boxing.tabs_menu
        if self.device_type != 'mobile':
            date_tabs = self.site.boxing.date_tab.items_names
            self.assertListEqual(date_tabs, self.coral_tabs_list if self.brand == 'bma' else self.lads_tabs_list,
                                 msg=f'Actaul tabs list: "{date_tabs}" is not same as Expected tabs: "{self.coral_tabs_list if self.brand == "bma" else self.lads_tabs_list}"')
        else:
            default_tab = tabs_menu.current
            self.assertIn(default_tab.upper(), [vec.sb.TABS_NAME_FIGHTS.upper(), vec.sb.TABS_NAME_COMPETITIONS.upper(), vec.sb.TABS_NAME_OUTRIGHTS.upper()],
                          msg=f'Actual default tab: "{default_tab.upper()}" is not same as Expected tab: "{vec.sb.TABS_NAME_FIGHTS.upper()}"')
            tabs_menu.items_as_ordered_dict.get('COMPETITIONS').click()  # Sometimes inplay events are present under matches/fights tab
            self.site.wait_content_state_changed()

    def test_002_block_eventtooutcomeforclass_request_in_chrome_dev_tools___request_blocking_and_refresh_the_page(self):
        """
        DESCRIPTION: Block EventToOutcomeForClass request in Chrome Dev tools -> Request blocking and refresh the page
        EXPECTED: * "Oops! We are having trouble loading this page. Please check your connection" message is shown
        EXPECTED: * "TRY AGAIN" button is displayed under the error message and is clickable
        """
        sleep(3)
        self.block_unblock_request_domain(cmd='Network.setBlockedURLs', params={"urls": [self.coral_domain_url if self.brand == 'bma' else self.lads_domain_url]})
        self.block_unblock_request_domain(cmd='Network.enable', params={})
        self.device.refresh_page()
        self.site.wait_content_state_changed()
        error = self.site.sports_page.tab_content.has_opps_error_message()
        self.assertTrue(error, msg=f'"{vec.sb.OOPS_ERROR_MESSAGE}" is not displayed')
        error_message = self.site.sports_page.tab_content.opps_error_message.text
        self.assertEqual(error_message, vec.sb.OOPS_ERROR_MESSAGE,
                         msg=f'Actual Oops message: "{error_message}" is not same as Expected message: "{vec.sb.OOPS_ERROR_MESSAGE}"')
        self.__class__.try_again_button = self.site.sports_page.tab_content.try_again_button
        self.assertTrue(self.try_again_button.is_enabled(), msg='"TRY AGAIN" button is not clickable')

    def test_003_unblock_eventtooutcomeforclass_request_in_chrome_dev_tools___request_blocking_and_press_on_try_again_button(self):
        """
        DESCRIPTION: Unblock EventToOutcomeForClass request in Chrome Dev tools -> Request blocking and press on 'Try Again' button
        EXPECTED: * EventToOutcomeForClass request is resent
        EXPECTED: * EventToOutcomeForClass request is not failed and EventToOutcomeForClass data is received
        EXPECTED: * Error message and 'Try Again' button are no longer displayed
        """
        self.block_unblock_request_domain(cmd='Network.disable', params={})
        sleep(3)
        self.try_again_button.click()
        error = self.site.sports_page.tab_content.has_opps_error_message()
        if error:
            self.device.refresh_page()
            error = self.site.sports_page.tab_content.has_opps_error_message()
        self.assertFalse(error, msg=f'Opps message: "{vec.sb.OOPS_ERROR_MESSAGE}" is still displayed')
        response_url = self.get_response_url('EventToOutcomeForClass')
        self.assertTrue(response_url, msg='EventToOutcomeForClass data is not received after unblocking request')
