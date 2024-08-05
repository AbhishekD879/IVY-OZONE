import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C62171815_Verify_display_of_Mark_this_promotion_as_Bet_Pack_Enabler_checkbox(Common):
    """
    TR_ID: C62171815
    NAME: Verify display of 'Mark this promotion as Bet Pack Enabler' checkbox
    DESCRIPTION: This test case verifies display of 'Mark this promotion as Bet Pack Enabler' checkbox below to description field in promotions page
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
        EXPECTED: * Ok and cancel CTA
        """
        pass

    def test_005_click_on_ok_button_on_the_creation_of_bet_pack_enabler_pop_up(self):
        """
        DESCRIPTION: Click on 'OK' button on the creation of 'Bet Pack Enabler' pop-up
        EXPECTED: 'Bet Pack Enabler' button is added into description field
        """
        pass

    def test_006_verify_the_display_of_mark_this_promotion_as_betpack_enabler_checkbox(self):
        """
        DESCRIPTION: Verify the display of 'Mark this promotion as BetPack Enabler' checkbox
        EXPECTED: 'Mark this promotion as BetPack Enabler' checkbox should be displayed as uncheck by default below to description field
        """
        pass

    def test_007_checkuncheck_the_mark_this_promotion_as_betpack_enabler_checkbox(self):
        """
        DESCRIPTION: Check/Uncheck the 'Mark this promotion as BetPack Enabler' checkbox
        EXPECTED: User should be able to check/uncheck the confirmation Pop up checkbox
        """
        pass

    def test_008_check_the_mark_this_promotion_as_betpack_enabler_checkbox_and_verify_the_confirmation_pop_up_and_verify_the_fields(self):
        """
        DESCRIPTION: Check the 'Mark this promotion as BetPack Enabler' checkbox and verify the Confirmation Pop up and verify the fields
        EXPECTED: Below fields should be displayed
        EXPECTED: * Text
        EXPECTED: * Congrats Message
        EXPECTED: * OB Promotion ID
        EXPECTED: * Trigger Ids
        EXPECTED: * Value
        EXPECTED: * Low funds
        EXPECTED: * Non Logged In
        EXPECTED: * Error message
        EXPECTED: * Message field below to (Low funds, Non Logged In and error message)
        """
        pass

    def test_009_uncheck_the_mark_this_promotion_as_betpack_enabler_checkbox_and_verify_the_fields(self):
        """
        DESCRIPTION: Uncheck the 'Mark this promotion as BetPack Enabler' checkbox and verify the fields
        EXPECTED: Below fields should not be displayed
        EXPECTED: * Text
        EXPECTED: * Congrats Message
        EXPECTED: * OB Promotion ID
        EXPECTED: * Trigger Ids
        EXPECTED: * Value
        EXPECTED: * Low funds
        EXPECTED: * Non Logged In
        EXPECTED: * Error message
        EXPECTED: * Message field below to (Low funds, Non Logged In and error message)
        """
        pass
