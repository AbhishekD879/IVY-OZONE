import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from crlat_siteserve_client.utils.exceptions import SiteServeException
from voltron.utils.waiters import wait_for_result
from voltron.utils.helpers import do_request


# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.reg156_fix
@pytest.mark.one_two_free
@pytest.mark.other
@vtest
class Test_C57732118_Verify_displaying_of_Submit_button_when__User_has_a_prediction(Common):
    """
    TR_ID: C57732118
    NAME: Verify displaying of 'Submit' button when - User has a prediction
    DESCRIPTION: This test case verifies displaying of 'Submit' button when - User has a prediction
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: 1. User is logged In
    PRECONDITIONS: 2. User have a prediction (GET /api/v1/prediction/{username}/{gameId} returns 200)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        Description: User should have prediction.
        """
        username = tests.settings.default_username
        self.site.login(username=username)
        home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
        tab_name = next((tab for tab in home_page_tabs if tab.upper() == '1-2-FREE'), None)
        home_page_tabs.get(tab_name).click()
        if not tab_name:
            raise SiteServeException(f'1-2-FREE tab is not available in {home_page_tabs}')
        self.site.wait_content_state_changed()
        one_two_free = self.site.one_two_free
        try:
            welcome_screen_play_here_button = wait_for_result(
                lambda: one_two_free.one_two_free_welcome_screen.play_button.is_displayed(), timeout=15)
            self.assertTrue(welcome_screen_play_here_button, msg='"PLAY HERE!" button is not available')
            one_two_free.one_two_free_welcome_screen.play_button.click()

            submit_button = wait_for_result(
                lambda: one_two_free.one_two_free_current_screen.submit_button.is_displayed(), timeout=15)
            self.assertTrue(submit_button, msg='"SUBMIT" button is not available')
            one_two_free.one_two_free_current_screen.submit_button.click()

            close_button = wait_for_result(lambda: one_two_free.one_two_free_you_are_in.close.is_displayed(),
                                           timeout=15)
            self.assertTrue(close_button, msg='"close button [X]" button is not available')
            one_two_free.one_two_free_you_are_in.close.click()

            home_page_tabs = self.site.home.tabs_menu.items_as_ordered_dict
            tab_name = next((tab for tab in home_page_tabs if tab.upper() == '1-2-FREE'), None)
            home_page_tabs.get(tab_name).click()
            if not tab_name:
                raise SiteServeException(f'1-2-FREE tab is not available in {home_page_tabs}')

        except VoltronException:
            self._logger.info("Play button not available, user already played 1-2-Free")

        bpp_token = self.get_local_storage_cookie_value_as_dict('OX.USER')['bppToken']
        headers = {
            'Content-Type': 'application/json',
            'token': bpp_token
        }
        active_game_url = tests.settings.otf_url + f'{"initial-data/"}' + f'{username}'
        active_game = do_request(method='GET', url=active_game_url, headers=headers)
        active_game_id = active_game['activeGame']['id']

        url = tests.settings.otf_url + f'{"prediction/"}' + f'{username + "/"}' + f'{active_game_id}'
        prediction_data = do_request(method='GET', url=url, headers=headers)
        self.assertEqual(prediction_data['userId'], username,
                         msg=f"User doesn't have a prediction (GET /api/v1/prediction/{username}/{active_game_id} returns 200)")

    def test_001_open_current_tab(self):
        """
        DESCRIPTION: Open 'Current Tab'
        EXPECTED: - 'Submit' button **NOT displayed**
        EXPECTED: - Arrows **NOT displayed** on scores switcher
        """
        one_two_free = self.site.one_two_free
        submit_button = wait_for_result(
            lambda: one_two_free.one_two_free_current_screen.has_submit_button(expected_result=False),
            timeout=5)
        self.assertFalse(submit_button, msg='"Submit Button" is displayed.')

        matches = list(one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())
        for match in matches:
            score_switchers = match.score_selector_container.items
            self.assertFalse(score_switchers, msg='Score containers are available with up and down arrows')
