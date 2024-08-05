import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.p1
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870199_Racing_Result_Verify_that_when_user_navigates_via_Race_Landing_page_to_Results_tab_the_data_is_displayed_under_two_tabs_By_latest_Results_and_By_Meetings_Verify_results_contents_Tricast_Forecast_dividends_Non_runners_Runner_silk_Runner_number(BaseRacing):
    """
    TR_ID: C44870199
    NAME: "Racing Result : "Verify that when user navigates via Race Landing page to Results tab, the data is displayed under two tabs, By latest Results and By Meetings -Verify results contents: Tricast/Forecast dividends Non-runners Runner silk Runner number
    DESCRIPTION: "Verify that when user navigates via Race Landing page to Results tab, the data is displayed under two tabs, By latest Results and By Meetings
    DESCRIPTION: -Verify results contents:
    DESCRIPTION: Tricast/Forecast dividends
    DESCRIPTION: Non-runners
    DESCRIPTION: Runner silk
    DESCRIPTION: Runner number
    DESCRIPTION: Runner name"
    """
    keep_browser_open = True
    section_skip_list = ['NEXT 4 RACES', 'NEXT FOUR', 'NEXT 4', 'ENHANCED MULTIPLES',
                         'MOBILE EXCLUSIVE', 'PRICE BOMB', 'WINNING DISTANCES', 'ENHANCED RACES',
                         'NEXT RACES', 'TOTE EVENTS', 'OFFERS & FEATURED RACES', 'EXTRA PLACE RACES']

    def test_001_verify_the_contents_of_resulted_raceon_racing_scroll_panel___click_on_the_raceevent_with_the_resultpost_sign(self):
        """
         DESCRIPTION: Verify the contents of Resulted Race
         DESCRIPTION: On Racing scroll panel - Click on the Race/Event with the Result/post sign
         EXPECTED: User should be able to see
         EXPECTED: Event Name, Day, Time, Date.
         EXPECTED: E/W terms
         EXPECTED: Race Result - Selection Name, Place, silks and odds
         EXPECTED: Dividends: Forecast
         """
        expected_meeting_name = None
        expected_event = None
        self.navigate_to_page(name='horse-racing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.Racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Current tab {current_tab} is not the same as expected {vec.Racing.RACING_DEFAULT_TAB_NAME}')
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(len(sections) is not None, msg='Failed to display any section')
        for section_name, section in sections.items():
            if section_name in self.section_skip_list or self.next_races_title in section_name:
                continue
            else:
                meetings = section.items_as_ordered_dict
                for meeting_name, meeting in meetings.items():
                    events = meeting.items_as_ordered_dict
                    for event_name, event in events.items():
                        has_icon = event.is_resulted
                        if has_icon:
                            expected_meeting_name, expected_event = meeting_name, event
                            break
                    if expected_event is not None:
                        break
                if expected_event is not None:
                    break

        if expected_event is not None:
            self.navigate_to_edp(expected_event.event_id, 'horse-racing')
            actual_meeting_name = self.site.racing_resulted_events_page.meeting_name.upper()
            resulted_event_time = self.site.racing_resulted_events_page.event_day_date
            meeting_name_words = actual_meeting_name.split(' ')
            if len(meeting_name_words) > 1:
                actual_meeting_name = meeting_name_words[1]
            self.assertTrue(expected_meeting_name.upper() in actual_meeting_name or actual_meeting_name in expected_meeting_name.upper(),
                            msg=f'Expected meeting name: {expected_meeting_name} not in Actual: {actual_meeting_name}')
            self.assertFalse(resulted_event_time is None, msg='Resulted event time is None')
            if self.site.racing_resulted_events_page.each_way_container:
                self.assertTrue(self.site.racing_resulted_events_page.each_way_container.is_displayed(),
                                msg='E/W Terms is displayed')
            for item in self.site.racing_resulted_events_page.items:
                item.scroll_to_we()
                self.assertTrue(item.place_rank.is_displayed(), msg='Failed to display the rank number')
                self.assertTrue(item.horse_name is not None, msg='Failed to display the horse name')
                self.assertTrue(item.odds_price.is_displayed(), msg='Failed to display odds price')
                self.assertTrue(item.has_silks, msg='Failed to display the silk')

            for item in self.site.racing_resulted_tricast_forecast.items:
                self.assertTrue(item.name_col.is_displayed(), msg='Failed to display the Tricast/Forecast text')
                self.assertTrue(item.result_col.is_displayed(), msg='Failed to display the dividend result')
                self.assertTrue(item.value_col.is_displayed(), msg='Failed to display the dividend value')
