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
class Test_C44870300_2Admin_user_can_not_find_bet_history_for_invalid_customer_details_in_admin(Common):
    """
    TR_ID: C44870300
    NAME: 2.Admin user can not find bet history for invalid customer details  in admin
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

    def test_003_in_customer_search_criteria_type_in_an_invalid_username_and_click_on_find_customers(self):
        """
        DESCRIPTION: In Customer Search Criteria, type in an invalid username and click on Find Customers
        EXPECTED: You should have been taken to a page which says Customer Search Results and it should show the message "No customers match your search criteria"
        """
        pass
