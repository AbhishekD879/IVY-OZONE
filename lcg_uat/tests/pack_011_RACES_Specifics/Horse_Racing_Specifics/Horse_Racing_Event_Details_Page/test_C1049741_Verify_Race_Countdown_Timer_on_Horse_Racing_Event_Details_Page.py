from datetime import datetime

import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C1049741_Verify_Race_Countdown_Timer_on_Horse_Racing_Event_Details_Page(BaseRacing):
    """
    TR_ID: C1049741
    NAME: Verify Count Down timer and Event Status
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing events in OB
        """
        event_params_20min = self.ob_config.add_UK_racing_event(time_to_start=20)
        self.__class__.eventID_20min = event_params_20min.event_id

        event_params_50min = self.ob_config.add_UK_racing_event(time_to_start=50)
        self.__class__.eventID_50min = event_params_50min.event_id

    def test_001_select_an_event_where_the_Race_start_time_is_more_than_45_minutes(self):
        """
        DESCRIPTION: Select an event where Race start time is more than 45 minutes > Go to the Horse Racing Event details page
        EXPECTED: Event Details Page is opened
        EXPECTED: A countdown timer is not displayed
        """
        self.navigate_to_edp(event_id=self.eventID_50min, sport_name='horse-racing')
        self.assertFalse(self.site.racing_event_details.tab_content.race_details.has_countdown_timer(expected=False),
                         msg='Countdown timer was found for event with time to start ~50 min')

    def test_002_go_back_to_horse_racing_landing_page__select_an_event_where_race_start_time_is_less_then_or_equal_to_45_minutes_minutes__go_to_the_horse_racing_event_details_page(self):
        """
        DESCRIPTION: Select an event where the Race start time is less than or equal to 45 minutes
        EXPECTED: Event Details Page is opened
        EXPECTED: Countdown timer displays corresponding time left
        """
        self.navigate_to_edp(event_id=self.eventID_20min, sport_name='horse-racing')
        self.assertTrue(self.site.racing_event_details.tab_content.race_details.has_countdown_timer(),
                        msg='Countdown timer was not found for event with time to start ~20 min')

        time = datetime.strptime(self.site.racing_event_details.tab_content.race_details.countdown_timer.value, '%M:%S')

        self.assertTrue(17 < time.minute < 20,
                        msg=f'Countdown time does not display corresponding time left. Minutes left {time.minute}')

    def test_003_select_an_event_where_the_Race_start_time_is_more_than_45_minutes_wait_till_45_minutes_is_left_to_start(self):
        """
        DESCRIPTION: Select an event where the Race start time is more than 45 minutes (e.g. 50 min), wait till 45 minutes is left to start
        EXPECTED: Event Details Page is opened
        EXPECTED: A timer module counting down from 45 minutes is displayed
        """
        event_params_46min = self.ob_config.add_UK_racing_event(time_to_start=46)
        event_id_46min = event_params_46min.event_id

        self.navigate_to_edp(event_id=event_id_46min, sport_name='horse-racing')

        self.assertFalse(self.site.racing_event_details.tab_content.race_details.has_countdown_timer(expected=False),
                         msg='Countdown timer was found for event with time to start in 46 min')

        self.assertTrue(self.site.racing_event_details.tab_content.race_details.has_countdown_timer(timeout=70),
                        msg='Countdown timer has not been shown')

    def test_004_refresh_event_details_page(self):
        """
        DESCRIPTION: Refresh event details page
        EXPECTED: Countdown timer displays corresponding time left
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        time = datetime.strptime(self.site.racing_event_details.tab_content.race_details.countdown_timer.value, '%M:%S')

        self.assertTrue(43 < time.minute < 46,
                        msg=f'Countdown time does not display corresponding time left. Minutes left {time.minute}')
