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
class Test_C10841455_Verify_countdown_timer_on_event_in_Next_Races_module(Common):
    """
    TR_ID: C10841455
    NAME: Verify countdown timer on event in Next Races module
    DESCRIPTION: This case verifies countdown timer on event in Next Races module
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Horse Racing Landing Page
        EXPECTED: Landing page is opened
        """
        pass

    def test_002_select_the_event_with_start_time_less_than_45_minutes_in_next_races_module(self):
        """
        DESCRIPTION: Select the event with start time less than 45 minutes in Next Races module
        EXPECTED: Countdown timer is displayed in the bottom left part of the event panel in the 'Starts: MM:SS' format
        """
        pass

    def test_003_select_the_event_with_start_time_more_than_45_minutes_in_next_races_module(self):
        """
        DESCRIPTION: Select the event with start time more than 45 minutes in Next Races module
        EXPECTED: Countdown timer is not displayed in the bottom left part of the event panel
        """
        pass
