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
class Test_C28538_Handicap_section_order_in_markets_list(Common):
    """
    TR_ID: C28538
    NAME: Handicap section order in markets list
    DESCRIPTION: This test case verifies Handicap section order in markets list
    DESCRIPTION: Test case needs to be run on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with Handicap markets (name="Handicap Match Result", name="Handicap First Half", name="Handicap Second Half")
    PRECONDITIONS: To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. EN)
    PRECONDITIONS: Jira ticket: BMA-3900
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Home page is loaded
        """
        pass

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing Page is opened
        """
        pass

    def test_003_select_football_event_with_handicap_markets_available(self):
        """
        DESCRIPTION: Select Football event with Handicap Markets available
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_tapclick_on_all_markets_tab(self):
        """
        DESCRIPTION: Tap/click on 'All markets' tab
        EXPECTED: All available markets are shown
        """
        pass

    def test_005_go_to_handicap_results_section(self):
        """
        DESCRIPTION: Go to 'Handicap Results' section
        EXPECTED: Market section contains data from three markets:
        EXPECTED: *   Handicap Match Result ('90 min' tab)
        EXPECTED: *   Handicap First Half ('1st half' tab)
        EXPECTED: *   Handicap Second Half (2nd half' tab)
        EXPECTED: If markets are not available - section is not shown
        """
        pass

    def test_006_check_displayorder_attribute_values_of_all_markets_available_in_handicap_results_section_in_ss_response(self):
        """
        DESCRIPTION: Check 'displayOrder' attribute values of all markets available in 'Handicap Results' section in SS response
        EXPECTED: **Smallest displayOrder** of Handicap Match Result, Handicap First Half, Handicap Second Half markets **is set as section's display order**
        """
        pass

    def test_007_check_market_sections_order_in_markets_list(self):
        """
        DESCRIPTION: Check market section's order in markets list
        EXPECTED: Section is ordered by:
        EXPECTED: *   by** displayOrder** **in ascending**
        EXPECTED: *   if displayOrder is the same then **alphanumerically**
        """
        pass
