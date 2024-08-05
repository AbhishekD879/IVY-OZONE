import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29121_Overask_and_Quick_Deposit_functionality(Common):
    """
    TR_ID: C29121
    NAME: Overask and Quick Deposit functionality
    DESCRIPTION: this test case verifies Overask and Quick Deposit interaction
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-9519 Overask - handle Quick Deposit
    DESCRIPTION: BMA-20390 New Betslip - Overask design improvements
    PRECONDITIONS: * Go to CMS >'System-configuration' section > Config' tab > find 'Overask' config
    PRECONDITIONS: * Initial Data' checkbox is present within 'Overask' config and unchecked by default
    PRECONDITIONS: * The Initial response of the config contains 'The initialDataConfig: false'
    PRECONDITIONS: * The Initial Data response on homepage is absent
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Overask:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    PRECONDITIONS: ![](index.php?/attachments/get/109045765)
    """
    keep_browser_open = True

    def test_001_login_to_application_with_user_who_has_registered_deposit_method(self):
        """
        DESCRIPTION: Login to application with user who has registered deposit method.
        EXPECTED: 
        """
        pass

    def test_002_add_selection_to_betslip_and_enter_stake_value_which_is_higher_then_users_balance_and_higher_then_max_allowed_stake_for_the_selection(self):
        """
        DESCRIPTION: Add selection to Betslip and enter Stake value which is higher then user's balance and higher then max  allowed stake for the selection
        EXPECTED: -   'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: -   'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_003_tap_on_funds_needed_for_bet_linkmake_a_quick_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Funds needed for bet..' link/'MAKE A QUICK DEPOSIT' button
        EXPECTED: - 'Quick Deposit' section is expanded
        EXPECTED: - 'Amount' field is filled with needed amount for a bet
        """
        pass

    def test_004_enter_correct_cvv_code(self):
        """
        DESCRIPTION: Enter correct 'CVV' code
        EXPECTED: -  'DEPOSIT & PLACE BET' button becomes enabled
        """
        pass

    def test_005_tapclick_on_deposit__bet_button(self):
        """
        DESCRIPTION: Tap/Click on 'DEPOSIT & BET' button
        EXPECTED: -   Money are deposited successfully
        EXPECTED: -   Overask review process is started
        """
        pass

    def test_006_verify_information_which_is_displayed_for_user_after_message_about_successful_deposit_stops_to_display(self):
        """
        DESCRIPTION: Verify information which is displayed for user after message about successful deposit stops to display
        EXPECTED: Message: "Please wait, your bet is being reviewed by one of our traders. This normally takes less than a minute." appears on the yellow background, anchored to the footer of the Betslip
        EXPECTED: **From OX 99**
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass
