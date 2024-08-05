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
class Test_C22329878_Verify_that_Win_Only_is_not_shown_when_leg_type_doesnt_change(Common):
    """
    TR_ID: C22329878
    NAME: Verify that ‘Win Only’ is not shown when leg type doesn't change
    DESCRIPTION: This test case verifies that ‘Win Only’ is shown only when leg type is changed from ‘E/W’
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

    def test_001_add_a_selectionfrom_racing_event_to_the_betslip(self):
        """
        DESCRIPTION: Add a selection from Racing event to the Betslip
        EXPECTED: Selection is successfully added
        """
        pass

    def test_002___enter_stake_value_which_is_higher_than_maximum_limit_each_way_checkbox_is_not_checked(self):
        """
        DESCRIPTION: *  Enter stake value which is higher than maximum limit
        DESCRIPTION: * 'Each Way' checkbox is NOT checked
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

    def test_004__do_not_change_leg_type_from_win_to_each_way_make_stakeprice_modification_by_trader_and_verify_offer_displaying_in_betslip(self):
        """
        DESCRIPTION: * Do NOT change Leg Type (from Win to Each way)
        DESCRIPTION: * Make Stake/Price modification by Trader and verify offer displaying in Betslip
        EXPECTED: *   'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: *  The new stake/price is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: *  ‘Each Way’ is NOT displayed below the new stake
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        pass

    def test_005_tap_on_place_bet_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap on 'Place bet' or 'Cancel' buttons
        EXPECTED: * Tapping 'Confirm'/ 'Place bet' (From OX 99) button places bet(s) as per normal process
        EXPECTED: * Tapping 'Cancel' button/and than 'Cancel offer' pop-up (From OX 99) clears offer and selection(s) is shown without stake
        """
        pass
