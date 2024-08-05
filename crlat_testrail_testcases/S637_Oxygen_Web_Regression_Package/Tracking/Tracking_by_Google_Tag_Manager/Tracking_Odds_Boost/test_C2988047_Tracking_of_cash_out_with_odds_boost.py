import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2988047_Tracking_of_cash_out_with_odds_boost(Common):
    """
    TR_ID: C2988047
    NAME: Tracking of cash out with odds boost
    DESCRIPTION: This Test Case verifies tracking of cash out when bet placed with odds boost
    PRECONDITIONS: User is logged in and has positive balance
    PRECONDITIONS: Browser console should be opened
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CREATE Odds Boost token with ANY Bet Type
    PRECONDITIONS: Add just created odds boost tokens to USER1
    PRECONDITIONS: Login with USER1.
    PRECONDITIONS: Place Single bet with odds boost (where cash out available)
    PRECONDITIONS: To view response open Dev tools -> Network -> WS -> choose the last request
    """
    keep_browser_open = True

    def test_001_navigate_to_by_betscash_outverify_that_placed_single_bet_in_preconditions_is_shown_with_odds_boost_title(self):
        """
        DESCRIPTION: Navigate to By Bets>Cash Out
        DESCRIPTION: Verify that placed SINGLE bet in preconditions is shown with odds boost title
        EXPECTED: - Odds Boost title is shown for SINGLE bet
        EXPECTED: - SINGLE Bet is shown with 'Cash Out' and 'Partial Cash Out' buttons
        """
        pass

    def test_002_tap_partial_cash_outcash_out__buttontap_partial_confirm_cash_outverify_that_successful_cash_out_button_is_shown(self):
        """
        DESCRIPTION: Tap Partial Cash Out>Cash Out  button
        DESCRIPTION: Tap Partial Confirm Cash Out
        DESCRIPTION: Verify that Successful Cash Out button is shown
        EXPECTED: - Successful Cash Out button is shown
        """
        pass

    def test_003_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: cashOutType: "partial"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "attempt"
        EXPECTED: eventCategory: "cash out"
        EXPECTED: eventLabel: "success"
        EXPECTED: 'oddsBoost' : 'yes'
        """
        pass

    def test_004_navigate_to_by_betscash_out_one_more_timeverify_that_placed_single_bet_in_preconditions_is_shown_with_odds_boost_title(self):
        """
        DESCRIPTION: Navigate to By Bets>Cash Out one more time
        DESCRIPTION: Verify that placed SINGLE bet in preconditions is shown with odds boost title
        EXPECTED: - Odds Boost title is shown for SINGLE bet
        EXPECTED: - SINGLE Bet is shown with 'Cash Out' and 'Partial Cash Out' buttons
        """
        pass

    def test_005_tap_cash_out_buttontap_confirm_cash_outverify_that_successful_cash_out_button_is_shown_and_the_bet_is_disappeared_from_cash_out_list(self):
        """
        DESCRIPTION: Tap Cash Out button
        DESCRIPTION: Tap Confirm cash out
        DESCRIPTION: Verify that Successful Cash Out button is shown and the bet is disappeared from Cash out list
        EXPECTED: - Successful Cash Out button is shown
        EXPECTED: - Bet is NOT shown in My Bets>Cash Out list
        """
        pass

    def test_006_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: cashOutType: "fulll"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "attempt"
        EXPECTED: eventCategory: "cash out"
        EXPECTED: eventLabel: "success"
        EXPECTED: 'oddsBoost' : 'yes'
        """
        pass

    def test_007_provide_the_same_verification_for_double_betverify_that__oddsboost_no__push_is_sent_to_ga(self):
        """
        DESCRIPTION: Provide the same verification for DOUBLE bet
        DESCRIPTION: Verify that " 'oddsBoost': 'no' " push is sent to GA
        EXPECTED: The next push is sent to GA same as for SINGLE bet:
        EXPECTED: cashOutType: "fulll"
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "attempt"
        EXPECTED: eventCategory: "cash out"
        EXPECTED: eventLabel: "success"
        EXPECTED: 'oddsBoost' : 'no'
        """
        pass
