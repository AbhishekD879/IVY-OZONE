import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.hl
@pytest.mark.medium
@vtest
class Test_C44870201_Verify_that_if_user_taps_in_any_resulted_race_on_Race_landing_page_will_be_navigated_to_Results_tab_and_there_user_is_able_to_find_the_race_details_correct_and_complete_displayed_in_both_tabs_By_latest_Results_and_By_Meetings(BaseRacing):
    """
    TR_ID: C44870201
    NAME: Verify that if user taps in any resulted race on Race landing page will be navigated to Results tab and there user is able to find the race details correct and complete displayed, in both tabs, By latest Results and By Meetings
    DESCRIPTION: Verify that if user taps in any resulted race on Race landing page will be navigated to Results tab and there user is able to find the race details correct and complete displayed, in both tabs, By latest Results and By Meetings
    PRECONDITIONS: "User is in Race Landing page on Today tab or in EDP and event status is OFF or Resulted.
    PRECONDITIONS: 1. Horse Racing
    PRECONDITIONS: 2. Greyhounds"
    """
    keep_browser_open = True
    section_skip_list = ['NEXT 4 RACES', 'NEXT FOUR', 'NEXT 4', 'ENHANCED MULTIPLES', 'VIRTUAL RACING',
                         'VIRTUAL RACE CAROUSEL', 'MOBILE EXCLUSIVE', 'PRICE BOMB', 'WINNING DISTANCES',
                         'ENHANCED RACES', 'NEXT RACES', 'TOTE EVENTS', 'OFFERS & FEATURED RACES', 'EXTRA PLACE RACES']

    def test_001_load_the_siteapp(self):
        """
        DESCRIPTION: Load the site/app
        EXPECTED: User is on the Homepage
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to Horse racing page
        EXPECTED: User is on the Featured page of Horse racing
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab "{current_tab}" is not the same as expected "{vec.racing.RACING_DEFAULT_TAB_NAME}"')

    def test_003_verify_the_results_icon_for_any_resulted_event_and_click_on_it(self, sport='horse racing'):
        """
        DESCRIPTION: Verify the Results icon for any resulted event and click on it
        EXPECTED: User is taken to the resulted page of that particular event
        """
        expected_event = None
        if sport == 'horse racing':
            sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        else:
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display any section')
        for i in range(len(sections.items())):
            if sport == 'horse racing':
                sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
            else:
                sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            section_name, section = list(sections.items())[i]
            if section_name not in self.section_skip_list and section_name not in self.next_races_title:
                meetings = sections[section_name].items_as_ordered_dict
                self.assertTrue(meetings, msg='Failed to display any meeting')
                for meeting_name, meeting in meetings.items():
                    events = meeting.items_as_ordered_dict
                    self.assertTrue(events, msg='Failed to display any event')
                    for event_name, event in events.items():
                        has_icon = event.is_resulted
                        if has_icon:
                            event.click()
                            expected_event = event
                            break
                    if expected_event is not None:
                        break
                if expected_event is not None:
                    break
        self.assertIsNotNone(expected_event, msg=f'No resulted markets found for this "{sport}"')

    def test_004_verify_the_results1st2nd3rd__dividends__non_runners_silks(self):
        """
        DESCRIPTION: Verify the results
        DESCRIPTION: 1st/2nd/3rd , dividends & Non runners, silks
        EXPECTED: Results are displayed with
        EXPECTED: 1st/2nd/3rd, dividends, non-runners and silks available
        EXPECTED: Screenshot for reference below:
        EXPECTED: ![](index.php?/attachments/get/103338360)
        """
        for item in self.site.racing_resulted_events_page.items:
            item.scroll_to_we()
            self.assertTrue(item.place_rank.is_displayed(), msg=f'Failed to display the rank number "{item.name}"')
        for item in self.site.racing_headers.items:
            item.scroll_to_we()
            self.assertTrue(item, msg=f'Failed to display header "{item.name}"')

    def test_005_verify_step_2_4_for_greyhounds(self):
        """
        DESCRIPTION: Verify Step 2-4 for Greyhounds
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')
        if self.brand == 'ladbrokes':
            today = vec.sb.TABS_NAME_TODAY
        else:
            today = vec.sb.SPORT_DAY_TABS.today
        self.site.greyhound.tabs_menu.click_button(today)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(today).is_selected(),
                        msg='"Specials tab" is not present')
        self.test_003_verify_the_results_icon_for_any_resulted_event_and_click_on_it(sport='greyhound racing')
        self.test_004_verify_the_results1st2nd3rd__dividends__non_runners_silks()
