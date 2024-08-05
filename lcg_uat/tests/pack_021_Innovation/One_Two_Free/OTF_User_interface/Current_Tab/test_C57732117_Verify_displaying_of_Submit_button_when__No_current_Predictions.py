import pytest
import tests
from requests import HTTPError
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import do_request


# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.one_two_free
@pytest.mark.other
@vtest
class Test_C57732117_Verify_displaying_of_Submit_button_when__No_current_Predictions(Common):
    """
    TR_ID: C57732117
    NAME: Verify displaying of 'Submit' button when - No current Predictions
    DESCRIPTION: This test case verifies displaying of 'Submit' button when - No current Predictions
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User Do not have prediction yet (GET /api/v1/prediction/{username}/{gameId} returns 404)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: user logged in
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username)
        bpp_token = self.get_local_storage_cookie_value_as_dict('OX.USER')['bppToken']
        self.assertTrue(bpp_token, msg='after login, token is not available')
        headers = {
            'Content-Type': 'application/json',
            'token': bpp_token
        }
        active_game_url = tests.settings.otf_url + f'{"initial-data/"}' + f'{username}'
        active_game = do_request(method='GET', url=active_game_url, headers=headers)
        active_game_id = active_game['activeGame']['id']

        url = tests.settings.otf_url + f'{"prediction/"}' + f'{username+"/"}' + f'{active_game_id}'
        self.navigate_to_page('1-2-free')
        try:
            do_request(method='GET', url=url, headers=headers)
        except HTTPError as e:
            if '404' in e.args[0]:
                self._logger.info("User Do not have prediction yet (GET /api/v1/prediction/{username}/{gameId} returns 404)")
            else:
                raise e

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: - 'Submit' button is **active**
        EXPECTED: - Arrows **displayed** on scores
        """
        one_two_free = self.site.one_two_free
        wait_for_result(lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed(),
                        timeout=15)
        one_two_free.one_two_free_welcome_screen.play_button.click()
        submit_button = wait_for_result(lambda:
                                        one_two_free.one_two_free_current_screen.submit_button.is_enabled(expected_result=True),
                                        timeout=15)
        self.assertTrue(submit_button, msg='"Submit Button" is not active')
        matches = list(one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
        for match in matches:
            score_switchers = match.score_selector_container.items
            for score_switcher in score_switchers:
                self.assertTrue(score_switcher.increase_score_up_arrow.is_displayed(),
                                msg=f'Upper arrow not displayed for "{match.name}".')
                self.assertTrue(score_switcher.decrease_score_down_arrow.is_displayed(),
                                msg=f'Down arrow not displayed for "{match.name}".')
                self.assertTrue(score_switcher.score,
                                msg=f'Score is not displayed for "{match.name}".')
