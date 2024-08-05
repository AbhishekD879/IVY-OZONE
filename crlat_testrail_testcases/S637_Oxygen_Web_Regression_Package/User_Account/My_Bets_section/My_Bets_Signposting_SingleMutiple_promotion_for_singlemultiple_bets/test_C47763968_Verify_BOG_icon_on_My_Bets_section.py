import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C47763968_Verify_BOG_icon_on_My_Bets_section(Common):
    """
    TR_ID: C47763968
    NAME: Verify BOG icon on My Bets section
    DESCRIPTION: This test case verifies that the BOG icon is displayed on the Bet Receipt and My Bets section
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: [https://jira.egalacoral.com/browse/BMA-49331]
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has a positive balance
    PRECONDITIONS: * User has already placed a bet which is impacted by BOG
    PRECONDITIONS: * BOG has been enabled in CMS
    """
    keep_browser_open = True

    def test_001_open_open_bets_tab_in_my_bets_section(self):
        """
        DESCRIPTION: Open 'Open bets' tab in 'My Bets' section
        EXPECTED: * 'BOG' icon is located below market name/event name section
        EXPECTED: * If any other signposting are available for the bet they are placed one by one in line with 'Cashout' icon coming first
        """
        pass

    def test_002_switch_to_cash_out_tab(self):
        """
        DESCRIPTION: Switch to 'Cash out' tab
        EXPECTED: * 'Cash out' tab is displayed
        """
        pass

    def test_003_verify_bog_icon_on_cash_out_tab(self):
        """
        DESCRIPTION: Verify 'BOG' icon on 'Cash out' tab
        EXPECTED: * 'BOG' icon is located below market name/event name section
        EXPECTED: * If any other signposting are available for the bet they are placed one by one in line with 'Cashout' icon coming first
        """
        pass

    def test_004_switch_to_settled_bets_tab(self):
        """
        DESCRIPTION: Switch to 'Settled bets' tab
        EXPECTED: * 'Settled bets' tab is displayed
        """
        pass

    def test_005_verify_bog_icon_on_settled_bets_tab(self):
        """
        DESCRIPTION: Verify 'BOG' icon on 'Settled bets' tab
        EXPECTED: * 'BOG' icon is located below market name/event name section
        EXPECTED: * If any other signposting are available for the bet they are placed one by one in line with 'Cashout' icon coming first
        EXPECTED: * If **Start Price & Taken Price** are the same only starting price should be displayed
        EXPECTED: * If the **Price Taken** is bigger than the **Starting Price** then the bigger Price Taken should not be shown as struck out.
        EXPECTED: * If the **Starting Price** is bigger than the **Price Taken** then we should display both prices, the Price Taken will be struck out and the new bigger Starting Price will be displayed, as per designs.
        EXPECTED: **Designs**
        EXPECTED: Ladbrokes: https://zpl.io/VxvkMgk
        EXPECTED: Coral: https://zpl.io/Vq5nErm
        """
        pass
