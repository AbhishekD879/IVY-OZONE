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
class Test_C49893364_Verify_betErrors_field_in_buildBet(Common):
    """
    TR_ID: C49893364
    NAME: Verify <betErrors> field in <buildBet>
    DESCRIPTION: This test case verifies <betErrors> field in <buildBet> request after adding selection to BetSlip
    PRECONDITIONS: - Oxygen app is loaded
    PRECONDITIONS: - TI is loaded
    """
    keep_browser_open = True

    def test_001_open_oxygens_home_page(self):
        """
        DESCRIPTION: Open Oxygen's home page
        EXPECTED: Home page is loaded, list of events is displayed
        EXPECTED: (may be tested from sport landing page or from any other place where User can add selection to BetSlip)
        """
        pass

    def test_002_open_chrome_devtools_and_apply_network___all_filtering(self):
        """
        DESCRIPTION: Open Chrome DevTools and apply Network - All filtering
        EXPECTED: DevTools window is displayed, filter is applied
        """
        pass

    def test_003_filter_requests_by_buildbet(self):
        """
        DESCRIPTION: Filter requests by <buildBet>
        EXPECTED: List of requests is empty
        """
        pass

    def test_004_add_2_selections_from_different_events_to_betslip(self):
        """
        DESCRIPTION: Add 2 selections from different events to Betslip
        EXPECTED: Both selections are added to Betslip
        """
        pass

    def test_005_go_to_ti_and_open_one_of_selections_added_to_betslip_previously(self):
        """
        DESCRIPTION: Go to TI, and open one of selections, added to Betslip previously
        EXPECTED: '~ti/hierarchy/selection/selection_id' is opened
        """
        pass

    def test_006_change_selections_status_to_suspended_save_changes(self):
        """
        DESCRIPTION: Change selection's Status to 'Suspended', save changes
        EXPECTED: 
        """
        pass

    def test_007_open_oxygen_and_verify_that_one_of_selections_in_betslip_became_suspended(self):
        """
        DESCRIPTION: Open Oxygen and verify that one of selections in Betslip became suspended
        EXPECTED: 
        """
        pass

    def test_008_remove_active_selection_from_betslip_open_newest_buildbet_request(self):
        """
        DESCRIPTION: Remove ACTIVE selection from Betslip, open newest buildBet request
        EXPECTED: buildBet request is in the requests list with next branches:
        EXPECTED: - legs
        EXPECTED: - bets
        EXPECTED: - outcomeDetails
        EXPECTED: - betErrors
        """
        pass

    def test_009_expand_outcomedetails_and_beterrors_branches(self):
        """
        DESCRIPTION: Expand outcomeDetails and betErrors branches
        EXPECTED: Next result is displayed (example):
        EXPECTED: outcomeDetails: [,…]
        EXPECTED: 0: {id: "112957526", priceNum: "1", priceDen: "56", startPriceNum: "", startPriceDen: "", fbResult: "H",…}
        EXPECTED: id: "112957526"
        EXPECTED: priceNum: "1"
        EXPECTED: priceDen: "56"
        EXPECTED: startPriceNum: ""
        EXPECTED: startPriceDen: ""
        EXPECTED: fbResult: "H"
        EXPECTED: eventMarketSort: "MR"
        EXPECTED: handicap: ""
        EXPECTED: eachWayNum: ""
        EXPECTED: eachWayDen: ""
        EXPECTED: eachWayPlaces: ""
        EXPECTED: name: "|Bumble|"
        EXPECTED: marketId: "31500162"
        EXPECTED: marketDesc: "|Match Betting|"
        EXPECTED: eventId: "776548"
        EXPECTED: eventDesc: "|Bumble| |vs| |Bee DNTOUCH|"
        EXPECTED: typeId: "442"
        EXPECTED: typeDesc: "|Premier League|"
        EXPECTED: classId: "97"
        EXPECTED: className: "|Football England|"
        EXPECTED: categoryId: "16"
        EXPECTED: category: "FOOTBALL"
        EXPECTED: status: "S"
        EXPECTED: birIndex: ""
        EXPECTED: accMin: "1"
        EXPECTED: accMax: "25"
        EXPECTED: betErrors: [{errorDesc: "Bet override found", subErrorCode: "OUTCOME_SUSPENDED", code: "EVENT_ERROR",…}]
        EXPECTED: 0: {errorDesc: "Bet override found", subErrorCode: "OUTCOME_SUSPENDED", code: "EVENT_ERROR",…}
        EXPECTED: errorDesc: "Bet override found"
        EXPECTED: subErrorCode: "OUTCOME_SUSPENDED"
        EXPECTED: code: "EVENT_ERROR"
        EXPECTED: outcomeRef: {id: "112957526"}
        EXPECTED: id: "112957526"
        """
        pass

    def test_010_repeat_steps_8_13_on_market_and_event_levels(self):
        """
        DESCRIPTION: Repeat steps 8-13 on market and event levels
        EXPECTED: Behavior is the same on event and market levels, 'betErrors' branch is added in case of event/market suspension
        """
        pass
