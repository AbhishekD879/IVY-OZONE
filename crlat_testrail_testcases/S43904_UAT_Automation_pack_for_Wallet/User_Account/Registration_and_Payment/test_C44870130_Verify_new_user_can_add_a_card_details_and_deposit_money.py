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
class Test_C44870130_Verify_new_user_can_add_a_card_details_and_deposit_money(Common):
    """
    TR_ID: C44870130
    NAME: Verify new user can add a card details and deposit money.
    DESCRIPTION: AUTOTESTS:
    DESCRIPTION: Mobile : [C48750671]
    DESCRIPTION: Desktop : [C48750672]
    PRECONDITIONS: Please ignore if 'Cardholder name' option is not available. As we will be mostly using Test cards (Cardholder name) can be ignored.
    """
    keep_browser_open = True

    def test_001_open_deposit_page(self):
        """
        DESCRIPTION: Open 'Deposit' page
        EXPECTED: Visa/Mastercard/Maestro options are available.
        """
        pass

    def test_002_tap_on_the_card_types_available(self):
        """
        DESCRIPTION: Tap on the Card types available
        EXPECTED: Select payment option page is displayed with following fields:
        EXPECTED: Enter amount(+ / -) with quick deposit of £20 "50 £100
        EXPECTED: Card Number
        EXPECTED: Cardholder Name
        EXPECTED: Expiration Date
        EXPECTED: CVV2
        """
        pass

    def test_003_update_all_required_fields__tab_on_deposit(self):
        """
        DESCRIPTION: Update all required fields & Tab on Deposit
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        EXPECTED: Amount on message is displayed in decimal format
        EXPECTED: "OK" & "Make another deposit" tabs
        """
        pass

    def test_004_click_okcheck_balance_in_the_header(self):
        """
        DESCRIPTION: Click "OK"
        DESCRIPTION: Check balance in the header
        EXPECTED: User is taken to the Homepage
        EXPECTED: Balance is increased on sum of deposit
        """
        pass
