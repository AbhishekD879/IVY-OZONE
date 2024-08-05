from random import randint
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import pytest
import tests


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # creation of events involved
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.desktop
@vtest
class Test_C60094798_Verify_the_status_change_from_RACE_OFF_to_RESULT(BaseRacing):
    """
    TR_ID: C60094798
    NAME: Verify the status change from "RACE OFF" to "RESULT"
    DESCRIPTION: Verify that when race is completed the "RACE OFF" status changes to "RESULT"
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Race should be completed
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
            self.__class__.event_id, self.__class__.market_id, self.__class__.selection_ids = \
                event_params.event_id, event_params.market_id, event_params.selection_ids

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

    def test_003_click_on_any_race_from_the_meeting_pointpick_a_race_off_race_event_and_wait_for_the_status_change(self):
        """
        DESCRIPTION: Click on any race from the meeting point
        DESCRIPTION: (Pick a RACE OFF race event and wait for the status change)
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        """
        self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')
        events = self.site.racing_event_details.tab_content.has_event_off_times_list()
        self.assertTrue(events, msg='other races not found')

    def test_004_validate_result_status(self):
        """
        DESCRIPTION: Validate "RESULT" status
        EXPECTED: 1: User should be displayed "RESULT" status.
        EXPECTED: 2: "RACE OFF" status should be Changed to "RESULT" status once the race has been completed
        """
        races = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        self.assertTrue(races, msg='other races not found')
        race = races.get(self.site.racing_event_details.tab_content.event_off_times_list.selected_item)
        self.assertTrue(race.is_race_off(), msg='Event do not have race off label')

        self.result_event(selection_ids=list(self.selection_ids.values()), market_id=self.market_id,
                          event_id=self.event_id)
        self.device.refresh_page()
        races_after = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        race_after = races_after.get(self.site.racing_event_details.tab_content.event_off_times_list.selected_item)
        self.assertTrue(race_after.is_resulted, msg='Event do not have resulted label')
        self.assertFalse(race.is_race_off(), msg='Event do not have race off label')
