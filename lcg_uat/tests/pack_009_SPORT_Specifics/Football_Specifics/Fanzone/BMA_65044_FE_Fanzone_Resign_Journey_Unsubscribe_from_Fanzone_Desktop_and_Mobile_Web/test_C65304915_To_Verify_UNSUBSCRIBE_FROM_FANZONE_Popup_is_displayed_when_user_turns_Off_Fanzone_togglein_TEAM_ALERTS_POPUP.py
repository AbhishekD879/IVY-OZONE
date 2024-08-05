import tests
import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from time import sleep
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_h1
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304915_To_Verify_UNSUBSCRIBE_FROM_FANZONE_Popup_is_displayed_when_user_turns_Off_Fanzone_togglein_TEAM_ALERTS_POPUP(Common):
    """
    TR_ID: C65304915
    NAME: To Verify UNSUBSCRIBE FROM FANZONE Popup is displayed when user turns Off Fanzone togglein TEAM ALERTS POPUP
    DESCRIPTION: To Verify UNSUBSCRIBE FROM FANZONE Popup is displayed when user turns Off Fanzone toggle
    DESCRIPTION: in TEAM ALERTS POPUP
    PRECONDITIONS: 1) User has logged into lads application
    PRECONDITIONS: 2) User has subscribed to Fanzone Previously
    PRECONDITIONS: 3) Configure fanzone data in CMS
    PRECONDITIONS: CMS-->Fanzone-->Fanzones
    PRECONDITIONS: 4) In System Config Fanzone should be enabled
    PRECONDITIONS: 5) All entry points for each and every Fanzone team should be enabled
    PRECONDITIONS: 6) User is in Fanzone Page
    PRECONDITIONS: Note: User could navigate to Fanzone page through any of the 4 entry points
    PRECONDITIONS: a) Fanzone in A-Z sports
    PRECONDITIONS: b) Fanzone in Sports Ribbon
    PRECONDITIONS: c) Launch banner in Highlight tab
    PRECONDITIONS: d) Launch banner in Football landing page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has logged into lads application
        PRECONDITIONS: 2) User has subscribed to Fanzone Previously
        PRECONDITIONS: 3) Configure fanzone data in CMS
        PRECONDITIONS: CMS-->Fanzone-->Fanzones
        PRECONDITIONS: 4) In System Config Fanzone should be enabled
        PRECONDITIONS: 5) All entry points for each and every Fanzone team should be enabled
        PRECONDITIONS: 6) User is in Fanzone Page
        PRECONDITIONS: Note: User could navigate to Fanzone page through any of the 4 entry points
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state(state_name='HomePage')
        sleep(3)
        self.site.login(username=username)
        self.site.open_sport(name='Football', fanzone=True, timeout=30)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed')
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        sleep(5)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=30)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS, timeout=30)
        dialog_teamalert.exit_button.click()
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_001_click_on_settings_button(self):
        """
        DESCRIPTION: Click on settings button
        EXPECTED: User should be prompted with TEAM ALERTS screen
        """
        self.site.fanzone.setting_link.click()
        self.__class__.dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS,
                                                                    timeout=30)

    def test_002_check_settings_button_position(self):
        """
        DESCRIPTION: Check settings button position
        EXPECTED: Settings button should be at top corner of the page
        """
        # cannot automate the settings button position

    def test_003_verify_team_alerts_popup_as_below_detailstitle_team_alertspopup_message_dont_miss_a_thing_go_to_the_ladbrokes_app_and_set_your_push_notification_preferences_to_receive_team_news_in_play_match_updates_and_more_these_are_for_the_app_platform_only_they_are_not_sent_on_desktop_or_mobile_web_platformsfanzone_togglecta_exitnote_view_page_no_17_in_mockup_pptattached_to_the_story(self):
        """
        DESCRIPTION: Verify TEAM ALERTS popup as below details
        DESCRIPTION: Title: TEAM ALERTS
        DESCRIPTION: Popup Message: Donâ€™t miss a thing! Go to the Ladbrokes app and setâ€‹ your push notification preferences to receive teamâ€‹ news, in-play match updates and more. â€‹these are for the app platform only; they are notâ€‹ sent on desktop or mobile web platforms.
        DESCRIPTION: FANZONE Toggle
        DESCRIPTION: CTA: EXIT
        DESCRIPTION: Note: View Page no 17 in Mockup PPT,attached to the story
        EXPECTED: All listed information should display in the popup
        """
        self.assertTrue(self.dialog_teamalert.header_object.title_text, msg='Team alerts title is not displayed')
        self.assertEquals(self.dialog_teamalert.description, vec.FANZONE.TEAM_ALERTS_MSG,
                          msg=f"Actual message '{self.dialog_teamalert.description}' is not same as expected message '{vec.FANZONE.TEAM_ALERTS_MSG}'")
        self.assertTrue(self.dialog_teamalert.toggle_switch, msg='Team alerts toggle is not displayed')
        self.assertTrue(self.dialog_teamalert.exit_button, msg='Team alerts exit button is not displayed')

    def test_004_set_fanzone_toggle_to_off(self):
        """
        DESCRIPTION: Set Fanzone toggle to OFF
        EXPECTED: User should be prompted with UNSUBSCRIBE FROM FANZONE popup
        """
        self.dialog_teamalert.toggle_switch.click()
        sleep(3)
        dialog_unsubscribe_fanzone = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE)
        self.assertTrue(dialog_unsubscribe_fanzone.header_object.title_text,
                        msg='header text is not displayed for unsubscribed dialog')
        self.assertEquals(dialog_unsubscribe_fanzone.description, vec.FANZONE.UNSUBSCRIBE_MSG,
                          msg=f"Actual message '{dialog_unsubscribe_fanzone.description}' is not same as expected message '{vec.FANZONE.UNSUBSCRIBE_MSG}'")
        self.assertTrue(dialog_unsubscribe_fanzone.exit_button.is_displayed(),
                        msg='exit button is not displayed for unsubscribed dialog')
        self.assertTrue(dialog_unsubscribe_fanzone.confirm_button.is_displayed(),
                        msg='confirm button is not displayed for unsubscribed dialog')