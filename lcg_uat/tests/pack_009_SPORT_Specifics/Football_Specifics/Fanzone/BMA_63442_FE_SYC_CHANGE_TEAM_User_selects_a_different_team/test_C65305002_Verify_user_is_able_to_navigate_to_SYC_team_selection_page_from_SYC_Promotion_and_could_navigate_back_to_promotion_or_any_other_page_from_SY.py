import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65305002_Verify_user_is_able_to_navigate_to_SYC_team_selection_page_from_SYC_Promotion_and_could_navigate_back_to_promotion_or_any_other_page_from_SYC_team_selection_page_for_a_logged_out_user(Common):
    """
    TR_ID: C65305002
    NAME: Verify user is able to navigate to SYC team selection page from SYC Promotion and could navigate back to promotion or any other page from SYC team selection page for a logged out user
    DESCRIPTION: This test case is to verify  user is able to navigate to SYC team selection page from SYC Promotion and could navigate back to promotion or any other page from SYC team selection page for a logged out user
    PRECONDITIONS: 1) In CMS- SYC Promotion should be configured to get SYC team selection page from promotion.
    PRECONDITIONS: 2) User should be in logged out state
    PRECONDITIONS: 3) User should be in promotions page
    """
    keep_browser_open = True

    def test_001_open_syc_promotion(self):
        """
        DESCRIPTION: Open SYC promotion
        EXPECTED: SYC promotion should be open
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions', timeout=20)
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promo = promotions[vec.fanzone.PROMOTION_TITLE]
        promo.more_info_button.click()
        self.site.wait_content_state(state_name='PromotionDetails')

    def test_002_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: User should  be navigated to SYC team selection page
        """
        promotion_details = self.site.promotion_details.tab_content.promotion
        fz_syc_button = promotion_details.detail_description.fanzone_syc_button
        fz_syc_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.show_your_colors, msg='Team Selection page is not opened')
        sleep(3)

    def test_003_click_on_back_button_on_team_selection_page(self):
        """
        DESCRIPTION: Click on back button on team selection page
        EXPECTED: user should be navigated back to SYC promotion
        """
        if self.device_type != "mobile":
            back_button = self.site.show_your_colors.back_button
            self.assertTrue(back_button, msg="Back Button in sys page is not displayed")
        else:
            back_button = self.site.header.back_button
            self.assertTrue(back_button, msg="Back Button in sys page is not displayed")
        back_button.click()
        self.site.wait_content_state(state_name='PromotionDetails')

    def test_004_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: user should be navigated to SYC team selection page
        """
        self.test_002_click_on_cta_button_in_promotion()

    def test_005_click_on_horseracing(self):
        """
        DESCRIPTION: Click on horseracing
        EXPECTED: user should navigate to HR landing page
        """
        self.navigate_to_page("horse-racing")
        self.site.wait_content_state("HorseRacing", timeout=20)

    def test_006_go_to_promotions_and_open_syc_promotion(self):
        """
        DESCRIPTION: Go to promotions and open SYC promotion
        EXPECTED: SYC promotion should be open
        """
        self.test_001_open_syc_promotion()

    def test_007_click_on_cta_button_in_promotion(self):
        """
        DESCRIPTION: Click on CTA button in promotion
        EXPECTED: user should be navigated to SYC team selection page
        """
        self.test_002_click_on_cta_button_in_promotion()

    def test_008_repeate_step_no_56__7_with_other_sport_pages(self):
        """
        DESCRIPTION: Repeate step no 5,6 & 7 with other sport pages
        EXPECTED:
        """
        self.navigate_to_page('sport/tennis')
        self.site.wait_content_state(state_name='tennis', timeout=20)
        self.test_001_open_syc_promotion()
        self.test_002_click_on_cta_button_in_promotion()
