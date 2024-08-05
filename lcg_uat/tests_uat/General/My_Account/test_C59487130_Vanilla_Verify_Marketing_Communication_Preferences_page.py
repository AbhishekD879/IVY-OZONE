import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C59487130_Vanilla_Verify_Marketing_Communication_Preferences_page(Common):
    """
    TR_ID: C59487130
    NAME: [Vanilla] Verify Marketing/Communication Preferences page
    DESCRIPTION: This test case verifies Communication Preferences page
    DESCRIPTION: *Note:*
    DESCRIPTION: My Account Menu or User Menu is handled and set on GVC side.
    DESCRIPTION: Marketing/Communication Preferences page is handled on GVC side.
    PRECONDITIONS: User is logged in with valid credentials
    """
    keep_browser_open = True

    def test_001_navigate_to_my_account__settings__marketing_coral__communication_ladbrokes_preferences(self):
        """
        DESCRIPTION: Navigate to My Account > Settings > Marketing (Coral) / Communication (Ladbrokes) Preferences
        EXPECTED: *Coral:*
        EXPECTED: Marketing Preferences page consists of:
        EXPECTED: * Title 'Marketing Preferences', 'Back' and 'Close' button
        EXPECTED: * Decription of the page purpose
        EXPECTED: * "I would like to receive the latest offers and promotions from Coral by:" text in caps.
        EXPECTED: * Checkboxes (Email, Phone call, SMS, Post)
        EXPECTED: * Blue infobox is displayed if no or email checkbox not selected
        EXPECTED: * "You can update your preferences at any time. Further details are available in our Privacy Notice". "Privacy Notice" is hyperlinked.
        EXPECTED: * 'Save' button
        EXPECTED: ![](index.php?/attachments/get/115430232)
        EXPECTED: *Ladbrokes:*
        EXPECTED: Communication Preferences page consists of:
        EXPECTED: * Title 'Communication Preferences', 'Back' and 'Close' button
        EXPECTED: * Decription of the page purpose
        EXPECTED: * "I would like to receive the latest offers and promotions from Coral by:" text.
        EXPECTED: * Checkboxes (Email, Phone call, SMS, Post)
        EXPECTED: * Blue infobox is displayed if no or email checkbox not selected
        EXPECTED: * "You can update your preferences at any time. Further details are available in our Privacy Notice". "Privacy Notice" is hyperlinked.
        EXPECTED: * 'Save' button
        EXPECTED: ![](index.php?/attachments/get/115430233)
        """
        self.site.login()
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')
        setting_menu_item = self.site.window_client_config.settings_menu_title
        self.site.right_menu.click_item(item_name=setting_menu_item)
        marketing_preferences_menu_item = self.site.window_client_config.marketing_preferences_menu_title
        self.site.right_menu.click_item(item_name=marketing_preferences_menu_item)
        self.site.wait_content_state_changed()
        self.__class__.marketing_preference = self.site.marketing_preferences
        if self.device_type == 'mobile':
            self.assertTrue(self.marketing_preference.close_icon.is_displayed(),
                            msg='Close icon is not displayed')
            self.assertTrue(self.marketing_preference.back_button.is_displayed(),
                            msg='Close icon is not displayed')
        self.assertTrue(self.marketing_preference.save_button.is_displayed(), msg='Save button is not displayed')
        self.__class__.communication_checkboxes = self.marketing_preference.items_as_ordered_dict
        self.assertEqual(list(self.communication_checkboxes.keys()), vec.GVC.COMMUNICATION_CHECKBOXES,
                         msg=f'Actual items: "{self.communication_checkboxes.keys()}" '
                             f'is not same as Expected items: "{vec.GVC.COMMUNICATION_CHECKBOXES}"')
        self.__class__.email_checkbox, self.__class__.email = list(self.communication_checkboxes.items())[0]

    def test_002_make_all_checkboxes_deselected_and_verify_text_in_blue_infobox(self):
        """
        DESCRIPTION: Make all checkboxes deselected and verify text in blue Infobox
        EXPECTED: "Don't miss out on offers and promotions from Coral/Ladbrokes." Text displayed
        """
        for checkbox in list(self.communication_checkboxes.values())[1:]:
            if checkbox.is_selected():
                checkbox.perform_click()
        self.assertEqual(self.email_checkbox, vec.GVC.COMMUNICATION_CHECKBOXES[0],
                         msg=f'The Marketing preference checkbox option is "{self.email_checkbox}" '
                             f'instead of "{vec.GVC.COMMUNICATION_CHECKBOXES[0]}"')

    def test_003_select_any_checkbox_except_email_and_verify_text_changes_blue_infobox(self):
        """
        DESCRIPTION: Select any checkbox except "Email" and Verify text changes blue Infobox
        EXPECTED: "Don't miss out on email offers and promotions from Coral/Ladbrokes" text displayed
        """
        for checkbox in list(self.communication_checkboxes.values())[1:]:
            if not checkbox.is_selected():
                checkbox.perform_click()
        if self.email.is_selected():
            self.email.perform_click()
        self.assertTrue(self.marketing_preference.validation_message.is_displayed(),
                        msg='The message indicating that the preferences have updated is not been displayed')

    def test_004_select_email_checkbox_and_verify_blue_infobox(self):
        """
        DESCRIPTION: Select "Email" checkbox and verify blue Infobox
        EXPECTED: Infobox not displayed
        """
        if not self.email.is_selected():
            self.email.perform_click()
        self.assertFalse(self.marketing_preference.validation_message,
                         msg='Infobox has been displayed')

    def test_005_click_privacy_notice(self):
        """
        DESCRIPTION: Click Privacy Notice
        EXPECTED: User redirected to corresponding brand Privacy Policy page
        """
        self.marketing_preference.privacy_notice.click()
        self.site.wait_content_state_changed()
        wait_for_result(lambda: self.device.switch_to_new_tab(), timeout=10)
        self.device.driver.implicitly_wait(5)
        actual_url = self.device.get_current_url()
        self.assertIn('privacy-policy', actual_url,
                      msg=f'User is redirected to the wrong page: "{actual_url}"')
        self.device.driver.switch_to.window(self.device.driver.window_handles[0])

    def test_006_select_some_checkboxes_and_click_save_button(self):
        """
        DESCRIPTION: Select some checkboxes and click 'Save' button
        EXPECTED: "Your communication preferences have been saved successfully" message displayed.
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/115430235)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/115430236)
        """
        self.marketing_preference.save_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.marketing_preference.validation_message.is_displayed(),
                        msg='The message indicating that the preferences have updated is not been displayed')
