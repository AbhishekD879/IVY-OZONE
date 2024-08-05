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
class Test_C28531_Double_Chance_section_order_in_markets_list(Common):
    """
    TR_ID: C28531
    NAME: Double Chance section order in markets list
    DESCRIPTION: This test case verifies Double Chance '90 mins / 1st Half / 2nd Half' section order in markets list.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with Double Chance '90 mins / 1st Half / 2nd Half' markets (name='Double Chance', name="Half-Time Double Chance", name="Second-Half Double Chance")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:** Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Half-Time Double Chance"
    PRECONDITIONS: *   PROD: name="1st Half Double Chance"
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

    def test_003_go_to_double_chance_market_section(self):
        """
        DESCRIPTION: Go to 'Double Chance' market section
        EXPECTED: Section contains data from three markets:
        EXPECTED: *   Double Chance ('90 mins' section)
        EXPECTED: *   Half-Time Double Chance ('1st Half' section)
        EXPECTED: *   Second-Half Double Chance (2st Half' section)
        EXPECTED: If markets are not available - section does not contain data
        """
        pass

    def test_004_check_displayorder_attribute_values_of_all_markets_available_in_double_chance_section_in_ss_response_and_displaying_in_markets_list(self):
        """
        DESCRIPTION: Check 'displayOrder' attribute values of all markets available in 'Double Chance' section in SS response and displaying in markets list
        EXPECTED: **Smallest displayOrder** of Double Chance, Half-Time Double Chance, Second-Half Double Chance markets **is set as section's display order**
        """
        pass

    def test_005_check_double_chance_market_section_order_in_markets_list(self):
        """
        DESCRIPTION: Check 'Double Chance' market section order in markets list
        EXPECTED: Market section is ordered by:
        EXPECTED: *   ** displayOrder** **in ascending**
        EXPECTED: *   if displayOrder is the same then **alphanumerically**
        """
        pass
