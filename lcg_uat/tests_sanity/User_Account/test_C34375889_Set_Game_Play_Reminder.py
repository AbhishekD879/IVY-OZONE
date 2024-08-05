import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from time import sleep


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.low
@pytest.mark.desktop
# @pytest.mark.sanity
@pytest.mark.user_account
@vtest
class Test_C34375889_Set_Game_Play_Reminder(BaseUserAccountTest):
    """
    TR_ID: C34375889
    NAME: Set Game Play Reminder
    DESCRIPTION: This test case verifies confirming of Game Play Reminder Frequency
    PRECONDITIONS: Application is opened
    PRECONDITIONS: User is successfully logged in
    """
    keep_browser_open = True
    time_limit = "15 Minutes"

    def test_001_open_my_account_menu__select_gambling_controls(self):
        """
        DESCRIPTION: Open 'My Account' menu > Select 'Gambling Controls'
        EXPECTED: 'Gambling Controls' page is opened
        """
        username = tests.settings.gaming_user
        self.site.login(username=username)
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS)
        self.assertTrue(self.site.gambling_controls.is_displayed(timeout=10),
                        msg=f'"Gambling Controls" page is not opened')

    def test_002_selecttime_management_option(self):
        """
        DESCRIPTION: Select 'Time Management' option
        EXPECTED: *   'Time Management' option is selected
        EXPECTED: *   Description is changed to:
        EXPECTED: - Control how long you spend gaming and get notified once your time limit is reached
        EXPECTED: - You can change your settings at any time
        """
        self.site.gambling_controls.time_management.click()
        actual_option_name = self.site.gambling_controls.option_content.replace('\n', '')
        self.assertEqual(actual_option_name, vec.bma.TIME_MANAGEMENT_TEXT,
                         msg=f'Actual description: "{actual_option_name}" is not the same as "{vec.bma.GAMBLING_CONTROLS}"')

    def test_003_click_choose_button(self):
        """
        DESCRIPTION: Click 'CHOOSE' button
        EXPECTED: 'Time Management' page is opened with following controls:
        EXPECTED: *   'Time limit' drop-down with options to select: <15 minutes, 30 minutes, 45 minutes, 60 minutes #Only four options observed
        EXPECTED: (Default or previously set value is selected in the drop-down)
        EXPECTED: *   'Save' button
        """
        self.site.gambling_controls.choose_button.click()
        tm_drop_down = self.site.time_management_page.dropdown.available_options
        self.assertEqual(tm_drop_down, vec.bma.TIME_LIMIT_OPTIONS, msg='Time limit dropdown values not found')
        save_btn = self.site.time_management_page.save_button
        self.assertTrue(save_btn, msg='Save button is not displayed')

    def test_004_change_the_selected_value_in_the_drop_down(self):
        """
        DESCRIPTION: Change the selected value in the drop-down
        EXPECTED: *   New value is shown in the drop-down
        """
        self.site.time_management_page.dropdown.value = self.time_limit
        actual_value = self.site.time_management_page.dropdown.value.strip()
        self.assertEqual(actual_value, self.time_limit,
                         msg=f'Actual value "{actual_value}" is not the same as "{self.time_limit}"')

    def test_005_tap_save_button(self):
        """
        DESCRIPTION: Tap 'Save' button
        EXPECTED: Success message appears:
        EXPECTED: * 'Your time management settings have been successfully saved.'
        """
        self.site.time_management_page.save_button.click()
        sleep(4)
        actual_success_message = self.site.time_management_overlay.successful_message.text
        self.assertEqual(actual_success_message, vec.dialogs.DIALOG_MANAGER_TIME_LIMIT,
                         msg=f'Actual message: "{actual_success_message}" '
                             f'is not the same as "{vec.dialogs.DIALOG_MANAGER_TIME_LIMIT}"')

    def test_006_refresh_time_management_page(self):
        """
        DESCRIPTION: Refresh 'Time Management' page
        EXPECTED: *   Success message is not displayed
        EXPECTED: *   New value is set and shown in the drop-down
        """
        self.device.refresh_page()
        success_message = self.site.time_management_page.successful_message
        self.assertFalse(success_message, msg="Successful message is displayed")
        new_value = self.site.time_management_page.dropdown.value.strip()
        self.assertEqual(new_value, self.time_limit, msg=f'Actual value:"{new_value}"'
                                                         f'is not the same as "{self.time_limit}"')
