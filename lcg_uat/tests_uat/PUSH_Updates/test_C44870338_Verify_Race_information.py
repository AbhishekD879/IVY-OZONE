import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.pages.shared.components.home_page_components.home_page_next_races_tab import HomePageNextRacesTabContent
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
# @pytest.mark.prod - OB is involved in event creation and changing the state of the event
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.other
@vtest
class Test_C44870338_Verify_Race_information(BaseRacing, HomePageNextRacesTabContent):
    """
    TR_ID: C44870338
    NAME: Verify  Race information
    DESCRIPTION: Verify that Race information is updated in any page through the site
    PRECONDITIONS: User loads the Oxygen Application and logs in.
    """
    keep_browser_open = True
    device_name = "Desktop Chrome"

    def get_next_races_events(self):
        modules = self.site.home.desktop_modules.items_as_ordered_dict
        self.assertTrue(modules, msg='No modules found on page')
        if self.brand == 'ladbrokes':
            expected_module = vec.racing.NEXT_RACES.upper()
        else:
            expected_module = vec.racing.NEXT_RACES
        module = modules.get(expected_module)
        self.assertTrue(module, msg=f'Module: "{expected_module}" is not found')
        events = module.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(events, msg='No events found')
        return events

    def get_horse_race_meeting(self):
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found on page')
        name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern
        self.__class__.meeting_name = name.upper() if self.brand != 'ladbrokes' else name
        section = sections.get(self.uk_and_ire_type_name)
        self.assertTrue(section, msg=f'Section: "{self.uk_and_ire_type_name}" is not found')
        meeting = section.items_as_ordered_dict.get(self.meeting_name)
        return meeting

    def create_event(self, is_live=False):
        """
        DESCRIPTION: Creating events
        Expected: Events created
        """
        self.cms_config.set_next_races_numbers_of_event(number_of_event=20)
        racing_event = self.ob_config.add_UK_racing_event(number_of_runners=1,
                                                          time_to_start=+15, is_live=is_live)
        self.__class__.eventID = racing_event.event_id
        self.__class__.marketID = racing_event.market_id
        self.__class__.created_event_time = f'{racing_event.event_off_time}'
        self.__class__.created_event_name = f'{racing_event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.racing_selection_ids = list(racing_event.selection_ids.values())[0]

    def test_001_navigate_to_home_page___next_racesverify_that_races_are_updated_by_pushverify__race_card_information_event_name_and_timeverify_the_event_is_dropped_off_by_push_after_the_event_has_startedfinished(self):
        """
        DESCRIPTION: Navigate to Home Page - Next Races
        DESCRIPTION: Verify that Races are updated by push
        DESCRIPTION: Verify  Race Card information: event name and time
        DESCRIPTION: Verify the event is dropped off by Push (after the event has started/finished)
        EXPECTED: In Home page - Next Races, the event info is updated by push
        """
        self.create_event()
        self.site.wait_content_state('Homepage')
        if self.device_type == 'mobile':
            self.navigate_to_page(name='home/next-races')
            self.site.wait_content_state(state_name='Homepage')
            events = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(events, msg='No events found on next races tab')
            if self.brand == 'ladbrokes':
                event_name = self.created_event_name.upper()
            else:
                event_name = self.created_event_name
            event = events.get(event_name)
            self.assertTrue(event, msg=f'event: "{self.created_event_name}" is not found')
            self.assertEqual(event.name, event_name,
                             msg=f'Actual event : "{event.name}" is not equal to Expected event : "{event_name}"')
            self.assertIn(self.created_event_time, event.name,
                          msg=f'Time "{self.created_event_time}" is not as expected')
            self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
            sleep(3)
            self.device.refresh_page()
            sleep(3)
            events = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(events, msg='No events found on next races tab')
            self.assertNotIn(event_name, events,
                             msg=f'Event "{event_name}" is displayed in horse racing - next races')
        else:
            events = self.get_next_races_events()
            if self.brand == 'ladbrokes':
                event_name = self.created_event_name.upper()
            else:
                event_name = self.created_event_name
            event = events.get(event_name)
            self.assertTrue(event, msg=f'event: "{self.created_event_name}" is not found')
            self.assertEqual(event.event_name, event_name,
                             msg=f'Actual event : "{event.event_name}" is not equal to Expected event : "{event_name}"')
            self.assertIn(self.created_event_time, event.event_name,
                          msg=f'Time "{self.created_event_time}" is not as expected')
            self.ob_config.change_event_state(self.eventID, displayed=False, active=False)
            sleep(3)
            self.device.refresh_page()
            sleep(3)
            events = self.get_next_races_events()
            if self.brand == 'ladbrokes':
                event_name = self.created_event_name.upper()
            else:
                event_name = self.created_event_name
            self.assertNotIn(event_name, events,
                             msg=f'Event "{event_name}" is displayed in Next Races')

    def test_002_navigate_to_horse_racing___meetingsverify_that_event_status_is_updated_by_push_result_race_live_race_offverify_that_events_dont_drop_offverify_the_event_is_dropped_off_by_push_after_the_event_has_startedfinished(self):
        """
        DESCRIPTION: Navigate to Horse Racing - Meetings
        DESCRIPTION: Verify that event status is updated by push (Result, Race live, Race off)
        DESCRIPTION: Verify that events don't drop off
        DESCRIPTION: Verify the event is dropped off by Push (after the event has started/finished)
        EXPECTED: In HR page - Meetings the event info is updated by push
        """
        self.create_event(is_live=True)
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        meeting = self.get_horse_race_meeting()
        self.assertTrue(meeting, msg=f'Meeting: "{self.meeting_name}" is not found')
        events = meeting.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found on {self.meeting_name}')
        event = events.get(self.created_event_time)
        self.assertTrue(event, msg=f'event: "{self.created_event_time}" is not found')
        self.assertTrue(event.has_is_live(), msg=f'event: "{self.created_event_time}" is not live')
        self.ob_config.result_selection(selection_id=self.racing_selection_ids, market_id=self.marketID, event_id=self.eventID)
        self.ob_config.confirm_result(selection_id=self.racing_selection_ids, market_id=self.marketID, event_id=self.eventID)
        sleep(7)
        self.device.refresh_page()
        meeting = self.get_horse_race_meeting()
        self.assertTrue(meeting, msg=f'Meeting: "{self.meeting_name}" is not found')
        events = meeting.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found on "{self.meeting_name}"')
        event = events.get(self.created_event_time)
        self.assertTrue(event, msg=f'event: "{self.created_event_time}" is not found')
        self.assertTrue(event.has_icon(timeout=10), msg=f'event: "{self.created_event_time}" is not resulted')
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
        sleep(3)
        self.device.refresh_page()
        sleep(3)
        meeting = self.get_horse_race_meeting()
        self.assertTrue(meeting, msg=f'Meeting: "{self.meeting_name}" is not found')
        events = meeting.items_as_ordered_dict
        self.assertNotIn(self.created_event_time, events,
                         msg=f'Event "{self.created_event_time}" is displayed in meetings')

    def test_003_navigate_to_horse_racing___next_racesverify_that_races_are_listed_in_chronological_order_and_info_is_updated_by_pushverify__race_card_information_event_name_and_time(self):
        """
        DESCRIPTION: Navigate to Horse Racing - Next Races
        DESCRIPTION: Verify that Races are listed in chronological order and info is updated by push
        DESCRIPTION: Verify  Race Card information: event name and time
        EXPECTED: In HR page - Next Races, the event info is updated by push
        """
        if self.brand == 'ladbrokes':
            self.create_event()
            next_races = vec.racing.RACING_NEXT_RACES_NAME
            self.site.horse_racing.tabs_menu.click_button(next_races)
            self.assertTrue(self.site.horse_racing.tabs_menu.items_as_ordered_dict.get(next_races).is_selected(),
                            msg=f'{vec.racing.RACING_NEXT_RACES_NAME} is not selected')
            events = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(events, msg='No events found on next races tab')
            event_name = self.created_event_name.upper()
            event = events.get(event_name)
            self.assertTrue(event, msg=f'event: "{self.created_event_name}" is not found')
            self.assertEqual(event.name, event_name,
                             msg=f'Actual event : "{event.name}" is not equal to Expected event :  {event_name}')
            self.assertIn(self.created_event_time, event.name,
                          msg=f'Time "{self.created_event_time}" is not as expected')
            self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
            sleep(3)
            self.device.refresh_page()
            sleep(3)
            events = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(events, msg='No events found on next races tab')
            self.assertNotIn(event_name, events,
                             msg=f'Event "{event_name}" is displayed in horse racing - next races')

    def test_004_navigate_to_horse_racing___edp_and_verify_that_race_info_is_updated_by_pushverify_that_the_event_name_and_time_are_displayedverify_that_data_update__or_the_event_is_suspended_by_push(self):
        """
        DESCRIPTION: Navigate to Horse Racing - EDP and verify that Race info is updated by push:
        DESCRIPTION: Verify that the event name and time are displayed
        DESCRIPTION: Verify that data update  or the event is suspended by push
        EXPECTED: In HR page - EDP the event info is updated by push
        """
        self.create_event()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        event_title = self.site.racing_event_details.tab_content.race_details.event_title
        self.assertEqual(event_title, self.created_event_name, msg=f'Actual event name : {event_title}'
                                                                   f'is not eqaual to :{self.created_event_name}')
        self.assertIn(self.created_event_time, event_title,
                      msg=f'Time "{self.created_event_time}" is not as expected')
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)
        sleep(2)
        self.device.refresh_page()
        sleep(3)
        self.site.wait_splash_to_hide()
