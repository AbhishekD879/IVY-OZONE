import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C64663350_Verify_the_display_of_Price_Buttons(Common):
    """
    TR_ID: C64663350
    NAME: Verify the display of Price Buttons
    DESCRIPTION: This test cases verifies the display of price button for list templet
    PRECONDITIONS: arket with List templet should be available ex:Outright,GetAPrice etc..
    PRECONDITIONS: ![](index.php?/attachments/get/3a8ccece-ed71-4d4a-a6c8-6ec83ba8b333)
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_edp_page(self):
        """
        DESCRIPTION: Navigate to EDP page
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_any_market_which_has_list_templetexoutrightgetaprice(self):
        """
        DESCRIPTION: Expand any market which has list templet
        DESCRIPTION: Ex:Outright,GetAPrice
        EXPECTED: * Market Header should be displayed along with signposting if available
        EXPECTED: * List of Options (each with a Price Button)
        EXPECTED: * “SHOW MORE/LESS” option available
        """
        pass

    def test_004_validate_price_button_for_list_templet_market(self):
        """
        DESCRIPTION: Validate price button for List templet Market
        EXPECTED: Each selection should have a price button for List market templet
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/971dc547-e143-4d71-a0b7-97a28c75c810)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/609e9a8f-ef13-4fed-a22a-300cf3680cad)
        """
        pass
