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
class Test_C48981676_Preconditions_should_be_updated_Accept_a_Single_and_Double_Boosted_Bets(Common):
    """
    TR_ID: C48981676
    NAME: [Preconditions should be updated] Accept a Single and Double Boosted Bets
    DESCRIPTION: This test case verifies accepting of a boosted bets by a trader triggered by overask functionality
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is more that allowed Max stake value
    PRECONDITIONS: * User has stake limit set on OB TI
    PRECONDITIONS: * Odds Boosts are available for user
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

    def test_001_add_single_and_double_bets_to_betslip(self):
        """
        DESCRIPTION: Add Single and Double bets to Betslip
        EXPECTED: 
        """
        pass

    def test_002_navigate_betslip___boost_the_bets(self):
        """
        DESCRIPTION: Navigate Betslip -> Boost the Bets
        EXPECTED: 
        """
        pass

    def test_003_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_particular_selection_and_click__tap_bet_now_button_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Bet Now' button/ 'Place bet' (From OX 99) button
        EXPECTED: The bet is sent to Openbet system for review
        """
        pass

    def test_004_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        pass

    def test_005_go_to_openbet_system__bet__bi_requests(self):
        """
        DESCRIPTION: Go to OpenBet system > Bet > BI Requests
        EXPECTED: 
        """
        pass

    def test_006_open_received_bi_request_decrease_stake_for_double_bet__select_offer_leave_single_bet_without_changes__select_accept(self):
        """
        DESCRIPTION: Open received BI request:
        DESCRIPTION: * Decrease stake for Double Bet > select Offer
        DESCRIPTION: * Leave Single Bet without changes > select Accept
        EXPECTED: 
        """
        pass

    def test_007_trigger_the_offer_of_bets_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger the offer of bets by a trader in OpenBet system
        EXPECTED: *   The bet is accepted in OpenBet
        EXPECTED: *   Confirmation is sent and received in Oxygen app
        """
        pass

    def test_008_open_oxygen_app__verify_betslip(self):
        """
        DESCRIPTION: Open Oxygen app > Verify Betslip
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * 'i'icon is displayed on the left side of the message
        EXPECTED: * Selection is expanded
        EXPECTED: * Stake for Single Bet is without changes
        EXPECTED: * The new stake for Double Bet is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/59007999)
        """
        pass

    def test_009_click_place_bet_button(self):
        """
        DESCRIPTION: Click 'Place Bet' button
        EXPECTED: Bet Receipts for every bet are displayed
        """
        pass

    def test_010_go_to_open_bets_tab(self):
        """
        DESCRIPTION: Go to 'Open Bets' tab
        EXPECTED: Single and Double Bets are displayed in 'Open Bets' tab
        EXPECTED: Stake values are the same as in step #8
        """
        pass
