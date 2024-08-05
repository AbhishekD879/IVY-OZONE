import pytest
from tests.base_test import vtest
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304995_Veriy_change_team_popup_UI(Common):
    """
    TR_ID: C65304995
    NAME: Veriy change team popup UI
    DESCRIPTION: This test case is to verify change team popup UI
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be logged into ladbroks
    PRECONDITIONS: 3) User should subscribe to fanzone and not compled 30 days
    PRECONDITIONS: 4) User should be  in SYC promotion page
    """
    keep_browser_open = True

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
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=30)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='SYC is displayed',
                        timeout=5)
        teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        teams[1].scroll_to_we()
        teams[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
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
        self.__class__.teams = list(self.site.show_your_colors.items_as_ordered_dict.values())
        self.assertTrue(self.teams[1].is_highlighted(), msg='Subscribed team is not highlighted')

    def test_003_click_on_any_other_team_tile(self):
        """
        DESCRIPTION: Click on any other team tile
        EXPECTED: User should get change team popup
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        for team_name, team in teams.items():
            if team_name != self.teams[1]:
                team.click()
                break

    def test_004_check_change_team_popup_ui(self):
        """
        DESCRIPTION: Check change team popup UI
        EXPECTED: Popup should have below:
        EXPECTED: 1. Tittle : "Change Team"
        EXPECTED: 2. Message: " You signed upâ€‹less than 30 days ago you will need toâ€‹ wait until the 30 days expire to change your team.â€‹"
        EXPECTED: 3. CTA button:  "EXIT"
        """
        dialog_change_team = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM)
        self.assertTrue(dialog_change_team, msg=" Change team pop is not displayed")
        self.assertEqual(dialog_change_team.name, vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM, msg=f'Actual title "{dialog_change_team.name}" is not same as Expected title "{vec.dialogs.DIALOG_MANAGER_CHANGE_TEAM}"')
        self.assertEqual(dialog_change_team.description, vec.fanzone.CHANGE_TEAM_MESSAGE, msg=f'Actual change team message "{dialog_change_team.description}" is not same as Expected change team message "{vec.fanzone.CHANGE_TEAM_MESSAGE}"')
        self.assertTrue(dialog_change_team.exit_button, msg=" EXIT button is not displayed")
