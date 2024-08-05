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
class Test_C51109622_Verify_changing_cash_out_value_on_Banach_bets(Common):
    """
    TR_ID: C51109622
    NAME: Verify changing cash out value on Banach bets
    DESCRIPTION: Test case verifies cash out the value on Banach bets
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check Open Bet data for the event on Cash-out tab
    PRECONDITIONS: in Dev tools > Network > XHR > find bet-details request > initial
    PRECONDITIONS: User has placed Banach bet(s)
    PRECONDITIONS: Banach bet is displayed on Cash out tab
    PRECONDITIONS: to update cash out value need to ask Banach for help
    """
    keep_browser_open = True

    def test_001_ask_banach_to_change_the_price_for_bet_id_that_is_present_on_the_cash_out_tab(self):
        """
        DESCRIPTION: Ask Banach to change the price for bet id that is present on the Cash Out tab
        EXPECTED: Price is changed
        """
        pass

    def test_002_go_to_ws__bet_details__initial_data_and_check_the_response(self):
        """
        DESCRIPTION: Go to WS > bet-details > initial data and check the response
        EXPECTED: betUpdate is present in the EventStream
        EXPECTED: cashoutValue is changed
        """
        pass

    def test_003_open_ui_and_check_cash_out_value(self):
        """
        DESCRIPTION: Open UI and check Cash out value
        EXPECTED: Cash out value is the same as in betUpdate
        """
        pass

    def test_004_check_step_1_3_for_coral_and_ladbrokes_brand(self):
        """
        DESCRIPTION: check step 1-3 for coral and ladbrokes brand
        EXPECTED: 
        """
        pass
