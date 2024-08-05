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
class Test_C2605968_Verify_suspended_event_market_selection_in_Quick_bet_for_boosted_bet(Common):
    """
    TR_ID: C2605968
    NAME: Verify suspended event/market/selection in Quick bet for boosted bet
    DESCRIPTION: This test case verifies suspension of event/market/selection in Quick Bet for boosted bet and the behavior of related UI elements.
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: Enable Odds Boost in CMS
    PRECONDITIONS: Load Application
    PRECONDITIONS: Login into App by user with Odds boost token generated
    PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page
        EXPECTED: Boost is available for this bet ('Boost' button is present)
        """
        pass

    def test_002_make_eventmarketselection_suspended_for_the_selection_in_quickbet(self):
        """
        DESCRIPTION: Make event/market/selection suspended for the selection in QuickBet
        EXPECTED: 'Your event/market/selection has been suspended' warning message is displayed below Quick Bet (yellow) background for Coral; cyan background for Ladbrokes)
        EXPECTED: 'Boost' button disappears
        """
        pass

    def test_003_unsuspended_eventmarketselection_used_in_quickbet(self):
        """
        DESCRIPTION: Unsuspended event/market/selection used in QuickBet
        EXPECTED: Warning message disappears
        EXPECTED: Boost is again available for this bet ('Boost' button is shown again)
        """
        pass

    def test_004_tap_on_boost_button(self):
        """
        DESCRIPTION: Tap on 'Boost' button
        EXPECTED: Button changes to 'Boosted'
        EXPECTED: Crossed out original price(its value) of the selection is shown near the 'boosted' value within the grey(Coral)/yellow(Ladbrokes) frame
        """
        pass

    def test_005_make_eventmarketselection_suspended_for_the_selection_in_quickbet(self):
        """
        DESCRIPTION: Make event/market/selection suspended for the selection in QuickBet
        EXPECTED: Your event/market/selection has been suspended' warning message is displayed below Quick Bet (yellow) background for Coral; cyan background for Ladbrokes)
        EXPECTED: 'Boost' button disappears
        EXPECTED: Crossed out original price and 'boosted' value disappear
        """
        pass

    def test_006_unsuspended_eventmarketselection_used_in_quickbet(self):
        """
        DESCRIPTION: Unsuspended event/market/selection used in QuickBet
        EXPECTED: Warning message disappears
        EXPECTED: 'Boosted' button is shown again
        EXPECTED: Crossed out original price(its value) of the selection is shown near the 'boosted' value within the grey(Coral)/yellow(Ladbrokes) frame
        """
        pass
