import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.p2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C44870195_GHNavigation_journeys(BaseRacing):
    """
    TR_ID: C44870195
    NAME: GHNavigation journeys
    DESCRIPTION: GH Navigation journeys:
    DESCRIPTION: Home page, Highlights tab -> Tap on ""View All Greyhounds Betting"" - will lead to landing page
    DESCRIPTION: Home page, carousel link or Tab bar - App Sports (Menu) -> Tap on Greyhounds will lead to landing page
    PRECONDITIONS: Load Roxanne App / Site
    PRECONDITIONS: User is on Home Page
    """
    keep_browser_open = True

    def test_001_navigate_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds Landing page
        EXPECTED: User should land on Grey Hounds Race Landing Page.
        EXPECTED: The page contains the following tabs :
        EXPECTED: NEXT RACES
        EXPECTED: TODAY
        EXPECTED: TOMORROW
        EXPECTED: BY meeting
        EXPECTED: By Time
        """
        self.site.wait_content_state("Homepage")
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing')

        actual_tabs = self.site.greyhound.tabs_menu.items_names
        if self.brand == 'ladbrokes':
            expected_tabs = [vec.racing.NEXT_RACES.upper(), vec.sb.SPORT_DAY_TABS.today.upper(),
                             vec.sb.SPORT_DAY_TABS.tomorrow.upper(),
                             vec.sb.SPORT_DAY_TABS.future.upper()]
            for tab in expected_tabs:
                self.assertIn(tab, actual_tabs,
                              msg=f'Expected tab: "{tab}" is not in '
                                  f'Actual tabs: "{actual_tabs}"')
        else:
            expected_tabs = [vec.sb.SPORT_DAY_TABS.today, vec.sb.SPORT_DAY_TABS.tomorrow, vec.sb.SPORT_DAY_TABS.future]
            actual_sub_tabs = self.site.greyhound.tab_content.items_names
            self.assertEqual(actual_sub_tabs, vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING,
                             msg=f'Actual tabs: "{actual_sub_tabs}" is not equal with the'
                                 f'Expected tabs: "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING}"')
            self.assertEqual(actual_tabs, expected_tabs,
                             msg=f'Actual tabs: "{actual_tabs}" is not same as '
                                 f'Expected tabs: "{expected_tabs}"')

    def test_002_verify_next_races_tab(self):
        """
        DESCRIPTION: Verify 'NEXT RACES' tab
        EXPECTED: All the next races that are about to start should load in order of start time, earliest being on the top.
        EXPECTED: Each event displays the first 3 entries (count can be increased as configured in the CMS) with an option to view the full race card by clicking on 'MORE'
        EXPECTED: User should be able to scroll up and down the list of races.
        """
        no_of_sel_on_widget = self.get_greyhound_next_races_selections_number_from_cms()

        if self.brand == 'ladbrokes':
            next_race_tab = self.site.greyhound.tabs_menu.current
            self.assertEqual(next_race_tab, vec.racing.RACING_NEXT_RACES_NAME,
                             msg=f'Currently opened tab is "{next_race_tab}" '
                                 f'instead of "{vec.racing.RACING_NEXT_RACES_NAME}"')

            meetings = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(meetings, msg='Meetings are not displayed')
            meetings_names = list(meetings.keys())
            actual_time_list = []
            for times in meetings_names:
                time = times.split(" ")[0]
                actual_time_list.append(time)
            expected_sort_list = sorted(actual_time_list)
            self.assertEqual(actual_time_list, expected_sort_list,
                             msg=f'Actual text: "{actual_time_list}" is not equal with the'
                                 f'Expected text: "{expected_sort_list}"')

            meetings_details = meetings.values()
            for selection in meetings_details:
                actual_length = len(selection.runners.items_names)
                self.assertLessEqual(actual_length, no_of_sel_on_widget,
                                     msg=f'Actual text: "{actual_length}" is not equal with the'
                                         f'Expected text: "{no_of_sel_on_widget}"')

            for i in range(0, 3):
                meetings = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
                meetings_details = list(meetings.values())[i]
                expected_meeting_name = meetings_details.name
                self.assertTrue(meetings_details, msg=f'"{expected_meeting_name}" meeting is not displayed')
                self.assertTrue(meetings_details.header.full_race_card,
                                msg=f'Full race card is not displayed for "{expected_meeting_name}" meeting')
                meetings_details.header.full_race_card.click()
                self.site.wait_splash_to_hide(5)
                actual_meeting_name = self.site.greyhound_event_details.event_name.upper()
                self.assertEqual(actual_meeting_name, expected_meeting_name,
                                 msg=f'Actual text: "{actual_meeting_name}" is not equal with the'
                                     f'Expected text: "{expected_meeting_name}"')
                self.device.go_back()
                self.assertTrue(self.site.greyhound.is_displayed(), msg=f'Greyhound page is not displayed')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            for section_name, self.__class__.section in sections.items():
                if section_name.lower() == vec.racing.NEXT_RACES.lower():
                    break
            meetings = self.section.items_as_ordered_dict
            self.assertTrue(meetings, msg='Meetings are not displayed')
            meetings_names = list(meetings.keys())
            actual_time_list = []
            for times in meetings_names:
                time = times.split(" ")[0]
                actual_time_list.append(time)
            expected_sort_list = sorted(actual_time_list)
            self.assertEqual(actual_time_list, expected_sort_list,
                             msg=f'Actual text: "{actual_time_list}" is not equal with the'
                                 f'Expected text: "{expected_sort_list}"')

            meetings_details = meetings.values()
            for selection in meetings_details:
                actual_length = len(selection.items_names)
                self.assertEqual(actual_length, no_of_sel_on_widget,
                                 msg=f'Actual text: "{actual_length}" is not equal with the'
                                     f'Expected text: "{no_of_sel_on_widget}"')

            for i in range((len(meetings))):
                sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
                for section_name, self.__class__.section in sections.items():
                    if section_name.lower() == vec.racing.NEXT_RACES.lower():
                        break
                event = list(self.section.items_as_ordered_dict.values())[i]
                expected_meeting_name = event.event_name
                self.assertTrue(event, msg=f'"{expected_meeting_name}" event is not displayed')
                self.assertTrue(event.full_race_card,
                                msg=f'Full race card is not displayed for "{expected_meeting_name}" event')
                event.full_race_card.click()
                self.site.wait_splash_to_hide(5)
                wait_for_result(lambda: self.site.greyhound_event_details.is_back_button_displayed(),
                                name='back button is displayed',
                                timeout=5)
                self.assertTrue(self.site.greyhound_event_details.is_back_button_displayed(),
                                msg=f'Back button is not displayed on greyhound page details')
                self.site.contents.scroll_to_bottom()
                self.site.contents.scroll_to_top()
                self.site.greyhound_event_details.back_button_click()
                self.assertTrue(self.site.greyhound.is_displayed(), msg=f'Greyhound page is not displayed')
