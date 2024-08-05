import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_haul


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.avtar_menu
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.other
@vtest
# this testcase also covers C65950084
class Test_C65950083_Validate_Avtar_menu_gambling_pages(Common):
    """
    TR_ID: C65950083
    NAME: Validate Avtar menu gambling pages
    DESCRIPTION: This test case is to verify the Avtar menu gambling pages
    PRECONDITIONS: 1.User should have vaild login credentials to log into the application
    """
    keep_browser_open = True
    GAMBLING_CONTROLS_MENU_ITEMS = ['IMMEDIATE 24-HOUR BREAK', 'SPENDING CONTROLS', 'TIME MANAGEMENT', 'ACCOUNT CLOSURE & REOPENING']


    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should loaded succesfully
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)

    def test_002_verify_avatar__icon_in_the__header(self):
        """
        DESCRIPTION: Verify avatar  icon in the  header
        EXPECTED: User should be able to see Avatar  icon should be present
        """
        # covered in below step

    def test_003_click_on_avatar_menu_icon(self):
        """
        DESCRIPTION: Click on Avatar menu icon
        EXPECTED: User should able to see avatar menus
        """
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        self.__class__.actual_right_menu = self.site.right_menu.items_as_ordered_dict
        self.assertTrue((item.upper() in vec.bma.EXPECTED_RIGHT_MENU for item in self.actual_right_menu),
                        msg=f'Actual items: "{self.actual_right_menu}" are not equal with the '
                            f'Expected items: "{vec.bma.EXPECTED_RIGHT_MENU}"')

    def test_004_click_on_gambling_controls(self):
        """
        DESCRIPTION: Click on gambling controls
        EXPECTED: User should be navigate to gambling control page with the following items order display
        EXPECTED: a)Immediate 24- hour break
        EXPECTED: b)Spending controls
        EXPECTED: c)Time mangement
        EXPECTED: d)Account closure &Reopening
        """
        for item_name, item in self.actual_right_menu.items():
            if item_name.upper() == 'GAMBLING CONTROLS':
                item.click()
        wait_for_haul(10)
        gambling_controls = self.site.gambling_controls.items_as_ordered_dict
        actual_gc_items = list(gambling_controls.keys())
        output_list = [word.upper() for word in actual_gc_items]
        self.assertEqual(output_list, self.GAMBLING_CONTROLS_MENU_ITEMS,
                         msg=f'Actual gambling controls menu items "{actual_gc_items}" is not as same as'
                             f'Expected gambling controls menu items "{self.GAMBLING_CONTROLS_MENU_ITEMS}"')

    def test_005_verify_by_clicking_on_x_mark_beside_gambling_controls_header(self):
        """
        DESCRIPTION: Verify by clicking on X mark beside gambling controls header
        EXPECTED: User should be navigate to homepage successfully
        """
        if self.device_type=='desktop':
            self.site.gambling_controls.header_line.close.click()
            self.test_003_click_on_avatar_menu_icon()
            self.test_004_click_on_gambling_controls()

    def test_006_mobileverify_by_clicking_on_the_backward_chevron_beside_gambling_controls_header(self):
        """
        DESCRIPTION: Mobile
        DESCRIPTION: Verify by clicking on the backward chevron beside gambling controls header
        EXPECTED: User should be navigate to avatar menu page  successfully
        """
        if self.device_type=='mobile':
            self.site.gambling_controls.header_line.back_button.click()
            self.site.header.right_menu_button.click()
            self.test_003_click_on_avatar_menu_icon()
            self.test_004_click_on_gambling_controls()

    def test_007_desktopverify_the_username_with_avatar_beside_gambling_controls_header(self):
        """
        DESCRIPTION: Desktop
        DESCRIPTION: Verify the username with avatar beside gambling controls header
        EXPECTED: User should able to see the username with avatar icon
        """
        if self.device_type=='desktop':
            self.site.gambling_controls.header_line.header_title.is_displayed()
            self.site.gambling_controls.header_line.avatar.is_displayed()
            self.__class__.panels = self.site.gambling_controls.items_as_ordered_dict

    def test_008_verify_the_listed_above_4_items_expand_and_collapse_mode(self):
        """
        DESCRIPTION: Verify the listed above 4 items expand and collapse mode
        EXPECTED: 1.User should be able to see collasped mode as default
        EXPECTED: 2.User should be able to access the data when in expanded state
        EXPECTED: 3.User should not see data when in collapsed state
        """
        if self.device_type=='mobile':
            self.__class__.panels = self.site.gambling_controls.items_as_ordered_dict
            for panel_name, panel in self.panels.items():
                self.assertFalse(panel.is_expanded(), msg=f'{panel_name} panel is expanded')
                panel.click()
                self.assertTrue(panel.is_expanded(), msg=f'{panel_name} panel is not expanded')

    def test_009_verify_by_expanding__immediate_24__hour_break(self):
        """
        DESCRIPTION: Verify by expanding  Immediate 24- hour break
        EXPECTED: User should be able to see the data
        """
        panel_name, panel = next(((panel_name, panel) for panel_name, panel in self.panels.items() if panel_name.upper()=='IMMEDIATE 24-HOUR BREAK'),None)
        if self.device_type == 'mobile':
            if not panel.is_expanded():
                panel.click()
        menu_items = self.site.gambling_controls.items_as_ordered_dict.get(panel_name).items_as_ordered_dict
        immediate_stop_menu = next((menu for menu_item, menu in menu_items.items() if menu_item.upper() == 'IMMEDIATE STOP'))
        immediate_stop_menu.click()
        wait_for_haul(5)
        self.assertTrue(self.site.immediate_24_hours_break.has_message_panel_displayed(timeout=10), msg=f"'Your account has now been put on Time Out for the next 24 hours.' message not displayed")
        self.site.immediate_24_hours_break.close.click()
        self.site.wait_content_state_changed()
        self.site.logout()
        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        dialog.username = self.username
        dialog.password = tests.settings.default_password
        dialog.click_login()
        wait_for_haul(5)
        not_login = dialog.error_message
        self.assertTrue(not_login, msg=f"Login successful even user {self.username} is blocked for 24 Hours")




