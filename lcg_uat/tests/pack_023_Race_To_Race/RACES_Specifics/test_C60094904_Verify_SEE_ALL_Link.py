import re
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.low
# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.mobile_only
@pytest.mark.horseracing
@pytest.mark.next_races
@pytest.mark.races
@pytest.mark.sports
@vtest
class Test_C60094904_Verify_SEE_ALL_Link(BaseRacing):
    """
    TR_ID: C60094904
    NAME: Verify ''SEE ALL' Link
    DESCRIPTION: This test case is for checking of 'View Full Race Card' link.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: "Next Races" should be enabled in CMS (CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
        PRECONDITIONS: Load Oxygen app.
        PRECONDITIONS: Tap on 'Next Races' tab on the Horse Racing EDP
        """
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle.get('nextRacesTabEnabled'):
            raise CmsClientException('Next Races Tab is not enabled for HorseRacing in CMS')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state('homepage')

    def test_002__for_ladbrokes_navigate_to_horse_racing_landing_pageclick_on_next_races_tab(self):
        """
        DESCRIPTION: ** FOR LADBROKES **
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        DESCRIPTION: Click on Next races tab
        EXPECTED: * 'Horse Racing' landing page is loaded
        EXPECTED: * 'Featured' tab is opened by default
        EXPECTED: * 'Next Races' section is shown
        """
        if self.brand == 'ladbrokes':
            self.navigate_to_page(name='horse-racing')
            self.site.wait_content_state('Horseracing')
            self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_NEXT_RACES_NAME)
            wait_for_result(lambda: self.site.horse_racing.tabs_menu.current, timeout=10, name='Current tab is not displayed')
            self.__class__.next_races_tab = self.site.horse_racing.tabs_menu.current
            self.assertTrue(self.next_races_tab, msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
            self.__class__.sections = self.get_sections('horse-racing')
            self.assertTrue(self.sections, msg='No race sections are found in next races')

    def test_003_on_next_races_module_find_see_all_link(self):
        """
        DESCRIPTION: On 'Next Races' module find 'SEE ALL' link
        EXPECTED: * 'SEE ALL' is displayed for each event in 'Next Races' module
        EXPECTED: * Link is displayed at the top right corner of the section
        EXPECTED: * Link is aligned to the right
        EXPECTED: * Text is hyperlinked
        """
        if self.brand == 'ladbrokes':
            for race_name, race in self.sections.items():
                self.assertTrue(race.header.has_view_full_race_card(),
                                msg=f'"More" link is not found for race: "{race_name}"')

    def test_004_clicktap_see_all_link(self):
        """
        DESCRIPTION: Click/Tap 'SEE ALL' link
        EXPECTED: The event's details page is opened.
        """
        if self.brand == 'ladbrokes':
            race_name, race = list(self.sections.items())[0]
            link_url = race.header.full_race_card.get_link()
            self.assertTrue(link_url, msg='"SEE ALL LINK" is hyperlinked')
            event_id = link_url.split('?origin')[0].split('/')[-1]  # .../123456?origin...
            event_id = int(''.join(re.findall('\d+', event_id)))
            event_ss_info = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
            ss_event_name = normalize_name(event_ss_info[0]['event']['name'])
            ss_event_time = event_ss_info[0]['event']['startTime']
            event_time = self.convert_time_to_local(date_time_str=ss_event_time,
                                                    ob_format_pattern=self.ob_format_pattern,
                                                    ui_format_pattern='%H:%M',
                                                    ss_data=True)
            ss_event_name = ss_event_name if ss_event_name[0].isdigit() else f'{event_time} {ss_event_name}'
            race.header.click()
            self.site.wait_content_state(state_name='RacingEventDetails')
            ui_event_name = self.site.racing_event_details.event_title
            self.assertEqual(ui_event_name, ss_event_name, msg=f'SiteServe event name "{ss_event_name}" != '
                                                               f'UI event name "{ui_event_name}"')

    def test_005_clicktap_back_button(self):
        """
        DESCRIPTION: Click/Tap 'Back' button
        EXPECTED: The previously visited page is opened
        """
        if self.brand == 'ladbrokes':
            self.site.back_button_click()
            self.site.wait_content_state(state_name='Horseracing')
            self.assertTrue(self.next_races_tab,
                            msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected when user revisits the page')

    def test_006_for_coral__ladbrokesnavigate_to_home_page__next_races_tab(self):
        """
        DESCRIPTION: **For CORAL & LADBROKES**
        DESCRIPTION: Navigate to Home page > Next races tab
        EXPECTED: **For CORAL& LADBROKES**
        EXPECTED: 'Next Races' section is shown
        """
        if self.brand == 'ladbrokes':
            self.navigate_to_page(name='homepage')
            self.site.wait_content_state('homepage')
        self.site.home.tabs_menu.click_button(button_name=vec.sb.TABS_NAME_NEXT.upper())
        # used sleep because Next race tab is taking time to reflect, other synchronization method is not working
        sleep(2)
        next_races_tab = self.site.home.tabs_menu.current
        self.assertTrue(next_races_tab, msg=f'"{vec.sb.TABS_NAME_NEXT.upper()}" tab is not selected after click')
        self.__class__.meetings = self.site.home.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.meetings, msg='No race sections are found in next races')

    def test_007_for_coral__ladbrokesrepeat_steps__3___5(self):
        """
        DESCRIPTION: **For CORAL & LADBROKES**
        DESCRIPTION: Repeat steps # 3 - 5
        """
        for event in list(self.meetings.values())[0:2]:
            self.assertTrue(event.full_race_card,
                            msg=f'"SEE ALL" link is not found for race: "{event.event_name}"')
        event = list(self.meetings.values())[0]
        link_url = event.full_race_card.get_link()
        event_id = link_url.split('?origin')[0].split('/')[-1]  # .../123456?origin...
        event_id = int(''.join(re.findall('\d+', event_id)))
        event_ss_info = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        ss_event_name = normalize_name(event_ss_info[0]['event']['name'])
        ss_event_time = event_ss_info[0]['event']['startTime']
        if self.brand == 'ladbrokes':
            event_time = self.convert_time_to_local(date_time_str=ss_event_time,
                                                    ob_format_pattern=self.ob_format_pattern,
                                                    ui_format_pattern='%H:%M',
                                                    ss_data=True)
            ss_event_name = ss_event_name if ss_event_name[0].isdigit() else f'{event_time} {ss_event_name}'
        event.full_race_card.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
        ui_event_name = self.site.racing_event_details.event_title
        if self.brand == 'bma':
            ui_event_name = ui_event_name.replace('\n', ' ')
        self.assertEqual(ui_event_name, ss_event_name, msg=f'SiteServe event name "{ss_event_name}" != '
                                                           f'UI event name "{ui_event_name}"')
        self.site.back_button_click()
        self.site.wait_content_state(state_name='homepage')
        next_races_tab = self.site.home.tabs_menu.current
        self.assertTrue(next_races_tab,
                        msg=f'"{vec.sb.TABS_NAME_NEXT.upper()}" tab is not selected when user revisits the page')
