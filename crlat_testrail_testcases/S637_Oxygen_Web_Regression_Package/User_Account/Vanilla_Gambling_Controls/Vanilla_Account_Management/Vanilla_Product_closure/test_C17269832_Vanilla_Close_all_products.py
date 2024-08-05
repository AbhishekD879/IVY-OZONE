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
class Test_C17269832_Vanilla_Close_all_products(Common):
    """
    TR_ID: C17269832
    NAME: [Vanilla] Close all products
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and **DON'T** have any closed products
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects 'I want to close my account or sections of it' option and clicks the Continue button
    """
    keep_browser_open = True

    def test_001_click_the_close_all_button(self):
        """
        DESCRIPTION: Click the **Close all** button
        EXPECTED: The confirmation screen of product closure is displayed with closure duration and reason selections.
        """
        pass

    def test_002_verify_continue_button(self):
        """
        DESCRIPTION: Verify **Continue** button
        EXPECTED: **Continue** button is disabled
        """
        pass

    def test_003_select_account_closure_duration_time(self):
        """
        DESCRIPTION: Select account closure duration time
        EXPECTED: **Continue** button is disabled
        """
        pass

    def test_004_select_closure_reason(self):
        """
        DESCRIPTION: Select closure reason
        EXPECTED: **Continue** button becomes enabled
        """
        pass

    def test_005_click_the_continue_button(self):
        """
        DESCRIPTION: Click the **Continue** button
        EXPECTED: Another confirmation screen of product closure is displayed.
        """
        pass

    def test_006_click_the_close_my_account_button(self):
        """
        DESCRIPTION: Click the **Close my account** button
        EXPECTED: All products are closed for the selected period of time.
        EXPECTED: The confirmation message:
        EXPECTED: **Successfully closed: <prod1>, ..., <prodn>'**
        EXPECTED: is displayed on the ** Account Closure** confirmation page.
        EXPECTED: There shouldn't be any other text information under the confirmation message.
        """
        pass
