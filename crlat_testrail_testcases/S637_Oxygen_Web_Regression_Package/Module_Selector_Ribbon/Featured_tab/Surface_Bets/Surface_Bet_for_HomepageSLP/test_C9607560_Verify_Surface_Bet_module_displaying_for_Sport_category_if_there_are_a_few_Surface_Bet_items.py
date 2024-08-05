import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.homepage_featured
@vtest
class Test_C9607560_Verify_Surface_Bet_module_displaying_for_Sport_category_if_there_are_a_few_Surface_Bet_items(Common):
    """
    TR_ID: C9607560
    NAME: Verify Surface Bet module displaying for Sport category if there are a few Surface Bet items
    DESCRIPTION: This test case verifies displaying of Surface Bets module when there is a few selections configured for the module in CMS.
    DESCRIPTION: AUTOTEST [C9858656]
    PRECONDITIONS: 1. There are a few Surface Bets added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Content/Was price/Icon for one Surface Bet are not defined
    PRECONDITIONS: 2. Content/Was price/Icon for one Surface Bet are defined
    PRECONDITIONS: 3. Valid Selection Ids are set
    PRECONDITIONS: 4. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_verify_the_surface_bet_carousel(self):
        """
        DESCRIPTION: Verify the Surface Bet carousel
        EXPECTED: * Full first SB card and ~1/4 of the following card are shown
        EXPECTED: * Carousel can be smoothly swiped to the left/right
        """
        pass

    def test_002_verify_the_surface_bet_without_contentwas_priceicon_displaying(self):
        """
        DESCRIPTION: Verify the Surface Bet without Content/Was price/Icon displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: * Content placeholder is empty
        EXPECTED: * Was price placeholder is empty, "Was" word isn't displayed
        EXPECTED: * Title is aligned as there is no icon placeholder
        """
        pass

    def test_003_verify_the_surface_bet_with_contentwas_priceicon_displaying(self):
        """
        DESCRIPTION: Verify the Surface Bet with Content/Was price/Icon displaying
        EXPECTED: * Surface Bet card contains elements:
        EXPECTED: >* Icon, uploaded in the CMS
        EXPECTED: >* Title (Ladbrokes: on the orange background), defined in the CMS
        EXPECTED: >* Price button, price is loaded from the TI
        EXPECTED: >* Content, defined in the CMS
        EXPECTED: >* Price, defined in the CMS (Coral: price is struck through; Ladbrokes: "Was" and price are struck through)
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
