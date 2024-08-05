import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.build_your_bet
@vtest
class Test_C58836512_Banach_Events_availability_according_to_integer_decimal_hours_in_timezones_for_BYB_microservice(Common):
    """
    TR_ID: C58836512
    NAME: [Banach] Events availability according to  integer, decimal hours in timezones for BYB microservice
    DESCRIPTION: This test case verifies events availability according to different time zones (integer, decimal hours) for BYB microservice
    PRECONDITIONS: Requests to BYB MS by leagues (devO):
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=Y&tz=X (or X.X)
    PRECONDITIONS: where
    PRECONDITIONS: days=Y - number of upcoming days,
    PRECONDITIONS: tz=X - integer hour of the timezone
    PRECONDITIONS: tz=X.X - decimal hour of the timezone
    PRECONDITIONS: Example: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=12&tz=5.5
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=Y&tz=X (or X.X)
    PRECONDITIONS: where
    PRECONDITIONS: tz=X - integer hour of the timezone
    PRECONDITIONS: tz=X.X - decimal hour of the timezone
    PRECONDITIONS: Example: https://buildyourbet-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=12&tz=5.5
    PRECONDITIONS: **PROD** BYB requests by leagues examples:
    PRECONDITIONS: **LADBROKES** - https://buildyourbet.ladbrokes.com/api/v1/leagues-upcoming?days=6&tz=3
    PRECONDITIONS: **CORAL** - https://buildyourbet.coral.co.uk/api/v1/leagues-upcoming?days=6&tz=3
    PRECONDITIONS: - Open the site -> User is on the Home Page -> 'Build Your Bet' **CORAL** / 'Bet Builder' **LADBROKES** section is available
    PRECONDITIONS: - Open devtools (Network tab)
    """
    keep_browser_open = True

    def test_001_filter_requests_in_network_tab_according_to_byb_ms(self):
        """
        DESCRIPTION: Filter requests in Network tab according to BYB MS
        EXPECTED: - Request by leagues is displayed in Network tab and is successful (https://buildyourbet.ladbrokes.com/api/v1/leagues-upcoming?days=Y&tz=X)
        EXPECTED: - Banach events are displayed in 'Today' and 'Upcoming' tabs in 'Build Your Bet' **CORAL** / 'Bet Builder' **LADBROKES** section on the Home page
        """
        pass

    def test_002_change_timezone_to_decimal_hour___hyderabad___india_tz55_on_the_computer_in_open_datetime_preferences_window(self):
        """
        DESCRIPTION: Change timezone to decimal hour - 'Hyderabad - India' (tz=5.5) on the computer in 'Open Date&Time Preferences' window
        EXPECTED: - Request by leagues is displayed in Network tab and is successful (https://buildyourbet.ladbrokes.com/api/v1/leagues-upcoming?days=Y&tz=5.5)
        EXPECTED: - Banach events are displayed in 'Today' and 'Upcoming' tabs in 'Build Your Bet' **CORAL** / 'Bet Builder' **LADBROKES** section on the Home page
        """
        pass

    def test_003_trigger_byb_call_by_leagues_directly_in_the_browser_tab_with_tz3_integer_hourprod_ladbrokes___httpsbuildyourbetladbrokescomapiv1leagues_upcomingdays6tz3prod_coral___httpsbuildyourbetcoralcoukapiv1leagues_upcomingdays6tz3(self):
        """
        DESCRIPTION: Trigger BYB call by leagues directly in the browser tab with **tz=3** (integer hour):
        DESCRIPTION: **PROD LADBROKES** - https://buildyourbet.ladbrokes.com/api/v1/leagues-upcoming?days=6&tz=3
        DESCRIPTION: **PROD CORAL** - https://buildyourbet.coral.co.uk/api/v1/leagues-upcoming?days=6&tz=3
        EXPECTED: Response with available Banach events is displayed
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/109061196)
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/109061197)
        """
        pass

    def test_004_trigger_byb_call_by_leagues_directly_in_the_browser_tab_with_tz55_decimal_hourprod_ladbrokes___httpsbuildyourbetladbrokescomapiv1leagues_upcomingdays6tz55prod_coral___httpsbuildyourbetcoralcoukapiv1leagues_upcomingdays6tz55(self):
        """
        DESCRIPTION: Trigger BYB call by leagues directly in the browser tab with **tz=5.5** (decimal hour):
        DESCRIPTION: **PROD LADBROKES** - https://buildyourbet.ladbrokes.com/api/v1/leagues-upcoming?days=6&tz=5.5
        DESCRIPTION: **PROD CORAL** - https://buildyourbet.coral.co.uk/api/v1/leagues-upcoming?days=6&tz=5.5
        EXPECTED: Response with available Banach events is displayed
        """
        pass
