import pytest
from crlat_siteserve_client.siteserve_client import SiteServeRequests

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import get_in_play_module_from_ws
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@pytest.mark.featured
@pytest.mark.google_analytics
@pytest.mark.event_details
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.in_play
@pytest.mark.login
@pytest.mark.quick_bet
@vtest
class Test_C10669040_In_play_Module_tracking_of_adding_selection_to_Betslip_from_Featured_In_play_module(BaseDataLayerTest, BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C10669040
    VOL_ID: C14050295
    NAME: In-play Module: tracking of adding selection to Betslip from Featured In-play module
    DESCRIPTION: This test case verifies GA tracking of adding selection from Featured In-play module on home page to Betslip
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Betslip GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    PRECONDITIONS: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
    PRECONDITIONS: - You should have a Featured In-play module on home page
    PRECONDITIONS: - You should be on Home page > Featured tab in application
    """
    keep_browser_open = True

    def get_ui_event(self):
        inplay_module_items = self.site.home.tab_content.in_play_module.items_as_ordered_dict
        self.assertTrue(inplay_module_items, msg='Can not find any module items')
        self.assertIn(self.sport_name, inplay_module_items.keys(), msg=f'{self.sport_name} container is not displayed')
        test_sport = inplay_module_items.get(self.sport_name)
        self.assertTrue(test_sport, msg=f'Can not find  "{self.sport_name}" in {inplay_module_items.keys()}')
        events = test_sport.items_as_ordered_dict
        self.assertTrue(events, msg='No event cards found on Football page')
        event = events.get(normalize_name(self.event_name), None)
        self.assertTrue(event, msg=f'Event with name "{normalize_name(self.event_name)}" not found')
        return event

    def click_on_selection(self, event, selection_name):
        bet_buttons = event.get_available_prices()
        self.assertTrue(bet_buttons, msg='No selections found')
        self.assertIn(selection_name, bet_buttons.keys(), msg=f'"{selection_name}" not found in "{bet_buttons.keys()}"')
        bet_button = bet_buttons.get(selection_name)
        bet_button.click()
        self.assertTrue(bet_button.is_selected(timeout=1), msg='Outcome button is not highlighted in green')

    def test_000_preconditions(self):
        """
        DESCRIPTION: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
        DESCRIPTION: - You should have a Featured In-play module on home page
        DESCRIPTION: - You should be on Home page > Featured tab in application
        """
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')

        inplay_module = self.get_initial_data_system_configuration().get('Inplay Module', {})
        if not inplay_module:
            inplay_module = self.cms_config.get_system_configuration_item('Inplay Module')
        if not inplay_module.get('enabled'):
            raise CmsClientException('"Inplay Module" module is disabled in system config')

        self.site.wait_content_state(state_name='Homepage')

        self.__class__.sport_name = 'Football' if self.brand != 'ladbrokes' else 'FOOTBALL'
        self.__class__.category_id = self.ob_config.football_config.category_id
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.category_id)
        try:
            in_play_module = get_in_play_module_from_ws()
            self.assertTrue(in_play_module, msg='There is no In-play module in ws')
            in_play_module_data = in_play_module.get('data')
            flatten_ids = next((sport_segment['eventsIds'] for sport_segment in in_play_module_data if
                                sport_segment['categoryName'] == 'Football'), None)
            self._logger.info(f'*** Found event ids in In-Play module: {flatten_ids}')
        except KeyError:
            flatten_ids = None

        if flatten_ids:
            for event_id in flatten_ids:
                event = ss_req.ss_event_to_outcome_for_event(event_id=event_id,
                                                             query_builder=self.ss_query_builder)
                try:
                    result = event[0]['event']['children'][0]['market']['children'][0]['outcome'].get('result', None)
                except KeyError:
                    continue
                is_active = event[0]['event'].get('isActive', None)
                if result == "-" or not result and is_active == 'true':
                    self.__class__.eventID = event_id
                    break
                continue
            self.__class__.event_name = normalize_name(event[0]['event']['name'])
            self.__class__.type_id = event[0]['event']['typeId']
            expected_market_name, outcomes = next(((market['market']['name'], market['market']['children'])
                                                  for market in event[0]['event']['children'] if
                                                  market['market'].get('children')), (None, None))
            if not outcomes:
                raise SiteServeException('There are no available outcomes')

            self.__class__.market_name = expected_market_name
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                          outcome['outcome'].get('outcomeMeaningMinorCode') and
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            if not team1:
                raise SiteServeException('No Home team present is SS response')
            team2 = next((outcome['outcome']['name'] for outcome in outcomes if
                          outcome['outcome']['outcomeMeaningMinorCode'] == 'A'), None)
            if not team2:
                raise SiteServeException('No Away team present is SS response')
            self.__class__.selection_id1 = selection_ids[team1]
            self.__class__.selection_id2 = selection_ids[team2]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.eventID = event.event_id
            self.__class__.event_name = f'{event.team1} v {event.team2}'
            self.__class__.type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
            self.__class__.market_name = self.expected_market_sections.match_result
            selection_ids = event.selection_ids
            self.__class__.selection_id1, self.__class__.selection_id2, _ = \
                list(selection_ids.values())[:2]

    def test_001_mobile_tap_odds_button_within_featured_in_play_module_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Tap ODDS button within Featured In-play module > tap 'ADD TO BETSLIP' button
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "add to betslip"
        EXPECTED: eventCategory: "quickbet"
        EXPECTED: eventLabel: "success"
        EXPECTED: ecommerce.add.products{
        EXPECTED: brand: "<<EVENT_MARKET>>"
        EXPECTED: category: "<<OPENBET_SPORT_CATEGORY_ID>>"
        EXPECTED: dimension60: "<<EVENT_ID>>"
        EXPECTED: dimension61: "<<SELECTION_ID>>"
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>"
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>"
        EXPECTED: dimension64: "HOME. FEATURED"
        EXPECTED: dimension65: "in-play module"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.__class__.featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        event = self.get_ui_event()
        self.click_on_selection(event=event, selection_name=event.first_player)

        self.site.add_first_selection_from_quick_bet_to_betslip()

        self.verify_betslip_counter_change(expected_value=1)

        self.verify_ga_tracking_record(brand=self.market_name.title(),
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id1,
                                       inplay_status=1, customer_built=0,
                                       location=f'HOME. {self.featured_tab_name}',
                                       module='in-play module',
                                       name=normalize_name(self.event_name),
                                       variant=self.type_id,
                                       event='trackEvent',
                                       event_action='add to betslip',
                                       event_category='quickbet',
                                       event_label='success',
                                       stream_active=False,
                                       stream_ID=None,
                                       dimension86=0,
                                       dimension87=0,
                                       dimension88=None,
                                       metric1=0)

    def test_002_tap_any_another_odds_button_within_featured_in_play_module(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Tap any another ODDS button within Featured In-play module
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "add to betslip"
        EXPECTED: eventCategory: "betslip"
        EXPECTED: eventLabel: "success"
        EXPECTED: ecommerce.add.products{
        EXPECTED: brand: "<<EVENT_MARKET>>"
        EXPECTED: category: "<<OPENBET_SPORT_CATEGORY_ID>>"
        EXPECTED: dimension60: "<<EVENT_ID>>"
        EXPECTED: dimension61: "<<SELECTION_ID>>"
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>"
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>"
        EXPECTED: dimension64: "HOME. FEATURED"
        EXPECTED: dimension65: "in-play module"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        event = self.get_ui_event()
        self.click_on_selection(event, event.second_player)

        self.verify_ga_tracking_record(brand=self.market_name.title(),
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id2,
                                       inplay_status=1, customer_built=0,
                                       location=f'HOME. {self.featured_tab_name}',
                                       module='in-play module',
                                       name=self.event_name,
                                       variant=self.type_id,
                                       event='trackEvent',
                                       event_action='add to betslip',
                                       event_category='betslip',
                                       event_label='success',
                                       stream_active=False,
                                       stream_ID=None,
                                       dimension86=0,
                                       dimension87=0,
                                       dimension88=None,
                                       quantity=1)

    def test_003_login_and_go_to_right_menu_settings_disabled_allow_quick_bet(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Login and go to Right Menu > Settings > disabled 'Allow Quick Bet' or go to CMS > System Configuration > Structure > quickBet disable Quick Bet functionality
        DESCRIPTION: - Remove all selections from betslip
        DESCRIPTION: - Tap ODDS button within Featured In-play module
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push{
        EXPECTED: event: "trackEvent"
        EXPECTED: eventAction: "add to betslip"
        EXPECTED: eventCategory: "betslip"
        EXPECTED: eventLabel: "success"
        EXPECTED: ecommerce.add.products{
        EXPECTED: brand: "<<EVENT_MARKET>>"
        EXPECTED: category: "<<OPENBET_SPORT_CATEGORY_ID>>"
        EXPECTED: dimension60: "<<EVENT_ID>>"
        EXPECTED: dimension61: "<<SELECTION_ID>>"
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>"
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>"
        EXPECTED: dimension64: "HOME. FEATURED"
        EXPECTED: dimension65: "in-play module"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.site.login(username=tests.settings.betplacement_user, timeout=10)
        self.site.toggle_quick_bet()

        # Remove all selections from betslip
        self.site.open_betslip()
        self.clear_betslip()

        event = self.get_ui_event()
        self.click_on_selection(event, event.first_player)

        self.verify_ga_tracking_record(brand=self.market_name.title(),
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id1,
                                       inplay_status=1, customer_built=0,
                                       location=f'HOME. {self.featured_tab_name}',
                                       module='in-play module',
                                       name=self.event_name,
                                       variant=self.type_id,
                                       event='trackEvent',
                                       event_action='add to betslip',
                                       event_category='betslip',
                                       event_label='success',
                                       stream_active=False,
                                       stream_ID=None,
                                       dimension86=0,
                                       dimension87=0,
                                       dimension88=None,
                                       quantity=1)
