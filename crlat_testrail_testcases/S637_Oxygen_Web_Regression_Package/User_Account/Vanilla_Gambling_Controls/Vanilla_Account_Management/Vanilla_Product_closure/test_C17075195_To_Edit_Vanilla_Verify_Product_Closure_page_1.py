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
class Test_C17075195_To_Edit_Vanilla_Verify_Product_Closure_page_1(Common):
    """
    TR_ID: C17075195
    NAME: [To Edit] [Vanilla] Verify Product Closure  page 1
    DESCRIPTION: This test case verifies the page after selecting 'I want to close my account or sections of it' option
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User is logged in and have a closed product
    PRECONDITIONS: 3. User opens My Account -> Gambling Controls -> Account Closure & Reopening
    """
    keep_browser_open = True

    def test_001_select_i_want_to_close_my_account_or_sections_of_it_option(self):
        """
        DESCRIPTION: Select 'I want to close my account or sections of it' option
        EXPECTED: User is redirected to **Account Closure** page with:
        EXPECTED: - **Account Closure** header,
        EXPECTED: - message:
        EXPECTED: ___Control which sections of your account should be accessible through the options below.___,
        EXPECTED: - products list (e.g. Casino, Poker, Sports),
        EXPECTED: - button **CLOSE ALL** to close all products at once
        """
        pass

    def test_002_verify_products_list(self):
        """
        DESCRIPTION: Verify products list
        EXPECTED: There are:
        EXPECTED: - **CLOSE** button on the right hand side of each product,
        EXPECTED: - **Current status** of a product under each option with the label **open** and **the green dot icon** on the left hand side of the label
        """
        pass
