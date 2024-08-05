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
class Test_C91382_Trader_modifies_the_Stake_Odds_and_Leg_Type_Each_Way(Common):
    """
    TR_ID: C91382
    NAME: Trader modifies the Stake, Odds and Leg Type (Each Way)
    DESCRIPTION: This test case verifies offers displaying in Betslip when Stake, Price and Leg Type was changed by Trader
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Leg Type (Each Way) is available for Racing selections (Each way terms are shown if isEachWayAvailable='true'):
    PRECONDITIONS: For verifying specific event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_add_selectionfrom_racing_event_to_the_betslip(self):
        """
        DESCRIPTION: Add selection from Racing event to the Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002___enter_stake_value_which_is_higher_than_maximum_limit_for_added_selection_each_way_checkbox_is_unchecked(self):
        """
        DESCRIPTION: *  Enter stake value which is higher than maximum limit for added selection
        DESCRIPTION: * 'Each Way' checkbox is unchecked
        EXPECTED: 
        """
        pass

    def test_003_tap_bet_now_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' /'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_004_trigger_stake_price_odds_and_leg_type_modification_by_trader_and_verify_offer_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Stake, Price (Odds) and Leg Type modification by Trader and verify offer displaying in Betslip
        EXPECTED: *   Info message is displayed above 'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons with text: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: *   Bet selection is expanded
        EXPECTED: *   Enabled pre-ticked checkbox with a green icon is shown next to bet selection instead of '+'/'-' icon
        EXPECTED: *   New Price is displayed and highlighted in green
        EXPECTED: *   The new stake is shown to the user on the Betslip (in green)
        EXPECTED: *   "You're accepting this Trade Offer" message on the grey background is shown below the selection
        EXPECTED: *   'Each Way' checkbox is selected and highlighted in green
        EXPECTED: *   The Estimate returns are updated according to new stake (also highlighted in red)
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Selection is expanded
        EXPECTED: * The new Price is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * 'E/W' with a tick is displayed below the new stake
        EXPECTED: * The Estimate returns are updated according to new stake
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/31458)
        EXPECTED: ![](index.php?/attachments/get/31459)
        """
        pass

    def test_005_tap_on_confirmplace_bet_from_ox_99_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap on 'Confirm'/'Place bet' (From OX 99) or 'Cancel' buttons
        EXPECTED: * Tapping 'Accept & Bet ([number of accepted bets])'/ 'Place bet' button places bet(s) as per normal process
        EXPECTED: * Tapping 'Cancel' button/and than 'Cancel offer' pop-up (From OX 99) clears offer and selection(s) is shown without stake
        """
        pass

    def test_006_repeat_steps_1_4_with_enabled_each_way_checkbox(self):
        """
        DESCRIPTION: Repeat steps #1-4 with enabled 'Each Way' checkbox
        EXPECTED: *   Info message is displayed above 'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons with text: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: *   Bet selection is expanded
        EXPECTED: *   Enabled pre-ticked checkbox with a green icon is shown next to bet selection instead of '+'/'-' icon
        EXPECTED: *   New Price is displayed and highlighted in green
        EXPECTED: *   The new stake is shown to the user on the Betslip (in green)
        EXPECTED: *   'Each Way' checkbox is unselected and highlighted in green
        EXPECTED: *   The Estimate returns are updated according to new stake (also highlighted in green)
        EXPECTED: *    "You're accepting this Trade Offer" message on the grey background is shown below the selection
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Selection is expanded
        EXPECTED: * The new Price is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * 'Win Only' is displayed below the new stake
        EXPECTED: * The Estimate returns are updated according to new stake
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        pass

    def test_007_tap_on_accept__bet_place_bet_from_ox_99_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap on ''Accept & Bet '/'Place bet' (From OX 99) or 'Cancel' buttons
        EXPECTED: 
        """
        pass
