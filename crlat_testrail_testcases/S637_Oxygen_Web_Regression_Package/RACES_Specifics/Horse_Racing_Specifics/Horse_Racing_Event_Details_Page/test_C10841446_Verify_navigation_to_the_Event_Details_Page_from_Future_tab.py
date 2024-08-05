import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C10841446_Verify_navigation_to_the_Event_Details_Page_from_Future_tab(Common):
    """
    TR_ID: C10841446
    NAME: Verify navigation to the Event Details Page from Future tab
    DESCRIPTION: This test case verifies how a user can get to the event details page for <Horse Racing> sport type from Future tab
    PRECONDITIONS: In order to create HR Antepost event use TI tool http://backoffice-tst2.coral.co.uk/ti/
    PRECONDITIONS: 'Antepost' check box should be checked on event level ('drilldownTagNames'='EVFLAG_AP' in SS response)
    PRECONDITIONS: with only one of the following:
    PRECONDITIONS: 'Flat' check box should be checked on event level ('drilldownTagNames'='EVFLAG_FT' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: 'National Hunt' check box should be checked on event level ('drilldownTagNames'='EVFLAG_NH' in SS response)
    PRECONDITIONS: OR
    PRECONDITIONS: 'International' check box should be checked on event level ('drilldownTagNames'='EVFLAG_IT' in SS response)
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing Landing page
        EXPECTED: Horse Racing Landing Page is opened
        """
        pass

    def test_002_tap_on_future_tab(self):
        """
        DESCRIPTION: Tap on 'Future' tab
        EXPECTED: * Future tab is opened
        EXPECTED: * 'Flat Races', 'National Hunt' and 'International' subtabs are displayed (if containing at least one event that meets Preconditions, otherwise a switcher is not displayed)
        """
        pass

    def test_003_open_flat_races_subtab_and_click_on_an_event(self):
        """
        DESCRIPTION: Open 'Flat Races' subtab and click on an event
        EXPECTED: Event Details Page of the selected event is opened
        """
        pass

    def test_004_open_national_hunt_subtab_and_click_on_an_event(self):
        """
        DESCRIPTION: Open 'National Hunt' subtab and click on an event
        EXPECTED: Event Details Page of the selected event is opened
        """
        pass

    def test_005_open_international_subtab_and_click_on_an_event(self):
        """
        DESCRIPTION: Open 'International' subtab and click on an event
        EXPECTED: Event Details Page of the selected event is opened
        """
        pass
