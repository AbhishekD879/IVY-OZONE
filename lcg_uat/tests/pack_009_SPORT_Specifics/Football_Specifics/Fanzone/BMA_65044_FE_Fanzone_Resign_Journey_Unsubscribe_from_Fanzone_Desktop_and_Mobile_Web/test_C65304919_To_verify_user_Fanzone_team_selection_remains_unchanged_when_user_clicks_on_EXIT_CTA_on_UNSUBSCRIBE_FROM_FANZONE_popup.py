import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result, wait_for_haul
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@pytest.mark.other
@vtest
class Test_C65304919_To_verify_user_Fanzone_team_selection_remains_unchanged_when_user_clicks_on_EXIT_CTA_on_UNSUBSCRIBE_FROM_FANZONE_popup(Common):
    """
    TR_ID: C65304919
    NAME: To verify user Fanzone team selection remains unchanged when user clicks on EXIT CTA on UNSUBSCRIBE FROM FANZONE popup
    DESCRIPTION: To verify user Fanzone team selection remains unchanged when user clicks on EXIT CTA on UNSUBSCRIBE FROM FANZONE popup
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

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        self.__class__.teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        self.teams[1].scroll_to_we()
        self.teams[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_click_on_settings_button(self):
        """
        DESCRIPTION: Click on settings button
        EXPECTED: User should be prompted with TEAM ALERTS screen
        """
        # as per the new change, after subscription, we will be in fanzone page only
        # banner = self.site.home.fanzone_banner()
        # banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

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
        wait_for_haul(3)

        dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
        if dialog_alert_email:
            dialog_alert_email.remind_me_later.click()
        wait_for_haul(3)

        dialog_alert_fanzone_game = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES)
        if dialog_alert_fanzone_game:
            dialog_alert_fanzone_game.close_btn.click()

        self.site.fanzone.setting_link.click()
        wait_for_haul(3)
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        self.assertEqual(self.dialog.title, vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS,
                         msg=f'Actual dialog title "{self.dialog.title}" is not as same as'
                             f' Expected title "{vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS}"')
        self.assertEqual(self.dialog.description, vec.FANZONE.TEAM_ALERTS_MSG,
                         msg=f'Actual dialog title "{self.dialog.description}" is not as same as'
                             f' Expected title "{vec.FANZONE.TEAM_ALERTS_MSG}"')
        self.assertTrue(self.dialog.toggle_switch.is_displayed(), msg='"FANZONE Toggle" is not displayed')
        self.assertTrue(self.dialog.exit_button.is_displayed(), msg='"EXIT: CTA" is not displayed')

    def test_004_set_fanzone_toggle_to_off(self):
        """
        DESCRIPTION: Set Fanzone toggle to OFF
        EXPECTED: User should be prompted with UNSUBSCRIBE FROM FANZONE popup
        """
        self.dialog.toggle_switch.click()
        sleep(3)
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE}" popup is not displayed')

    def test_005_verify_ui_of_popup(self):
        """
        DESCRIPTION: Verify UI of popup
        EXPECTED: UNSUBSCRIBE FROM FANZOME popup should appear as per the sample provided in"Fanzone_POP UP MESSAGES MOCK TEXT FOR TESTING" PPT slide no 17
        """
        # covered in below step

    def test_006_verify_below_listed_details_should_present_in_popupheader_unsubscribe_from_fanzonepopup_text_are_you_sure_you_want_to_unsubscribe_by_pressing_confirm_you_will_lose_access_to_fanzone_if_you_signed_up_less_than_30_days_ago_you_will_need_to_wait_until_the_30_days_expire_to_re_subscribectas_exit_and_confirm(self):
        """
        DESCRIPTION: Verify below listed details should present in popup
        DESCRIPTION: Header: UNSUBSCRIBE FROM FANZONE
        DESCRIPTION: Popup text: Are you sure you want to unsubscribe?â€‹ By pressing CONFIRM you will loseâ€‹ access to FANZONE. If you signed upâ€‹ less than 30 days ago you will need toâ€‹ wait until the 30 days expire to re-subscribe.
        DESCRIPTION: CTA's: EXIT and CONFIRM
        EXPECTED: All listed information should display in the popup
        """
        self.assertEqual(self.dialog.title, vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE,
                         msg=f'Actual dialog title "{self.dialog.title}" is not as same as'
                             f' Expected title "{vec.dialogs.DIALOG_MANAGER_UNSUBSCRIBE_FROM_FANZONE}"')
        self.assertEqual(self.dialog.description, vec.FANZONE.UNSUBSCRIBE_MSG,
                         msg=f'Actual description "{self.dialog.description}" is not as same as'
                             f' Expected description "{vec.FANZONE.UNSUBSCRIBE_MSG}"')
        self.assertTrue(self.dialog.exit_button.is_displayed(), msg='"EXIT: CTA" button is not displayed')
        self.assertTrue(self.dialog.confirm_button.is_displayed(), msg='"CONFIRM" button is not displayed')

    def test_007_click_on_exit_cta(self):
        """
        DESCRIPTION: Click on EXIT CTA
        EXPECTED: User should be navigated Fanzone page
        """
        self.dialog.exit_button.click()
        sleep(3)
        self.assertEqual(self.site.fanzone.header_line.page_title.text, vec.sb.FANZONE,
                         msg=f'Actual page title "{self.site.fanzone.header_line.page_title.text}" '
                             f'is not same as Expected title "{vec.sb.FANZONE}"')

    def test_008_navigate_to_fanzone_page_and_verify_user_team_selection_remains_unchangedexample_if_user_has_selected_everton_as_his_favorite_team_then_user_should_still_remain_with_everton(self):
        """
        DESCRIPTION: Navigate to Fanzone page and verify user team selection remains unchanged
        DESCRIPTION: Example: If user has selected EVERTON as his favorite team, then user should still remain with EVERTON
        EXPECTED: User Fanzone team should remain unchanged
        """
        team_name = self.site.fanzone.fanzone_heading
        self.assertIn(self.teams[1].name, team_name, msg=f'Favorite team changed from '
                                                         f'{self.teams[1].name} to {team_name}')
