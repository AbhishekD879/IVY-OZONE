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
class Test_C44870133_Verify_deposit_instructions_for_each_deposit_methods(Common):
    """
    TR_ID: C44870133
    NAME: Verify deposit instructions for each deposit methods.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has attached credit//debit cards to his account
    PRECONDITIONS: Tap My Account - Click on Banking -> Click on Deposit
    """
    keep_browser_open = True

    def test_001_user_is_on_deposit_page(self):
        """
        DESCRIPTION: User is on Deposit page
        EXPECTED: Validate following  fields on Deposit page
        EXPECTED: 'Deposit' header and 'X' button (Note: This step is applicable for mobile only)
        EXPECTED: On desktop there is no 'X' button. The deposit window closes, when the user clicks anywhere outside the box.
        EXPECTED: Currency
        EXPECTED: Amount edit field
        EXPECTED: 'X' button inside the Amount field box
        EXPECTED: Quick deposit of £20, £50, £100
        EXPECTED: Credi/Debit card section consists of:
        EXPECTED: Credit/Debit card Dropdown and Placeholder
        EXPECTED: Card number displayed in the next format: XXXX **** **** XXXX
        EXPECTED: (where 'XXXX' - the first and last 4 number of the card)
        EXPECTED: 'Other payment options' under Dropdown.
        EXPECTED: CVV2 field
        EXPECTED: Transaction currency
        EXPECTED: 'i' information tool tip
        EXPECTED: Optional Bonus code
        EXPECTED: Option to enter Bonus code when clicked on the arrow next to it
        EXPECTED: Deposit button
        """
        pass
