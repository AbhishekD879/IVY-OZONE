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
class Test_C91378_Trader_modifies_the_Leg_Type_Each_Way(Common):
    """
    TR_ID: C91378
    NAME: Trader modifies the Leg Type (Each Way)
    DESCRIPTION: This test case verifies offers displaying in Betslip when Leg Type was changed by Trader
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

    def test_001_add_selectionfrom_racing_event_to_betslip(self):
        """
        DESCRIPTION: Add selection from Racing event to Betslip
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

    def test_004_trigger_leg_type_and_stake_modification_by_trader_and_verify_offer_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Leg Type and Stake modification by Trader and verify offer displaying in Betslip
        EXPECTED: *   Info message is displayed above 'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons with text: "Please consider alternative offer from our trader" on the yellow background
        EXPECTED: *   Selection is expanded
        EXPECTED: *   The new stake is shown to the user on the Betslip (in green)
        EXPECTED: *   Enabled pre-ticked checkbox with a green icon is shown next to selection instead of '+'/'-' icon
        EXPECTED: *   'Each Way' checkbox is selected and highlighted in green
        EXPECTED: *   The Estimate returns are updated according to new stake (also highlighted in green)
        EXPECTED: **From OX 99**
        EXPECTED: *   'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: *  Selection is expanded
        EXPECTED: *  The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: *  'E/W' with a tick is displayed below the new stake
        EXPECTED: *  Values in 'Stake' and 'Est. Returns' fields are shown
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/31453)
        EXPECTED: ![](index.php?/attachments/get/31454)
        """
        pass

    def test_005_tap_on_accept__bet_number_of_accepted_bets_place_bet_from_ox_99_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap on 'Accept & Bet ([number of accepted bets])'/ 'Place bet' (From OX 99) or 'Cancel' buttons
        EXPECTED: * Tapping 'Accept & Bet ([number of accepted bets])' / 'Place bet' (From OX 99) button places bet(s) as per normal process
        EXPECTED: * Tapping 'Cancel' button/and than 'Cancel offer' pop-up (From OX 99) clears offer and selection(s) is shown without stake
        """
        pass

    def test_006_repeat_steps_1_4_with_enabled__each_way_checkbox(self):
        """
        DESCRIPTION: Repeat steps #1-4 with enabled  'Each Way' checkbox
        EXPECTED: *   Info message is displayed above 'Accept & Bet ([number of accepted bets])' and 'Cancel' buttons with text: 'Please, consider our trader's alternative Offer', highlighted in green
        EXPECTED: *    The new stake is shown to the user on the Betslip (in green)
        EXPECTED: *   'Each Way' checkbox is unselected
        EXPECTED: *   The Estimate returns are updated according to new stake (also highlighted in green)
        EXPECTED: **From OX 99**
        EXPECTED: *   'Sorry your bet has not gone through, we are offering you the following bet as an alternative'. 'Offer expires: X:XX' is shown and anchored to the Betslip header
        EXPECTED: *  The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * Win Only' is displayed below the new stake
        EXPECTED: * The Estimate returns are updated according to new stake
        EXPECTED: ![](index.php?/attachments/get/36199)
        """
        pass

    def test_007_repeat_steps_5(self):
        """
        DESCRIPTION: Repeat steps #5
        EXPECTED: 
        """
        pass

    def test_008__add_few_selections_to_the_betslipand_for_few_of_them_enter_stake_value_which_will_trigger_overask_for_the_selection_enable_each_way_for_one_selection(self):
        """
        DESCRIPTION: * Add few selections to the Betslip and for few of them enter stake value which will trigger Overask for the selection
        DESCRIPTION: * Enable 'Each Way' for one selection
        EXPECTED: 
        """
        pass

    def test_009_tap_bet_now_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now'/ 'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        pass

    def test_010_trigger_leg_type_and_stake_modification_by_trader_and_verify_offer_displaying_in_betslip(self):
        """
        DESCRIPTION: Trigger Leg Type and Stake modification by Trader and verify offer displaying in Betslip
        EXPECTED: * Info message is displayed above 'Accept & Bet ([number of accepted bets])' and 'Cancel'  buttons with text: 'Please, consider our trader's alternative Offer' highlighted in yellow
        EXPECTED: * The new stake is shown to the user on the Betslip (in green)
        EXPECTED: * 'Each Way' checkbox is updated according to Trader's changes
        EXPECTED: * The Estimate returns are updated according to new stake (also highlighted in green)
        EXPECTED: **From OX 99**
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative'. 'Offer expires: X:XX' is shown and anchored to the Betslip header
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * 'Win Only' is displayed below the new stake
        EXPECTED: * The Estimate returns are updated according to new stake
        """
        pass

    def test_011_repeat_step_5(self):
        """
        DESCRIPTION: Repeat step #5
        EXPECTED: 
        """
        pass
