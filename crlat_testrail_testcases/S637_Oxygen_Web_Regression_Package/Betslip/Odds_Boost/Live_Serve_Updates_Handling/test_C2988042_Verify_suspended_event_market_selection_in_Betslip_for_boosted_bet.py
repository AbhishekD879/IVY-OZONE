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
class Test_C2988042_Verify_suspended_event_market_selection_in_Betslip_for_boosted_bet(Common):
    """
    TR_ID: C2988042
    NAME: Verify suspended event/market/selection in Betslip for boosted bet
    DESCRIPTION: This test case verifies suspended event/market/selection in Betslip for boosted bet
    PRECONDITIONS: Enable Odds Boost in CMS
    PRECONDITIONS: Load Application
    PRECONDITIONS: Login into App by user with Odds boost token generated
    PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Add selection to Betslip
    PRECONDITIONS: Tap 'Boost' button
    """
    keep_browser_open = True

    def test_001_make_eventmarketselection_suspended_for_added_selection_from_precondition_in_httpsbackoffice_tst2coralcoukti(self):
        """
        DESCRIPTION: Make event/market/selection suspended (for added selection from precondition) in https://backoffice-tst2.coral.co.uk/ti
        EXPECTED: Suspension overlay is displayed
        """
        pass

    def test_002_verify_the_overlay_content_for_suspendedselectionmarketevent(self):
        """
        DESCRIPTION: Verify the overlay content for suspended:
        DESCRIPTION: /selection/market/event
        EXPECTED: **Before OX99**
        EXPECTED: - Odds, Stake, Est. Returns are disabled
        EXPECTED: - Sorry, the outcome has been suspended/
        EXPECTED: Sorry, the market has been suspended/
        EXPECTED: Sorry, the event has been suspended
        EXPECTED: - Warning message 'Please beware that # of your selections has been suspended' is shown on the yellow background in the bottom of the Betslip
        EXPECTED: **From OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_003_verify_that_the_boost_remain_selected_when_the_suspension_ends(self):
        """
        DESCRIPTION: Verify that the boost remain selected when the suspension ends
        EXPECTED: When the suspension ends the boost remains selected
        """
        pass
