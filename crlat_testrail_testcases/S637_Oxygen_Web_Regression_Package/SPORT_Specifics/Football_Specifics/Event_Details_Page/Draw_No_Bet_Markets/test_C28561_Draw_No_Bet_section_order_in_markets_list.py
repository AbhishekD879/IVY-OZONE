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
class Test_C28561_Draw_No_Bet_section_order_in_markets_list(Common):
    """
    TR_ID: C28561
    NAME: Draw No Bet section order in markets list
    DESCRIPTION: This test case verifies 'Draw No Bet' section order in markets list on Event Details Page
    DESCRIPTION: Test case needs to be run on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with draw no bet markets (Draw No Bet, Half-Time Draw No Bet, Second-Half Draw No Bet)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Half-Time Draw No Bet"
    PRECONDITIONS: *   PROD: name="1st Half Draw No Bet"
    PRECONDITIONS: **Jira ticket: **BMA-4072
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_003_go_to_draw_no_bet_section(self):
        """
        DESCRIPTION: Go to 'Draw No Bet' section
        EXPECTED: Section contains data from three markets:
        EXPECTED: *   Draw No Bet
        EXPECTED: *   Half-Time Draw No Bet
        EXPECTED: *   Second-Half Draw No Bet
        EXPECTED: If markets are not available - section is not shown
        """
        pass

    def test_004_check_displayorder_attribute_values_of_all_markets_available_in_draw_no_bet_section_in_ss_response(self):
        """
        DESCRIPTION: Check '**displayOrder**' attribute values of all markets available in 'Draw No Bet' section in SS response
        EXPECTED: **Smallest displayOrder** of Draw No Bet, Half-Time Draw No Bet, Second-Half Draw No Bet markets **is set as section's display order**
        """
        pass

    def test_005_check_sections_order_in_markets_list(self):
        """
        DESCRIPTION: Check section's order in markets list
        EXPECTED: Section is ordered by:
        EXPECTED: *   by** displayOrder** **in ascending**
        EXPECTED: *   if displayOrder is the same then **alphanumerically**
        """
        pass
