import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_test_C65654500_To_verify_the_functionality_of_Log_In_to_Confirm_CTA_on_21st_tile_with_input_data(Common):
    """
    TR_ID: C65410859
    NAME: To Verify the functionality of "Log In to Confirm" CTA on 21st tile input without any text.
    DESCRIPTION: To Verify the functionality of Log in to confirm CTA on 21st tile
    PRECONDITIONS: 1.User shouldn't be subscribed to Fanzone previously and should be logged out state.
    PRECONDITIONS: 2.Syc promotion page should be created in CMS.
    """
    keep_browser_open = True

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
        sleep(2)
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
        sleep(3)

    def test_004_click_on_21st_tile__i_dont_support_any_of_these_teams(self):
        """
        DESCRIPTION: Click on 21st tile- i don't support any of these teams
        EXPECTED: A Free text popup should display, to tell us whom do they support
        """
        self.__class__.i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(self.i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')

    def test_005_enter_some_text_into_the_filed(self):
        """
        DESCRIPTION: Enter some text into the filed
        EXPECTED: User should see CTA text to "Log in to Confirm".
        """
        wait_for_result(lambda: self.site.show_your_colors.scroll_to_we(self.i_dont_support_any_teams), timeout=10)
        sleep(5)
        self.i_dont_support_any_teams.click()
        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
            verify_name=False)

        self.dialog.select_custom_team_name_input = vec.fanzone.TEAMS_LIST.arsenal
        self.assertTrue(self.dialog.select_custom_team_name_input,
                        msg='Choice name has not entered')

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
        EXPECTED: Logged in successfully and the 21st tile input field text still persists and shouldn't revert back to being blank.
        """
        login_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        if login_dialog is None:
            raise VoltronException(f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not present on page')
        login_dialog.username = self.username
        login_dialog.password = tests.settings.default_password
        login_dialog.click_login()
        sleep(2)
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=10)
        if dialog:
            dialog.close_dialog()
        if self.device_type == "mobile":
            try:
                self.site.timeline.timeline_splash_page.close_button.click()
            except VoltronException:
                pass
        i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')

    def test_008_Click_on_confirm_button(self):
        """
        DESCRIPTION: Click on confirm button
        EXPECTED: User should get Thank you message -"Thank you for telling us which team you support. We'll hopefully have a FANZONE for your team soon..
        """
        sleep(5)
        self.dialog.confirm_button.click()
        self.site.wait_content_state_changed()
        sleep(2)
        self.__class__.msg_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_THANK_YOU,
                                                              verify_name=False)
        self.assertTrue(self.msg_dialog, msg="Thank you message pop up is not displayed")
        self.assertEqual(self.msg_dialog.description, vec.FANZONE.THANK_YOU_MESSAGE,
                         msg=f"Actual message '{self.msg_dialog.description}' is not same as expected message '{vec.FANZONE.THANK_YOU_MESSAGE}'")

    def test_009_user_clicks_on_exit_button(self):
        """
        DESCRIPTION: User clicks on EXIT button.
        EXPECTED: User should be navigate to Football landing page
        """
        self.assertTrue(self.msg_dialog.exit_button, msg='"EXIT" CTA Button is not displayed')
        self.msg_dialog.exit_button.click()
        sleep(2)
        self.site.wait_content_state(state_name="football")
