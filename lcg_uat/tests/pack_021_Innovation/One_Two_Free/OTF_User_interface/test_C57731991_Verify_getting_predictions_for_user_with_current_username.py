import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.utils.helpers import do_request
from json import JSONDecodeError


# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.one_two_free
@pytest.mark.other
@pytest.mark.reg157_fix
@vtest
class Test_C57731991_Verify_getting_predictions_for_user_with_current_username(Common):
    """
    TR_ID: C57731991
    NAME: Verify getting predictions for user with current 'username'
    DESCRIPTION: This test case verifies getting predictions for user with current 'username'
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE predictor and win £150' is available on Homepage or Football landing page
    PRECONDITIONS: 3. User made prediction previously for this Active Game
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    headers = {
        'Content-Type': 'application/json',
        'token': None
    }

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

    def test_001_tap_on_play_1_2_free_predictor_and_win_150_quick_link(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE predictor and win £150' quick link
        EXPECTED: User successfully navigated to 1-2-Free
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        event_hub_one_two_free_tab_name = next(
            (tab.upper() for tab in home_page_tabs if tab.upper() == '1-2-FREE'), None)
        self.assertTrue(event_hub_one_two_free_tab_name, msg='1-2-free tab is not available in home page tabs')
        home_page_tabs.get(event_hub_one_two_free_tab_name).click()

        self.site.wait_content_state_changed()
        try:
            one_two_free = self.site.one_two_free
        except VoltronException:
            self.navigate_to_page('1-2-free')
            one_two_free = self.site.one_two_free
        try:
            wait_for_result(lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed(),
                            timeout=15)
            one_two_free.one_two_free_welcome_screen.play_button.click()
            wait_for_result(lambda: one_two_free.one_two_free_current_screen.submit_button.is_displayed(), timeout=15)
            one_two_free.one_two_free_current_screen.submit_button.click()
            wait_for_result(lambda: one_two_free.one_two_free_you_are_in.close.is_displayed(), timeout=15)
            one_two_free.one_two_free_you_are_in.close.click()
        except VoltronException:
            self._logger.info("Play button not available, user already played 1-2-Free")

    def test_002_open_browser_network__xhr_requests_eg_httpsotf_hlv0coralsportsnonprodcloudladbrokescoralcomapiv1initial_datausername(self):
        """
        DESCRIPTION: Open browser Network > XHR requests (e.g. https://otf-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/initial-data/'username')
        EXPECTED: GET request for predictions exits with valid keys:
        EXPECTED: - userId
        EXPECTED: - game Id
        EXPECTED: - eventPredictions
        EXPECTED: - customerId
        EXPECTED: - resulted
        """
        bpp_token = self.get_local_storage_cookie_value_as_dict('OX.USER')['bppToken']
        self.headers['token'] = bpp_token
        url = tests.settings.otf_url + f'{"initial-data/"}' + f'{self.username}'
        response_url = self.get_response_url(self.username)
        self.assertEqual(response_url, url,
                         msg=f'Actual URL : "{response_url}" is not same as'
                             f'Expected URL: "{url}"')
        otf_request = do_request(method='GET', url=url, headers=self.headers)
        prediction = otf_request['prediction']
        self.assertIn('userId', prediction.keys(),
                      msg='"userId" is not present in predictions')
        self.assertIn('gameId', prediction.keys(),
                      msg='"gameId" is not present in predictions')
        self.assertIn('eventPredictions', prediction.keys(),
                      msg='"eventPredictions" is not present in predictions')
        self.assertIn('customerId', prediction.keys(),
                      msg='"customerId" is not present in predictions')
        self.assertIn('resulted', prediction.keys(),
                      msg='"resulted" is not present in predictions')
