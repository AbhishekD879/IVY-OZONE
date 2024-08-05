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
class Test_C2745403_Double_Chance_market_section__no_data(Common):
    """
    TR_ID: C2745403
    NAME: Double Chance market section - no data
    DESCRIPTION: This test case verifies Double Chance market section.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with Double Chance markets (name="Double Chance", name="First-Half Double Chance, name="Second-Half Double Chance")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Half-Time Double Chance"
    PRECONDITIONS: *   PROD: name="1st Half Double Chance"
    """
    keep_browser_open = True

    def test_001_open_event_details_page(self):
        """
        DESCRIPTION: Open Event Details page
        EXPECTED: 
        """
        pass

    def test_002_verify_double_chance_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Double Chance' section in case of data absence
        EXPECTED: 'Double Chance' section is not shown if:
        EXPECTED: *   all markets that section consists of are absent
        EXPECTED: *   all markets that section consists of do not have any outcomes
        """
        pass
