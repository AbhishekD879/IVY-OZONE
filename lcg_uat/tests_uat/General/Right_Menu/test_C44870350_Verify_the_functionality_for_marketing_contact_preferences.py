import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.prod
# @pytest.mark.uat
# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870350_Verify_the_functionality_for_marketing_contact_preferences(Common):
    """
    TR_ID: C44870350
    NAME: Verify the functionality for marketing/contact preferences.
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_000_pre_condition(self):
        """
        DESCRIPTION: User is logged in
        """
        self.site.login()

    def test_001_click_on_the_avatar__settings__marketing_preferences(self):
        """
        DESCRIPTION: Click on the Avatar > Settings > Marketing Preferences.
        EXPECTED: Communication preferences are displayed.
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')
        setting_menu_item = self.site.window_client_config.settings_menu_title
        self.site.right_menu.click_item(item_name=setting_menu_item)
        self.assertEqual(self.site.right_menu.header.title, setting_menu_item,
                         msg=f'"{setting_menu_item}" menu is not displayed')
        menu_items = self.site.right_menu.items_as_ordered_dict
        marketing_preferences_menu_item = self.site.window_client_config.marketing_preferences_menu_title
        self.assertIn(marketing_preferences_menu_item, menu_items.keys(),
                      msg=f'"{marketing_preferences_menu_item}" not present in the Right column')
        self.site.right_menu.click_item(item_name=marketing_preferences_menu_item)
        self.site.wait_content_state_changed()
        self.__class__.marketing_preference = self.site.marketing_preferences
        if self.device_type == 'desktop':
            actual_title = self.marketing_preference.title
            expected_title = vec.GVC.MARKETING_PREFERENCES_DESKTOP
        else:
            actual_title = self.marketing_preference.header.title.name
            expected_title = vec.GVC.MARKETING_PREFERENCES_MOBILE
        self.assertEqual(actual_title, expected_title,
                         msg='Marketing Preferences page is not open. '
                             f'Page name is "{actual_title}" instead of "{expected_title}"')
        self.__class__.communication_checkboxes = self.marketing_preference.items_as_ordered_dict
        self.assertEqual(list(self.communication_checkboxes.keys()), vec.GVC.COMMUNICATION_CHECKBOXES,
                         msg=f'Actual items: "{self.communication_checkboxes.keys()}" '
                             f'is not same as Expected items: "{vec.GVC.COMMUNICATION_CHECKBOXES}"')
        self.__class__.email_checkbox, self.__class__.email = list(self.communication_checkboxes.items())[0]

    def test_002_select_all_and_verify(self):
        """
        DESCRIPTION: Select 'All' and verify.
        EXPECTED: 1. The message indicating that the preferences have been updated is displayed.
        EXPECTED: 2. All the contact options/boxes are checked.
        """
        for checkbox in self.communication_checkboxes.values():
            if not checkbox.is_selected():
                checkbox.perform_click()
        self.marketing_preference.save_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.marketing_preference.validation_message.is_displayed(),
                        msg='The message indicating that the preferences have updated is not been displayed')
        for checkName, checkbox in self.communication_checkboxes.items():
            self.assertTrue(checkbox.is_selected(), msg=f'The "{checkName}" '
                                                        'in the Marketing Preferences options are not selected')

    def test_003_de_select_all_and_select_email_verify(self):
        """
        DESCRIPTION: De-select 'All' and select 'Email'. Verify.
        EXPECTED: 1. The message indicating that the preferences have been updated is displayed.
        EXPECTED: 2. The box/option for 'Email' is checked, remaining boxes/options are not selected/checked.
        """
        for checkbox in list(self.communication_checkboxes.values())[1:]:
            if checkbox.is_selected():
                checkbox.perform_click()
        self.assertEqual(self.email_checkbox, vec.GVC.COMMUNICATION_CHECKBOXES[0],
                         msg=f'The Marketing preference checkbox option is "{self.email_checkbox}" '
                             f'instead of "{vec.GVC.COMMUNICATION_CHECKBOXES[0]}"')
        if not self.email.is_selected():
            self.email.perform_click()
        self.marketing_preference.save_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.marketing_preference.validation_message.is_displayed(),
                        msg='The message indicating that the preferences have updated is not been displayed')
        self.assertTrue(self.email.is_selected(),
                        msg='The "Email" checkbox in Marketing Preference is not checked')
        for checkbox in list(self.communication_checkboxes.values())[1:]:
            self.assertFalse(checkbox.is_selected(), msg='Other Marketing Preferences checkboxes are selected')

    def test_004_click_on_save_button_and_navigate_to_marketing_preferences_again_verify(self):
        """
        DESCRIPTION: Click on Save button and navigate to Marketing preferences again. Verify.
        EXPECTED: The box/option for 'Email' is checked, remaining boxes/options are not selected/checked.
        """
        if self.device_type == "mobile":
            self.marketing_preference.close_icon.click()
        else:
            self.navigate_to_page('Home')
        self.site.wait_content_state('Home')
        self.test_001_click_on_the_avatar__settings__marketing_preferences()
        self.assertEqual(self.email_checkbox, vec.GVC.COMMUNICATION_CHECKBOXES[0],
                         msg=f'The Marketing preference checkbox option is "{self.email_checkbox}"'
                             f'instead of "{vec.GVC.COMMUNICATION_CHECKBOXES[0]}"')
        self.assertTrue(self.email.is_selected(), msg='The "Email" communication checkbox is not checked')
        for checkbox in list(self.communication_checkboxes.values())[1:]:
            self.assertFalse(checkbox.is_selected(), msg='Other Marketing Preferences checkboxes are selected')
