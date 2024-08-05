import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C22179407_Vanilla__Successful_Deposit_from_Cashier_via_Recent_payment_method_general_flow(Common):
    """
    TR_ID: C22179407
    NAME: [Vanilla] - Successful Deposit from Cashier via Recent payment method  (general flow)
    DESCRIPTION: This test case verifies Deposit of Funds from Cashier via Recent payment method
    DESCRIPTION: AUTOTEST [C23137733] [C23229013]
    PRECONDITIONS: 1. User should register at least 1 payment method (e.g Mastercard);
    PRECONDITIONS: 2. User logged into the application;
    PRECONDITIONS: 3. User performed Deposit for registered payment Method;
    """
    keep_browser_open = True

    def test_001_click_on_user_avatar_icon_on_the_header(self):
        """
        DESCRIPTION: Click on User "Avatar" icon on the header.
        EXPECTED: User menu is opened;
        """
        pass

    def test_002_click_on_cashier_section_in_user_menu(self):
        """
        DESCRIPTION: Click on "Cashier" section in User menu;
        EXPECTED: Cashier Menu is opened and "Deposit" section is present there;
        """
        pass

    def test_003_click_on_deposit_section(self):
        """
        DESCRIPTION: Click On "Deposit" section
        EXPECTED: Deposit menu is opened;
        """
        pass

    def test_004_1_enter_amount_for_deposit2_select_card3_enter_security_codeid4_click_on_the_deposit_button(self):
        """
        DESCRIPTION: 1. Enter Amount for Deposit;
        DESCRIPTION: 2. Select Card
        DESCRIPTION: 3. Enter Security code/id
        DESCRIPTION: 4. Click on the 'Deposit' button;
        EXPECTED: Deposit is Successful
        """
        pass

    def test_005_verify_that_balance_is_changed(self):
        """
        DESCRIPTION: Verify that balance is changed;
        EXPECTED: Ballance changed and increased equal to the amount of Deposit;
        """
        pass
