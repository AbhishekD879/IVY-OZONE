import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C1471148_T0_EditVerify_Settled_Bets_table_on_Settled_Bets_page(Common):
    """
    TR_ID: C1471148
    NAME: [T0-Edit]Verify "Settled Bets" table on Settled Bets page
    DESCRIPTION: [T0-Edit] - needs to be edited according to all changes with Vanilla
    DESCRIPTION: This test case verifies "Settled Bets" table on 'Settled Bets' tab on 'My Bets' and on 'Account History' pages
    DESCRIPTION: Test case is applicable for:
    DESCRIPTION: Settlrd Bets tab 'Account History' page (for mobile)
    DESCRIPTION: 'Bet Slip' widget (for Tablet/Desktop)
    DESCRIPTION: "Settled Bets" page (for Tablet/Desktop)
    DESCRIPTION: AUTOTEST Mobile: [C2554765]
    DESCRIPTION: AUTOTEST Desktop: [C2555446]
    PRECONDITIONS: 1. User should be logged in to see his settled bets
    PRECONDITIONS: 2. User should have a few settled bets: won/settled/void/cashed out bets
    PRECONDITIONS: 3. User should have bets that were reviewed by Overask functionality (rejected, offered and so on)
    """
    keep_browser_open = True

    def test_001_open_settled_bets_tab_on_my_bets_pageset_a_date_range_in_the_date_pickers_in_order_to_see_users_settled_bets(self):
        """
        DESCRIPTION: Open 'Settled Bets' tab on 'My Bets' page
        DESCRIPTION: Set a date range in the date pickers in order to see user's settled bets
        EXPECTED: * Settled bets for the selected time period appears
        EXPECTED: * "Settled Bets" accordion is present and collapsed by default
        """
        pass

    def test_002_expand_the_settled_bets_accordion(self):
        """
        DESCRIPTION: Expand the "Settled Bets" accordion
        EXPECTED: * Accordion is expanded
        EXPECTED: * Table is shown
        """
        pass

    def test_003_verify_the_table(self):
        """
        DESCRIPTION: Verify the table
        EXPECTED: The table contains the following columns:
        EXPECTED: * **T. Stakes** - showing the total stakes for the user
        EXPECTED: * **T. Returns** - showing the total returns for the user
        EXPECTED: * **Profit/Loss** - total profit/loss for the user
        EXPECTED: * **'Regular (Sports & Gaming), Lotto and Pools bets are included in the table above'** message is displayed below the columns
        """
        pass

    def test_004_verify_data_in_the_table(self):
        """
        DESCRIPTION: Verify data in the table
        EXPECTED: Data in the table corresponds to the data, received in response to **wss://openapi.egalacoral.com/socket.io/1/websocket/** {"ID":32013,"} request to Playtech.
        EXPECTED: NOTE: For this step, manual calculation of the data, described in previous step, is NOT NEEDED. It's important to verify that we display exactly what we receive from Playtech.
        """
        pass
