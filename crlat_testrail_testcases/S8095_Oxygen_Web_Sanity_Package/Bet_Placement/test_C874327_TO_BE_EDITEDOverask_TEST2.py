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
class Test_C874327_TO_BE_EDITEDOverask_TEST2(Common):
    """
    TR_ID: C874327
    NAME: [TO BE EDITED]Overask [TEST2]
    DESCRIPTION: This test case should be edited according to the latest changes including Vanilla
    DESCRIPTION: This test case verifies:
    DESCRIPTION: - Accepting/rejecting/offering a bet by a trader for a user with enabled overask functionality
    DESCRIPTION: - Maximum Stake functionality for a user with disabled overask
    DESCRIPTION: AUTOTEST [C9690088] [C9690089] [C9690090] [C9690091] [C9690086] [C9690081]
    PRECONDITIONS: How to disable/enable Overask functionality for User or Event Type https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: - User has an account with enabled overask
    PRECONDITIONS: - User has an account with disabled overask
    PRECONDITIONS: - https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
    """
    keep_browser_open = True

    def test_001_log_in_with_account_with_enabled_overask(self):
        """
        DESCRIPTION: Log in with account with enabled overask
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_selections_to_the_betslip__open_betslip(self):
        """
        DESCRIPTION: Add selection(s) to the Betslip > Open Betslip
        EXPECTED: Added selection(s) are available within the Betslip
        """
        pass

    def test_003_enter_any_stake_amount_that_exceeds_maximum_allowed_bet_limit__tap_bet_nowplace_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Enter any Stake amount that exceeds maximum allowed bet limit > Tap 'Bet Now'/'Place bet' (From OX 99) button
        EXPECTED: - Overask is triggered
        EXPECTED: - 'Stake', 'Est. Returns' fields, 'Clear Betslip' and 'Bet Now' buttons are disabled and greyed out
        EXPECTED: - "Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute." message is displayed on yellow background above the Betslip footer
        EXPECTED: - Loading spinner is shown on 'Bet Now' button
        EXPECTED: **From OX 99**
        EXPECTED: *   CMS configurable title, topMessage and bottomMessage for OverAsk are displayed on an overlay on white background anchored to the footer.
        EXPECTED: *   Green (Coral) and black (Ladbrokes) loading spinner is centred and shown between title and text
        EXPECTED: * Background is disabled and not clickable
        """
        pass

    def test_004_in_ti_accept_bet(self):
        """
        DESCRIPTION: In TI: Accept bet
        EXPECTED: Bet is accepted
        """
        pass

    def test_005_in_application_verify_betslip(self):
        """
        DESCRIPTION: In application: Verify Betslip
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt is displayed
        EXPECTED: - Balance is reduced accordingly
        EXPECTED: **From OX 99**
        EXPECTED: * 'Go Betting' button is present and enabled
        EXPECTED: * Bet is placed successfully with the original amount
        EXPECTED: * Bet Receipt is displayed for a user
        EXPECTED: * Balance is reduced accordingly
        EXPECTED: * Bet is listed in 'Bet History' and 'My Account' pages
        """
        pass

    def test_006_tap_donego_bettingfrom_ox_99(self):
        """
        DESCRIPTION: Tap 'Done'/'Go Betting'(From OX 99)
        EXPECTED: Betslip is closed
        """
        pass

    def test_007_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: 
        """
        pass

    def test_008_in_ti_decline_bet(self):
        """
        DESCRIPTION: In TI: Decline bet
        EXPECTED: Bet is declined
        """
        pass

    def test_009_in_application_verify_betslip(self):
        """
        DESCRIPTION: In application: Verify Betslip
        EXPECTED: - Bet is not placed and 'One or more of your bets have been declined' message is shown above 'Continue' button
        EXPECTED: - Balance is not reduced
        EXPECTED: - All selections are shown expanded
        EXPECTED: - 'Stake' field, 'Clear Betslip' buttons remain disabled and greyed out
        EXPECTED: - 'Continue' button is available and enabled
        EXPECTED: **From OX 99**
        EXPECTED: *   Bet is not placed and a 'This bet has not been accepted by traders!' message is shown on **Bet receipt**
        EXPECTED: * 'Stake' field disappears
        EXPECTED: * 'Go betting' button is present
        EXPECTED: * Balance is not reduced
        """
        pass

    def test_010_tap_continuego_bettingfrom_ox_99(self):
        """
        DESCRIPTION: Tap 'Continue'/'Go Betting'(From OX 99)
        EXPECTED: Betslip is closed
        """
        pass

    def test_011_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: 
        """
        pass

    def test_012_in_ti_offer_max_stakeleg_type_for_racesoddsprice_type_for_racessplitlink_splitted_parts(self):
        """
        DESCRIPTION: In TI: Offer Max Stake/Leg Type (for Races)/Odds/Price Type (for Races)/Split/Link splitted parts
        EXPECTED: Max Stake/Leg Type (for Races)/Odds/Price Type (for Races)/Split/Link splitted parts are offered
        """
        pass

    def test_013_in_application_verify_betslip(self):
        """
        DESCRIPTION: In application: Verify Betslip
        EXPECTED: - All selections are shown expanded
        EXPECTED: - Modified Max Stake/Leg Type (for Races)/Odds/Price Type (for Races) are displayed in green
        EXPECTED: - 'Est. Returns' value is updated accordingly and displayed in green
        EXPECTED: - Enabled pre-ticked checkbox with a green icon is shown next to selection with an offer instead of '+'/'-' icon
        EXPECTED: - The linked bet parts are linked with 'link' symbol
        EXPECTED: - 'Bin' button is disabled
        EXPECTED: - 'Accept & Bet (# of accepting selections)' button is enabled
        EXPECTED: - 'Cancel' button is enabled (will empty and close the Betslip)
        EXPECTED: - Unchecking offered selections will decrease # on 'Accept & Bet' button
        EXPECTED: - If unchecking/checking back one of linked selections, its linked part is unchecked/checked as well
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Selection is expanded
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The Estimate returns are updated according to new Stake value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        pass

    def test_014_tap_on_accept__bet__of_accepting_selections_place_a_bet_from_ox_99(self):
        """
        DESCRIPTION: Tap on 'Accept & Bet (# of accepting selections)'/ 'Place a bet (From OX 99)
        EXPECTED: Bet is successfully placed
        """
        pass

    def test_015_log_in_with_account_with_disabled_overask(self):
        """
        DESCRIPTION: Log in with account with disabled overask
        EXPECTED: User is logged in
        """
        pass

    def test_016_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps 2-3
        EXPECTED: - 'Sorry, the maximum stake for this bet is X.XX' message is displayed right below the selection
        EXPECTED: - Bet is not placed
        """
        pass
