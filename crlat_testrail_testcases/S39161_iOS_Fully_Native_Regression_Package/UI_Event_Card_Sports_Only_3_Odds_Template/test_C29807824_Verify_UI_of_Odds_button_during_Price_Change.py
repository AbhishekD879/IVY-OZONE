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
class Test_C29807824_Verify_UI_of_Odds_button_during_Price_Change(Common):
    """
    TR_ID: C29807824
    NAME: Verify UI of 'Odds' button during Price Change
    DESCRIPTION: This test case verifies UI of 'Odds' button during Price Change
    PRECONDITIONS: Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: Featured Tab is displayed by default
    PRECONDITIONS: Pre-Match event card with 3 odds Template is available
    PRECONDITIONS: Design:
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: https://zpl.io/bL16pJd
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://zpl.io/VOpKOyj
    """
    keep_browser_open = True

    def test_001_emulate_price_change_price_up(self):
        """
        DESCRIPTION: Emulate price change (Price UP)
        EXPECTED: - The Odds Price within 'Odds' Button change color according to design:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/39904)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/704321)
        EXPECTED: - Price change animation duration is 2000ms
        """
        pass

    def test_002_emulate_price_change_price_down(self):
        """
        DESCRIPTION: Emulate price change (Price DOWN)
        EXPECTED: - Odds Price within 'Odds' Button change color as per design:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/39905)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/704322)
        EXPECTED: - Price change animation duration is 2000ms
        """
        pass
