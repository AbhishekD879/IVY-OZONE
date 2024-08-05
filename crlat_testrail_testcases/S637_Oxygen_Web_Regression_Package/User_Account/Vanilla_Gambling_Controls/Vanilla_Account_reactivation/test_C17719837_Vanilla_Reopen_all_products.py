import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17719837_Vanilla_Reopen_all_products(Common):
    """
    TR_ID: C17719837
    NAME: [Vanilla] Reopen all products
    DESCRIPTION: This test case verifies 'Reopen all' functionality that reopens all closed products
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User is logged in and have some products closed
    PRECONDITIONS: 3. User opens My Account -> Gambling Controls -> Account Closure
    """
    keep_browser_open = True

    def test_001_select_i_want_to_reopen_my_account_or_selections_of_it_option(self):
        """
        DESCRIPTION: Select 'I want to reopen my account or selections of it' option
        EXPECTED: User is redirected to **Account Reopening** page with:
        EXPECTED: - **Account Reopening** (Coral)/ **OPEN PRODUCTS** (Ladbrokes) header,
        EXPECTED: - message:
        EXPECTED: ___Control which sections of your account should be accessible through the options below.___,
        EXPECTED: - products list (e.g. Casino, Poker, Sports),
        EXPECTED: - button **REOPEN ALL** to open all products at once
        """
        pass

    def test_002_verify_products_list(self):
        """
        DESCRIPTION: Verify products list
        EXPECTED: There are:
        EXPECTED: - green **OPEN** button on the right hand side of each product,
        EXPECTED: - **Current status** of a product under each option with **red 'closed'** text and **the red dot with white lock icon** inside,
        EXPECTED: - **Closed until** with the exact date and time of closure period end
        """
        pass

    def test_003_click_the_reopen_all_button(self):
        """
        DESCRIPTION: Click the **Reopen all** button
        EXPECTED: A confirmation message:
        EXPECTED: ***'Successfully opened: <prod1>,.., <prodn>'*** is displayed
        EXPECTED: There shouldn't be any other text information under the confirmation message.
        """
        pass
