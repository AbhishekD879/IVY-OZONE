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
class Test_C17277681_To_edit_Vanilla_Verify_Account_Closure_long_time_page_3(Common):
    """
    TR_ID: C17277681
    NAME: {To edit} [Vanilla] Verify Account Closure long time page 3
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and DON'T have any closed products
    PRECONDITIONS: User opens My Account -> Settings -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects 'I'd like to close my account' option, selects which product to close, selects the duration & reason for closure and clicks the Continue button
    """
    keep_browser_open = True

    def test_001_click_the_close_products_button(self):
        """
        DESCRIPTION: Click the Close Products button
        EXPECTED: The chosen product(s) are closed for the selected duration.
        EXPECTED: A confirmation message is displayed on the Service Closure page.
        EXPECTED: Under the confirmation,  the list of products with states (open/closed) is displayed.
        """
        pass
