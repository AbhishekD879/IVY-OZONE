import re
from time import sleep
import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec
from voltron.utils.helpers import normalize_name


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.next_races
@pytest.mark.mobile_only
@pytest.mark.horseracing
@vtest
class Test_C9608034_Verify_More_link_functionality_for_Next_Races_module_on_Horse_Racing_EDP(BaseRacing):
    """
    TR_ID: C9608034
    VOL_ID: C23220559
    NAME: Verify 'More' link functionality for 'Next Races' module on Horse Racing EDP
    DESCRIPTION: This test case verifies 'More' link functionality for 'Next Races' module on Horse Racing EDP
    PRECONDITIONS: 1. "Next Races" should be enabled in CMS(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Tap on 'Next Races' tab on the Horse Racing EDP
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. List of Event Cards is displayed at the page
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 1) The number of events and selection are CMS configurable too. CMS -> system-configuration -> structure -> NextRaces.
    PRECONDITIONS: 2) To get info about class use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&existsFilter=event:simpleFilter:market.name:equals:%7CWin%20or%20Each%20Way%7C&simpleFilter=market.name:equals:%7CWin%20or%20Each%20Way%7C&priceHistory=true&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&racingForm=outcome&limitRecords=outcome:3&simpleFilter=event.siteChannels:contains:M&simpleFilter=outcome.outcomeStatusCode:equals:A&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&translationLang=en
    PRECONDITIONS: Where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
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

        self.site.open_sport(name=self.get_sport_title(self.ob_config.horseracing_config.category_id))
        self.__class__.next_races_tab = self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_NEXT_RACES_NAME)
        sleep(1) #fetching of the value from UI is taking some time
        self.assertTrue(self.next_races_tab, msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')

        self.__class__.sections = self.get_sections('horse-racing')
        self.assertTrue(self.sections, msg='No race sections are found in next races')

    def test_001_verify_more_link_displaying(self):
        """
        DESCRIPTION: Verify 'More' link displaying
        EXPECTED: * Link is displayed at the 'Event Card' header
        EXPECTED: * Link is displayed for each event in 'Next Races' module
        EXPECTED: * Link is aligned to the right
        """
        for race_name, race in self.sections.items():
            self.assertTrue(race.header.has_view_full_race_card(),
                            msg=f'"More" link is not found for race: "{race_name}"')

    def test_002_tap_on_more_link(self):
        """
        DESCRIPTION: Tap on 'More' link
        EXPECTED: The user takes to the particular event details page
        """
        race_name, race = list(self.sections.items())[0]
        link_url = race.header.full_race_card.get_link()
        event_id = link_url.split('?origin')[0].split('/')[-1]  # .../123456?origin...
        event_id = int(''.join(re.findall('\d+', event_id)))  # this finds all the digit characters from event_id and adds it to an empty string, then convert it to a integer
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
        sleep(1) #fetching of the value from UI is taking some time
        self.assertEqual(ui_event_name, ss_event_name, msg=f'SiteServe event name "{ss_event_name}" != '
                                                           f'UI event name "{ui_event_name}"')

    def test_003_tap_on_back_button(self):
        """
        DESCRIPTION: Tap on 'Back' button
        EXPECTED: The previously visited page is opened
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='Horseracing')
        self.assertTrue(self.next_races_tab,
                        msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected when user revisits the page')
