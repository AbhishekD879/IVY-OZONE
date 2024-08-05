import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C852692_Verify_Quick_Deposit_section_for_users_without_credit_card(Common):
    """
    TR_ID: C852692
    NAME: Verify Quick Deposit section for users without credit card
    DESCRIPTION: This test case verifies Quick Deposit section  within Quick Bet for users without credit card
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Log in with a user that has 0 on his balance and no credit card added to his account
    PRECONDITIONS: 3. Click/Tap 'Close' on 'Quick Deposit' pop-up
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1.  Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2.  Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: **NOTE** Steps 5-6 (Paypal, Neteller) are NOT supported anymore
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * Added selection and all data are displayed in Quick Bet
        """
        pass

    def test_002_enter_some_value_in_stake_field_manually_or_use_quick_stake__buttons(self):
        """
        DESCRIPTION: Enter some value in 'Stake' field manually or use 'Quick Stake ' buttons
        EXPECTED: * 'Stake' field is populated with entered value
        EXPECTED: * 'Please deposit a min of £X.XX to continue placing your bet' message is displayed
        """
        pass

    def test_003_clicktap_make_a_deposit_button(self):
        """
        DESCRIPTION: Click/Tap 'Make a Deposit' button
        EXPECTED: * 'QUICK DEPOSIT' section is not displayed
        EXPECTED: * Quick Bet is closed
        EXPECTED: * User is navigated to 'Deposit' page
        EXPECTED: * 'Select a deposit method' title is displayed (an item 'Debit Cards' ( **LADBROKES** ) / items 'Visa'/'Matercard'/'Maestro' ( **CORAL** )
        """
        pass
