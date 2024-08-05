import re
import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec
from voltron.utils.helpers import normalize_name


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.next_races
@pytest.mark.races
@vtest
class Test_C2989464_Verify_More_link_functionality_for_Next_Races_module_on_the_Homepage(BaseRacing):
    """
    TR_ID: C2989464
    NAME: Verify 'More' link functionality for 'Next Races' module on the Homepage
    DESCRIPTION: This test case verifies 'More' / 'Full Race Card'(for Coral Desktop) link functionality for 'Next Races' module on the Homepage
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load Oxygen app
        PRECONDITIONS: 2. Tap on 'Next Races' tab at the Homepage (for Mobile) / scroll the homepage down to 'Next Races' carousel (for Desktop)
        PRECONDITIONS: 3. Race events are available for the current day
        PRECONDITIONS: 4. List of Event Cards is displayed at the page
        PRECONDITIONS: *Note:*
        PRECONDITIONS: 1) 'Next Races' tab is CMS configurable, please look at the https://ladbrokescoral.testrail.com/index.php?/cases/view/29371 test case where this process is described.
        PRECONDITIONS: 2) The number of events and selection are CMS configurable too. CMS -> system-configuration -> structure -> NextRaces.
        PRECONDITIONS: 3) To get info about class use link:
        PRECONDITIONS: https://{openbet_env_link}/openbet-ssviewer/Drilldown/X.XX/NextNEventToOutcomeForClass/N/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&simpleFilter=market.templateMarketName:equals:|Win%20or%20Each%20Way|&priceHistory=true&simpleFilter=event.siteChannels:contains:M&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=outcome.outcomeStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.rawIsOffCode:notEquals:Y&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&limitRecords=outcome:4&translationLang=en&responseFormat=json
        PRECONDITIONS: Where
        PRECONDITIONS: X.XX - current supported version of OpenBet release
        PRECONDITIONS: YYYY - class ID
        PRECONDITIONS: N - number of events
        PRECONDITIONS: Note: OB supports only values:3, 5, 7 or 12. Example, if CMS value > 12 then 12 events is set on UI, if CMS value <= 5 then 5 events is set on UI and etc.
        """
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle.get('nextRacesTabEnabled'):
            raise CmsClientException('Next Races Tab is not enabled for HorseRacing in CMS')

        self.site.wait_content_state('homepage')

        if self.device_type == 'mobile':
            self.site.home.tabs_menu.click_button(button_name=vec.sb.TABS_NAME_NEXT.upper())
            # used sleep because Next race tab is taking time to reflect, other synchronization method is not working
            sleep(2)
            next_races_tab = self.site.home.tabs_menu.current
            self.assertTrue(next_races_tab, msg=f'"{vec.sb.TABS_NAME_NEXT.upper()}" tab is not selected after click')
            self.__class__.meetings = self.site.home.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.meetings, msg='No race sections are found in next races')
        else:
            self.__class__.meetings = self.site.home.get_module_content(module_name=self.next_races_title).accordions_list.items_as_ordered_dict
            self.assertTrue(self.meetings, msg='"Next Races" carousel is not displayed')

        for event in list(self.meetings.values())[0:2]:
            self.assertTrue(event.full_race_card,
                            msg=f'"SEE ALL" link is not found for race: "{event.event_name}"')
            self.__class__.event = list(self.meetings.values())[0]
            link_url = self.event.full_race_card.get_link()
            event_id = link_url.split('?origin')[0].split('/')[-1]  # .../123456?origin...
            event_id = int(''.join(re.findall('\d+', event_id)))
            event_ss_info = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
            self.__class__.ss_event_name = normalize_name(event_ss_info[0]['event']['name'])
            ss_event_time = event_ss_info[0]['event']['startTime']
            if self.brand == 'ladbrokes':
                event_time = self.convert_time_to_local(date_time_str=ss_event_time,
                                                        ob_format_pattern=self.ob_format_pattern,
                                                        ui_format_pattern='%H:%M',
                                                        ss_data=True)
                self.__class__.ss_event_name = self.ss_event_name if self.ss_event_name[0].isdigit() else f'{event_time} {self.ss_event_name}'

    def test_001_verify_more__full_race_cardfor_coral_desktop_link_displaying(self):
        """
        DESCRIPTION: Verify 'More' / 'Full Race Card'(for Coral Desktop) link displaying
        EXPECTED: * Link is displayed at the 'Event Card' header / at the Event Card footer (for Coral Desktop)
        EXPECTED: * Link is displayed for each event in 'Next Races' module
        EXPECTED: * Link is aligned to the right
        """
        for event in list(self.meetings.values())[0:2]:
            self.assertTrue(event.full_race_card,
                            msg=f'"SEE ALL" link is not found for race: "{event.event_name}"')
        self.__class__.event = list(self.meetings.values())[0]
        link_url = self.event.full_race_card.get_link()
        event_id = link_url.split('?origin')[0].split('/')[-1]  # .../123456?origin...
        event_id = int(''.join(re.findall('\d+', event_id)))
        event_ss_info = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        self.__class__.ss_event_name = normalize_name(event_ss_info[0]['event']['name'])
        ss_event_time = event_ss_info[0]['event']['startTime']
        if self.brand == 'ladbrokes':
            event_time = self.convert_time_to_local(date_time_str=ss_event_time,
                                                    ob_format_pattern=self.ob_format_pattern,
                                                    ui_format_pattern='%H:%M',
                                                    ss_data=True)
            self.__class__.ss_event_name = self.ss_event_name if self.ss_event_name[0].isdigit() else f'{event_time} {self.ss_event_name}'

    def test_002_tap_on_more__full_race_cardfor_coral_desktop_link(self):
        """
        DESCRIPTION: Tap on 'More' / 'Full Race Card'(for Coral Desktop) link
        EXPECTED: The user takes to the particular event details page
        """
        self.event.full_race_card.click()
        self.site.wait_content_state(state_name='RacingEventDetails', timeout=20)
        ui_event_name = self.site.racing_event_details.event_title
        if self.brand == 'bma':
            ui_event_name = ui_event_name.replace('\n', ' ')
        self.assertEqual(ui_event_name, self.ss_event_name, msg=f'SiteServe event name "{self.ss_event_name}" != '
                                                                f'UI event name "{ui_event_name}"')

    def test_003_tap_on_back_button(self):
        """
        DESCRIPTION: Tap on 'Back' button
        EXPECTED: The previously visited page is opened
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='homepage')
        if self.device_type == 'mobile':
            next_races_tab = self.site.home.tabs_menu.current
            self.assertTrue(next_races_tab,
                            msg=f'"{vec.sb.TABS_NAME_NEXT.upper()}" tab is not selected when user revisits the page')
        else:
            self.site.wait_content_state('homepage')
            next_races_module = self.site.home.get_module_content(module_name=self.next_races_title).accordions_list.items_as_ordered_dict
            self.assertTrue(next_races_module, msg='"Next Races" carousel is not displayed')
