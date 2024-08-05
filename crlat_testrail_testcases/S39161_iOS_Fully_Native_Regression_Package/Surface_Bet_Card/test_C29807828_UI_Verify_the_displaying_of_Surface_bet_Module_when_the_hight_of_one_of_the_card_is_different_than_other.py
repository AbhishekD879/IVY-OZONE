import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.native
@vtest
class Test_C29807828_UI_Verify_the_displaying_of_Surface_bet_Module_when_the_hight_of_one_of_the_card_is_different_than_other(Common):
    """
    TR_ID: C29807828
    NAME: [UI] Verify the displaying of Surface bet Module when the hight of one of the card is different than other
    DESCRIPTION: This test case verifies the displaying of Surface bet Module when the hight of one of the card is different than other
    PRECONDITIONS: 1) Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: 2) Featured Tab is displayed by default
    PRECONDITIONS: 3) Surface Bets Module is displayed
    PRECONDITIONS: Design Ladbrokes: https://zpl.io/ad1NwYl
    PRECONDITIONS: Design CORAL: https://zpl.io/V1pyeOX
    """
    keep_browser_open = True

    def test_001_add_to_the_surface_bet_module_the_title_with_more_than_50_symbols_and_verify_that_the_long_title_is_shortened_properly(self):
        """
        DESCRIPTION: Add to the Surface bet Module the title with more than 50 symbols and verify that the long title is shortened properly
        EXPECTED: The long title is shortened and fits the Title area
        """
        pass

    def test_002_add_to_the_surface_bet_module_the_content_with_more_than_250_symbols_and_verify_that_content_with_a_long_text_is_shown_properly(self):
        """
        DESCRIPTION: Add to the Surface bet Module the content with more than 250 symbols and verify that content with a long text is shown properly
        EXPECTED: The height of the Surface Bet card is increased to fit the text
        EXPECTED: Content is properly shown within the Content area
        """
        pass

    def test_003_add_long_content_to_the_second_surface_bet_module_and_verify_the_ui_in_the_case_when_the_bet_card_is_higher_than_the_other(self):
        """
        DESCRIPTION: Add long content to the second Surface Bet Module and verify the UI in the case when the bet card is higher than the other
        EXPECTED: Both cards use the same height as of the highest card
        EXPECTED: According to design:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/43678)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/43680)
        """
        pass
