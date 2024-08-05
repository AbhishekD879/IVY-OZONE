import pytest
import voltron.environments.constants as vec
from json import JSONDecodeError
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request
from datetime import datetime


# @pytest.mark.tst2 #can't get the feed
# @pytest.mark.stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.next_races
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.reg157_fix
@vtest
class Test_C9608033_Verify_layout_of_event_cards_on_Next_Races_tab(Common):
    """
    TR_ID: C9608033
    NAME: Verify layout of event cards on 'Next Races' tab
    DESCRIPTION: This test case verifies layout of event cards on 'Next Races' tab
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS(CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. Navigate to Horse Racing
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The number of events and selections are CMS configurable. CMS -> system-configuration -> structure -> NextRaces.
    PRECONDITIONS: 2) To get info about class for SiteServe use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/YYYY?simpleFilter=event.typeFlagCodes:intersects:UK,IE,INT&simpleFilter=event.isActive:isTrue&existsFilter=event:simpleFilter:market.name:equals:%7CWin%20or%20Each%20Way%7C&simpleFilter=market.name:equals:%7CWin%20or%20Each%20Way%7C&priceHistory=true&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:1&simpleFilter=outcome.outcomeMeaningMinorCode:notEquals:2&racingForm=outcome&limitRecords=outcome:3&simpleFilter=event.siteChannels:contains:M&simpleFilter=outcome.outcomeStatusCode:equals:A&existsFilter=event:simpleFilter:market.marketStatusCode:equals:A&simpleFilter=market.marketStatusCode:equals:A&simpleFilter=event.eventStatusCode:equals:A&translationLang=en
    PRECONDITIONS: Where,
    PRECONDITIONS: X.XX - current supported version of OpenBet release
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

    def test_001_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: * 'Next Races' tab is selected and highlighted
        EXPECTED: * Content is loaded
        """
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state('Horseracing')
        next_races_tab = self.site.horse_racing.tabs_menu.click_button(button_name=vec.racing.RACING_NEXT_RACES_NAME)
        self.assertTrue(next_races_tab, msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')

    def test_002_verify_event_cards_layout(self):
        """
        DESCRIPTION: Verify 'Event Cards' layout
        EXPECTED: * Event cards are displayed one by one as the list
        EXPECTED: * 'Event Card' consist of:
        EXPECTED: * Header
        EXPECTED: * Subheader
        EXPECTED: * Event card main body
        """
        self.__class__.sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No race sections are found in Next Races')
        for section_name, section in self.sections.items():
            self.assertTrue(section.sub_header, msg=f'No sub_header found in racing card "{section_name}"')
            if section.sub_header.has_e_w_and_places():
                runners_main_body = section.runners.items_as_ordered_dict
                self.assertTrue(runners_main_body, msg=f'No runners main body found in racing card "{section_name}"')
            if section.sub_header.has_watch_label():
                self.assertTrue(section.sub_header.watch_label, msg="watch level is not displayed")
            runners = section.runners.items_as_ordered_dict
            for runner_name, runner in runners.items():
                self.assertTrue(runner_name, msg="runner name is not displayed")
                self.assertTrue(runner.bet_button, msg="bet button is not displayed")

    def test_003_verify_event_card_header_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' header layout
        EXPECTED: 'Event Card' header consists of:
        EXPECTED: * Event name in the next format: **'HH:MM typeName'**(correspond to **'typeName'** and **'startTime'** in SS response or **'courseName"** and **'obStartTime'** in RDH response)
        EXPECTED: * 'More >' link on Desktop and 'See all >' on Mobile
        EXPECTED: * 'Going' status (corresponds to **'going'** within RDH response or **'racingFormEvent'** section from SS response)
        EXPECTED: * 'Distance' value in the next format: **XXm XXf XXy** (corresponds to **'distance'** within RDH response or within **'racingFormEvent'** section from SS response)
        EXPECTED: * 'Countdown timer' in the next format: **'Starts in mm:ss'**
        """
        actual_url = self.get_response_url('/NextNEventToOutcomeForClass')
        response = do_request(method='GET', url=actual_url)
        flag = 0
        for event in response["SSResponse"]["children"]:
            if event["event"]["className"] == "Horse Racing - Live":
                type_name = event["event"]["typeName"]
                start_time = event["event"]["startTime"]
                self.assertTrue(datetime.strptime(str(start_time.rsplit('T', 1)[1].rsplit(':', 1)[0]), '%H:%M'))
                name = event["event"]["name"]
                exact_time = str(name.split(' ', 1)[0])
                section = self.sections.get(exact_time + " " + type_name.upper())
                self.assertTrue(section,
                                msg=f'No "{exact_time + " " + type_name.upper()}" section found in "{self.sections.keys()}"')
                self.assertEqual(section.header.more_link.text, "SEE ALL", msg='more link is not displayed in header')
                for market in event["event"]["children"]:
                    if "eachWayFactorDen" in market.keys():
                        den_value = market["market"]["eachWayFactorDen"]
                        num_value = market["market"]["eachWayFactorNum"]
                        self.assertIn((num_value + "/" + den_value), section.sub_header.e_w_and_places.text,
                                      msg="each way of SS response is not in "
                                          "UI each way palaces")
                        each_way_places = market["market"]["eachWayPlaces"]
                        self.assertTrue(each_way_places, msg="eachWayPlaces attribute is not displayed")
                if "drilldownTagNames" in event["event"].keys():
                    drilldown_tagnames = event["event"]["drilldownTagNames"]
                    self.assertTrue(drilldown_tagnames, msg="signposting icon is not  displayed")
                cashout = event["event"]["cashoutAvail"]
                self.assertTrue(cashout, msg="cashout icon is not displayed")
                flag = flag + 1
                if flag == len(response["SSResponse"]["children"]) - 1 or len(self.sections) == flag:
                    break

    def test_004_verify_event_card_subheader_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' subheader layout
        EXPECTED: 'Event Card' subheader consists of:
        EXPECTED: * 'Each Way' terms in the next format: e.g. E/W 1/5 Places 1-2-3 (taken from SS response and correspond to **'eachWayFactorNum'**, **'eachWayFactorDen'** and **'eachWayPlaces'** attributes )
        EXPECTED: * 'Signposting Promotion' icon (if one or all of **'drilldownTagNames="EVFLAG_EPR,EVFLAG_FI,EVFLAG_MB,EVFLAG_BBL** attributes are received in SS response)
        EXPECTED: * 'CashOut' icon is shown on the right (if the event has **'cashoutAvail'='Y'** in SS response)
        EXPECTED: * 'WATCH' icon
        """
        actual_url = self.get_response_url('/sportsbook-api/categories')
        if not actual_url:
            actual_url = self.get_response_url('/sportsbook-api/categories')
        response = do_request(method='GET', url=actual_url)
        Flag = True
        for event in response["document"]:
            event = response["document"].get(event)
            if event.get("raceNo") and event.get("going"):
                Flag =False
                self.assertTrue(event.get("horses"), msg="horses attribute is not displayed")
                self.assertTrue(event.get("yards"), msg="Distance attribute is not displayed")
                self.assertTrue(event.get("raceNo"), msg="raceNo attribute is not displayed")
                self.assertTrue(event.get("going"), msg="going attribute is not displayed")
                for horse_details in event.get("horses"):
                    self.assertTrue(horse_details.get("saddle"), msg="saddle attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                    self.assertTrue(horse_details.get("silk"), msg="silk attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                    self.assertTrue(horse_details.get("trainer"), msg="trainer attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                    if "draw" in horse_details.keys():
                        self.assertTrue(horse_details.get("draw"), msg="draw number attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                    if "jockey" not in horse_details.keys():
                        for form in horse_details.get("form"):
                            self.assertTrue(form.get("jockey"),
                                            msg="jockey attribute is not displayed in "f'{form} {form.keys()}')
                    else:
                        self.assertTrue(horse_details.get("jockey"), msg="jockey attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                    self.assertTrue(horse_details.get("horseName"), msg="horseName attribute is not displayed in "f'{horse_details} {horse_details.keys()}')
                break
        if Flag==True:
            raise SiteServeException('No events found with attribute raceNo and going ')


    def test_005_verify_event_card_body_layout(self):
        """
        DESCRIPTION: Verify 'Event Card' body layout
        EXPECTED: 'Event Card' body consists of:
        EXPECTED: * Runner Number (taken from **'saddle'** attribute within **'horses'** section of RDH response or **'racingFormEvent'** section in SS response)
        EXPECTED: * Draw Number (In brackets below Runner Number) (taken from **'horses'** section in RDH response or from **'racingFormEvent'** section in SS response)
        EXPECTED: * Silk (taken from **'horses'** section in RDH response or from **'racingFormEvent'** section in SS response)
        EXPECTED: * Horse Name (taken from **'horses'** section in RDH response or **'racingFormEvent'** section in SS response)
        EXPECTED: * Jockey/Trainer Information (taken from **'horses'** section in RDH response)
        EXPECTED: * 'Prive/Odds' button
        """
        # covered in step 005
