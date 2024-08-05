import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request
from json import JSONDecodeError
from datetime import datetime


# @pytest.mark.lad_tst2
# @pytest.mark.lad_stg2 // no runner info in qa2
@pytest.mark.lad_prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C9770776_Verify_layout_of_event_cards_on_Next_Races_tab(BaseRacing):
    """
    TR_ID: C9770776
    NAME: Verify layout of event cards on 'Next Races' tab
    DESCRIPTION: This test case verifies layout of event cards on 'Next Races' tab
    DESCRIPTION: To add: step 5 - additional details (Trainer, Form) can be displayed in Event Card body if received from Racing Post MS
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. Navigate to Greyhounds
    PRECONDITIONS: Note:
    PRECONDITIONS: To get info about class use link:
    PRECONDITIONS: https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&existsFilter=event:simpleFilter:market.name:equals:%7CWin%20or%20Each%20Way%7C&simpleFilter=market.name:equals:%7CWin%20or%20Each%20Way%7C&priceHistory=true&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&racingForm=outcome&limitRecords=outcome:3&simpleFilter=event.siteChannels:contains:M&simpleFilter=outcome.outcomeStatusCode:equals:A&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&translationLang=en
    PRECONDITIONS: Where:
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: YYYY - class ID
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_response_url(self, url):

        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_000_preconditions(self):
        """
        PRECONDITIONS: "Next Races" should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
        PRECONDITIONS: Load Oxygen app.
        PRECONDITIONS: Tap on 'Next Races' tab on the Greyhounds.
        """
        self.get_active_events_for_category(category_id=self.ob_config.backend.ti.greyhound_racing.category_id)

        greyhound_next_races_toggle = self.get_initial_data_system_configuration().get('GreyhoundNextRacesToggle', {})
        if not greyhound_next_races_toggle:
            greyhound_next_races_toggle = self.cms_config.get_system_configuration_item('GreyhoundNextRacesToggle')
        if not greyhound_next_races_toggle.get('nextRacesTabEnabled'):
            raise CmsClientException('Next Races Tab is not enabled for greyhounds in CMS')

        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')

    def test_001_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: * 'Next Races' tab is selected and highlighted
        EXPECTED: * Content is loaded
        """
        next_races_tab = self.site.greyhound.tabs_menu.click_button(button_name=vec.racing.RACING_NEXT_RACES_NAME)
        self.assertTrue(next_races_tab, msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
        self.device.refresh_page()
        self.__class__.sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No race sections are found in next races')
        actual_url = self.get_response_url('/NextNEventToOutcomeForClass')
        if not actual_url:
            raise SiteServeException(f'No event data available for GreyhoundSport')
        self.__class__.response = do_request(method='GET', url=actual_url)

    def test_002_verify_event_cards_layout(self):
        """
        DESCRIPTION: Verify 'Event Cards' layout
        EXPECTED: * Event cards are displayed one by one as the list
        EXPECTED: * 'Event Card' consists of:
        EXPECTED: * Header
        EXPECTED: * Subheader
        EXPECTED: * Event card main body
        """
        for event_card_name, race in self.sections.items():
            self.assertTrue(event_card_name,
                            msg="Event cards are not displayed")
            self.assertTrue(race.header, msg="Header is not displayed in event card")
            self.assertTrue(race.sub_header, msg="subHeader is not displayed in event card")
            self.assertTrue(race.runners, msg="event card main body is not displayed in event card")

    def test_003_verify_event_card_header_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' header layout
        EXPECTED: 'Event Card' header consists of:
        EXPECTED: * Event name in the next format: 'HH:MM typeName'(correspond to 'typeName' and 'startTime' in SS response)
        EXPECTED: * 'More' link with chevron
        """
        event_name_ui = []
        for event_card_name, race in self.sections.items():
            header = race.header
            self.assertTrue(header.more_link, msg='more link is not displayed in header')
            event_name_ui.append(event_card_name.split(" ", 1)[1])

        for event in self.response["SSResponse"]["children"]:
            if not event.get('event'):
                break
            start_time = event["event"]["startTime"]
            self.assertTrue(datetime.strptime(str(start_time.rsplit('T', 1)[1].rsplit(':', 1)[0]), '%H:%M'))
            event_name = event["event"]["typeName"]
            self.assertIn(event_name.upper(), event_name_ui,
                          msg=f'event name"{event_name.upper()}" is not found in event header')

    def test_004_verify_event_card_subheader_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' subheader layout
        EXPECTED: * 'Event Card' subheader consists of:
        EXPECTED: * 'Each Way' terms in the next format: e.g. E/W 1/5 Places 1-2-3 (taken from SS response and correspond to 'eachWayFactorNum', 'eachWayFactorDen' and 'eachWayPlaces' attributes )
        EXPECTED: * 'Signposting Promotion' icon (if one or all of 'drilldownTagNames="EVFLAGEPR,EVFLAGFI,EVFLAGMB,EVFLAGBBL" attributes are received in SS response)
        EXPECTED: * 'CashOut' icon is shown on the right (if the event has 'cashoutAvail'='Y' in SS response)
        EXPECTED: * 'WATCH' icon
        """
        for event_card_name, race in self.sections.items():
            sub_header = race.sub_header
            self.assertTrue(sub_header.watch_label, msg="watch level is not displayed")
            self.assertTrue(sub_header.e_w_and_places, msg="each way places are not displayed")
        for event in self.response["SSResponse"]["children"]:
            if not event.get('event'):
                break
            drilldown_tagnames = event["event"]["drilldownTagNames"]
            if drilldown_tagnames in "EVFLAGEPR,EVFLAGFI,EVFLAGMB,EVFLAGBBL":
                self.assertTrue(drilldown_tagnames, msg="signposting icon is not  displayed")
            cashout = event["event"]["cashoutAvail"]
            if cashout == "Y":
                self.assertTrue(cashout, msg="cashout icon is not displayed")

    def test_005_verify_event_card_body_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' body layout
        EXPECTED: * 'Event Card' body consists of:
        EXPECTED: * Runner Number (taken from 'runnerNumber' section in SS response)
        EXPECTED: * Silk (depens on runner number)
        EXPECTED: * Greyhounds Name (taken from 'name' section in SS response)
        EXPECTED: * 'Prive/Odds' button
        """
        for event_card_name, race in self.sections.items():
            runners = race.runners.items_as_ordered_dict
            for runner_name, runner in runners.items():
                self.assertTrue(runner_name, msg="runner name is not displayed")
                self.assertTrue(runner.bet_button, msg="bet button is not displayed")
                self.assertTrue(runner.runner_info.has_silks_info, msg="silk are not displayed in event card")

        for event in self.response["SSResponse"]["children"]:
            if "".join(list(event.keys())) == "event":
                for market in event['event']['children']:
                    for outcomes in market['market']['children']:
                        self.assertTrue(outcomes['outcome']['runnerNumber'],
                                        msg='runnernumber is available in ss response')
