import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.promotions_banners_offers
@vtest
class Test_C62171808_Verify_display_of_Bet_Pack_Enabler_BMA_button_option_in_create_promotions_page(Common):
    """
    TR_ID: C62171808
    NAME: Verify display of Bet Pack Enabler BMA button option in create promotions page
    DESCRIPTION: This test case verifies display of Bet Pack Enabler BMA button option in 'create bma button' dropdown inside description field in create promotions page
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Login to CMS
    """
    keep_browser_open = True

    def test_001_click_on_promotions_tab(self):
        """
        DESCRIPTION: Click on 'Promotions' tab
        EXPECTED: Below sub menu fields are displayed
        EXPECTED: * Promotions
        EXPECTED: * Sections
        """
        pass

    def test_002_click_on_promotions_in_sub_menu_and_tap_on_create_promotion_cta(self):
        """
        DESCRIPTION: Click on 'Promotions' in sub menu and tap on create promotion CTA
        EXPECTED: Promotion detailed page is displayed
        """
        pass

    def test_003_tap_on_create_bma_button_in_description_field_and_verify_bet_pack_enabler_button_option(self):
        """
        DESCRIPTION: Tap on 'Create bma button' in Description field and verify 'Bet Pack Enabler Button' option
        EXPECTED: 'Bet Pack Enabler Button' option should be displayed
        """
        pass
