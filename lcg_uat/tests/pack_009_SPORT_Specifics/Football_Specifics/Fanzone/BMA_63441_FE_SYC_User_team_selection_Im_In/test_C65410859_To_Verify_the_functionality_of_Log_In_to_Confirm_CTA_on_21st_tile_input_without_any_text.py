import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result, wait_for_haul
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import stop_after_attempt, retry, retry_if_exception_type, wait_fixed


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@pytest.mark.other
@vtest
class Test_C65410859_To_Verify_the_functionality_of_Log_In_to_Confirm_CTA_on_21st_tile_input_without_any_text(Common):
    """
    TR_ID: C65410859
    NAME: To Verify the functionality of "Log In to Confirm" CTA on 21st tile input without any text.
    DESCRIPTION: To Verify the functionality of Log in to confirm CTA on 21st tile
    PRECONDITIONS: 1.User shouldn't be subscribed to Fanzone previously and should be logged out state.
    PRECONDITIONS: 2.Syc promotion page should be created in CMS.
    """
    keep_browser_open = True

    @retry(stop=stop_after_attempt(5),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), wait=wait_fixed(wait=2))
    def confirm_click(self, dialog):
        dialog.confirm_button.click()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
        PRECONDITIONS: 2) User should be logged into ladbroks
        PRECONDITIONS: 3) User not  subscribed to fanzone
        PRECONDITIONS: 4) User should be  in SYC promotion page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username

    def test_001_navigate_to_promotion_page(self):
        """
        DESCRIPTION: Navigate to Promotion page
        EXPECTED: Promotion page displayed
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

    def test_002_click_on_see_more_cta_button_for_fanzone_promotion_page(self):
        """
        DESCRIPTION: Click on see more CTA Button for fanzone promotion page
        EXPECTED: user is navigated to SYC team selection page.
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')
        wait_for_haul(2)
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()

    def test_003_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Team selection page should be displayed with all available team tiles
        """
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        wait_for_haul(3)

    def test_004_click_on_21st_tile__i_dont_support_any_of_these_teams(self):
        """
        DESCRIPTION: Click on 21st tile- i don't support any of these teams
        EXPECTED: A Free text popup should display, to tell us whom do they support
        """
        self.__class__.i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(self.i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')

    def test_005_keep_21st_tile_input_text_field_is_blank(self):
        """
        DESCRIPTION: Keep 21st tile input text field is blank
        EXPECTED: User should see CTA text to "Log in to Confirm".
        """
        wait_for_result(lambda: self.site.show_your_colors.scroll_to_we(self.i_dont_support_any_teams), timeout=10)
        wait_for_haul(3)
        self.i_dont_support_any_teams.click()
        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
            verify_name=False)

    def test_006_clicks_on_log_in_to_confirm_cta(self):
        """
        DESCRIPTION: Clicks on "Log in to Confirm" CTA
        EXPECTED: Login popup populated.
        """
        self.dialog.login_to_confirm_button.click()
        self.site._wait_for_login_dialog(timeout=30)

    def test_007_enter_valid_credentials(self):
        """
        DESCRIPTION: Enter valid credentials.
        EXPECTED: Logged in successfully and should user lands back to free text popup.
        """
        login_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        if login_dialog is None:
            raise VoltronException(f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not present on page')
        login_dialog.username = self.username
        login_dialog.password = tests.settings.default_password
        login_dialog.click_login()
        dialog_closed = login_dialog.wait_dialog_closed()
        if not dialog_closed:
            raise VoltronException('User is not logged in as Login Dialog was not closed')
        if self.site.root_app.has_timeline_overlay_tutorial(timeout=5):
            self.site.timeline_tutorial_overlay.close_icon.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=5)
        if dialog:
            dialog.close_dialog()
        if self.device_type == "mobile":
            try:
                self.site.timeline.timeline_splash_page.close_button.click()
            except VoltronException:
                pass
        wait_for_haul(3)
        i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')

    def test_008_keep_free_input_text_field_blank(self):
        """
        DESCRIPTION: Keep free input text field blank
        EXPECTED: Blank field should be highlighted in Red.
        """
        # Covered in below step

    def test_009_click_on_confirm_button_by_keeping_text_field_blank(self):
        """
        DESCRIPTION: Click on confirm button by keeping Text Field blank.
        EXPECTED: Blank field should be highlighted in Red.
        """
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
                                           timeout=30)
        self.confirm_click(dialog=dialog)
        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS)
        if self.device_type == "mobile":
            self.assertTrue(wait_for_result(lambda: self.dialog.is_underscored_red(), timeout=30),
                            msg='Free text box is not highlight in red color')

    def test_010_enter_any_team_of_user_choice_name_in_the_text_popup(self):
        """
        DESCRIPTION: Enter any team of user choice name in the text popup
        EXPECTED: User should be able to input the team of their of choice successfully
        """
        self.dialog.select_custom_team_name_input = vec.fanzone.TEAMS_LIST.arsenal
        self.assertTrue(self.dialog.select_custom_team_name_input,
                        msg='Choice name has not entered')

    def test_011_user_click_on_confirm_cta_button(self):
        """
        DESCRIPTION: User click on confirm CTA button
        EXPECTED: User should get Thank you message -"Thank you for telling us which team you support. We'll hopefully have a FANZONE for your team soon."
        """
        self.dialog.confirm_button.click()
        self.site.wait_content_state_changed()
        wait_for_haul(2)
        self.__class__.msg_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_THANK_YOU,
                                                              verify_name=False)
        self.assertTrue(self.msg_dialog, msg="Thank you message pop up is not displayed")
        self.assertEqual(self.msg_dialog.description, vec.FANZONE.THANK_YOU_MESSAGE,
                         msg=f"Actual message '{self.msg_dialog.description}' is not same as expected message '{vec.FANZONE.THANK_YOU_MESSAGE}'")

    def test_012_user_clicks_on_exit_button(self, popup_handle=True):
        """
        DESCRIPTION: User clicks on EXIT button
        EXPECTED: User should be navigate to Football landing page.
        """
        if self.msg_dialog :
            self.assertTrue(self.msg_dialog.exit_button, msg='"EXIT" CTA Button is not displayed')
            self.msg_dialog.exit_button.click()
        wait_for_haul(3)
        if popup_handle:
            dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
            if dialog_alert_email:
                dialog_alert_email.remind_me_later.click()
            wait_for_haul(3)
            dialog_alert_fanzone_game = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES)
            if dialog_alert_fanzone_game:
                dialog_alert_fanzone_game.close_btn.click()
        self.site.wait_content_state(state_name='FANZONEEVENTS')

    def test_013_user_logged_out_enter_the_url___httpstestsportsladbrokescomfanzonesport_footballshow_your_colors(self):
        """
        DESCRIPTION: User logged out, enter the URL - https://test.sports.ladbrokes.com/fanzone/sport-football/show-your-colors
        EXPECTED: User should navigated to SYC Page directly
        """
        url = f'https://{tests.HOSTNAME}/fanzone/sport-football/show-your-colours'
        self.site.logout()
        self.device.navigate_to(url=url)
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')

    def test_014_repeat_above_steps_from_3_to_12(self):
        """
        DESCRIPTION: Repeat above steps from 3 to 12.
        EXPECTED: User should be navigate to Football landing page.
        """
        self.test_003_check_team_selection_page()
        self.test_004_click_on_21st_tile__i_dont_support_any_of_these_teams()
        self.test_005_keep_21st_tile_input_text_field_is_blank()
        self.test_006_clicks_on_log_in_to_confirm_cta()
        self.test_007_enter_valid_credentials()
        self.test_008_keep_free_input_text_field_blank()
        self.test_009_click_on_confirm_button_by_keeping_text_field_blank()
        self.test_010_enter_any_team_of_user_choice_name_in_the_text_popup()
        self.test_011_user_click_on_confirm_cta_button()
        self.test_012_user_clicks_on_exit_button(popup_handle=False)
