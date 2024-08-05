import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.horseracing
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C60094817_Verify_display_of_SHOW_INFO_HIDE_INFO_label_HR_Panel(BaseRacing):
    """
    TR_ID: C60094817
    NAME: Verify display of "SHOW INFO"/HIDE INFO" label -HR Panel
    DESCRIPTION: This test case verifies  "SHOW INFO" label is changed to "HIDE INFO" label on clicking the Horse panel view (anywhere in the horse panel to view and  get the information)
    PRECONDITIONS: 1. Horse racing meeting events, should be available
    """
    keep_browser_open = True

    def test_001_launch__coral_urlfor_coral_mobile_app_launch_app(self):
        """
        DESCRIPTION: Launch  Coral URL
        DESCRIPTION: For Coral Mobile App: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: Coral App should be opened
        """
        self.site.wait_content_state("Homepage")
        expected_url = "https://" + tests.HOSTNAME + "/"
        actual_url = self.device.get_current_url()
        self.assertIn(expected_url, actual_url,
                      msg=f'Actual URL: "{actual_url}" is not same as Expected URL: {expected_url}')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        if self.device_type == 'desktop':
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.HORSERACING.upper()).click()
        else:
            self.navigate_to_page('horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_003_verify_any_country_panel_meeting_is_available(self):
        """
        DESCRIPTION: Verify any Country Panel meeting is available
        EXPECTED: The meetings in Country panel should be displayed
        """
        self.site.wait_splash_to_hide()
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Failed to display any section')
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
                        if 'race-on' in event.get_attribute('class'):
                            event.click()
                            self.site.wait_splash_to_hide()
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

    def test_004_click_on_the_any_horse_race_meeting_event(self):
        """
        DESCRIPTION: Click on the any horse race meeting event
        EXPECTED: User should be able to navigate to event detail page. (EDP)
        """
        # functionality convered in step test_003

    def test_005_verify__show_info_label_is_changed_to_hide_info_label_on_clicking_the_horse_panel_viewanywhere_in_the_horse_panel_to_view_and_get_the_information(self):
        """
        DESCRIPTION: Verify  "SHOW INFO" label is changed to "HIDE INFO" label on clicking the Horse panel view(anywhere in the horse panel to view and get the information)
        EXPECTED: User should able to view "HIDE INFO" link
        """
        racing_details = self.site.racing_event_details
        market_tabs = racing_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        selected_market = None
        for market_name, market_value in market_tabs.items():
            if market_name not in ['FORECAST', 'TRICAST', 'TOTEPOOL']:
                market_value.click()
                selected_market = list(racing_details.tab_content.event_markets_list.items_as_ordered_dict.values())[0]
                self.assertTrue(selected_market, msg='No expected market tabs found on EDP')
                break
        outcome = list(selected_market.items_as_ordered_dict.values())[0]
        link_text = racing_details.show_info_link_text
        self.assertEqual(link_text.upper(), vec.racing.SHOW_INFO_TEXT.upper(),
                         msg=f'Actual link text : "{link_text}" Expected link text : "{vec.racing.SHOW_INFO_TEXT}"')

        outcome.show_summary_toggle.click()
        wait_for_result(
            lambda: racing_details.show_info_link_text.upper() == vec.racing.HIDE_INFO_TEXT.upper(),
            name='Wait for show info link to display',
            timeout=20)
        link_text = racing_details.show_info_link_text
        self.assertEqual(link_text.upper(), vec.racing.HIDE_INFO_TEXT.upper(),
                         msg=f'Actual link text : "{link_text}" Expected link text : "{vec.racing.HIDE_INFO_TEXT}"')
