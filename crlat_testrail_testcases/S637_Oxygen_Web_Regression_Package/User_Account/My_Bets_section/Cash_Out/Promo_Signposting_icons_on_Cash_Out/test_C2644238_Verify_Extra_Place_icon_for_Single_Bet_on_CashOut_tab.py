import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C2644238_Verify_Extra_Place_icon_for_Single_Bet_on_CashOut_tab(Common):
    """
    TR_ID: C2644238
    NAME: Verify Extra Place icon for Single Bet on CashOut tab
    DESCRIPTION: This test case verifies that the Extra Place icon for Single Bet is displayed on the CashOut tab
    PRECONDITIONS: * Signposting toggle is Turn ON in the CMS
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Extra Place promo is available for <Race> event on Market lvl.
    PRECONDITIONS: * User has placed a Single bet on event with Extra Place promo and CashOut available
    """
    keep_browser_open = True

    def test_001_navigate_to_the_cashout_tab(self):
        """
        DESCRIPTION: Navigate to the CashOut tab
        EXPECTED: * CashOut tab is opened
        EXPECTED: * Single bet from precondition is present on CashOut tab
        """
        pass

    def test_002_verify_extra_place_icon_on_the_single_bet_for_event_with_extra_place_promo_available_on_market_level(self):
        """
        DESCRIPTION: Verify 'Extra Place' icon on the Single bet for event with Extra Place promo available on **Market level**
        EXPECTED: * 'Extra Place' icon and label are displayed between event name and stake info
        EXPECTED: * 'Extra Place' icon and label are aligned to the left
        """
        pass
