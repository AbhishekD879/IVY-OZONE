import pytest
import tests
from time import sleep
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.one_two_free
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C57732126_Verify_closing_You_are_in_page(Common):
    """
    TR_ID: C57732126
    NAME: Verify closing 'You are in' page
    DESCRIPTION: This test case verifies closing 'You are in' page
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: for Qubit version (deprecated) https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: for Oxygen version: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: 1. User is logged In
    """
    keep_browser_open = True

    def test_001_open_current_tab_and_submit_a_prediction(self):
        """
        DESCRIPTION: Open 'Current Tab' and submit a prediction
        EXPECTED: - Prediction is successfully saved
        EXPECTED: - 'You are in' page appear
        """
        username = tests.settings.default_username
        self.site.login(username)
        self.navigate_to_page('1-2-free')
        self.__class__.one_two_free = self.site.one_two_free
        wait_for_result(lambda: self.one_two_free.one_two_free_welcome_screen.play_button.is_displayed(),
                        timeout=15)
        self.one_two_free.one_two_free_welcome_screen.play_button.click()
        submit_button = wait_for_result(lambda:
                                        self.one_two_free.one_two_free_current_screen.submit_button.is_enabled(expected_result=True),
                                        timeout=15)
        match = list(self.one_two_free.one_two_free_current_screen.items_as_ordered_dict.values())[0]
        score_switcher = list(match.score_selector_container.items)[0]
        score_switcher.increase_score_up_arrow.click()
        sleep(2)
        actual_score = score_switcher.score
        self.assertEqual(actual_score, '1',
                         msg=f'Actual Score "{actual_score}" is not the same as expected "1"')

        self.assertTrue(submit_button, msg='"Submit Button" is not active')
        self.one_two_free.one_two_free_current_screen.submit_button.click()
        self.__class__.one_two_free_you_are_in = self.one_two_free.one_two_free_you_are_in
        self.assertTrue(self.one_two_free_you_are_in, msg=f'"1-2 free you are in" is not displayed')

    def test_002_navigate_away_or_close_x_you_are_in_page(self):
        """
        DESCRIPTION: Navigate away or Close [x] 'You ar in' page
        EXPECTED: - App closed
        """
        self.assertTrue(self.one_two_free_you_are_in.close, msg='"Close Button" is not active')
        self.one_two_free_you_are_in.close.click()
        self.site.wait_content_state('homepage')
