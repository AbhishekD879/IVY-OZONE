import pytest
from time import sleep
from selenium.webdriver import ActionChains
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.Common import Common
from voltron.pages.shared import get_driver


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305004_Verify_LOGIn_CTA_button_in_popup_which_gets_after_selecting_a_team_in_select_fanzone_page_from_promotion(Common):
    """
    TR_ID: C65305004
    NAME: Verify LOGIn CTA button in  popup which gets after selecting a team in select fanzone page from  promotion
    DESCRIPTION: This test case is to verify LOGIn CTA button in  popup which gets after selecting a team in select fanzone page from  promotion
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be in logged out state
    PRECONDITIONS: 3) User should be in SYC promotions page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        User should be in SYC promotions page
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        promotions[vec.fanzone.PROMOTION_TITLE].more_info_button.click()
        # self.site.wait_content_state(state_name='PromotionDetails')

    def test_001_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: User should  be navigated to SYC team selection page
        """
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()

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
        teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        for team in teams:
            if team.name == team_name:
                self.assertTrue(team.is_highlighted(), msg='Subscribed team is not highlighted')
                break

    def test_004_check_ui_of_the_popup(self):
        """
        DESCRIPTION: check UI of the popup
        EXPECTED: The should have below:
        EXPECTED: 1) Tittle - TEAM CONFIRMATION
        EXPECTED: 2) Message: " You need to be logged in to proceed. Pleaseâ€‹ LOG IN via the button below to proceed withâ€‹ choosing your favourite team."
        EXPECTED: 3) CTA buttons: EXIT and LOGIN
        """
        sleep(5)
        self.__class__.dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)

    def test_005_click_on_exit_button(self):
        """
        DESCRIPTION: Click on EXIT button
        EXPECTED: Popup should be disappeared and user stays in team selection page
        """
        self.dialog_confirm.team_confirmation_exit_button.click()

    def test_006_select_any_team_tile(self):
        """
        DESCRIPTION: select any Team Tile
        EXPECTED: The selected team tile should be highlighted and getslogin popup
        """
        self.test_003_select_any_team_tile(team_name=vec.fanzone.TEAMS_LIST.brentford.title())
        try:
            self.test_004_check_ui_of_the_popup()
        except Exception:
            self.test_003_select_any_team_tile(team_name=vec.fanzone.TEAMS_LIST.arsenal.title())
            self.test_004_check_ui_of_the_popup()

    def test_007_click_on_remaining_portion_of_the_page(self):
        """
        DESCRIPTION: Click on remaining portion of the page
        EXPECTED: Popup should be disappeared and user stays in team selection page
        """
        ActionChains(get_driver()).move_by_offset(30, 30).click().perform()
        sleep(1)
        try:
            dialog_change_team = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM,
                                                           timeout=5)
            self.assertFalse(dialog_change_team, msg='Change team pop-up appeared, it should not appear')
        except Exception:
            pass

    def test_008_select_any_team_tile(self):
        """
        DESCRIPTION: select any Team Tile
        EXPECTED: The selected team tile should be highlighted and getslogin popup
        """
        self.test_003_select_any_team_tile(team_name=vec.fanzone.TEAMS_LIST.aston_villa.title())

    def test_009_click_on_login_button(self):
        """
        DESCRIPTION: Click on LOGIN button
        EXPECTED: User should redirected to login page
        """
        self.dialog_confirm.confirm_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        self.assertTrue(dialog, msg='Login dialog is not opened')
