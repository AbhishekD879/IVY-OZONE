import pytest
import tests
from datetime import datetime
from voltron.utils.waiters import wait_for_haul
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing, BaseGreyhound
from json import JSONDecodeError
from voltron.environments import constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request


# @pytest.mark.tst2 #can't get the feed
# @pytest.mark.stg2
# @pytest.mark.hl
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C15830106_Feature_Toggle_for_Racing_Data_Hub_on_UI_for_Greyhounds_Switched_on(BaseSportTest, BaseBetSlipTest, BaseGreyhound, BaseRacing):
    """
    TR_ID: C15830106
    NAME: Feature Toggle for Racing Data Hub on UI for Greyhounds (Switched on)
    DESCRIPTION: This test case verifies that information from Racing Data Hub (Greyhounds GH) on UI can be switched on in CMS
    PRECONDITIONS: Load CMS and make sure:
    PRECONDITIONS: **Greyhounds (GH) Racing Data Hub toggle is turned on:**  System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: Horse Racing (HR) Racing Data Hub toggle is turned off: System-configuration > RacingDataHub > isEnabledForHorseRacing = false
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
        DESCRIPTION: Find events
        """
        event = self.get_event_details(datafabric_data=True, df_event_summary=True)
        self.__class__.event_id = event.event_id
        self.__class__.event_name = event.event_name
        self.__class__.hr_event_id = \
            self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id)[0]['event']['id']

    def test_001_tap_on_greyhounds_icon_from_the_sports_menu_ribbon__open_1_event(self):
        """
        DESCRIPTION: Tap on 'Greyhounds' icon from the Sports Menu Ribbon > Open 1 event
        EXPECTED: * GH Event Details Page is opened
        EXPECTED: * Data are displayed from Racing Data Hub
        EXPECTED: (Dev tool > Network > type [eventid] in search field > find '%-dev1.api.datafabric.dev.%' request > data on UI correspond to data from the response):
        EXPECTED: ***Coral:***
        EXPECTED: **Mobile**
        EXPECTED: - Header area: Distance; Going; Racing Post Pick.
        EXPECTED: - Runner area: Trainer, Form, Comment (Upward / Downward chevron)
        EXPECTED: **Desktop**
        EXPECTED: - Header area: Distance, Going.
        EXPECTED: - Runner area: Trainer, Form, Comment ( Show more / Show less )
        EXPECTED: * In openbet link for event there are no 'racingForm: outcome' and 'racingForm: events' parameters (Query String Parameters) and such info is absent in the response (look attachment EDP.DF))
        """
        self.site.login()
        self.site.wait_content_state('homepage')
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')
        self.navigate_to_edp(event_id=self.event_id, sport_name='greyhound-racing')
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        self.assertEqual(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB,
                         self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.current,
                         msg=f'{vec.racing.RACING_EDP_DEFAULT_MARKET_TAB}is not selected')
        sections = self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in today tab')
        wait_for_haul(1)
        actual_url = self.get_response_url('/EventToOutcomeForEvent/' + str(self.event_id))
        response = do_request(method='GET', url=actual_url)
        if not response:
            raise SiteServeException(f'No event data available for GreyhoundSport')
        for event in response["SSResponse"]["children"]:
            if not event.get('event'):
                break
            self.assertEqual(event["event"]["categoryName"], "Greyhound Racing",
                             msg="CategoryName is not matching with GreyHounds")
            self.assertEqual(event["event"]["id"], self.event_id,
                             msg="event id is not matching with SSresponse event id")
            self.assertEqual(event["event"]["name"], self.event_name,
                             msg="event name is not matching with SSresponse event id")
        if tests.settings.brand == 'ladbrokes':
            self.assertTrue(self.site.greyhound_event_details.tab_content.has_post_info(),
                            msg='Racing Post info section is not found')
        self.assertTrue(self.site.greyhound_event_details.tab_content.race_details.has_race_distance(),
                        msg='Distance not found')
        if self.site.greyhound_event_details.tab_content.race_details.has_race_going():
            self.assertTrue(self.site.greyhound_event_details.tab_content.race_details.race_going,
                            msg='Going status should be present, but it is not')
        self.__class__.markets = self.site.greyhound_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No markets found')
        market = self.markets.get(vec.racing.RACING_EDP_DEFAULT_MARKET_TAB)
        outcomes = market.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found')
        for outcome_name, outcome in outcomes.items():
            if 'N/R' not in outcome_name and 'Unnamed' not in outcome_name:
                self.assertTrue(outcome.form, msg='There are no Forms with in the event')
                self.assertTrue(outcome.has_show_summary_toggle, msg='There is no show more link with in the event')
                if outcome.jockey_trainer_info is not '':
                    self.assertTrue(outcome.jockey_trainer_info,
                                    msg='There are no jockey_trainer_info with in the event')
                self.assertEqual(vec.racing.SHOW_MORE.upper(), outcome.toggle_icon_name.upper(),
                                 msg='Get the text of show more link')
                outcome.show_summary_toggle.click()
                wait_for_haul(1)
                self.assertEqual(vec.racing.SHOW_LESS.upper(), outcome.toggle_icon_name.upper(),
                                 msg='Get the text of show less link')
                outcome.show_summary_toggle.click()
                wait_for_haul(1)
        self.assertNotIn('racingForm: events', actual_url,
                         msg=f'Expected: "racingForm: events" is not present in Actual: "{actual_url}"')
        self.assertNotIn('racingForm: outcome', actual_url,
                         msg=f'Expected: "racingForm: outcome" is not present in Actual: "{actual_url}"')

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
        EXPECTED: * Data in all tabs are displayed from Horse Racing Data Hub
        """
        section_name, section = list(self.markets.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % section_name)
        stake_name, outcome = list(outcomes.items())[0]
        outcome.bet_button.click()
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
        EXPECTED: * Data are displayed from Racing Data Hub
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
        EXPECTED: * Data are displayed from Openbet
        EXPECTED: * In openbet link for event there are 'racingForm: outcome' and 'racingForm: events' parameters (Query String Parameters) and such info is present in the response
        EXPECTED: * Racing Data Hub request ('%-dev1.api.datafabric.dev.%') is absent
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
