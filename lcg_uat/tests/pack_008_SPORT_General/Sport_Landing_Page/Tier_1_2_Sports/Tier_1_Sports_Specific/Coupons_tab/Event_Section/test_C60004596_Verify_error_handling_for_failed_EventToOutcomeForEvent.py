import pytest
import tests
import voltron.environments.constants as vec
from json import JSONDecodeError
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request
from tests.base_test import vtest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60004596_Verify_error_handling_for_failed_EventToOutcomeForEvent(BaseSportTest):
    """
    TR_ID: C60004596
    NAME: Verify error handling for failed /EventToOutcomeForEvent
    DESCRIPTION: This test case verifies error handling for failed /EventToOutcomeForEvent on the coupon details page
    PRECONDITIONS: Go to the sports landing page
    PRECONDITIONS: Open Coupon tab (ACCA)
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    lads_domain_url = vec.sb.LADS_PROD_ENV_DOMAIN_URL if tests.settings.backend_env == 'prod' else vec.sb.LADS_TST_ENV_DOMAIN_URL
    coral_domain_url = vec.sb.CORAL_PROD_ENV_DOMAIN_URL if tests.settings.backend_env == 'prod' else vec.sb.CORAL_TST_ENV_DOMAIN_URL
    autotest_coupon = vec.siteserve.EXPECTED_COUPON_NAME

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

    def test_001_open_any_coupon_details_page(self):
        """
        DESCRIPTION: Open any coupon details page
        EXPECTED: Events are displayed
        """
        if self.brand == 'bma':
            self.__class__.expected_tab = self.expected_sport_tabs.accumulators
        else:
            self.__class__.expected_tab = self.expected_sport_tabs.accas
        if tests.settings.backend_env != 'prod':
            event_matches_params = self.ob_config.add_autotest_premier_league_football_event()
            market_short_name = self.ob_config.football_config. \
                autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
            event_coupons_id = self.ob_config.market_ids[event_matches_params.event_id][market_short_name]
            self.ob_config.add_event_to_coupon(market_id=event_coupons_id, coupon_name=self.autotest_coupon)
            if self.brand == 'bma':
                self.expected_tab = self.expected_sport_tabs.accumulators
            else:
                self.expected_tab = self.expected_sport_tabs.coupons

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name=vec.sb.FOOTBALL)

        tabs_menu = self.site.football.tabs_menu
        if self.expected_tab in tabs_menu.items_names:
            tabs_menu.click_button(self.expected_tab)
        else:
            raise CmsClientException(f'{self.expected_tab} is not configured in CMS')
        self.site.wait_content_state_changed()
        coupons = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupons, msg=f'No coupons available on "{self.expected_tab}" tab')
        events = list(coupons.values())[0].items_as_ordered_dict
        if not events:
            raise SiteServeException('No events are available')

    def test_002_block_eventtooutcomeforevent_request_in_chrome_dev_tools___request_blocking_and_refresh_the_page(self):
        """
        DESCRIPTION: Block EventToOutcomeForEvent request in Chrome Dev tools -> Request blocking and refresh the page
        EXPECTED: - 'Oops! We are having trouble loading this page. Please check your connection' message with "TRY AGAIN" buttons are displayed
        """
        sleep(3)
        self.block_unblock_request_domain(cmd='Network.setBlockedURLs', params={
            "urls": [self.coral_domain_url if self.brand == 'bma' else self.lads_domain_url]})
        self.block_unblock_request_domain(cmd='Network.enable', params={})
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=5)
        error = self.site.sports_page.tab_content.has_opps_error_message()
        self.assertTrue(error, msg=f'"{vec.sb.OOPS_ERROR_MESSAGE}" is not displayed')
        error_message = self.site.sports_page.tab_content.opps_error_message.text
        self.assertEqual(error_message, vec.sb.OOPS_ERROR_MESSAGE,
                         msg=f'Actual Oops message: "{error_message}" is not same as Expected message: "{vec.sb.OOPS_ERROR_MESSAGE}"')
        self.__class__.try_again_button = self.site.sports_page.tab_content.try_again_button
        self.assertTrue(self.try_again_button.is_enabled(), msg='"TRY AGAIN" button is not clickable')

    def test_003_unblock_eventtooutcomeforevent_request_in_chrome_dev_tools___request_blocking_and_refresh_the_page(self):
        """
        DESCRIPTION: Unblock EventToOutcomeForEvent request in Chrome Dev tools -> Request blocking and refresh the page
        EXPECTED: - EventToOutcomeForEvent request is resent
        EXPECTED: - EventToOutcomeForEvent request is not failed and
        EXPECTED: - EventToOutcomeForEvent data is received
        EXPECTED: - 'Oops! We are having trouble loading this page. Please check your connection' message with "TRY AGAIN" buttons are no longer displayed
        EXPECTED: - Events loaded and displayed on the page
        """
        self.block_unblock_request_domain(cmd='Network.disable', params={})
        sleep(3)
        self.try_again_button.click()
        error = self.site.sports_page.tab_content.has_opps_error_message()
        if error:
            self.device.refresh_page()
            error = self.site.sports_page.tab_content.has_opps_error_message()
        self.assertFalse(error, msg=f'Opps message: "{vec.sb.OOPS_ERROR_MESSAGE}" is still displayed')
        try_again_button = self.site.sports_page.tab_content.try_again_button
        self.assertFalse(try_again_button, msg='TRY AGAIN button is still displayed')
        coupons = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupons, msg=f'No coupons available on "{self.expected_tab}" tab')
        events = list(coupons.values())[0].items_as_ordered_dict
        if not events:
            raise SiteServeException('No events are available')

        if not list(coupons.values())[0].is_expanded():
            list(coupons.values())[0].click()
            self.site.wait_content_state_changed(timeout=5)
        sleep(3)
        response_url = self.get_response_url('EventToOutcomeFor')
        self.assertTrue(response_url, msg='EventToOutcomeForEvent data is not received after unblocking request')
        response = do_request(method='GET', url=response_url)
        self.assertTrue(response, msg='No response received for the "EventToOutcomeForEvent" call')
