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
class Test_C29807826_Verify_UI_of_Handicap_Odds_Button(Common):
    """
    TR_ID: C29807826
    NAME: Verify UI of 'Handicap Odds' Button
    DESCRIPTION: This test case verifies the UI of 'Handicap Odds' Button
    PRECONDITIONS: - Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: - Featured Tab is displayed by default
    PRECONDITIONS: - Pre-Match event card with 3 odds Template is available
    PRECONDITIONS: - the market is a 3odds Handicap market
    PRECONDITIONS: Design:
    PRECONDITIONS: Ladbrokes: https://zpl.io/bL16pJd
    PRECONDITIONS: Coral: https://zpl.io/VOpKOyj
    """
    keep_browser_open = True

    def test_001_generate_selection_with_handicap_market(self):
        """
        DESCRIPTION: Generate selection with Handicap market
        EXPECTED: The handicap value above the Odds within the Odds Button is displayed as per design:
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/39936)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/704225)
        """
        pass

    def test_002_emulate_price_change_price_up_for_handicap_market(self):
        """
        DESCRIPTION: Emulate price change (Price UP) for Handicap market
        EXPECTED: The handicap value above the Odds with price change within the Odds Button is displayed as per design
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/650075)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/704226)
        """
        pass

    def test_003_emulate_price_change_down_for_handicap_market(self):
        """
        DESCRIPTION: Emulate price change (Down) for Handicap market
        EXPECTED: The handicap value above the Odds with price change within the Odds Button is displayed as per design
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/650076)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/704227)
        """
        pass
