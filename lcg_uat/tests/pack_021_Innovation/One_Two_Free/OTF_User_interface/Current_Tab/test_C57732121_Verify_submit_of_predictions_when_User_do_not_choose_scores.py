import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_result, wait_for_haul
from requests import HTTPError


# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.mobile_only
@pytest.mark.one_two_free
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732121_Verify_submit_of_predictions_when_User_do_not_choose_scores(Common):
    """
    TR_ID: C57732121
    NAME: Verify submit of predictions when User do not choose scores
    DESCRIPTION: This test case verifies submit of predictions when User do not chose scores
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User Do not have prediction yet (GET /api/v1/prediction/{username}/{gameId} returns 404)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. User is logged In
        PRECONDITIONS: 2. User Do not have prediction yet (GET /api/v1/prediction/{username}/{gameId} returns 404)
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('Homepage')
        self.site.login(self.username)
        bpp_token = self.get_local_storage_cookie_value_as_dict('OX.USER')['bppToken']
        self.assertTrue(bpp_token, msg='after login, token is not available')
        self.__class__.headers = {
            'Content-Type': 'application/json',
            'token': bpp_token
        }
        active_game_url = tests.settings.otf_url + f'{"initial-data/"}' + f'{self.username}'
        active_game = do_request(method='GET', url=active_game_url, headers=self.headers)
        self.__class__.active_game_id = active_game['activeGame']['id']

        url = tests.settings.otf_url + f'{"prediction/"}' + f'{self.username + "/"}' + f'{self.active_game_id}'
        self.navigate_to_page('1-2-free')
        self.assertTrue(self.site.one_two_free.one_two_free_welcome_screen.is_displayed(timeout=5),
                        msg='1-2-Free welcome screen is not shown')
        try:
            do_request(method='GET', url=url, headers=self.headers)
        except HTTPError as e:
            if '404' in e.args[0]:
                self._logger.info(
                    "User Do not have prediction yet (GET /api/v1/prediction/{username}/{gameId} returns 404)")
            else:
                raise e

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: 'Current Tab' is successfully opened
        """
        self.__class__.one_two_free = self.site.one_two_free
        one_two_free_welcome_screen = wait_for_result(lambda: self.one_two_free.one_two_free_welcome_screen.play_button.is_displayed(), timeout=10)
        self.assertTrue(one_two_free_welcome_screen)
        self.one_two_free.one_two_free_welcome_screen.play_button.click()

    def test_002_do_not_choose_scores_and_tap_on_submit_button(self):
        """
        DESCRIPTION: Do NOT choose scores and Tap on 'Submit' button
        EXPECTED: FE should send POST /api/v1/prediction with Game ID and User ID and body (see Swagger for actual request example)
        EXPECTED: **where scores is 0-0**
        """
        submit_button = wait_for_result(lambda:
                                        self.one_two_free.one_two_free_current_screen.submit_button.is_enabled(
                                            expected_result=True),
                                        timeout=15)
        self.assertTrue(submit_button, msg='"Submit Button" is not active')
        self.one_two_free.one_two_free_current_screen.submit_button.click()
        wait_for_haul(2)
        url = tests.settings.otf_url + f'{"prediction/"}' + f'{self.username + "/"}' + f'{self.active_game_id}'
        otf_request = do_request(method='GET', url=url, headers=self.headers)
        for pre in otf_request['eventPredictions']:
            actual_predictions = pre['predictionScores']
            self.assertListEqual(actual_predictions, [0, 0],
                                 msg = f'Actual duration list  "{actual_predictions}" is not matching with '
                                       f'expected list "{[0, 0]}"')
