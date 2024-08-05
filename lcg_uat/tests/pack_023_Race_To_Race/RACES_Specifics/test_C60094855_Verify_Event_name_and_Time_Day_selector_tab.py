import pytest
import calendar
import voltron.environments.constants as vec
from datetime import datetime
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can't create events in prob ob
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.races
@pytest.mark.horseracing
@vtest
class Test_C60094855_Verify_Event_name_and_Time_Day_selector_tab(BaseRacing):
    """
    TR_ID: C60094855
    NAME: Verify Event name and Time- Day selector tab
    DESCRIPTION: Verify horse racing event name and time in each selector tab are matching with EDP page
    PRECONDITIONS: 1: Login to TI and schedule races for Today, Tomorrow, Day 3 and Day 4
    """
    keep_browser_open = True
    current_datetime = datetime.now()
    dayNumber = calendar.weekday(current_datetime.year, current_datetime.month, current_datetime.day)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]

    if dayNumber == 4:
        day3 = days[6]
        day4 = days[0]
    elif dayNumber == 5:
        day3 = days[0]
        day4 = days[1]
    elif dayNumber == 6:
        day3 = days[1]
        day4 = days[2]
    else:
        day3 = (days[dayNumber + 2])
        day4 = (days[dayNumber + 3])
    days_list = [vec.sb.TABS_NAME_TOMORROW.upper(),
                 vec.sb.TABS_NAME_TODAY.upper(),
                 day3.upper(),
                 day4.upper()]

    def verify_EDP_for_selected_tabs(self, tab):
        self.site.wait_splash_to_hide()
        grouping_buttons = self.site.contents.tab_content.grouping_buttons
        req_tab = tab.upper() if self.brand == 'bma' else tab.title()
        grouping_buttons.items_as_ordered_dict.get(req_tab).click()
        self.site.wait_content_state_changed()
        current_tab = grouping_buttons.current
        self.assertEqual(current_tab.upper(), tab.upper(),
                         msg=f'Actual tab: "{current_tab.upper()}" is not same as'
                         f'Expected tab: "{tab.upper()}".')
        self.site.wait_splash_to_hide()
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display any section')
        found_event = False
        for section_name, section in sections.items():
            if section_name in self.section_skip_list or self.next_races_title in section_name:
                continue
            else:
                meetings = section.items_as_ordered_dict
                self.assertTrue(meetings, msg='Failed to display any meeting')
                for meeting_name, meeting in meetings.items():
                    events = meeting.items_as_ordered_dict
                    self.assertTrue(events, msg='Failed to display any event')
                    for event_name, event in events.items():
                        race_started = event.is_resulted or event.has_race_off()
                        if not race_started:
                            event.click()
                            self.site.wait_content_state('RacingEventDetails')
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
        self.site.wait_content_state_changed()
        self.site.wait_splash_to_hide()
        events_ribbon = self.site.racing_event_details.tab_content.event_off_times_list
        self.assertTrue(events_ribbon, msg="Events ribbon is not displayed")
        if self.device_type == 'desktop':
            event_time = self.site.racing_event_details.sub_header.event_time
            self.assertTrue(event_time, msg="Event time is not displayed")

    def test_000_preconditions(self):
        # for today tab
        self.__class__.event1 = self.ob_config.add_UK_racing_event(is_live=True, number_of_runners=1, perform_stream=True, at_races_stream=True)
        self.ob_config.add_enhanced_multiples_racing_event(number_of_runners=1)

        # for tomorrow tab
        tomorrow = self.get_date_time_formatted_string(days=1)
        self.__class__.event2 = self.ob_config.add_UK_racing_event(number_of_runners=1, start_time=tomorrow)

        # for Day3 tab
        day3 = self.get_date_time_formatted_string(days=2)
        self.__class__.event3 = self.ob_config.add_UK_racing_event(number_of_runners=1, start_time=day3)

        # for Day4tab
        day4 = self.get_date_time_formatted_string(days=3)
        self.__class__.event4 = self.ob_config.add_UK_racing_event(number_of_runners=1, start_time=day4)
        self.__class__.meeting_name = self.horseracing_autotest_uk_name_pattern if self.brand == 'ladbrokes' else self.horseracing_autotest_uk_name_pattern.upper()
        category_id = self.ob_config.horseracing_config.category_id
        self.__class__.cms_horse_tab_name = self.get_sport_title(category_id=category_id)

    def test_001_click_on_horse_racing_button_from_main_menu(self):
        """
        DESCRIPTION: Click on 'Horse Racing' button from main menu
        EXPECTED: Horse Racing Page is loaded
        EXPECTED: Meetings tab is selected by default
        EXPECTED: "UK & IRE" section is displayed followed by "International" ( divided by coutries)
        EXPECTED: "Enhanced Multiples" module (if available) is displayed below "International"
        EXPECTED: The Horse Racing meetings with video stream available should be marked with "Play" icon(Coral) and 'Watch' label(Ladbrokes)
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg='Current tab %s is not the same as expected %s'
                             % (current_tab, vec.racing.RACING_DEFAULT_TAB_NAME))

        accordions = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions, msg='Accordion list is empty on Horse Racing page')
        if vec.racing.UK_AND_IRE_TYPE_NAME in accordions.keys():
            uk_and_ire_module = accordions.get(vec.racing.UK_AND_IRE_TYPE_NAME)
            self.assertTrue(uk_and_ire_module,
                            msg=f'"{vec.racing.UK_AND_IRE_TYPE_NAME}" is not found in {accordions.keys()}')
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern
        meeting_name = name.upper() if self.brand != 'ladbrokes' else name
        section = sections.get(self.uk_and_ire_type_name)
        meeting = section.items_as_ordered_dict.get(meeting_name)
        self.assertTrue(meeting.has_live_stream,
                        msg=f'Meeting: "{meeting_name}" has no stream icon')
        if self.device_type == " mobile":
            self.assertIn(vec.racing.ENHANCED_MULTIPLES_NAME, sections, msg=f'No "{self.enhanced_races_name}" in {list(sections.keys())}')

    def test_002_click_on_any_horse_race_event_under_today_selector_tab(self):
        """
        DESCRIPTION: Click on any horse race event under 'Today selector tab
        EXPECTED: + Appropriate Horse Racing event race card is loaded
        EXPECTED: + Meeting name in top of the page should be same as horse race landing page
        EXPECTED: + The Date in top of the page should be **today's date** (eg: Tuesday 5th May)
        EXPECTED: + The event selector (time ribbon) is displayed right under the meeting selector
        """
        self.verify_EDP_for_selected_tabs(tab=self.days_list[1])

    def test_003_navigate_back_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate back to Horse racing Landing Page
        """
        self.site.back_button_click()

    def test_004_click_on_any_horse_race_event_under_tomorrow_selector_tab(self):
        """
        DESCRIPTION: Click on any horse race event under 'Tomorrow selector tab
        EXPECTED: + Appropriate Horse Racing event race card is loaded
        EXPECTED: + Meeting name in top of the page should be same as horse race landing page
        EXPECTED: + The Date in top of the page should be **tomorrow's date**
        EXPECTED: (eg: **Wednesday 6th May** if today is Tuesday 5th may)
        EXPECTED: + The event selector (time ribbon) is displayed right under the meeting selector
        """
        self.verify_EDP_for_selected_tabs(tab=self.days_list[0])

    def test_005_navigate_back_to_horse_racing_landing_page(self):
        """
        DESCRIPTION: Navigate back to Horse racing Landing Page
        """
        self.site.back_button_click()

    def test_006_click_on_any_horse_race_event_under_next_following_day_or_day3_selector_tab(self):
        """
        DESCRIPTION: Click on any horse race event under 'Next following day' or 'Day3' selector tab
        EXPECTED: + Appropriate Horse Racing event race card is loaded
        EXPECTED: + Meeting name in top of the page should be same as horse race landing page
        EXPECTED: + The Date in top of the page should be **Day after tomorrow's date**
        EXPECTED: (eg: **Thursday 7th May** if today is Tuesday 5th may)
        EXPECTED: + The event selector (time ribbon) is displayed right under the meeting selector
        """
        self.verify_EDP_for_selected_tabs(tab=self.day4)
