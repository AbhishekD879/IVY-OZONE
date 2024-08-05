import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
import tests
from tests.Common import Common


@pytest.mark.lad_prod
@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@pytest.mark.one_two_free
@vtest
class Test_C57731995_Verify_displaying_of_Login_Splash_page(Common):
    """
    TR_ID: C57731995
    NAME: Verify displaying of 'Login Splash page'
    DESCRIPTION: This test case verifies displaying login pop-up
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: Deprecated: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: Oxygen CMS guide: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: see section Text Configuration - Splash Page
    PRECONDITIONS: 1. The user is NOT logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE' is available on Homepage / Football sports page (configure in CMS quick link and set link to 1-2-free as '{evnURL}/1-2-free')
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_quick_link_on_homepage__football_sports_page(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE' quick link on Homepage / Football sports page
        EXPECTED: User should see Login Splash page, designed:
        EXPECTED: ![](index.php?/attachments/get/30763)
        EXPECTED: - 'Login to Play' button
        EXPECTED: - Cancel button
        """
        self.navigate_to_page(name='1-2-free')
        dialog = self.site._wait_for_login_dialog(15)
        if dialog:
            self.assertTrue(dialog, '"Log In" pop-up is not displayed')
            dialog.close_dialog()
            self.assertFalse(vec.dialogs.DIALOG_MANAGER_LOG_IN in self.site.dialog_manager.items_as_ordered_dict,
                             msg='"Log In" dialog should not be displayed on the screen')
        self.assertTrue(self.site.one_two_free.login_to_play_button.is_displayed(),
                        msg='1-2-Free login to play is not shown')
        self.assertTrue(self.site.one_two_free.login_page_cancel_button.is_displayed(),
                        msg='1-2-Free login page cancel is not shown')

    def test_002_tap_on_login_to_play_button(self):
        """
        DESCRIPTION: Tap on 'Login to Play' button
        EXPECTED: Login pop-up should successfully opens
        """
        self.site.one_two_free.login_to_play_button.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        self.assertTrue(self.dialog, msg='"Log In" dialog is not shown')

    def test_003_login_with_valid_user_credentialstap_login_button(self):
        """
        DESCRIPTION: Login with valid user credentials
        DESCRIPTION: Tap 'Login' button
        EXPECTED: - User successfully login
        EXPECTED: - Splash page or Current page should be displayed depending on previous actions
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg='Failed to close Login dialog')
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=5)
        if dialog:
            dialog.close_dialog()
            dialog.wait_dialog_closed()
        self.assertTrue(self.site.one_two_free.is_displayed(timeout=5),
                        msg='1-2-Free welcome screen is not shown')
