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
class Test_C2861767_1st_Half__2nd_Half_Result_market_section__no_data(Common):
    """
    TR_ID: C2861767
    NAME: 1st Half / 2nd Half Result market section - no data
    DESCRIPTION: This test case verifies '1st Half / 2nd Half Result' market section on Event Details Page.
    PRECONDITIONS: Football events with 1st Half / 2nd Half Result markets (name="First-Half Result", name="Second-Half Result")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First-Half Result"
    PRECONDITIONS: *   PROD: name="1st Half Result"
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_003_go_to_1st_half__2nd_half_result_market_section(self):
        """
        DESCRIPTION: Go to '1st Half / 2nd Half Result' market section
        EXPECTED: 
        """
        pass

    def test_004_verify_market_shown_for_1st_half_result(self):
        """
        DESCRIPTION: Verify market shown for '1st Half Result'
        EXPECTED: If market/outcomes within market are absent - nothing is shown within selected option
        """
        pass

    def test_005_verify_market_shown_for_2nd_half_result(self):
        """
        DESCRIPTION: Verify market shown for '2nd Half Result'
        EXPECTED: If market/outcomes within market are absent - nothing is shown within selected option
        """
        pass

    def test_006_verify_1st_half2nd_half_result_filters_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify '1st Half/2nd Half Result' filters in case of data absence
        EXPECTED: '1st Half/2nd Half Result' filters is not shown if:
        EXPECTED: *   all markets that section consists of are absent
        EXPECTED: *   all markets that section consists of do not have any outcomes
        """
        pass
