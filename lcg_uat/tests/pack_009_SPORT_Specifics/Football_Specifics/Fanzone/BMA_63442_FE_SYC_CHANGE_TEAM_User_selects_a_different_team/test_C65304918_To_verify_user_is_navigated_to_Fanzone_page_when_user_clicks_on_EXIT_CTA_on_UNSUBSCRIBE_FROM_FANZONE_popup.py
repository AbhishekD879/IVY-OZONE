import pytest
import tests
from time import sleep
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65304918_To_verify_user_is_navigated_to_Fanzone_page_when_user_clicks_on_EXIT_CTA_on_UNSUBSCRIBE_FROM_FANZONE_popup(Common):
    """
    TR_ID: C65304918
    NAME: To verify user is navigated to Fanzone page when user clicks on EXIT CTA on UNSUBSCRIBE FROM FANZONE popup
    DESCRIPTION: To verify user is navigated to Fanzone page when user clicks on EXIT CTA on UNSUBSCRIBE FROM FANZONE popup
    PRECONDITIONS: 1) User has logged into lads application
    PRECONDITIONS: 2) User has subscribed to Fanzone Previously
    PRECONDITIONS: 3) Configure fanzone data in CMS
    PRECONDITIONS: CMS-->Fanzone-->Fanzones
    PRECONDITIONS: 4) In System Config Fanzone should be enabledC65304975
    PRECONDITIONS: 5) All entry points for each and every Fanzone team should be enabled
    PRECONDITIONS: 6) User is in Fanzone Page
    PRECONDITIONS: Note: User could navigate to Fanzone page through any of the 4 entry points
    PRECONDITIONS: a) Fanzone in A-Z sports
    PRECONDITIONS: b) Fanzone in Sports Ribbon
    PRECONDITIONS: c) Launch banner in Highlight tab
    PRECONDITIONS: d) Launch banner in Football landing page
    """
    keep_browser_open = True
    teamname = vec.fanzone.TEAMS_LIST.aston_villa.title()

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
        burnley_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if burnley_fanzone['active'] is not True:
            self.cms_config.update_fanzone(self.teamname)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state(state_name='HomePage')
        sleep(3)
        self.site.login(username=username)
        self.site.open_sport(name='Football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[self.teamname].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
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
        self.__class__.dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)

    def test_002_check_settings_button_position(self):
        """
        DESCRIPTION: Check settings button position
        EXPECTED: Settings button should be at top corner of the page
        """
        # NA

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

    def test_005_verify_ui_of_popup(self):
        """
        DESCRIPTION: Verify UI of popup
        EXPECTED: UNSUBSCRIBE FROM FANZOME popup should appear as per the sample provided in"Fanzone_POP UP MESSAGES MOCK TEXT FOR TESTING" PPT slide no 17
        """
        sleep(3)
        self.__class__.dialog_unsubscribe_fanzone = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE)
        self.assertTrue(self.dialog_unsubscribe_fanzone.header_object.title_text,
                        msg='header text is not displayed for unsubscribed dialog')
        self.assertEquals(self.dialog_unsubscribe_fanzone.description, vec.FANZONE.UNSUBSCRIBE_MSG,
                          msg=f"Actual message '{self.dialog_unsubscribe_fanzone.description}' is not same as expected message '{vec.FANZONE.UNSUBSCRIBE_MSG}'")
        self.assertTrue(self.dialog_unsubscribe_fanzone.exit_button.is_displayed(),
                        msg='exit button is not displayed for unsubscribed dialog')
        self.assertTrue(self.dialog_unsubscribe_fanzone.confirm_button.is_displayed(),
                        msg='confirm button is not displayed for unsubscribed dialog')

    def test_006_verify_below_listed_details_should_present_in_popupheader_unsubscribe_from_fanzonepopup_text_are_you_sure_you_want_to_unsubscribe_by_pressing_confirm_you_will_lose_access_to_fanzone_if_you_signed_up_less_than_30_days_ago_you_will_need_to_wait_until_the_30_days_expire_to_re_subscribectas_exit_and_confirm(self):
        """
        DESCRIPTION: Verify below listed details should present in popup
        DESCRIPTION: Header: UNSUBSCRIBE FROM FANZONE
        DESCRIPTION: Popup text: Are you sure you want to unsubscribe?â€‹ By pressing CONFIRM you will loseâ€‹ access to FANZONE. If you signed upâ€‹ less than 30 days ago you will need toâ€‹ wait until the 30 days expire to re-subscribe.
        DESCRIPTION: CTA's: EXIT and CONFIRM
        EXPECTED: All listed information should display in the popup
        """
        # Covered in above step

    def test_007_click_on_exit_cta(self):
        """
        DESCRIPTION: Click on EXIT CTA
        EXPECTED: User should be navigated Fanzone page
        """
        self.dialog_unsubscribe_fanzone.exit_button.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')
