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
class Test_C24917871_Verify_odds_button_state_for_2_odds_Spread_Handicap_market(Common):
    """
    TR_ID: C24917871
    NAME: Verify odds button state for 2 odds Spread/Handicap market
    DESCRIPTION: This test case verifies odds button state for 2 odds Spread/Handicap market
    DESCRIPTION: Design
    DESCRIPTION: Ladbrokes:
    DESCRIPTION: https://app.zeplin.io/project/5d7764168919b56be93722fb/screen/5d7766d3cba5d54eb5d8fad3
    DESCRIPTION: Coral:
    DESCRIPTION: https://app.zeplin.io/project/5da04022f2c331081a4c9961/screen/5da0531c74c7950852a0e0dd
    PRECONDITIONS: * Coral/Ladbrokes app is installed and launched
    PRECONDITIONS: * Featured Tab is displayed by default
    PRECONDITIONS: * Pre-Match event card with 2 odds Template is available
    PRECONDITIONS: * User is navigated to the Event that contains 2 Odds Template
    """
    keep_browser_open = True

    def test_001_generate_selection_with_handicap_market(self):
        """
        DESCRIPTION: Generate selection with Handicap market
        EXPECTED: the handicap value above the Odds within the Odds Button is displayed as per design
        EXPECTED: ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/44146)
        EXPECTED: coral:
        EXPECTED: ![](index.php?/attachments/get/745386)
        """
        pass

    def test_002_emulate_price_change_price_up_for_handicap_market(self):
        """
        DESCRIPTION: emulate price change (Price UP) for Handicap market
        EXPECTED: the handicap value above the Odds with price change within the Odds Button is displayed as per design
        EXPECTED: ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/44147)
        EXPECTED: coral:
        EXPECTED: ![](index.php?/attachments/get/745387)
        """
        pass

    def test_003_emulate_price_change_down_for_handicap_market(self):
        """
        DESCRIPTION: emulate price change (Down) for Handicap market
        EXPECTED: the handicap value above the Odds with price change within the Odds Button is displayed as per design
        EXPECTED: ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/44148)
        EXPECTED: coral:
        EXPECTED: ![](index.php?/attachments/get/745388)
        """
        pass
