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
class Test_C1474021_Verify_Next_Events_Module_data_correctness(Common):
    """
    TR_ID: C1474021
    NAME: Verify Next Events Module data correctness
    DESCRIPTION: This test case verifies data correctness for Next Events Module on Big Competition page
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Module with type = 'NEXT_EVENTS' should be created, enabled and set up in CMS
    PRECONDITIONS: * To check response open DEV Tools -> select 'Network' tab -> 'XHR' -> set 'competition' filter and select GET tab/subtab by ID request
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_competition_page(self):
        """
        DESCRIPTION: Navigate to Competition page
        EXPECTED: * Competition page is opened
        EXPECTED: * Default Tab is opened (e.g. Featured)
        """
        pass

    def test_003_go_to_next_events_module(self):
        """
        DESCRIPTION: Go to Next Events Module
        EXPECTED: 
        """
        pass

    def test_004_verify_events_filtering(self):
        """
        DESCRIPTION: Verify events filtering
        EXPECTED: Events displayed corresponds to **competitionModules.events** attribute from GET tab/sub tab response
        """
        pass

    def test_005_verify_events_ordering(self):
        """
        DESCRIPTION: Verify events ordering
        EXPECTED: Events ordering is done according to date/time of events and corresponds to **competitionModules.events.startTime** attribute from GET tab/sub tab response
        EXPECTED: If two events have the same date/time, then the order corresponds to **competitionModules.markets.data.displayOrder** attribute from GET tab/sub tab response
        """
        pass

    def test_006_verify_primary_market(self):
        """
        DESCRIPTION: Verify primary market
        EXPECTED: Primary market corresponds to **competitionModules.events.markets.name** attribute from GET tab/sub tab response
        """
        pass

    def test_007_verify_abbreviation_correctness(self):
        """
        DESCRIPTION: Verify abbreviation correctness
        EXPECTED: Abreviation of Home Team corresponds to **competitionModules.events.participants.HOME** attribute from GET tab/sub tab response
        EXPECTED: Abreviation of Away Team corresponds to **competitionModules.events.participants.AWAY** attribute from GET tab/sub tab response
        """
        pass

    def test_008_verify_event_date(self):
        """
        DESCRIPTION: Verify event date
        EXPECTED: Event start time corresponds to **competitionModules.events.startTime** attribute from GET tab/sub tab response
        """
        pass

    def test_009_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection names corresponds to **competitionModules.events.markets.outcomes[i].name** attribute from GET tab/sub tab response
        EXPECTED: Where **i** is corresponds to each selection
        """
        pass

    def test_010_verify_price_odds(self):
        """
        DESCRIPTION: Verify price odds
        EXPECTED: Prices odds corresponds to **competitionModules.events.markets.outcomes.prices** attribute from GET tab/sub tab response
        """
        pass
