import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094797_Verify_the_CSS_for_RACE_OFF_status(BaseRacing):
    """
    TR_ID: C60094797
    NAME: Verify the CSS for "RACE OFF" status
    DESCRIPTION: Verify the CSS for "RACE OFF" status
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Race should kick start
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state("Homepage")

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.sb.HORSERACING.upper() if self.brand == 'bma' else vec.sb.HORSERACING.title()).click()
        if tests.settings.backend_env != 'prod':
            self.__class__.event = self.ob_config.add_international_racing_event(is_live=True, number_of_runners=1)
            self.__class__.live_event_off_time = self.event.event_off_time
        self.site.wait_content_state('Horseracing')

    def test_003_click_on_any_race_off_race_from_the_meeting_point(self):
        """
        DESCRIPTION: Click on any "RACE OFF" race from the meeting point
        EXPECTED: 1: User should be navigated to Event display page
        EXPECTED: 2: All other races in that meeting point should be displayed for the user to scroll and click
        """
        sleep(8)  # the created event is taking time to reflect in the FE
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display any section')
        if tests.settings.backend_env == 'prod':
            found_event = False
            for section_name, section in sections.items():
                if section_name in vec.racing.COUNTRY_SKIP_LIST or self.next_races_title in section_name:
                    continue
                else:
                    meetings = section.items_as_ordered_dict
                    self.assertTrue(meetings, msg='Failed to display any meeting')
                    for meeting_name, meeting in meetings.items():
                        events = meeting.items_as_ordered_dict
                        self.assertTrue(events, msg='Failed to display any event')
                        for event_name, event in events.items():
                            if event.has_race_off():
                                self.__class__.live_event_off_time = event_name
                                event.click()
                                self.site.wait_splash_to_hide()
                                self.site.wait_content_state(state_name='RacingEventDetails')
                                found_event = True
                                break
                        if found_event is True:
                            break
                        else:
                            continue
                    if found_event is True:
                        break
                    else:
                        continue
            if not found_event:
                self._logger.info('*********No "RACE OFF" event found ***********')
                exit()
        else:
            name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_international.name_pattern
            meeting_name = name.upper() if self.brand != 'ladbrokes' else name
            section = sections.get(self.international_type_name)
            self.assertTrue(section, msg=f'Section: "{self.international_type_name}" is not found')
            meeting = section.items_as_ordered_dict.get(meeting_name)
            self.assertTrue(meeting, msg=f'Meeting: "{meeting_name}" is not found')
            events = meeting.items_as_ordered_dict
            self.assertTrue(events, msg='Events not found')
            off_time_event = events.get(self.live_event_off_time)
            self.assertTrue(off_time_event.has_race_off(),
                            msg=f'Event : "{self.live_event_off_time}" is not race off')
            off_time_event.click()

        self.site.wait_content_state_changed()
        self.__class__.events_ribbon = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        for event_name in self.events_ribbon.keys():
            if len(self.events_ribbon.keys()) == 1:
                break
            elif event_name == self.live_event_off_time:
                continue
            else:
                self.events_ribbon[event_name].click()
                self.site.wait_content_state(state_name='RacingEventDetails')
            self.events_ribbon = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict

        self.events_ribbon[self.live_event_off_time].click()

    def test_004_validate_css_for_race_off_status(self):
        """
        DESCRIPTION: Validate CSS for "RACE OFF" status
        EXPECTED: Ladbrokes:
        EXPECTED: User should be displayed "RACE OFF" status as per design mentioned
        EXPECTED: CSS
        EXPECTED: .RACE-OFF {
        EXPECTED: width: 42px;
        EXPECTED: height: 13px;
        EXPECTED: font-family: Roboto;
        EXPECTED: font-size: 10px;
        EXPECTED: font-weight: bold;
        EXPECTED: font-stretch: condensed;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: normal;
        EXPECTED: letter-spacing: 0.3px;
        EXPECTED: color: #ff0000;
        EXPECTED: }
        EXPECTED: Coral:
        EXPECTED: .RACE-OFF {
        EXPECTED: width: 43px;
        EXPECTED: height: 11px;
        EXPECTED: font-family: Lato;
        EXPECTED: font-size: 9px;
        EXPECTED: font-weight: 700;
        EXPECTED: font-stretch: 100%;
        EXPECTED: font-style: normal;
        EXPECTED: line-height: 14px;
        EXPECTED: letter-spacing: normal;
        EXPECTED: color: #f56b23;
        EXPECTED: }
        """
        race_off = wait_for_result(lambda: self.events_ribbon[self.live_event_off_time].race_off, timeout=20)
        actual_font_size = race_off.css_property_value('font-size')
        self.assertEqual(actual_font_size, '9px' if self.brand == 'bma' else '10px',
                         msg=f'Race off font size is not equal to "9px", actual result: "{actual_font_size}"')
        actual_font_family = race_off.css_property_value('font-family')
        self.assertIn('Lato' if self.brand == 'bma' else 'Roboto', actual_font_family,
                      msg=f'Race off font family is not equal to "Lato", actual result "{actual_font_family}"')
        actual_font_weight = race_off.css_property_value('font-weight')
        self.assertEqual(actual_font_weight, '700', msg='Race off font weight is not equal to "700", '
                                                        f'actual result "{actual_font_weight}"')
        actual_color = race_off.css_property_value('color')
        self.assertEqual(actual_color, vec.colors.RACE_OFF_COLOR,
                         msg=f'actual color of Race off: "{actual_color}" is not equal to the expected Race off '
                             f'color:"{vec.colors.RACE_OFF_COLOR if self.brand == "bma" else vec.colors.RACE_OFF_COLOR}"')
