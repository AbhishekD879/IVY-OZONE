from random import randint
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec
import pytest
import tests


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.horseracing
@pytest.mark.desktop
@vtest
class Test_C60094793_Verify_Race_Start_Time(BaseRacing):
    """
    TR_ID: C60094793
    NAME: Verify Race Start Time
    DESCRIPTION: Verify that User is able to view Race start time for all the races at that meeting point.
    PRECONDITIONS: Horse racing event should be available
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create UK & IRE events
        EXPECTED: Events are created
        """
        if tests.settings.backend_env != 'prod':
            minutes = randint(40, 50)
            start_time = self.get_date_time_formatted_string(minutes=-minutes)
            self.ob_config.add_UK_racing_event(start_time=start_time, cashout=True, is_live=True)

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
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg='Current tab %s is not the same as expected %s'
                             % (current_tab, vec.racing.RACING_DEFAULT_TAB_NAME))

        accordions = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions, msg='No accordions found on Horse Racing Landing page')
        uk_ire_type_name = self.uk_and_ire_type_name
        self.assertIn(self.uk_and_ire_type_name, accordions,
                      msg=f'Failed to display {uk_ire_type_name} accordion')

        accordion = accordions[uk_ire_type_name]
        accordion.expand()
        meetings = accordion.items_as_ordered_dict
        self.assertTrue(meetings, msg=f'No meetings found in "{uk_ire_type_name}"')
        for meeting in meetings.values():
            races = meeting.items_as_ordered_dict
            for race_name, race in races.items():
                race.click()
                self.site.wait_content_state('RacingEventDetails')
                events = self.site.racing_event_details.tab_content.event_off_times_list
                event_names = events.items_names
                for event_name in event_names:
                    self.assertRegex(event_name, r'\d{2}:\d{2}',
                                     msg=f'Event name: "{event_name}" doesn\'t match expected pattern (<HH:MM>)')
                break
            break

    def test_004_validate_race_time_of_start(self):
        """
        DESCRIPTION: Validate race time of start
        EXPECTED: User should be able view the race times displayed for all the meeting places
        EXPECTED: Example:
        EXPECTED: New Castle
        EXPECTED: 19:40 19:50
        """
        # covered in step 003
