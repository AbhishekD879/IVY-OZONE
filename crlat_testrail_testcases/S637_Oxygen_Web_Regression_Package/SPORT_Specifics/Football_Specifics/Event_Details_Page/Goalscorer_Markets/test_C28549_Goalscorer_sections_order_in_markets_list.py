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
class Test_C28549_Goalscorer_sections_order_in_markets_list(Common):
    """
    TR_ID: C28549
    NAME: Goalscorer sections order in markets list
    DESCRIPTION: This test case verifies Goalscorer sections order (Popular Goalscorer Markets and Other Goalscorer Markets) in markets list on Football Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with goalscorer markets (First Goalscorer, Anytime Goalscorer, Goalscorer - 2 or More, Last Goalscorer, Hat trick)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Anytime Goalscorer"
    PRECONDITIONS: *   PROD: name="Goal Scorer - Anytime"
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

    def test_003_go_to_popular_goalscorer_markets_section(self):
        """
        DESCRIPTION: Go to 'Popular Goalscorer Markets' section
        EXPECTED: Section contains data from three goalscorer markets:
        EXPECTED: *   'First Goalscorer'
        EXPECTED: *   'Anytime Goalscorer'
        EXPECTED: *   'Goalscorer - 2 or More'
        """
        pass

    def test_004_check_displayorder_attribute_values_of_all_markets_available_in_goalscorer_section_in_ss_response(self):
        """
        DESCRIPTION: Check '**displayOrder**' attribute values of all markets available in Goalscorer section in SS response
        EXPECTED: **Smallest displayOrder** of markets **is set as section's display order**
        """
        pass

    def test_005_check_sections_order_in_markets_list(self):
        """
        DESCRIPTION: Check section's order in markets list
        EXPECTED: Section is ordered by:
        EXPECTED: *   by displayOrder in ascending
        EXPECTED: *   if displayOrder is the same then Alphanumerically
        """
        pass

    def test_006_go_to_other_goalscorer_markets_section(self):
        """
        DESCRIPTION: Go to 'Other Goalscorer Markets' section
        EXPECTED: Section contains data from two goalscorer markets:
        EXPECTED: *   'Last Goalscorer'
        EXPECTED: *   'Hat trick'
        """
        pass

    def test_007_verify_location_ofother_goalscorer_markets_section(self):
        """
        DESCRIPTION: Verify location of 'Other Goalscorer Markets' section
        EXPECTED: *   'Other Goalscorer Markets' section is located right after 'Popular Goalscorer Markets' section
        EXPECTED: *   If 'Popular Goalscorer Markets' section is absent repeat step №4-5
        """
        pass
