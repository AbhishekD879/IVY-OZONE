import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from time import sleep
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305523_Verify_GA_tracking_for_users_action_onPC_screen_unsubscribe_CTA_via_Fanzone(BaseDataLayerTest):
    """
    TR_ID: C65305523
    NAME: Verify GA tracking for user's action onÂ PC screen unsubscribe CTA via Fanzone
    DESCRIPTION: This test case is to verify GA tracking for user's action on PC screen unsubscribe CTA via Fanzone
    PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
    PRECONDITIONS: 2) Create fanzone tabs: now&next, stats and clubs
    PRECONDITIONS: 3) Create surface bets, HC and outrights data for fanzone
    PRECONDITIONS: 4) User has subscribed to Fanzone
    PRECONDITIONS: 5) User should be logged in state
    """
    keep_browser_open = True

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('Football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        teams[1].scroll_to_we()
        teams[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_launch_application_and_click_on_any_fanzone_entry_point(self):
        """
        DESCRIPTION: Launch application and click on any fanzone entry point
        EXPECTED: User should be navigated to fanzone page
        """
        # banner = self.site.home.fanzone_banner()
        # banner.let_me_see.click()
        # result = wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
        #                          name='Fanzone page not displayed',
        #                          timeout=5)
        # self.assertTrue(result, msg='fanzone page not loaded')

    def test_002_click_on_fanzone_settings_icon(self):
        """
        DESCRIPTION: Click on fanzone settings icon
        EXPECTED: User should be navigated to preference center screen
        """
        self.site.fanzone.setting_link.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        self.assertTrue(self.dialog,
                        msg=f'"{vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS}" popup is not displayed')

    def test_003_toggle_off_the_subscribe_option_and_click_on_submit_button(self):
        """
        DESCRIPTION: Toggle off the subscribe option and click on submit button
        EXPECTED: user should get confirmation popup
        """
        self.dialog.toggle_switch.click()
        sleep(3)
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE)
        self.assertTrue(self.dialog,
                        msg=f'"{vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE}" popup is not displayed')

    def test_004_click_on_exit_button_and_check_ga_tracking(self):
        """
        DESCRIPTION: Click on exit button and check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "preference center",
        EXPECTED: "eventCategory": "fanzone",
        EXPECTED: "eventLabel": "EXIT"
        EXPECTED: })
        """
        self.dialog.exit_button.click()
        expected_response = {
            "event": "trackEvent",
            "eventAction": "Preference Centre",
            "eventCategory": "fanzone",
            "eventLabel": "EXIT"
        }
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='fanzone')
        self.compare_json_response(actual_response, expected_response)

    def test_005_repeat_step_1_to_3_and_click_on_confirm_button_in_popupcheck_ga_tracking(self):
        """
        DESCRIPTION: Repeat step 1 to 3 and click on Confirm button in popup
        DESCRIPTION: Check GA tracking
        EXPECTED: The tag should contain
        EXPECTED: dataLayer.push({
        EXPECTED: "event": "trackEvent",
        EXPECTED: "eventAction": "preference center",
        EXPECTED: "eventCategory": "fanzone",
        EXPECTED: "eventLabel":" "Confirm"
        EXPECTED: })
        """
        self.navigate_to_page('homepage')
        self.test_001_launch_application_and_click_on_any_fanzone_entry_point()
        self.test_002_click_on_fanzone_settings_icon()
        self.test_003_toggle_off_the_subscribe_option_and_click_on_submit_button()
        self.dialog.confirm_button.click()
        expected_response = {
            "event": "trackEvent",
            "eventAction": "Preference Centre",
            "eventCategory": "fanzone",
            "eventLabel": "Confirm"
        }
        sleep(2)
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='fanzone')
        self.compare_json_response(actual_response, expected_response)
