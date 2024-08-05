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
class Test_C325661_Cash_Out_value_change_on_CASH_OUT_button(Common):
    """
    TR_ID: C325661
    NAME: Cash Out value change on 'CASH OUT' button
    DESCRIPTION: This test case verifies price change on 'CASH OUT' button on 'My Bets' tab on Event Details page
    DESCRIPTION: **Jira tickets:** BMA-3712, BMA-998
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Singles and Multiple bets with available Cash Out offer
    PRECONDITIONS: **NOTE:** In order to get increased Cashed Out value Price/Odds should be decreased. In order to get decreased Cashed Out value Price/Odds should be increased.
    PRECONDITIONS: **Live Price Updates behaviour:**
    PRECONDITIONS: * Application reacts on notification with new prices and unsuspended Event/Market/Outome from LiveServer
    PRECONDITIONS: * After that application makes 'getBetDetail' request in order to get new Cash Out value
    PRECONDITIONS: * Value from getBetDetail repsonse is shown on 'CASH OUT' button
    PRECONDITIONS: **Note:** Sometimes getBetDetail repsonse can contain obsolete information
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page(self):
        """
        DESCRIPTION: Navigate to 'My Bets' tab on Event Details page
        EXPECTED: 'Cash Out' tab is opened
        """
        pass

    def test_002_trigger_cash_out_value_increasingfor_single_bet(self):
        """
        DESCRIPTION: Trigger cash out value INCREASING for **Single** bet
        EXPECTED: *   Corresponding 'Price/Odds' data is not changed
        EXPECTED: *   Corresponding priceNum/priceDen is changed on SiteServer
        EXPECTED: *   'CASH OUT' button immediately displays new cash out value
        """
        pass

    def test_003_trigger_cash_out_value_increasingfor_multiple_bet(self):
        """
        DESCRIPTION: Trigger cash out value INCREASING for **Multiple** bet
        EXPECTED: *   Corresponding 'Price/Odds' button is not changed
        EXPECTED: *   Corresponding priceNum/priceDen are changed on SiteServer
        EXPECTED: *   Corresponding ''CASH OUT' button immediately displays new cash out value
        """
        pass

    def test_004_verify_cash_out_value_increasingbefore_page_is_opened(self):
        """
        DESCRIPTION: Verify cash out value INCREASING before page is opened
        EXPECTED: If application was not opened and value was changed, after opening 'Cash Out' page - updated value will be shown there
        """
        pass

    def test_005_repeat_steps_2_4_with_decreasedcash_out_value(self):
        """
        DESCRIPTION: Repeat steps #2-4 with DECREASED cash out value
        EXPECTED: Results are the same
        """
        pass

    def test_006_move_partial_cashout_slider_to_less_than_100trigger_cash_out_value_change(self):
        """
        DESCRIPTION: Move 'Partial CashOut' slider to less than 100%
        DESCRIPTION: Trigger cash out value change
        EXPECTED: * Slider jumps to 100%
        EXPECTED: * Updated full cash out value is displayed
        """
        pass
