import pytest
import tests
import voltron.environments.constants as vec
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod   # Cannot grant odds boost on prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C2555531_Verify_Log_in_with_user_that_has_configured_new_Odds_Boost_notification_token(BaseUserAccountTest):
    """
    TR_ID: C2555531
    NAME: Verify Log in with user that has configured new Odds Boost notification token
    DESCRIPTION: This test case verifies Log in with user that has configured new Odds Boost notification token
    PRECONDITIONS: Enable "Odds Boost" Feature Toggle in CMS
    PRECONDITIONS: Generate for user Odds boost token in TST2 Backoffice
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: 'Allow User To Toggle Visibility option' is enabled in CMS > Odds Boost
    PRECONDITIONS: User has a new Odds Boosts token. Token is NOT expired
    """
    keep_browser_open = True
    username = tests.settings.betplacement_user

    def test_001_login_to_application(self):
        """
        DESCRIPTION: Login to application
        EXPECTED: * User is logged in successfully
        EXPECTED: * The "Odds Boost" token notification is displayed
        """
        # self.ob_config.grant_odds_boost_token(self.username, token_value=1)
        self.site.login(username=self.username, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        self.__class__.odd_boost_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=40)
        self.assertTrue(self.odd_boost_dialog,
                        msg='odd boost dialog is not shown for user with odd boost: "%s"')

    def test_002_verify_pop_up_dialog_elements(self):
        """
        DESCRIPTION: Verify pop-up dialog elements
        EXPECTED: It should contain the following information:
        EXPECTED: - Hardcoded image (odds boost logo)
        EXPECTED: - Static header text: 'Odds Boost'
        EXPECTED: - Hardcoded content text: 'You Have X Odds Boosts Available' (X is a value specific to the user as fetched on login)
        EXPECTED: - Hardcoded compliance text: '18+. Terms Apply'
        EXPECTED: - 'SHOW MORE' button
        EXPECTED: - 'OK, THANKS' close button
        EXPECTED: - 'X' close button
        EXPECTED: - Check-box - "Don’t show this again"
        EXPECTED: (updated for OX 105 design)
        EXPECTED: ![](index.php?/attachments/get/115670351)
        EXPECTED: ![](index.php?/attachments/get/115670352)
        """
        odd_boost_logo = self.odd_boost_dialog.odd_boost_logo
        self.assertTrue(odd_boost_logo, msg='Odd boost logo is not appearing in odd boost token notification')
        actual_odd_boost_header_text = self.odd_boost_dialog.name
        expected_odd_boost_header_text = vec.odds_boost._tokens_info_dialog_title.upper() if self.brand == 'bma' else vec.odds_boost._tokens_info_dialog_title
        self.assertEqual(actual_odd_boost_header_text, expected_odd_boost_header_text,
                         msg=f'Incorrect odd boost header text, actual: "{actual_odd_boost_header_text}" and expected "{expected_odd_boost_header_text}"')
        odds_boost_content = self.odd_boost_dialog.description.split('\n')
        self.assertTrue(odds_boost_content, msg='Odds boost content is not displayed')
        terms_available = vec.odds_boost._tokens_info_dialog_terms if self.brand == 'bma' else vec.odds_boost._tokens_info_dialog_terms.replace('Apply', 'Available').replace('.', ',')
        self.assertIn(terms_available, odds_boost_content,
                      msg=f'Incorrect terms available text, actual text is "{odds_boost_content}" and expected text is "{terms_available}"')
        show_more_btn = self.odd_boost_dialog.show_more_button.is_displayed()
        self.assertTrue(show_more_btn, msg='Show more button is not displaying')
        thanks_link = self.odd_boost_dialog.thanks_link.is_displayed()
        self.assertTrue(thanks_link, msg='thanks link is not displaying')
        close_btn = self.odd_boost_dialog.header_object.close_button.is_displayed()
        self.assertTrue(close_btn, msg='close button is not displaying')

    def test_003_tap_x_button_on_the_notification_or_ok_thanks_button_or_tap_outside_the_content_odds_boost_notification_area(self):
        """
        DESCRIPTION: Tap "X" button on the notification (or "OK THANKS" button, or tap outside the content "Odds Boost" notification area)
        EXPECTED: * The pop up is closed
        EXPECTED: * The respective underlying page is displayed
        EXPECTED: * Odds Boost token with added offer ID is saved in Local Storage (Developer Tools -> Application -> Local Storage -> OX.oddsBoost)
        """
        self.odd_boost_dialog.header_object.close_button.click()
        expected_url = f'https://{tests.HOSTNAME}'
        actual_url = self.device.get_current_url()
        self.softAssert(self.assertIn, expected_url, actual_url,
                        msg=f'Failed to Redirected target Uri "{expected_url}" actual "{actual_url}"')

    def test_004_log_out_from_application(self):
        """
        DESCRIPTION: Log Out from application
        EXPECTED: User is logged out
        """
        self.device.refresh_page()
        self.site.wait_content_state('homepage')
        self.site.logout()

    def test_005__clear_storage_dev_tools___application___clear_storage_repeat_steps_1_2(self):
        """
        DESCRIPTION: * Clear Storage (Dev Tools -> Application -> Clear storage)
        DESCRIPTION: * Repeat Steps 1-2
        EXPECTED: Results are the same
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.driver.implicitly_wait(5)

        self.test_001_login_to_application()
        self.test_002_verify_pop_up_dialog_elements()

    def test_006_tap_show_more_button(self):
        """
        DESCRIPTION: Tap 'SHOW MORE' button
        EXPECTED: * The pop-up is closed
        EXPECTED: * The user is navigated to odds boost page
        """
        self.odd_boost_dialog.show_more_button.click()
        self.assertFalse(self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST),
                         msg='odd boost dialog is shown, exepected- odd boost dailog should not appear')
        actual_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}/oddsboost'
        self.assertEqual(actual_url, expected_url,
                         msg=f'User is re-directed incorrect URL, actual url is "{actual_url}", expected url is "{expected_url}"')
