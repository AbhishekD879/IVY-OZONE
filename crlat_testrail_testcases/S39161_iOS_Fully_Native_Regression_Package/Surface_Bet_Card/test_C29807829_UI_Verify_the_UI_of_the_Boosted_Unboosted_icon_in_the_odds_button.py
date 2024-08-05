import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C29807829_UI_Verify_the_UI_of_the_Boosted_Unboosted_icon_in_the_odds_button(Common):
    """
    TR_ID: C29807829
    NAME: [UI] Verify the UI of the Boosted/Unboosted icon in the odds button
    DESCRIPTION: This test case verifies the UI of the Boosted/Unboosted icon in the odds button
    PRECONDITIONS: The app is installed and launched
    PRECONDITIONS: Design Ladbrokes: https://zpl.io/ad1NwYl
    PRECONDITIONS: Design CORAL: https://zpl.io/V1pyeOX
    """
    keep_browser_open = True

    def test_001_verify_ui_of_surface_bets_module_with_was_price_for_the_surface_bet(self):
        """
        DESCRIPTION: Verify UI of Surface Bets Module with WAS price for the surface bet
        EXPECTED: The boosted icon is displayed in the 'odds' button
        EXPECTED: 'WAS' is crossed out
        EXPECTED: According to design:
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/47364)
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/47365)
        """
        pass

    def test_002_verify_ui_of_surface_bets_module_when_there_is_a_no_was_price_for_the_surface_bet(self):
        """
        DESCRIPTION: Verify UI of Surface Bets Module when there is a no WAS price for the surface bet
        EXPECTED: The boosted icon in the odds button is not displayed
        EXPECTED: 'WAS' is not crossed out
        """
        pass
