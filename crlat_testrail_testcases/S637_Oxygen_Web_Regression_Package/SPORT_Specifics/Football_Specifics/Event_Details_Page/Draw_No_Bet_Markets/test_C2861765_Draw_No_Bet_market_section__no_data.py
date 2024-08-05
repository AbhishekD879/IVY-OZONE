import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C2861765_Draw_No_Bet_market_section__no_data(Common):
    """
    TR_ID: C2861765
    NAME: Draw No Bet market section - no data
    DESCRIPTION: This test case verifies 'Draw No Bet' market section on Event Details Page
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with draw no bet markets (Draw No Bet, Half-Time Draw No Bet, Second-Half Draw No Bet)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Half-Time Draw No Bet"
    PRECONDITIONS: *   PROD: name="1st Half Draw No Bet"
    PRECONDITIONS: **Jira ticket: **BMA-4072
    """
    keep_browser_open = True

    def test_001_go_to_event_details_page_of_football_event_and_expand_draw_no_bet_market(self):
        """
        DESCRIPTION: Go to Event Details page of Football event and expand 'Draw No Bet' market
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_002_verify_market__90_mins(self):
        """
        DESCRIPTION: Verify market  '90 mins'
        EXPECTED: If market/outcomes within market are absent - nothing is shown within selected option
        """
        pass

    def test_003_verify_market_1st_half(self):
        """
        DESCRIPTION: Verify market '1st Half'
        EXPECTED: If market/outcomes within market are absent - nothing is shown within selected option
        """
        pass

    def test_004_verify_market_2nd_half(self):
        """
        DESCRIPTION: Verify market '2nd Half'
        EXPECTED: If market/outcomes within market are absent - nothing is shown within selected option
        """
        pass

    def test_005_verify_draw_no_bet_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Draw No Bet' section in case of data absence
        EXPECTED: 'Draw No Bet' section is not shown if:
        EXPECTED: *   all markets that section consists of are absent
        EXPECTED: *   all markets that section consists of do not have any outcomes
        """
        pass
