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
class Test_C8146662_Triggering_accepting_bet_while_doing_other_actionswithdraw_funds_place_another_bet_etc_negative_case(Common):
    """
    TR_ID: C8146662
    NAME: Triggering accepting bet while doing other actions(withdraw funds, place another bet, etc) (negative case)
    DESCRIPTION: This test case verifies accepting of a bet by a trader triggered by overask functionality while doing other actions(withdraw funds, place another bet, etc)
    DESCRIPTION: !!! Step 7 should be updated
    PRECONDITIONS: **Request URL**: http://bp-stg2.coral.co.uk/Proxy/v1/offerBet
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User's balance is more that allowed Max stake value
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User is logged in to the app
    PRECONDITIONS: 3. Overask functionality is enabled for the user
    PRECONDITIONS: 4. Go to CMS >'System-configuration' section > Config' tab > find 'Overask' config
    PRECONDITIONS: 5. Initial Data' checkbox is present within 'Overask' config and unchecked by default
    PRECONDITIONS: 6. The Initial response of the config contains 'The initialDataConfig: false'
    PRECONDITIONS: 7. The Initial Data response on homepage is absent
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Overask:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    PRECONDITIONS: ![](index.php?/attachments/get/109045765)
    """
    keep_browser_open = True

    def test_001___________add_selection_and_go_to_betslip_singles_section(self):
        """
        DESCRIPTION: *          Add selection and go to Betslip, 'Singles' section
        EXPECTED: *
        """
        pass

    def test_002___________enter_value_in_stake_field_that_exceeds_max_allowed_bet_limit_for_particular_selection_and_click__tap_bet_now_buttonplace_bet_from_ox_99_button(self):
        """
        DESCRIPTION: *          Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Bet Now' button/'Place bet' (From OX 99) button
        EXPECTED: *          The bet is sent to Openbet system for review
        """
        pass

    def test_003___________verify_betslip(self):
        """
        DESCRIPTION: *          Verify Betslip
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_004___________kill_the_apprefresh_the_page__________make_withdraw(self):
        """
        DESCRIPTION: *          Kill the app/refresh the page
        DESCRIPTION: *          Make Withdraw
        EXPECTED: *          Customer’s current IMS balance are reduced
        """
        pass

    def test_005__trigger_offer_by_changing_users_stake_the_bet_by_a_trader_in_openbet_system_the_stake_of_the_offer_must_still_be_greater_than_the_customers_current_ims_balance(self):
        """
        DESCRIPTION: * Trigger offer by changing user's stake the bet by a trader in OpenBet system
        DESCRIPTION: * (The stake of the offer must still be greater than the customer’s current IMS balance)
        EXPECTED: *          - Alternative offer is sent and received in Oxygen app
        """
        pass

    def test_006__verify_betslip(self):
        """
        DESCRIPTION: * Verify Betslip
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Selection is expanded
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * 'Please deposit a min...' message appears
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: * Actual for Ladbrokes *
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Selection is expanded
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        pass

    def test_007__tap_place_bet_button(self):
        """
        DESCRIPTION: * Tap 'Place bet' button
        EXPECTED: **Coral**
        EXPECTED: * "Funds needed for bet <currency symbol><amount of funds>" message is displayed on red background
        EXPECTED: * In offerBet request -> betRef -> status: "ERROR"; statusMessage: "Unable to accept offer at this time"
        EXPECTED: **Ladbrokes**
        EXPECTED: * 'Please deposit a min of £5.00 to continue placing your bet' message is displayed
        EXPECTED: * 'Make deposit' button appears
        EXPECTED: * In 'offerBet' response -> status: "SERVICE_ERROR"; error: "508 - LOW_FUNDS ob_bet::resolve_async_bets: Failed to resolve async bets"
        """
        pass

    def test_008__tap_make_deposit_button(self):
        """
        DESCRIPTION: * Tap 'Make deposit' button
        EXPECTED: * 'Quick Deposit' form appears
        """
        pass

    def test_009__enter_the_amount_to_quick_deposit_form_tap_deposit__place_bet_button(self):
        """
        DESCRIPTION: * Enter the amount to 'Quick Deposit' form
        DESCRIPTION: * Tap 'Deposit & Place Bet' button
        EXPECTED: * Overask process triggered again
        EXPECTED: For Coral tst2 (in analysis!)
        EXPECTED: *  *If stake is < then Max stakes *
        EXPECTED: * Bet is placed
        EXPECTED: *  *If stake is > then Max stakes *
        EXPECTED: * Overask process triggered again
        """
        pass

    def test_010__in_another_devicebrowser_either_place_a_bet_for_triggering_situation_that_you_do_not_have_sufficient_funds_to_cover_the_bet_verify_the_user_balance(self):
        """
        DESCRIPTION: * In another device/browser either place a bet for triggering situation that you do not have sufficient funds to cover the bet.
        DESCRIPTION: * Verify the user balance.
        EXPECTED: User balance is decreased
        """
        pass

    def test_011__trigger_accepting_the_bet_by_a_trader_in_openbet_system_verify_the_betslip(self):
        """
        DESCRIPTION: * Trigger accepting the bet by a trader in OpenBet system.
        DESCRIPTION: * Verify the Betslip
        EXPECTED: * Bet is not placed
        EXPECTED: * 'This bet has not been accepted by traders!' message is displayed in the Betslip
        EXPECTED: * In 'getBetDetail' response -> respTransGetBetDetail -> bet: asyncAcceptStatus: "T" status is received
        """
        pass
