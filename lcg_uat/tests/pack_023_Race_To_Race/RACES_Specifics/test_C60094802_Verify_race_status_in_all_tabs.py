import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Involves creation of horse event not valid for prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.races
@vtest
class Test_C60094802_Verify_race_status_in_all_tabs(BaseRacing):
    """
    TR_ID: C60094802
    NAME: Verify race status in all tabs
    DESCRIPTION: Verify race status is displayed in the below tabs,
    DESCRIPTION: 1: Horse Racing Homepage (Featured Tab)
    DESCRIPTION: 2: Horse Racing EDP
    PRECONDITIONS: Multiple Horse racing events should be available with different race status as below
    PRECONDITIONS: 1: One race should Kick start
    PRECONDITIONS: 2: One race should be completed
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create racing events
        EXPECTED: Racing events is created
        """
        event_params = self.ob_config.add_international_racing_event(number_of_runners=1)
        eventID = event_params.event_id
        marketID = event_params.market_id
        selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.event_off_time = event_params.event_off_time
        # created event is resulted
        self.ob_config.update_selection_result(event_id=eventID, market_id=marketID,
                                               selection_id=selection_id)
        live_event_params = self.ob_config.add_international_racing_event(is_live=True, number_of_runners=1)
        self.__class__.live_event_off_time = live_event_params.event_off_time

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        # Covered in step 2

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.site.home.menu_carousel.items_as_ordered_dict.get(
                vec.sb.HORSERACING.upper() if self.brand == 'bma' else vec.sb.HORSERACING.title()).click()
        self.site.wait_content_state_changed(timeout=10)
        self.site.wait_content_state('Horseracing')

    def test_003_validate_status(self):
        """
        DESCRIPTION: Validate Status
        EXPECTED: 1: User should be displayed "RACE OFF" status - when race kick started
        EXPECTED: 2: User should be displayed "RESULT" status - When race has been completed.
        """
        self.site.wait_splash_to_hide()
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        if self.brand == 'ladbrokes':
            sleep(5)
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found')
        name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_international.name_pattern
        self.__class__.meeting_name = name.upper() if self.brand != 'ladbrokes' else name
        section = sections.get(self.international_type_name)
        self.assertTrue(section, msg=f'Section: "{self.international_type_name}" is not found')
        meeting = section.items_as_ordered_dict.get(self.meeting_name)
        self.assertTrue(meeting, msg=f'Meeting: "{self.meeting_name}" is not found')
        events = meeting.items_as_ordered_dict
        self.assertTrue(events, msg='Events not found')
        sleep(3)
        self.__class__.race_off_event = events.get(self.live_event_off_time)
        self.assertTrue(self.race_off_event.has_race_off(),
                        msg=f'Event : "{self.live_event_off_time}" is not race off')
        result_event = events.get(self.event_off_time)
        self.assertTrue(result_event.is_resulted,
                        msg=f'Event : "{self.event_off_time}" is not result')

    def test_004_click_on_the_race_and_navigate_to_the_races_for_that_meeting_point(self):
        """
        DESCRIPTION: Click on the race and navigate to the races for that meeting point
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        EXPECTED: 3: User should be displayed "RACE OFF" status - when race kick started
        EXPECTED: 4: User should be displayed "RESULT" status - When race has been completed.
        """
        self.race_off_event.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
        event_off_times_list = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        self.assertTrue(event_off_times_list, msg='Horse racing top bar not found')
        race_off_event = event_off_times_list.get(self.live_event_off_time)
        self.assertTrue(race_off_event.is_race_off(),
                        msg=f'Event : "{self.live_event_off_time}" is not race off')
        result_event = event_off_times_list.get(self.event_off_time)
        self.assertTrue(result_event.is_resulted,
                        msg=f'Event : "{self.event_off_time}" is not result')
