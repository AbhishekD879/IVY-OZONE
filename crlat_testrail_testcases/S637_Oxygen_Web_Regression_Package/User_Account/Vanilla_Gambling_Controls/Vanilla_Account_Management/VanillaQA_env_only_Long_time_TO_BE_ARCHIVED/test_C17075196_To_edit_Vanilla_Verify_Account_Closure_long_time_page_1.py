import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C17075196_To_edit_Vanilla_Verify_Account_Closure_long_time_page_1(Common):
    """
    TR_ID: C17075196
    NAME: {To edit} [Vanilla] Verify Account Closure long time page 1
    DESCRIPTION: This test case verifies the page after selecting 'I'd like to close my account' option
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User is logged in and have a closed product
    PRECONDITIONS: 3. User opens My Account -> Settings -> Gambling Controls -> Account Closure
    """
    keep_browser_open = True

    def test_001_select_id_like_to_close_my_account_option(self):
        """
        DESCRIPTION: Select 'I'd like to close my account' option
        EXPECTED: User is redirected to Service Closure page with:
        EXPECTED: - 'Service Closure' header,
        EXPECTED: - message to select the product that can be made unavailable,
        EXPECTED: - products list (e.g. Casino, Poker, Sports),
        EXPECTED: - button to close all products at once
        """
        pass

    def test_002_verify_products_list(self):
        """
        DESCRIPTION: Verify products list
        EXPECTED: There are:
        EXPECTED: - buttons on the right hand side of each product (Close button - for open products, Open button - for closed products),
        EXPECTED: - current 'Customer status' of a product under each option with text (Closed/ open) and a red dot if closed/ green dot if open,
        EXPECTED: - closure date and time (for closed products),
        EXPECTED: - date and time to reopen the product (for closed products)
        """
        pass
