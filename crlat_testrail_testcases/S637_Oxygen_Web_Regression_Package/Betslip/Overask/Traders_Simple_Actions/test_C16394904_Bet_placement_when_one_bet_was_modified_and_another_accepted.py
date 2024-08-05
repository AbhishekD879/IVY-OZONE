import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C16394904_Bet_placement_when_one_bet_was_modified_and_another_accepted(Common):
    """
    TR_ID: C16394904
    NAME: Bet placement when one bet was modified  and another accepted
    DESCRIPTION: This test case verifies bet placement when one bet was modified and another accepted
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

    def test_001_add_two_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add two selections to the Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002__enter_stake_value_which_is_higher_than_maximum_limit_for_one_added_selection_enter_stake_value_which_is_higher_than_maximum_limit_for_another_added_selection(self):
        """
        DESCRIPTION: * Enter stake value which is higher than maximum limit for one added selection
        DESCRIPTION: * Enter stake value which is higher than maximum limit for another added selection
        EXPECTED: 
        """
        pass

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_004__trigger_any_modification_by_trader_for_the_first_bet_trigger_accepting_the_bet_by_a_trader_in_openbet_system_for_the_second_bet(self):
        """
        DESCRIPTION: * Trigger any modification by Trader for the first bet
        DESCRIPTION: * Trigger accepting the bet by a trader in OpenBet system for the second bet
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * 'i'icon is displayed on the left side of the message
        EXPECTED: * The accepted bet is shown to the user on the Betslip and NOT highlighted in yellow color
        EXPECTED: * The changed bet is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/34000) ![](index.php?/attachments/get/33999)
        """
        pass

    def test_005_tap_place_bet_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap 'Place bet' or 'Cancel' buttons
        EXPECTED: The bets are placed as per normal process
        """
        pass
