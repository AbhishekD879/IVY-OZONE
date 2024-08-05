import pytest
from time import sleep
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305414_Verify_user_gets_a_login_popup_after_selecting_a_team_in_team_selection_page_from_promotion(Common):
    """
    TR_ID: C65305414
    NAME: Verify user gets a login popup after selecting a team in team selection page from  promotion
    DESCRIPTION: This test case is to verify user gets a login popup after selecting a team in team selection page from  promotion
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
        PRECONDITIONS: 2) User should be in logged out state
        PRECONDITIONS: 3) User should be in SYC promotions page
        """
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        # username = self.gvc_wallet_user_client.register_new_user().username
        # self.site.login(username=username)
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
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')

    def test_002_check_team_selection_page(self):
        """
        DESCRIPTION: Check Team selection page
        EXPECTED: Team selection page should be diaplyed with all available team tiles
        """
        teams = self.site.show_your_colors.items_as_ordered_dict
        self.assertTrue(teams, msg='Team Selection page is not opened')

    def test_003_select_any_other_team_tile(self):
        """
        DESCRIPTION: Select any other team tile
        EXPECTED: The selected team tile should be highlighted and gets confiramtion popup
        """
        team = self.site.show_your_colors.items_as_ordered_dict.get(vec.fanzone.TEAMS_LIST.brentford.title())
        team.click()
        sleep(4)
        dialog_confirm = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION,
            verify_name=False)
        self.assertTrue(dialog_confirm,
                        msg='login popup not appeared')
