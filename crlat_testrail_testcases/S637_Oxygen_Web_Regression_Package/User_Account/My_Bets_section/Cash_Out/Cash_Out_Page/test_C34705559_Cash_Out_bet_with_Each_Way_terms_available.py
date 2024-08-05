import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C34705559_Cash_Out_bet_with_Each_Way_terms_available(Common):
    """
    TR_ID: C34705559
    NAME: Cash Out bet with Each Way terms available
    DESCRIPTION: This test case verifies Cash Out bet with Each Way terms available
    PRECONDITIONS: 1. Load app and log in
    PRECONDITIONS: 2. Place single and multiple HR bets with E/W option set and Cashout option available
    PRECONDITIONS: 3. Place single and multiple bets on Outright events with E/W option set and Cashout option available
    PRECONDITIONS: 4. Open DevTools and check the next request to SS to get Each-way data
    PRECONDITIONS: https://{domain}/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForOutcome/{outcomeIDs}?simpleFilter=event.suspendAtTime:greaterThan:2020-01-13T12:44:00.000Z&racingForm=outcome&includeUndisplayed=true&translationLang=en&includeRestricted=true&prune=event&prune=market
    PRECONDITIONS: where,
    PRECONDITIONS: *   outcomeIDs - valid ID(s) of outcome that bet was placed on
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   domain - resource domain
    PRECONDITIONS: e.g. ss-aka-ori.coral.co.uk - Prod
    PRECONDITIONS: ![](index.php?/attachments/get/52704924)
    """
    keep_browser_open = True

    def test_001_navigate_to_cash_out_tab_for_coral_brandor_open_bets_tab_for_ladbrokes_brand(self):
        """
        DESCRIPTION: Navigate to 'Cash Out' tab for **Coral** brand
        DESCRIPTION: or 'Open Bets' tab for **Ladbrokes** brand
        EXPECTED: * 'Cash Out'/'Open Bets' tab is loaded
        """
        pass

    def test_002_verify_single_hr_cash_out_bet_with_each_way_terms(self):
        """
        DESCRIPTION: Verify **single** HR Cash Out bet with each-way terms
        EXPECTED: * 'Each Way' text is shown in brackets next to bet type
        EXPECTED: * Each way terms are displayed next to the market name in the next format:
        EXPECTED: 'x/y odds - places z,j,k'
        EXPECTED: e.g. 1/4 odds - places 1,2,4
        EXPECTED: ![](index.php?/attachments/get/53285767)
        """
        pass

    def test_003_verify_each_way_terms_availability(self):
        """
        DESCRIPTION: Verify each-way terms availability
        EXPECTED: Each-way terms are displayed if 'isEachWayAvailable' = 'true' attribute is present in the SS response on market level for a particular event
        EXPECTED: ![](index.php?/attachments/get/53285768)
        """
        pass

    def test_004_verify_each_way_terms_correctness(self):
        """
        DESCRIPTION: Verify each-way terms correctness
        EXPECTED: Terms correspond to the 'eachWayFactorNum', 'eachWayFactorDen' and 'eachWayPlaces' attributes from SS response for particular event
        EXPECTED: ![](index.php?/attachments/get/53285769)
        """
        pass

    def test_005_repeat_steps_2_4_for_multiple_hr_cash_out_bet_with_each_way_terms(self):
        """
        DESCRIPTION: Repeat steps #2-4 for **multiple** HR Cash Out bet with each-way terms
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_2_4_for_single_outright_cash_out_bet_with_each_way_terms(self):
        """
        DESCRIPTION: Repeat steps #2-4 for **single** Outright Cash Out bet with each-way terms
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_2_4_for_multiple_outright_cash_out_bet_with_each_way_terms(self):
        """
        DESCRIPTION: Repeat steps #2-4 for **multiple** Outright Cash Out bet with each-way terms
        EXPECTED: 
        """
        pass
