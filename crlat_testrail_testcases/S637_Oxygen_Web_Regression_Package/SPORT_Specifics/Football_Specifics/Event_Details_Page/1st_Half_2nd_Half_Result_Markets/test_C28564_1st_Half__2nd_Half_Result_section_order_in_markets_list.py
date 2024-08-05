import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28564_1st_Half__2nd_Half_Result_section_order_in_markets_list(Common):
    """
    TR_ID: C28564
    NAME: 1st Half / 2nd Half Result section order in markets list
    DESCRIPTION: This test case verifies '1st Half / 2nd Half Result' section order in markets list on Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with 1st Half / 2nd Half Result markets (name="First-Half Result", name="Second-Half Result")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First-Half Result"
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

    def test_003_go_to_1st_half__2nd_half_result_section(self):
        """
        DESCRIPTION: Go to '1st Half / 2nd Half Result' section
        EXPECTED: Section contains data from two markets:
        EXPECTED: *   First-Half Result
        EXPECTED: *   Second-Half Result
        EXPECTED: If markets are not available - section is not shown
        """
        pass

    def test_004_check_displayorder_attribute_values_of_all_markets_available_in_1st_half__2nd_half_result_section_in_ss_response(self):
        """
        DESCRIPTION: Check '**displayOrder**' attribute values of all markets available in '1st Half / 2nd Half Result' section in SS response
        EXPECTED: **Smallest displayOrder** of First-Half Result, Second-Half Result markets **is set as section's display order**
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
