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
class Test_C28550_Verify_ordering_of_selections_within_Goalscorer_sections(Common):
    """
    TR_ID: C28550
    NAME: Verify ordering of selections within Goalscorer sections
    DESCRIPTION: This test case verifies ordering of selections within Goalscorer sections.
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
        EXPECTED: Section is expanded and displayed correctly
        """
        pass

    def test_004_find_first_available_market_first_column_in_the_list_in_goalscorer_section(self):
        """
        DESCRIPTION: Find first available market (first column) in the list in Goalscorer section
        EXPECTED: Markets are ordered in the following way
        EXPECTED: *   '1st' ('First Goalscorer')
        EXPECTED: *   'Anytime' ('Anytime Goalscorer')
        EXPECTED: *   '2 or More' ('Goalscorer - 2 or More')
        """
        pass

    def test_005_verify_prices_order_for_market_from_step_4(self):
        """
        DESCRIPTION: Verify prices order for market from step №4
        EXPECTED: *   Selections are ordered **by price** in ascending order for verified market
        EXPECTED: *   Players names are ordered accordingly with prices of verified market
        EXPECTED: *   Outcomes of other markets (e.g. '2 or More') are ordered accordingly
        EXPECTED: *   'No goalscorer' is shown at the end of the list if available
        """
        pass

    def test_006_go_to_other_goalscorer_markets_section(self):
        """
        DESCRIPTION: Go to 'Other Goalscorer Markets' section
        EXPECTED: Section is expanded and displayed correctly
        """
        pass

    def test_007_find_first_available_market_in_the_list_in_goalscorer_section(self):
        """
        DESCRIPTION: Find first available market in the list in Goalscorer section
        EXPECTED: Markets are ordered in the following way
        EXPECTED: *   'Last' ('Last Goalscorer')
        EXPECTED: *   'Hatrick' ('Hat trick')
        """
        pass

    def test_008_verify_prices_order_for_market_from_step_7(self):
        """
        DESCRIPTION: Verify prices order for market from step №7
        EXPECTED: *   Selections are ordered **by price** in ascending order for verified market
        EXPECTED: *   Players names are ordered accordingly with prices of verified market
        EXPECTED: *   Outcomes of other market are ordered accordingly
        EXPECTED: *   'No goalscorer' is shown in the end of the list if available
        """
        pass
