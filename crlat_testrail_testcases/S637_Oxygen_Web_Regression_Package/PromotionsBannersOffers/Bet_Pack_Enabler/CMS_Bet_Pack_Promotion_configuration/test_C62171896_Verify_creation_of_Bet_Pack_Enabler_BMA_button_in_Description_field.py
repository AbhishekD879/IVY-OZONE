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
class Test_C62171896_Verify_creation_of_Bet_Pack_Enabler_BMA_button_in_Description_field(Common):
    """
    TR_ID: C62171896
    NAME: Verify creation of Bet Pack Enabler BMA button in Description field
    DESCRIPTION: This test case verifies creation of Bet Pack Enabler BMA button in Description field in promotion page
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

    def test_004_select_bet_pack_enabler_button(self):
        """
        DESCRIPTION: Select 'Bet Pack Enabler Button'
        EXPECTED: Pop-up to create 'Bet Pack Enabler' button appears with the below fields
        EXPECTED: * Url
        EXPECTED: * Text to display
        EXPECTED: * Target'
        EXPECTED: * Ok and Cancel CTA
        """
        pass

    def test_005_click_on_ok_button_on_the_creation_of_bet_pack_enabler_pop_up(self):
        """
        DESCRIPTION: Click on 'OK' button on the creation of 'Bet Pack Enabler' pop-up
        EXPECTED: 'Bet Pack Enabler' button is added into description field
        """
        pass

    def test_006_click_on_cancel_button_on_the_creation_of_bet_pack_enabler_pop_up(self):
        """
        DESCRIPTION: Click on 'cancel' button on the creation of 'Bet Pack Enabler' pop-up
        EXPECTED: 'Bet Pack Enabler' pop up should be closed and 'Bet Pack Enabler' button should be added into description field
        """
        pass
