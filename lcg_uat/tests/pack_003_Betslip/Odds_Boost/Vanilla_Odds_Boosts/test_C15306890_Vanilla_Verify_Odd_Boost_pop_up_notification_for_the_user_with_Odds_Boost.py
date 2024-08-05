import pytest
import tests
import voltron.environments.constants as vec
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't grant odds boost tokens on prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C15306890_Vanilla_Verify_Odd_Boost_pop_up_notification_for_the_user_with_Odds_Boost(BaseUserAccountTest):
    """
    TR_ID: C15306890
    NAME: [Vanilla] Verify 'Odd Boost' pop-up notification for the user with Odds Boost
    DESCRIPTION: This test case verifies visibility of 'Odd Boost' pop-up notification
    PRECONDITIONS: User has an Odds Boosts token. Token is NOT expired
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    """
    keep_browser_open = True

    def login_grant_odd(self):
        username = self.gvc_wallet_user_client.register_new_user().username
        self.ob_config.grant_odds_boost_token(username)
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('homepage')
        self.site.login(username=username, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        self.__class__.odd_boost_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=40)
        self.assertTrue(self.odd_boost_dialog,
                        msg='odd boost dialog is not shown for user with odd boost: "%s"' % username)

    def test_001_login_into_application(self):
        """
        DESCRIPTION: Login into application
        EXPECTED: User is logged in successfully
        EXPECTED: The "Odds Boost" token notification is displayed
        """
        self.__class__.odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if self.odds_boost is None:
            self.cms_config.update_odds_boost_config(enabled=True)
        self.login_grant_odd()

    def test_002_verify_pop_up_dialog_elements(self):
        """
        DESCRIPTION: Verify pop-up dialog elements
        EXPECTED: It should contain the following information:
        EXPECTED: - Hardcoded image (odds boost logo)
        EXPECTED: - Static header text: 'Odds Boost'
        EXPECTED: - Hardcoded content text: 'You have X Odds Boost available' (X is a value specific to the user as fetched on login)
        EXPECTED: - Hardcoded compliance text: '18+. Terms Apply'
        EXPECTED: - 'SHOW MORE' button
        EXPECTED: - 'OK, THANKS' close button
        EXPECTED: - 'X' close button
        EXPECTED: - Checkbox - "Don’t show this again" is displayed if enabled in CMS > Odds Boost
        EXPECTED: ![](index.php?/attachments/get/36667)
        """
        odd_boost_logo = self.odd_boost_dialog.odd_boost_logo
        self.assertTrue(odd_boost_logo, msg='Odd boost logo is not appearing in odd boost token notification')
        actual_odd_boost_header_text = self.odd_boost_dialog.name
        expected_odd_boost_header_text = vec.odds_boost._tokens_info_dialog_title.upper() if self.brand == 'bma' else vec.odds_boost._tokens_info_dialog_title
        self.assertEqual(actual_odd_boost_header_text, expected_odd_boost_header_text,
                         msg=f'Incorrect odd boost header text, actual: "{actual_odd_boost_header_text}" and expected "{expected_odd_boost_header_text}"')
        odds_boost_content = self.odd_boost_dialog.description.split('\n')
        self.assertIn(vec.odds_boost.AVAIALABLE_ODD_BOOST, odds_boost_content,
                      msg=f'Actual odd boost content text: "{odds_boost_content}" is not equal with the'
                          f'Expected content: "{vec.odds_boost.AVAIALABLE_ODD_BOOST}"')
        terms_available = vec.odds_boost._tokens_info_dialog_terms if self.brand == 'bma' else vec.odds_boost._tokens_info_dialog_terms.replace('Apply', 'Available').replace('.', ',')
        self.assertIn(terms_available, odds_boost_content,
                      msg=f'Incorrect terms available text, actual text is "{odds_boost_content}" and expected text is "{terms_available}"')
        show_more_btn = self.odd_boost_dialog.show_more_button.is_displayed()
        self.assertTrue(show_more_btn, msg='Show more button is not displaying')
        thanks_link = self.odd_boost_dialog.thanks_link.is_displayed()
        self.assertTrue(thanks_link, msg='thanks link is not displaying')
        close_btn = self.odd_boost_dialog.header_object.close_button.is_displayed()
        self.assertTrue(close_btn, msg='close button is not displaying')
        if self.odds_boost['allowUserToToggleVisibility']:
            dont_show_this_again_checkbox = self.odd_boost_dialog.dont_show_this_again_checkbox
            self.assertTrue(dont_show_this_again_checkbox, msg='Don’t show this again checkbox is not displaying')
            self.assertIn(vec.odds_boost.DONT_SHOW_AGAIN, odds_boost_content,
                          msg=f'Incorrect terms available text, actual text is: "{odds_boost_content}" and expected text is "{terms_available}"')

    def test_003_tap_x_button_on_the_notification_or_ok_thanks_button_or_tap_outside_the_content_odds_boost_notification_area(
            self):
        """
        DESCRIPTION: Tap "X" button on the notification (or "OK THANKS" button, or tap outside the content "Odds Boost" notification area)
        EXPECTED: The pop up is removed from display
        EXPECTED: The respective underlying page is displayed
        """
        self.odd_boost_dialog.header_object.close_button.click()
        self.assertFalse(self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST),
                         msg='odd boost dialog is shown, exepected- odd boost dailog should not appear')
        expected_url = f'https://{tests.HOSTNAME}'
        actual_url = self.device.get_current_url()
        self.softAssert(self.assertIn, expected_url, actual_url,
                        msg=f'Failed to Redirected target Uri "{expected_url}" actual "{actual_url}"')

        if self.device_type == 'mobile':
            if self.brand == 'ladbrokes' and self.site.root_app.has_timeline_overlay_tutorial(timeout=10, expected_result=True):
                self.site.timeline_tutorial_overlay.close_icon.click()

    def test_004_log_out_from_application(self):
        """
        DESCRIPTION: Log Out from application
        EXPECTED: User is logged out
        """
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(), msg='User has not logged out!')

    def test_005_login_into_application_with_another_user_who_has_an_odds_boosts_token(self):
        """
        DESCRIPTION: Login into application with another user who has an Odds Boosts token
        EXPECTED: User is logged in successfully
        EXPECTED: The "Odds Boost" token notification is displayed
        """
        self.login_grant_odd()

    def test_006_tap_show_more_button(self):
        """
        DESCRIPTION: Tap 'SHOW MORE' button
        EXPECTED: The overlay is closed
        EXPECTED: The user is navigated to the hardcoded URL (Odds Boost page) with information about odds boost
        """
        self.odd_boost_dialog.show_more_button.click()
        self.assertFalse(self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST),
                         msg='odd boost dialog is shown, exepected- odd boost dailog should not appear')
        actual_url = self.device.get_current_url()
        expected_url = f'https://{tests.HOSTNAME}/oddsboost'
        self.assertEqual(actual_url, expected_url,
                         msg=f'User is re-directed incorrect URL, actual url is "{actual_url}", expected url is "{expected_url}"')

        odds_boost_sections = list(self.site.odds_boost_page.sections.items_as_ordered_dict.values())
        self.assertTrue(odds_boost_sections, msg='"Odds boost sections" are not displayed')
        self.assertTrue(odds_boost_sections[0], msg='Today\'s Odds Boosts section is missing in odd boost page')
        self.assertTrue(odds_boost_sections[1].items_as_ordered_dict.items(),
                        msg='Boost Available token" is not displayed')
        self.assertTrue(odds_boost_sections[2], msg='Upcoming boost section is missing in odd boost page')
        self.assertTrue(odds_boost_sections[3], msg='Terms and Condition section is missing in odd boost page')
