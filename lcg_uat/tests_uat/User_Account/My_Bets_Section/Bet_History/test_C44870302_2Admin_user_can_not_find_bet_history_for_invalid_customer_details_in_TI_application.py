import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870302_2Admin_user_can_not_find_bet_history_for_invalid_customer_details_in_TI_application(Common):
    """
    TR_ID: C44870302
    NAME: 2.Admin user can not find bet history for invalid customer details  in TI application
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_go_to_the_traders_interface_and_click_on_customer(self):
        """
        DESCRIPTION: Go to the Trader's Interface and click on Customer
        EXPECTED: You should be in the Customer section of TI
        """
        pass

    def test_002_type_in_an_invalid_username_and_click_on_search(self):
        """
        DESCRIPTION: Type in an invalid username and click on Search
        EXPECTED: You should be shown a section which says Search results and it should say that 'There are no results that meet your search criteria'
        """
        pass
