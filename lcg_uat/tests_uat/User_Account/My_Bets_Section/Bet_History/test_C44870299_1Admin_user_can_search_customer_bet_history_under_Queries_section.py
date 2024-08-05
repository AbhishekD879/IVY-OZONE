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
class Test_C44870299_1Admin_user_can_search_customer_bet_history_under_Queries_section(Common):
    """
    TR_ID: C44870299
    NAME: 1.Admin user can search customer bet history under Queries section
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_navigate_to_admin_in_openbet_example_is_below_and_click_on_the_queries_dropdownhttpsobbackofficedub1egalacoralcomadmin(self):
        """
        DESCRIPTION: Navigate to Admin in Openbet (example is below) and click on the Queries dropdown
        DESCRIPTION: https://obbackoffice.dub1.egalacoral.com/admin
        EXPECTED: You should have opened the Queries drop down in Openbet
        """
        pass

    def test_002_click_on_customer(self):
        """
        DESCRIPTION: Click on Customer
        EXPECTED: You should have been taken to a page where it has two search options:
        EXPECTED: 1. Customer Search Criteria
        EXPECTED: 2. Customer First/Last Activity Search
        """
        pass

    def test_003_in_customer_search_criteria_type_in_a_username_and__click_on_find_customers(self):
        """
        DESCRIPTION: In Customer Search Criteria, type in a username and  click on Find Customers
        EXPECTED: You should have been to the Customer Details page
        """
        pass

    def test_004_in_bet_search_criteria_type_in_a_from_and_to_date_in_the_bet_placed_between_fields_and_click_on_find_bets(self):
        """
        DESCRIPTION: In Bet Search Criteria, type in a from and to date in the Bet placed between fields and click on Find Bets
        EXPECTED: You should have been taken to the Bet Query Result
        """
        pass
