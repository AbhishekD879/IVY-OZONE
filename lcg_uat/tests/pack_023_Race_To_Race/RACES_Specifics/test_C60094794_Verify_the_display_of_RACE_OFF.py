from random import randint
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import pytest
import tests


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # creation of events involved.
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.desktop
@vtest
class Test_C60094794_Verify_the_display_of_RACE_OFF(BaseRacing):
    """
    TR_ID: C60094794
    NAME: Verify the display of "RACE OFF"
    DESCRIPTION: Verify that when the Race kick starts "RACE OFF" status of the race is displayed just below the Time of start
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Race should kick start
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create UK & IRE events
        EXPECTED: Events are created
        """
        if tests.settings.backend_env != 'prod':
            minutes = randint(40, 50)
            start_time = self.get_date_time_formatted_string(minutes=-minutes)
            event_params = self.ob_config.add_UK_racing_event(start_time=start_time, cashout=True, is_live=True)
            self.__class__.event_id = event_params.event_id

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        # covered in step 001

    def test_003_click_on_any_race_from_the_meeting_point(self):
        """
        DESCRIPTION: Click on any race from the meeting point
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')
        events = self.site.racing_event_details.tab_content.has_event_off_times_list()
        self.assertTrue(events, msg='other races not found')

    def test_004_validate_race_off_status(self):
        """
        DESCRIPTION: Validate "RACE OFF" status
        EXPECTED: 1: User should be displayed with "RACE OFF" status
        EXPECTED: 2: "RACE OFF" status should be displayed just below the Race Start Time
        """
        self.__class__.races = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        self.assertTrue(self.races, msg='other races not found')
        race = self.races.get(self.site.racing_event_details.tab_content.event_off_times_list.selected_item)
        self.assertTrue(race.is_race_off(), msg='Event do not have race off label')

        race_start_time = race.race_name()
        race_off_label = race.race_off_element()

        result = race_start_time.location.get('y') < race_off_label.location.get('y')
        self.assertTrue(result, msg='race off label is not present below the race start time')
