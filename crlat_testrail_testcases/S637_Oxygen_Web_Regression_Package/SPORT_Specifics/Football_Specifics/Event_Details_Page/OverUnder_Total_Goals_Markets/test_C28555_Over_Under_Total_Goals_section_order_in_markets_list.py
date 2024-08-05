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
class Test_C28555_Over_Under_Total_Goals_section_order_in_markets_list(Common):
    """
    TR_ID: C28555
    NAME: Over/Under Total Goals section order in markets list
    DESCRIPTION: This test case verifies 'Over/Under Total Goals' section order in markets list on Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with over/under markets (Total Goals Over/Under <figure afterward>, Over/Under First Half <figure afterward>, Over/Under Second Half <figure afterward>)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Note: **<figure afterward> **- variable part of market name shown in format 'X.5' as a amount of goals (e.g. 0.5, 1.5, 2.5 etc)
    PRECONDITIONS: Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Total Goals Over/Under x.x"
    PRECONDITIONS: *   PROD: name="Over/Under Total Goals x.x"
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

    def test_003_go_to_overunder_total_goals_section(self):
        """
        DESCRIPTION: Go to 'Over/Under Total Goals' section
        EXPECTED: Section contains data from the following markets:
        EXPECTED: *   Total Goals Over/Under <figure afterward>
        EXPECTED: *   Over/Under First Half <figure afterward>
        EXPECTED: *   Over/Under Second Half <figure afterward>
        EXPECTED: If markets are not available - section is not shown
        """
        pass

    def test_004_check_displayorder_attribute_values_of_all_markets_available_in_overunder_total_goals_section_in_ss_response(self):
        """
        DESCRIPTION: Check '**displayOrder**' attribute values of all markets available in 'Over/Under Total Goals' section in SS response
        EXPECTED: **Smallest displayOrder** of Total Goals Over/Under <figure afterward>, Over/Under First Half <figure afterward>, Over/Under Second Half <figure afterward> markets **is set as section's display order**
        """
        pass

    def test_005_check_sections_order_in_markets_list(self):
        """
        DESCRIPTION: Check section's order in markets list
        EXPECTED: Section is ordered by:
        EXPECTED: *   by displayOrder in ascending
        EXPECTED: *   if displayOrder is the same then alphanumerically
        """
        pass
