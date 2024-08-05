import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C9607559_Verify_Surface_Bet_module_displaying_for_Sport_category_if_there_is_one_Surface_Bet_item(Common):
    """
    TR_ID: C9607559
    NAME: Verify Surface Bet module displaying for Sport category if there is one Surface Bet item
    DESCRIPTION: This test case verifies displaying of Surface Bets module when there is only one selection configured for the module in CMS.
    DESCRIPTION: AUTOTEST [C9776316]
    PRECONDITIONS: 1. There is a single Surface Bet added to the SLP/Homepage in CMS.
    PRECONDITIONS: 2. Content/Was price/Icon are not defined
    PRECONDITIONS: 3. Valid Selection Id is set
    PRECONDITIONS: 4. Open this SLP/Homepage in Oxygen application.
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_verify_the_single_surface_bet_displaying(self):
        """
        DESCRIPTION: Verify the single Surface Bet displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: * Surface Bet is of the regular width, centered
        EXPECTED: * Content placeholder is empty
        EXPECTED: * Was price placeholder is empty, "Was" word isn't displayed
        EXPECTED: * Title is aligned as there is no icon placeholder
        """
        pass

    def test_002_in_the_cms_edit_the_surface_bet_add_content_upload_icon_add_price_both_numerator_and_denominator(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet, add content, upload icon, add price (both numerator and denominator)
        EXPECTED: 
        """
        pass

    def test_003_in_the_application_refresh_the_categoryhomepage_pageverify_the_single_surface_bet_displaying(self):
        """
        DESCRIPTION: In the application: Refresh the category/homepage page
        DESCRIPTION: Verify the single Surface Bet displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Icon, uploaded in the CMS
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: >* Content, defined in the CMS
        EXPECTED: >* Price, defined in the CMS (Coral: price is struck through; Ladbrokes: "Was" and price are struck through)
        EXPECTED: * Surface Bet is fit the full width of the screen
        """
        pass

    def test_004_verify_price_and_was__word_are_not_displayed_if_the_following_conditions_numerator_isnt_set_and_denominator_is_set_numerator_is_set_and_denominator_isnt_set(self):
        """
        DESCRIPTION: Verify price and "Was " word are not displayed if the following conditions:
        DESCRIPTION: * Numerator isn't set and denominator is set
        DESCRIPTION: * Numerator is set and denominator isn't set
        EXPECTED: Price and "Was " word are not displayed if numerator or denominator are not defined
        """
        pass

    def test_005_verify_the_long_title_is_shortened_properly(self):
        """
        DESCRIPTION: Verify the long title is shortened properly
        EXPECTED: Long title is shortened and fits the Title area
        """
        pass

    def test_006_verify_content_with_a_long_text_is_shown_properly(self):
        """
        DESCRIPTION: Verify content with a long text is shown properly
        EXPECTED: The height of the Surface Bet card is increased to fit the text
        EXPECTED: Content is properly shown within the Content area
        EXPECTED: All the Surface Bets are of the same size
        """
        pass
