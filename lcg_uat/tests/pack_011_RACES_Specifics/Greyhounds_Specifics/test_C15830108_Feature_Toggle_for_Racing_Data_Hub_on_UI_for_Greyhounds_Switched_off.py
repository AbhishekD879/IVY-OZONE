import pytest
import tests
from json import JSONDecodeError
from time import sleep
from datetime import datetime
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.environments import constants as vec
from tests.base_test import vtest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can't create events and update cms in Prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C15830108_Feature_Toggle_for_Racing_Data_Hub_on_UI_for_Greyhounds_Switched_off(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C15830108
    NAME: Feature Toggle for Racing Data Hub on UI for Greyhounds (Switched off)
    DESCRIPTION: This test case verifies that information from Racing Data Hub (Greyhounds GH) on UI can be switched off in CMS
    PRECONDITIONS: Load CMS and make sure:
    PRECONDITIONS: **Greyhounds (GH) Racing Data Hub toggle is turned off:**  System-configuration > RacingDataHub > isEnabledForGreyhound = false
    PRECONDITIONS: Horse Racing (HR) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForHorseRacing = true
    PRECONDITIONS: CMS and OB TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: ----------------
    PRECONDITIONS: **Racing Data Hub link:**
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com
    PRECONDITIONS: Ladbrokes DEV : ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: categoryKey : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: eventKey : OB Event id
    PRECONDITIONS: i.e. Racing Post information on Ladbrokes Digital for OB event id 5227306:
    PRECONDITIONS: https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/5227306/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: **Open bet link:** http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    PRECONDITIONS: -------------------------
    PRECONDITIONS: **Next races should be set:**
    PRECONDITIONS: CMS > System-configuration > NextRaces
    PRECONDITIONS: CMS > Module Ribbon Tab >  NEXT RACES
    PRECONDITIONS: ---------------------
    PRECONDITIONS: **Load Sportsbook App**
    PRECONDITIONS: **Log in as a user with a positive balance (e.g., mincyua/password)**
    """
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
        self.cms_config.update_system_configuration_structure(config_item='RacingDataHub',
                                                              field_name='isEnabledForGreyhound', field_value=False)
        self.cms_config.update_system_configuration_structure(config_item='RacingDataHub',
                                                              field_name='isEnabledForHorseRacing', field_value=True)
        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, cashout=True,
                                                                    lp_prices=['1/5'])
        self.__class__.event_id = event_params.event_id
        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.hr_event_id = self.ob_config.add_UK_racing_event().event_id
        self.ob_config.add_virtual_greyhound_racing_event(number_of_runners=1)

    def test_001_tap_on_greyhounds_icon_from_the_sports_menu_ribbon__open_1_event(self):
        """
        DESCRIPTION: Tap on 'Greyhounds' icon from the Sports Menu Ribbon > Open 1 event
        EXPECTED: * GH Event Details Page is opened
        EXPECTED: Data are displayed from Openbet (Dev tool > Network > type [eventid] in search field > find request https://backoffice-tst2.coral.co.uk > data on UI correspond to data from the response)
        """
        username = tests.settings.betplacement_user
        self.site.login(username=username)
        self.site.wait_content_state('homepage')
        sport_name = vec.sb.GREYHOUND if tests.settings.brand == 'ladbrokes' else vec.sb.GREYHOUND.upper()
        self.site.open_sport(name=sport_name, timeout=15)
        self.navigate_to_edp(event_id=self.event_id, sport_name='greyhound-racing')
        sections = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in today tab')
        sleep(2)
        actual_url = self.get_response_url('/EventToOutcomeForEvent/' + str(self.event_id))
        response = do_request(method='GET', url=actual_url)
        if not response:
            raise SiteServeException(f'No event data available for GreyhoundSport')
        for event in response["SSResponse"]["children"]:
            if not event.get('event'):
                break
            self.assertEqual(event["event"]["cashoutAvail"], "Y", msg="Cashout Avail is not available")
            self.assertEqual(event["event"]["categoryName"], "Greyhound Racing",
                             msg="CategoryName is not matching with GreyHounds")
            self.assertEqual(event["event"]["id"], self.event_id,
                             msg="event id is not matching with SSresponse event id")
            self.assertEqual(event["event"]["name"], self.event_name,
                             msg="event name is not matching with SSresponse event id")

    def test_002__tap_on_one_selection__add_to_betslip__place_a_betcoraltap_on_my_bets_button_at_the_header__open_bets_tabsettled_bets_tabladbrokestap_the_balance_button_at_the_header__my_bets_menu_item(
            self):
        """
        DESCRIPTION: * Tap on one selection > Add to betslip > Place a bet
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap on 'My bets' button at the header > 'Open bets' tab/'Settled bets' tab
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap the balance button at the header > 'My bets' menu item
        EXPECTED: * Bet is placed successfully
        EXPECTED: * 'My bets' section is opened
        EXPECTED: * Data in all tabs are displayed from Openbet
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        if self.site.wait_for_quick_bet_panel():
            self.site.wait_for_quick_bet_panel()
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
        self.site.open_betslip()
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_tap_on_next_races_tab(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab
        EXPECTED: * The 'Next Races' tab is opened
        EXPECTED: * Data are displayed from Openbet
        EXPECTED: (Dev tool > Network > type .. in search field > > data on UI correspond to data from the response)
        """
        if tests.settings.brand == 'ladbrokes':
            event_ui_names = []
            self.navigate_to_page(name="greyhound-racing")
            next_races_tab = self.site.greyhound.tabs_menu.click_button(
                button_name=vec.racing.RACING_NEXT_RACES_NAME)
            self.assertTrue(next_races_tab,
                            msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No race sections are found in Next Races')
            for section in sections.keys():
                event_ui_names.append(section.split(" ", 1)[1])
            actual_url = self.get_response_url('/NextNEventToOutcomeForClass')
            response = do_request(method='GET', url=actual_url)
            if not response:
                raise SiteServeException(f'No response found for NextNEventToOutcomeForClass"')
            for event in response["SSResponse"]["children"]:
                if not event.get('event'):
                    break
                type_name = event["event"]["typeName"]
                start_time = event["event"]["startTime"]
                self.assertTrue(datetime.strptime(str(start_time.rsplit('T', 1)[1].rsplit(':', 1)[0]), '%H:%M'))
                self.assertIn(type_name.upper(), event_ui_names,
                              msg=f'event name"{type_name.upper()}" is not found in "{sections.keys()}"')

    def test_004_tap_on_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on 'Horse Racing' icon from the Sports Menu Ribbon
        EXPECTED: * HR Event Details Page is opened
        EXPECTED: * Data are displayed from Racing Data Hub
        EXPECTED: (Dev tool > Network > type [eventid] in search field > find '%-dev1.api.datafabric.dev.%' request > data on UI correspond to data from the response)
        EXPECTED: * In openbet link for event there are no 'racingForm: outcome' and 'racingForm: events' parameters (Query String Parameters) and such info is absent in the response
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        self.navigate_to_edp(event_id=self.hr_event_id, sport_name='horse-racing')
        actual_url = self.get_response_url('/EventToOutcomeForEvent/' + str(self.hr_event_id))
        if not actual_url:
            raise SiteServeException(f'No event data available for GreyhoundSport')
        self.assertNotIn('racingForm: events', actual_url,
                         msg=f'Expected: "racingForm: events" is not present in Actual: "{actual_url}"')
        self.assertNotIn('racingForm: outcome', actual_url,
                         msg=f'Expected: "racingForm: outcome" is not present in Actual: "{actual_url}"')
