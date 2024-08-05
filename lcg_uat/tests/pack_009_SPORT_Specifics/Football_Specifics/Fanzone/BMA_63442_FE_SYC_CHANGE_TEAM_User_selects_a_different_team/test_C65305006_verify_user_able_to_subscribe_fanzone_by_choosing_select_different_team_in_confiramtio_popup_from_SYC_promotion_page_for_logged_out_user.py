import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65305006_verify_user_able_to_subscribe_fanzone_by_choosing_select_different_team_in_confiramtio_popup_from_SYC_promotion_page_for_logged_out_user(Common):
    """
    TR_ID: C65305006
    NAME: verify user able to subscribe fanzone  by choosing 'select different team" in confiramtio popup from SYC promotion page for logged out user
    DESCRIPTION: This test case is to verify user able to subscribe fanzone  by choosing 'select different team" in confiramtio popup from SYC promotion page for logged out user
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be in logged out state
    PRECONDITIONS: 3) User should be in SYC promotions page
    PRECONDITIONS: 4) User not subscribed to fanzone
    """
    keep_browser_open = True

    def test_001_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: User should  be navigated to SYC team selection page
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions', timeout=20)
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        sleep(3)

    def test_002_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Team selection page should be diaplyed with all available team tiles
        """
        self.__class__.teams = self.site.show_your_colors.items_as_ordered_dict
        self.assertTrue(self.teams, msg='Team tiles are not displayed')

    def test_003_select_any_team_tile(self, team_name=vec.fanzone.TEAMS_LIST.aston_villa.title()):
        """
        DESCRIPTION: Select any team tile
        EXPECTED: The selected team tile should be highlighted and getslogin popup
        """
        self.teams[team_name].scroll_to_we()
        self.teams[team_name].click()
        sleep(3)

    def test_004_click_on_login_button(self):
        """
        DESCRIPTION: Click on LOGIN button
        EXPECTED: User should redirected to login page
        """
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        self.assertTrue(self.dialog, msg='Login dialog is not opened')

    def test_005_enter_user_name_and_password_and_login(self):
        """
        DESCRIPTION: Enter user name and password and login
        EXPECTED: user should be logged in and  user gets a coonfirmation password
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed(timeout=15)
        self.assertTrue(dialog_closed, msg='Login dialog is not closed yet')
        if self.site.root_app.has_loss_limit_dialog(timeout=2, expected_result=True):
            self.site.loss_limit_dialog.im_happy_with_limit.click()
        try:
            self.site.close_all_dialogs(async_close=False)
        except Exception as e:
            self._logger.warning(e)
        if self.site.root_app.has_timeline_overlay_tutorial(timeout=2, expected_result=True):
            self.site.timeline_tutorial_overlay.close_icon.click()

    def test_006_click_on_select_different_team(self):
        """
        DESCRIPTION: Click on SELECT DIFFERENT TEAM
        EXPECTED: User should be navigated to SYC team selection page
        """
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.select_different_button.click()
        sleep(3)

    def test_007_select_any_other_team_tile(self):
        """
        DESCRIPTION: Select any other team tile
        EXPECTED: The selected team tile should be highlighted and gets confiramtion popup
        """
        self.test_002_check_team_selection_page()
        self.test_003_select_any_team_tile(team_name=vec.fanzone.TEAMS_LIST.manchester_united.title())

    def test_008_click_on_confirm_button(self):
        """
        DESCRIPTION: Click on confirm Button
        EXPECTED: Desktop:
        EXPECTED: User selection will store in BE and User navigate to SYC promotion page
        EXPECTED: Mobile:
        EXPECTED: User selection will store in BE and User navigate to preference centre screen
        """
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=10,
                        name='"Fanzone tab menus" to be displayed.')
