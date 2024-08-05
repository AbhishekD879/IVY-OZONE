import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result, wait_for_haul
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl # not configured in prod and Beta
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone_reg_tests
@pytest.mark.desktop
@vtest
class Test_C65305011_verify_change_team_for_a_logged_out_user_who_have_not_completed_30_days_from_fanzone_subscription(Common):
    """
    TR_ID: C65305011
    NAME: verify  change team  for a logged out user who have not completed 30 days from fanzone subscription
    DESCRIPTION: This test case is to verify change team  for a logged out user who have not completed 30 days from fanzone subscription
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be in logged out state
    PRECONDITIONS: 3) User should be in SYC promotions page
    PRECONDITIONS: 4) User subscribed to fanzone and user not complete 30 days
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
        PRECONDITIONS: 2) User should be in logged out state
        PRECONDITIONS: 3) User should be in SYC promotions page
        PRECONDITIONS: 4) User subscribed to fanzone and user not complete 30 days
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='OK button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        wait_for_haul(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        wait_for_haul(3)
        dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
        dialog_alert_email.remind_me_later.click()
        wait_for_haul(3)
        dialog_alert_fanzone_game = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FANZONE_GAMES)
        dialog_alert_fanzone_game.close_btn.click()
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

    def test_001_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: User should  be navigated to SYC team selection page
        """
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')

    def test_002_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Previously subscribed team should be in highlighted box
        """
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        wait_for_haul(3)

    def test_003_select_any_other_team_tile(self):
        """
        DESCRIPTION: Select any other team tile
        EXPECTED: The selected team tile should be highlighted and gets login popup
        """
        team = self.site.show_your_colors.items_as_ordered_dict.get(vec.fanzone.TEAMS_LIST.brentford.title())
        team.click()
        dialog_confirm = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION,
            verify_name=False)
        self.assertTrue(dialog_confirm,
                        msg='Team Confirmation popup not appeared')
        dialog_confirm.confirm_button.click()
        wait_for_haul(3)

    def test_004_click_on_login_button(self):
        """
        DESCRIPTION: Click on LOGIN button
        EXPECTED: User should redirected to login page
        """
        self.__class__.dialog_login = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog_login, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')

    def test_005_enter_user_name_and_password_and_login(self):
        """
        DESCRIPTION: Enter user name and password and login
        EXPECTED: user should be logged in and  user gets a coonfirmation password
        """
        self.dialog_login.username = self.username
        self.dialog_login.password = tests.settings.default_password
        self.dialog_login.click_login()
        dialog_closed = self.dialog_login.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')

    def test_006_user_should_get_change_team_popup(self):
        """
        DESCRIPTION: User should get change team popup
        EXPECTED: Popup should have below:
        EXPECTED: 1. Tittle : "Change Team"
        EXPECTED: 2. Message: " You signed upâ€‹less than 30 days ago you will need toâ€‹ wait until the 30 days expire to change your team.â€‹"
        EXPECTED: 3. CTA button:  "EXIT"
        """
        self.__class__.dialog_change_team = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM)
        self.assertTrue(self.dialog_change_team,
                        msg=f'"{vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM}" dialog is not displayed')
        self.assertEqual(self.dialog_change_team.description, vec.fanzone.CHANGE_TEAM_MESSAGE,
                         msg=f'Actual change team message "{self.dialog_change_team.description}" is not same as Expected change team message "{vec.fanzone.CHANGE_TEAM_MESSAGE}"')
        self.assertTrue(self.dialog_change_team.exit_button, msg=" EXIT button is not displayed")

    def test_007_click_on_exit__button(self):
        """
        DESCRIPTION: Click on exit  button
        EXPECTED: Popup should be disappeared.
        """
        self.dialog_change_team.exit_button.click()
        dialog_closed = self.dialog_change_team.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Change Team dialog was not closed')
