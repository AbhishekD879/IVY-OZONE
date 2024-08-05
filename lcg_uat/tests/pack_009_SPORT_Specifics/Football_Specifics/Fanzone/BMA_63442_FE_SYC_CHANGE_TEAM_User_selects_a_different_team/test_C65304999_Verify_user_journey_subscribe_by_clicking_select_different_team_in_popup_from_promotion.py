import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.other
@pytest.mark.high
@pytest.mark.fanzone_reg_tests
@pytest.mark.desktop
@vtest
class Test_C65304999_Verify_user_journey_to_subscribe_fanzone_by_clicking_on_select_different_team_in_confiramtion_popup_from_SYC_promotion_page_for_a_logged_in_user(Common):
    """
    TR_ID: C65304999
    NAME: Verify user journey to subscribe fanzone  by clicking on  "select different team" in confiramtion popup from SYC promotion page for a logged in user
    DESCRIPTION: This test case is to verify user journey to subscribe fanzone  by clicking on  "select different team" in confiramtion popup from SYC promotion page for a logged iin user
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be logged into ladbroks
    PRECONDITIONS: 3) User not  subscribed to fanzone
    PRECONDITIONS: 4) User should be  in SYC promotion page
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
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
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
        #self.site.wait_content_state(state_name='PromotionDetails')

    def test_002_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Team selection page should be diaplyed with all available team tiles
        """
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        sleep(3)

    def test_003_select_any_other_team_tile(self):
        """
        DESCRIPTION: Select any other team tile
        EXPECTED: The selected team tile should be highlighted and gets confiramtion popup
        """
        team = self.site.show_your_colors.items_as_ordered_dict.get(vec.fanzone.TEAMS_LIST.brentford.title())
        team.click()
        self.__class__.dialog_confirm = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION,
            verify_name=False)
        self.assertTrue(self.dialog_confirm,
                        msg='login popup not appeared')

    def test_004_click_on_select_different_team(self):
        """
        DESCRIPTION: Click on SELECT DIFFERENT TEAM
        EXPECTED: User should be navigated to SYC team selection page
        """
        self.dialog_confirm.select_different_button.click()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')

    def test_005_select_any_other_team_tile(self):
        """
        DESCRIPTION: Select any other team tile
        EXPECTED: The selected team tile should be highlighted and gets confiramtion popup
        """
        team = self.site.show_your_colors.items_as_ordered_dict.get(vec.fanzone.TEAMS_LIST.chelsea.title())
        team.click()
        dialog_confirm = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION,
            verify_name=False)
        self.assertTrue(dialog_confirm, msg='login popup not appeared')

    def test_006_click_on_confirm_button(self):
        """
        DESCRIPTION: Click on confirm Button
        EXPECTED: Desktop:
        EXPECTED: User selection will store in BE and User navigate to SYC promotion page
        EXPECTED: Mobile:
        EXPECTED: User selection will store in BE and User navigate to preference centre screen
        """
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(2)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()
        # self.site.wait_content_state(state_name='football') as per the new change, after subscription, we will be in fanzone page only
