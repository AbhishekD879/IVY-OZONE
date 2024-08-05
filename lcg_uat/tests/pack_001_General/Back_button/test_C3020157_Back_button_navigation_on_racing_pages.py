import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't create OB event on prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.horseracing
@pytest.mark.mobile_only
@pytest.mark.navigation
@vtest
class Test_C3020157_Back_button_navigation_on_racing_pages(BaseRacing):
    """
    TR_ID: C3020157
    NAME: Back button navigation on racing pages
    DESCRIPTION: This test case verifies back button functionality on racing pages, on race events details pages and after switching between tabs
    PRECONDITIONS: You should be on a Home page
    """
    keep_browser_open = True

    def clicking_event(self):
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

    def test_001___tap_on_any_race_icon_in_sports_ribbon_eg_horse_racing_greyhounds__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any Race icon in sports ribbon (e.g. Horse Racing, Greyhounds)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to Home page
        """
        self.ob_config.add_UK_racing_event(number_of_runners=2, forecast_available=True)
        self.ob_config.add_UK_racing_event(number_of_runners=2, forecast_available=True)
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state('horse-racing')
        self.site.back_button_click()
        self.site.wait_content_state('HomePage')

    def test_002___tap_on_any_race_icon_in_sports_ribbon_and_switch_between_tabs_on_races_landing_page_eg_antepost_specials_yourcall__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any Race icon in sports ribbon and switch between tabs on races landing page (e.g Antepost, Specials, Yourcall)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous tab
        """
        self.site.open_sport(name=self.get_sport_title(self.ob_config.horseracing_config.category_id))
        tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='No tab was found on page')
        expected_tabs = vec.racing.RACING_TAB_NAMES
        self.assertTrue(len(tabs) <= len(expected_tabs),
                        msg='Tabs number is not correct. Actual number of tabs ({0}) isn\'t equal to expected ({1})'
                        .format(len(tabs), len(expected_tabs)))
        default_tab = self.site.horse_racing.tabs_menu.current
        self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_FUTURE_TAB_NAME)
        wait_for_result(lambda: self.site.horse_racing.tabs_menu.current, timeout=10, name='Current tab is not displayed')
        self.site.back_button_click()
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(default_tab, current_tab, msg=f' User is not navigated to the previous tab')

    def test_003___tap_on_any_race_in_sports_ribbon_and_open_any_race_event__tap_back_button(self):
        """
        DESCRIPTION: - Tap on any race in sports ribbon and open any race event
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous page
        """
        self.clicking_event()
        self.site.back_button_click()
        self.site.wait_content_state('horse-racing')

    def test_004___open_any_race_event_and_switch_between_tabs_eg_win_or_ew_win_only_to_finish__tap_back_button(self):
        """
        DESCRIPTION: - Open any race event and switch between tabs (e.g. Win or E/W, Win Only, To Finish)
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous page
        """
        self.clicking_event()
        racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        open_tab = racing_event_tab_content.market_tabs_list.open_tab(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.assertTrue(open_tab, msg=f'"{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB}" is not opened')
        self.site.back_button_click()
        self.site.wait_content_state('horse-racing')

    def test_005___open_any_race_event_and_switch_to_any_another_race_event_in_race_events_ribbon__tap_back_button(self):
        """
        DESCRIPTION: - Open any race event and switch to any another race event in race events ribbon
        DESCRIPTION: - Tap "Back" button
        EXPECTED: User is navigated to the previous event
        """
        self.clicking_event()
        events_list = self.site.racing_event_details.tab_content.event_off_times_list.items_as_ordered_dict
        default_event = self.site.racing_event_details.tab_content.event_off_times_list.selected_item
        for event_name in events_list.keys():
            if event_name == default_event:
                continue
            events_list[event_name].click()
            break
        self.site.back_button_click()
        current_event = self.site.racing_event_details.tab_content.event_off_times_list.selected_item
        self.assertEqual(default_event, current_event, msg="User is not navigated to the previous event")
