import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from collections import OrderedDict


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.desktop
@vtest
class Test_C28083_Verify_Universal_Header_for_Logged_Out_user_for_DesktopNot_valid_for_vanilla(BaseSportTest):
    """
    TR_ID: C28083
    NAME: Verify Universal Header for Logged Out user for Desktop
    DESCRIPTION: This test case verifies Universal Header UI and functionality when user is logged out on Desktop.
    DESCRIPTION: Need to check on Windows ( IE, Edge, Chrome, FireFox ) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. User is logged out
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get Sub Navigation Menu tabs from CMS
        """
        menu_tabs_cms = self.cms_config.get_cms_header_menu_items()
        submenu_tabs_cms = self.cms_config.get_header_submenus()
        self.__class__.expected_tabs_dict = OrderedDict()
        self.__class__.expected_main_tabs_dict = OrderedDict()
        for tab_name in submenu_tabs_cms:
            if tab_name.get('linkTitle') and not tab_name['disabled']:
                self.expected_main_tabs_dict[tab_name['linkTitle'].strip().upper()] = tab_name

        for tab_name in menu_tabs_cms:
            if tab_name.get('linkTitle') and not tab_name['disabled']:
                self.expected_tabs_dict[tab_name['linkTitle'].strip().upper()] = tab_name

    def test_001_verify_universal_header_displaying(self):
        """
        DESCRIPTION: Verify Universal Header displaying
        EXPECTED: Universal Header is displayed on every page across the app
        """
        self.assertTrue(self.site.wait_logged_out(), "User is not logged out")
        self.site.wait_content_state(state_name='HomePage')

    def test_002_verify_universal_header_content(self):
        """
        DESCRIPTION: Verify Universal Header content
        EXPECTED: Following elements are displayed:
        EXPECTED: *   'Main Navigation' menu (CMS configurable)
        EXPECTED: *   'Sports Sub Navigation' menu (CMS configurable)
        EXPECTED: *   'Coral' logo
        EXPECTED: *   'Join Now' button
        EXPECTED: *   'Log in' button
        """
        # Main Navigation
        actual_sport_tabs = self.site.header.top_menu.items_as_ordered_dict
        self.assertTrue(actual_sport_tabs, msg='No one main menu tabs found')
        for item in self.expected_tabs_dict.keys():
            self.assertIn(item, list(self.expected_tabs_dict.keys()),
                          msg=f'Actual menu items order: \n["{item}"] '
                              f'\nExpected: \n["{list(self.expected_tabs_dict.keys())}"]')

        # Sub Navigation
        actual_sport_tabs = self.site.header.sport_menu.items_as_ordered_dict
        self.assertTrue(actual_sport_tabs, msg='No one submenu tabs found')
        self.assertEqual(list(actual_sport_tabs.keys()), list(self.expected_main_tabs_dict.keys()),
                         msg=f'Actual menu items order: \n["{list(actual_sport_tabs.keys())}"] '
                             f'\nExpected: \n["{list(self.expected_main_tabs_dict.keys())}"]')
        self.assertTrue(self.site.header.brand_logo.is_displayed(), "Top menu does not contain'Coral' logo option")
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='Top menu does not contain "Login" option')
        self.assertTrue(self.site.header.join_us.is_displayed(), msg='Top menu does not contain "Join" option')

    def test_003_navigate_to_any_page_in_app_and_click_on_coral_logo(self):
        """
        DESCRIPTION: Navigate to any page in app and click on 'Coral' logo
        EXPECTED: User is navigated to Homepage after clicking 'Coral' Logo
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='football')
        self.site.header.brand_logo.click()
        self.site.wait_content_state("HomePage")

    def test_004_click_on_join_now_button(self):
        """
        DESCRIPTION: Click on Join Now button
        EXPECTED: Registration Step 1 page is opened
        """
        self.site.header.join_us.click()
        self.assertTrue(self.site.three_steps_registration.is_displayed(timeout=10),
                        msg='"Registration" form is not opened')
        self.site.three_steps_registration.header.close_button.click()
        self.site.wait_content_state(state_name='HomePage')

    def test_005_click_on_log_in_button(self):
        """
        DESCRIPTION: Click on 'Log in' button
        EXPECTED: 'Log in' pop-up appears
        """
        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg='Login dialog is not present on page')
