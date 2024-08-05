import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl # not configured in prod and Beta
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305007_Verify_user_able_to_subscribe_for_I_DONT_SUPPORT_TEAM_from_SY_promo_for_loggedout_user(Common):
    """
    TR_ID: C65305007
    NAME: Verify user able to subscribe for I DON'T SUPPORT AN OF THE TEAM  from SY promotion  for logged out user
    DESCRIPTION: This test case is to verify user able to subscribe for I DON'T SUPPORT AN OF THE TEAM  from SY promotion  for logged out user
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be in logged out state
    PRECONDITIONS: 3) User should be in SYC promotions page
    PRECONDITIONS: 4) User not subscribed to fanzone
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
        PRECONDITIONS: 2) User should be in logged out state
        PRECONDITIONS: 3) User should be in SYC promotions page
        PRECONDITIONS: 4) User not subscribed to fanzone
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        promotions = self.cms_config.get_promotions()
        syc_promo = list(filter(lambda param: param['title'] == vec.fanzone.PROMOTION_TITLE.title(), promotions))
        self.assertTrue(syc_promo, msg='"SYC Promotions"is not configured in cms')
        self.__class__.syc_description = \
            list(filter(lambda param: param['title'] == vec.fanzone.PROMOTION_TITLE.title(), promotions))[0][
                'description']
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')

    def test_001_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: User should  be navigated to SYC team selection page
        """
        promotion_details = self.site.promotion_details.tab_content.promotion
        fanzone_syc_button = promotion_details.detail_description.fanzone_syc_button
        self.assertIn(vec.fanzone.FANZONE_SYC, self.syc_description,
                      msg=f'{vec.fanzone.FANZONE_SYC} CTA Button is Expected: ", '
                          f'but actual CTA button is not same in: "{self.syc_description}"')
        fanzone_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')

    def test_002_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Team selection page should be diaplyed with all available team tiles
        """
        # covered in step 1

    def test_003_select_i_dont_select_any_of_the_team(self):
        """
        DESCRIPTION: Select I DONT SELECT ANY OF THE TEAM
        EXPECTED: The selected team tile should be highlighted and gets login popup
        """
        i_dont_support_any_teams = self.site.show_your_colors.i_dont_support_any_teams
        self.assertTrue(i_dont_support_any_teams, msg='"I dont support any teams" is not displayed')
        wait_for_result(lambda: self.site.show_your_colors.scroll_to_we(i_dont_support_any_teams), timeout=10)
        sleep(5)
        i_dont_support_any_teams.click()
        dialog_confirm = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
            verify_name=False)
        sleep(5)
        self.assertTrue(dialog_confirm,
                        msg='Team Confirmation popup not appeared')
        dialog_confirm.login_to_confirm_button.click()

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
        sleep(5)
        self.dialog_login.username = self.gvc_wallet_user_client.register_new_user().username
        self.dialog_login.password = tests.settings.default_password
        self.dialog_login.click_login()
        dialog_closed = self.dialog_login.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')
        if self.site.root_app.has_loss_limit_dialog(timeout=2, expected_result=True):
            self.site.loss_limit_dialog.im_happy_with_limit.click()
        try:
            self.site.close_all_dialogs(async_close=False)
        except Exception as e:
            self._logger.warning(e)
        if self.site.root_app.has_timeline_overlay_tutorial(timeout=2, expected_result=True):
            self.site.timeline_tutorial_overlay.close_icon.click()

    def test_006_click_on_confirm_button_on_confirmation_page(self):
        """
        DESCRIPTION: Click on confirm Button on confirmation page
        EXPECTED: Desktop:
        EXPECTED: User selection will store in BE and User navigate to SYC promotion page
        EXPECTED: Mobile:
        EXPECTED: User selection will store in BE and User navigate to preference centre screen
        """
        dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_DONT_SUPPORT_ANY_OF_THESE_TEAMS,
            verify_name=False)
        dialog.select_custom_team_name_input = 'ABC'
        self.assertTrue(dialog.select_custom_team_name_input,
                        msg='Choice name has not entered')
        dialog.confirm_button.click()
        self.site.wait_content_state_changed()
        sleep(2)
        msg_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_THANK_YOU,
                                               verify_name=False)
        self.assertTrue(msg_dialog, msg="Thank you message pop up is not displayed")
        self.assertEqual(msg_dialog.description, vec.FANZONE.THANK_YOU_MESSAGE,
                         msg=f"Actual message '{msg_dialog.description}' is not same as expected message '{vec.FANZONE.THANK_YOU_MESSAGE}'")
        self.assertTrue(msg_dialog.exit_button, msg='"EXIT" CTA Button is not displayed')
        msg_dialog.exit_button.click()
        sleep(2)
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=10,
                        name='"Fanzone tab menus" to be displayed.')
