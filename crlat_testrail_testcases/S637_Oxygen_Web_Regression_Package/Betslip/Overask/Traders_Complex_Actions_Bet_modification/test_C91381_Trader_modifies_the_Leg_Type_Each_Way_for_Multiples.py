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
class Test_C91381_Trader_modifies_the_Leg_Type_Each_Way_for_Multiples(Common):
    """
    TR_ID: C91381
    NAME: Trader modifies the Leg Type (Each Way) for Multiples
    DESCRIPTION: This test case verifies offer for multiples displaying in Betslip when Leg Type was changed by Trader
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Leg Type (Each Way) is available for Racing selections (Each way terms are shown if isEachWayAvailable='true'):
    PRECONDITIONS: For verifying specific event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 4. Open Dev Tools -> Network -> XHR tab in order to check 'readBet' response
    """
    keep_browser_open = True

    def test_001_add_few_selectionfrom_different_racing_events_to_the_betslip(self):
        """
        DESCRIPTION: Add few selection from different Racing events to the Betslip
        EXPECTED: Selections are successfully added
        """
        pass

    def test_002___enter_stake_value_which_is_higher_than_maximum_limit_for_multiples_each_way_checkbox_is_not_checked(self):
        """
        DESCRIPTION: *  Enter stake value which is higher than maximum limit for multiples
        DESCRIPTION: * 'Each Way' checkbox is NOT checked
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

    def test_004_change_leg_type_from_win_to_each_way_and_stake_modification_by_trader_and_verify_offer_displaying_in_betslip(self):
        """
        DESCRIPTION: Change Leg Type from Win to Each way and Stake modification by Trader and verify offer displaying in Betslip
        EXPECTED: *   Info message is displayed above 'Confirm' and 'Cancel' buttons with text: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: *   The new stake is shown to the user on the Betslip (in red)
        EXPECTED: *   'Each Way' checkbox is selected and highlighted in red
        EXPECTED: **From OX 99**
        EXPECTED: *   'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: *  The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: *  'E/W' with a tick is displayed below the new stake
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/31453)
        EXPECTED: ![](index.php?/attachments/get/31454)
        """
        pass

    def test_005_verify_new_est_returns_value(self):
        """
        DESCRIPTION: Verify new 'Est Returns' value
        EXPECTED: * The 'Est. return' value corresponds to **bet.[i].payout.potential** attribute from **readBet** response,
        EXPECTED: where **i** is taken from the object where **isOffer="Y"**
        EXPECTED: * The 'Est. return' value is equal to **N/A** if no attribute is returned
        EXPECTED: * The 'Est. return' value is highlighted in green
        EXPECTED: **From OX 99**
        EXPECTED: * The 'Est. return' value is NOT highlighted
        """
        pass

    def test_006_tap_on_confirmplace_bet_from_ox_99_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap on 'Confirm'/'Place bet' (From OX 99) or 'Cancel' buttons
        EXPECTED: * Tapping 'Confirm'/ 'Place bet' (From OX 99) button places bet(s) as per normal process
        EXPECTED: * Tapping 'Cancel' button/and than 'Cancel offer' pop-up (From OX 99) clears and closes Betslip
        """
        pass

    def test_007_repeat_steps_1_5_but_with_enabled_each_way_checkbox(self):
        """
        DESCRIPTION: Repeat steps #1-5 but with enabled 'Each Way' checkbox
        EXPECTED: *   Info message is displayed above 'Confirm' and 'Cancel' buttons with text: Please consider alternative offer from our trader" on the yellow background
        EXPECTED: *   The new stake is shown to the user on the Betslip (in green)
        EXPECTED: *   'Each Way' checkbox is unselected and highlighted in green
        EXPECTED: *   The Estimate returns are 'N/A' and highlighted in green
        EXPECTED: **From OX 99**
        EXPECTED: *   'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: *  The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * 'Win Only' is displayed below the new stake
        EXPECTED: *  The Estimate returns are 'N/A'
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        pass

    def test_008_repeat_step__6(self):
        """
        DESCRIPTION: Repeat step # 6
        EXPECTED: 
        """
        pass
