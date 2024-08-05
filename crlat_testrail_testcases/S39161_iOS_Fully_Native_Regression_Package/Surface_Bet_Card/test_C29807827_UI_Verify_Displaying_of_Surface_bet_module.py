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
class Test_C29807827_UI_Verify_Displaying_of_Surface_bet_module(Common):
    """
    TR_ID: C29807827
    NAME: [UI] Verify Displaying of Surface bet  module
    DESCRIPTION: This test case verifies UI of Surface bet module
    PRECONDITIONS: The app is installed and launched
    PRECONDITIONS: Design Ladbrokes: https://zpl.io/ad1NwYl
    PRECONDITIONS: Design CORAL: https://zpl.io/V1pyeOX
    """
    keep_browser_open = True

    def test_001_verify_the_surface_bet_elements_displaying(self):
        """
        DESCRIPTION: Verify the Surface Bet elements displaying
        EXPECTED: Surface Bets Module is displayed with the following elements:
        EXPECTED: Ladbrokes:
        EXPECTED: * Icon of the sport
        EXPECTED: * Type of promotion
        EXPECTED: * Title of the event
        EXPECTED: * Text
        EXPECTED: * Promo icon
        EXPECTED: * WAS 'Price'
        EXPECTED: * Odds button as per the GD
        EXPECTED: Coral:
        EXPECTED: * Icon of the sport
        EXPECTED: * Title of the event
        EXPECTED: * Type of promotion
        EXPECTED: * Text
        EXPECTED: * Promo icon
        EXPECTED: * WAS 'Price'
        EXPECTED: * Odds button
        """
        pass

    def test_002_verify_ui_of_surface_bets_module(self):
        """
        DESCRIPTION: Verify UI of Surface Bets Module
        EXPECTED: According to design:
        EXPECTED: Ladbrokes
        EXPECTED: ![](index.php?/attachments/get/42437)
        EXPECTED: CORAL:
        EXPECTED: ![](index.php?/attachments/get/42441)
        """
        pass
