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
class Test_C9608412_Verify_Google_Tracking_of_Standings_on_Football_Competitions(Common):
    """
    TR_ID: C9608412
    NAME: Verify Google Tracking of Standings on Football Competitions
    DESCRIPTION: This test case verifies Google Analytics tracking of Standings on Football Competitions
    PRECONDITIONS: 1)Navigate to Football landing page > Competitions tab
    PRECONDITIONS: 2)Expand any class accordion and click on any type (e.g. Premier League)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: 'Standings' tab is displayed if a league table is available for that league on the competition page(received from Bet Radar)
    """
    keep_browser_open = True

    def test_001_tap_on_standings_tab(self):
        """
        DESCRIPTION: Tap on "Standings" tab
        EXPECTED: - User is navigated to the appropriate (e.g. Premier League) competition page
        EXPECTED: - The league table for that competition for current season is displayed
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: dataLayer.push(
        EXPECTED: {     'event' : 'trackEvent',     'eventCategory' : 'football',     'eventAction' : 'league table',     'eventLabel' : 'view league table'                 }
        EXPECTED: );
        """
        pass

    def test_003_tap_on_previous_season_link_if_it_is_available(self):
        """
        DESCRIPTION: Tap on previous season link (if it is available)
        EXPECTED: - User is navigated to page with the previous league table for that competition
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: dataLayer.push(
        EXPECTED: {     'event' : 'trackEvent',     'eventCategory' : 'football',     'eventAction' : 'league table',     'eventLabel' : 'change season' }
        EXPECTED: );
        """
        pass
