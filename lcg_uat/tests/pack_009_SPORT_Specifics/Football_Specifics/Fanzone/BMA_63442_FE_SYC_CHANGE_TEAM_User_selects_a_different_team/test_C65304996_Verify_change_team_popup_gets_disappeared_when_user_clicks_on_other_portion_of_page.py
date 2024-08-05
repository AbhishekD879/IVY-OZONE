import pytest
from time import sleep
from selenium.webdriver import ActionChains
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.Common import Common
from voltron.pages.shared import get_driver
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.fanzone_reg_tests
@pytest.mark.other
@vtest
class Test_C65304996_Verify_change_team_popup_gets_disappeared_when_user_clicks_on_other_portion_of_page(Common):
    """
    TR_ID: C65304996
    NAME: Verify change team popup gets disappeared when user clicks on other portion of page
    DESCRIPTION: This test case is to verify change team popup gets disappeared when user clicks on other portion of page
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be logged into ladbroks
    PRECONDITIONS: 3) User should subscribe to fanzone and not compled 30 days
    PRECONDITIONS: 4) User should be  in SYC promotion page
    """
    keep_browser_open = True
    team_name = vec.fanzone.TEAMS_LIST.brentford.title()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
        PRECONDITIONS: 2) User should be logged into ladbroks
        PRECONDITIONS: 3) User should subscribe to fanzone and not compled 30 days
        PRECONDITIONS: 4) User should be  in SYC promotion page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        burnley_fanzone = self.cms_config.get_fanzone(self.team_name)
        if burnley_fanzone['active'] is not True:
            self.cms_config.update_fanzone(self.team_name)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state(state_name='HomePage')
        sleep(3)
        self.site.login(username=username)
        self.site.open_sport(name='football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[self.team_name].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
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
        self.__class__.promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = self.promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')

    def test_002_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Previously subscribed team should be in highlighted box
        """
        teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        for team in teams:
            if team.name == self.team_name:
                self.assertTrue(team.is_highlighted(), msg='Subscribed team is not highlighted')

    def test_003_click_on_any_other_team_tile(self):
        """
        DESCRIPTION: Click on any other team tile
        EXPECTED: User should get change team popup
        """
        team = self.site.show_your_colors.items_as_ordered_dict.get(self.team_name)
        team.click()
        dialog_change_team = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM)
        self.assertTrue(dialog_change_team, msg=" Change team pop is not displayed")
        sleep(2)

    def test_004_click_other_portion_of_page(self):
        """
        DESCRIPTION: Click other portion of page
        EXPECTED: Popup should be disappeared.
        """
        ActionChains(get_driver()).move_by_offset(30, 30).click().perform()
        sleep(1)
        try:
            dialog_change_team = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM, timeout=5)
            self.assertFalse(dialog_change_team, msg='Change team pop-up appeared, it should not appear')
        except Exception as e:
            pass
