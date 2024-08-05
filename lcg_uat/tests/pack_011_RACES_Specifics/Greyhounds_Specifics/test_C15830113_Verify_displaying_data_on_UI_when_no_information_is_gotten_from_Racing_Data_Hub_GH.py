import pytest
import tests
from time import sleep
from tests.base_test import vtest
from json import JSONDecodeError
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.environments import constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Can't create events and update cms in Prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C15830113_Verify_displaying_data_on_UI_when_no_information_is_gotten_from_Racing_Data_Hub_GH(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C15830113
    NAME: Verify displaying data on UI when no information is gotten from Racing Data Hub (GH)
    DESCRIPTION: This test case verifies that app pages are properly displayed when data from Racing Data Hub is unavailable or partially missing (GH)
    PRECONDITIONS: Load CMS and make sure:
    PRECONDITIONS: **Greyhounds (GH) Racing Data Hub toggle is turned on:**  System-configuration > RacingDataHub > isEnabledForGreyhound = true
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
    PRECONDITIONS: **Data, that should be displayed on UI, is empty (values can be mocked)**
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
        self.ob_config.add_virtual_greyhound_racing_event(number_of_runners=1)

    def test_001_tap_on_greyhounds_icon_from_the_sports_menu_ribbon__open_1_event(self):
        """
        DESCRIPTION: Tap on 'Greyhounds' icon from the Sports Menu Ribbon > Open 1 event
        EXPECTED: * GH Event Details Page is opened
        EXPECTED: * Data are displayed from GH Data Hub (Dev tool > Network > type [eventid] in search field > find '%-dev1.api.datafabric.dev.%' reques > data on UI correspond to data from the response)
        EXPECTED: * If no data is available, no data is displayed
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

    def test_002__tap_on_one_selection__add_to_betslip__place_a_betcoraltap_on_my_bets_button_at_the_header__open_bets_tabsettled_bets_tabladbrokestap_the_balance_button_at_the_header__my_bets_menu_item(self):
        """
        DESCRIPTION: * Tap on one selection > Add to betslip > Place a bet
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap on 'My bets' button at the header > 'Open bets' tab/'Settled bets' tab
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap the balance button at the header > 'My bets' menu item
        EXPECTED: * Bet is placed successfully
        EXPECTED: * 'My bets' section is opened
        EXPECTED: * Data in all tabs are displayed from GH Data Hub. If no data is available, no data is displayed
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
        EXPECTED: **should be changed**
        EXPECTED: * The 'Next Races' tab is opened
        EXPECTED: * Data are displayed from GH Data Hub
        EXPECTED: If no data is available, no data is displayed
        EXPECTED: (Dev tool > Network > type .. in search field > data on UI correspond to data from the response)
        """
        self.navigate_to_page(name="greyhound-racing")
        self.site.wait_content_state('Greyhoundracing')
        if self.brand == 'ladbrokes':
            next_races_tab = self.site.greyhound.tabs_menu.click_button(
                button_name=vec.racing.RACING_NEXT_RACES_NAME)
            self.assertTrue(next_races_tab,
                            msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')
        else:
            if self.device_type == 'mobile':
                next_races_name, next_races_tab = \
                    list(self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict.items())[0]
                self.assertEqual(next_races_name, vec.racing.NEXT_RACES.upper(),
                                 msg=f'Currently opened tab is "{next_races_name}" '
                                     f'instead of "{vec.racing.NEXT_RACES.upper()}"')
            else:
                next_races_tab = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict[self.next_races_title]
                self.assertEqual(next_races_tab.name, vec.racing.NEXT_RACES,
                                 msg=f'Currently opened tab is "{next_races_tab.name}" '
                                     f'instead of "{vec.racing.NEXT_RACES}"')
        sections = self.get_sections('greyhound-racing')
        self.assertTrue(sections, msg='No race sections are found in next races')
        if self.brand == 'ladbrokes':
            actual_event_list = list(sections.keys())
        else:
            actual_event_list = list(sections[self.next_races_title].items_as_ordered_dict.keys())

        actual_url = self.get_response_url('/NextNEventToOutcomeForClass')
        response = do_request(method='GET', url=actual_url)
        event_name_ss = []
        for event in response['SSResponse']['children']:
            if not event.get('event'):
                break
            self.assertIn('NE', event['event']['typeFlagCodes'],
                          msg='attribute is not available')
            event_name_ss.append(event['event']['name'].upper())

        if self.device_type == 'desktop':
            self.assertListEqual(sorted(actual_event_list), sorted(event_name_ss),
                                 msg=f'Outcome name "{list(sections.keys())}" is not '
                                     f'the same as expected "{event_name_ss}"')
        else:
            for index in sorted(actual_event_list):
                self.assertIn(index, event_name_ss,
                              msg=f'Event name "{index}" is not ievent = list(next_race_tab.items_as_ordered_dict.values())[i]n '
                                  f'expected events "{event_name_ss}"')
