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
class Test_C1211834_Verify_events_data_on_Competitions_Outright_Details_page_on_Desktop(Common):
    """
    TR_ID: C1211834
    NAME: Verify events data on Competitions Outright Details page on Desktop
    DESCRIPTION: This test case verifies events data on Competitions Outright Details page on Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: * XXX - the event ID
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_football_competitions_details_page(self):
        """
        DESCRIPTION: Navigate to Football Competitions Details page
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' and 'Outrights' switchers are displayed in the same row as 'Market Selector' below the Competitions header and Breadcrumbs trail
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        """
        pass

    def test_003_choose_outrights_switcher_and_verify_outright_event_details(self):
        """
        DESCRIPTION: Choose 'Outrights' switcher and verify Outright event details
        EXPECTED: **Pre-match events:**
        EXPECTED: Events with next attributes are shown:
        EXPECTED: *   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20)
        EXPECTED: *   AND/OR **dispSortName **is positive (e.g. dispSortName="3W")
        EXPECTED: **Started events:**
        EXPECTED: Events with the following attributes are shown:
        EXPECTED: *   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20) AND/OR ​**dispSortName **is positive (e.g. dispSortName="3W")
        EXPECTED: *   AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED: *   AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
        """
        pass

    def test_004_verify_outrights_events_and_markets_attribute(self):
        """
        DESCRIPTION: Verify Outrights events and markets attribute
        EXPECTED: * Event name on 'Event Name Panel' corresponds to '**name**' attribute
        EXPECTED: * Event start date corresponds to '**startTime**' attribute
        EXPECTED: and it is shown in ** '&lt;name of the day&gt;, DD-MMM-YY 24 hours HH:MM'** format (e.g. 14:00 or 05:00)
        EXPECTED: * 'Each Way' terms is shown if '**isEachWayAvailable="true"**' attribute is received on market level
        EXPECTED: * 'LIVE' label is shown if event is live now: **rawIsOffCode="Y"** OR **rawIsOffCode="-"** AND **isStarted="true"**
        """
        pass

    def test_005_verify_events_order_on_competitions_details_page_outrights_switcher_that_has_several_outright_events_ie_world_cup_2018_europa_cup_copa_america_etc(self):
        """
        DESCRIPTION: Verify events order on Competitions Details page ('Outrights' switcher) that has several Outright events (i.e. 'World Cup 2018', 'Europa Cup', 'Copa America' etc.)
        EXPECTED: Events are ordered in the following way:
        EXPECTED: * 'startTime' - chronological order in the first instance
        EXPECTED: * Event 'displayOrder' in ascending
        EXPECTED: * Alphabetical order
        """
        pass

    def test_006_verify_markets_order_on_competitions_details_page(self):
        """
        DESCRIPTION: Verify markets order on Competitions Details page
        EXPECTED: Markets are ordered in the following way:
        EXPECTED: * Market 'displayOrder' in ascending
        EXPECTED: * Depends on ordering received in response from OB
        """
        pass
