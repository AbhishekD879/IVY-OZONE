import pytest
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@pytest.mark.football
@pytest.mark.google_analytics
@pytest.mark.event_details
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.login
@pytest.mark.quick_bet
@vtest
class Test_C10669034_Event_Details_Page_tracking_of_adding_selection_to_Betslip_on_sport_event_details_page(BaseDataLayerTest, BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C10669034
    VOL_ID: C13686102
    NAME: Event Details Page: tracking of adding selection to Betslip on <sport> event details page
    DESCRIPTION: This test case verifies GA tracking of adding selection from <sport> event details page to Betslip
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Betslip GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    """
    keep_browser_open = True

    def click_on_selection(self, selection_name):
        bet_button = self.get_selection_bet_button(selection_name=selection_name, market_name=self.expected_market_name)
        bet_button.click()
        self.assertTrue(bet_button.is_selected(timeout=2), msg='Outcome button is not highlighted in green')

    def test_000_preconditions(self):
        """
        DESCRIPTION: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
        DESCRIPTION: - You should be on <sport> event details page in application
        """
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')

        self.__class__.category_id = self.ob_config.backend.ti.football.category_id
        if tests.settings.backend_env == 'prod':
            additional_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_LIVE_NOW_EVENT, OPERATORS.IS_FALSE)
            event = self.get_active_events_for_category(category_id=self.category_id,
                                                        additional_filters=additional_filter)[0]
            self.__class__.eventID = event['event']['id']
            self.__class__.event_name = normalize_name(event['event']['name'])
            market = next((market['market'] for market in event['event']['children']
                           if 'Match Betting' == market['market']['templateMarketName']), {})
            outcomes = market['children']

            market_name = market['name']

            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_name1, self.__class__.selection_name2, self.__class__.selection_name3 = \
                list(selection_ids.keys())[:3]
            self.__class__.selection_id1, self.__class__.selection_id2, self.__class__.selection_id3 = \
                list(selection_ids.values())[:3]
            self.__class__.type_id = event['event']['typeId']
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
            self.__class__.eventID = event_params.event_id
            self.__class__.selection_name1, self.__class__.selection_name2, self.__class__.selection_name3 = \
                list(event_params.selection_ids.keys())[:3]
            self.__class__.selection_id1, self.__class__.selection_id2, self.__class__.selection_id3 = \
                list(event_params.selection_ids.values())[:3]
            self.__class__.type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
            market_name = normalize_name(
                self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)

        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

    def test_001_mobile__tap_any_odds_button__tap_add_to_betslip_button__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Tap any ODDS button > tap 'ADD TO BETSLIP' button
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
        EXPECTED: dimension64: "<<LOCATION>>"
        EXPECTED: dimension65: "edp"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.__class__.location = self.site.sport_event_details.markets_tabs_list.current
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.selection_name1,
                                                           market_name=self.expected_market_name)
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.verify_ga_tracking_record(brand=self.expected_market_name.title(),
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id1,
                                       inplay_status=0,
                                       customer_built=0,
                                       location=self.site.sport_event_details.markets_tabs_list.current,
                                       module='edp',
                                       name=self.event_name,
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
                                       dimension166='normal',
                                       dimension177='No show',
                                       dimension180='normal',
                                       metric1=0,
                                       normalize_name=True)

    def test_002_mobile__tap_any_another_odds_button__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Tap any another ODDS button
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
        EXPECTED: dimension64: "<<LOCATION>>"
        EXPECTED: dimension65: "edp"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.click_on_selection(selection_name=self.selection_name2)
        self.verify_ga_tracking_record(brand=self.expected_market_name.title(),
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id2,
                                       inplay_status=0,
                                       customer_built=0,
                                       location=self.site.sport_event_details.markets_tabs_list.current,
                                       module='edp',
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
                                       dimension177='No show',
                                       dimension180='normal',
                                       quantity=1,
                                       normalize_name=True)

    def test_003_mobile_login_and_go_to_right_menu__settings__disabled_allow_quick_bet_or_go_to_cms__system_configuration__structure__quickbet_disable_quick_bet_functionality__remove_all_selections_from_betslip__tap_any_odds_button__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Login and go to Right Menu > Settings > disabled 'Allow Quick Bet' or go to CMS > System Configuration > Structure > quickBet disable Quick Bet functionality
        DESCRIPTION: - Remove all selections from betslip
        DESCRIPTION: - Tap any ODDS button
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
        EXPECTED: dimension64: "<<LOCATION>>"
        EXPECTED: dimension65: "edp"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.navigate_to_page('/')
        self.site.login(username=tests.settings.betplacement_user)
        self.site.toggle_quick_bet()
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

        # Remove all selections from betslip
        self.site.open_betslip()
        self.clear_betslip()
        self.site.wait_content_state(state_name='EventDetails', timeout=5)

        self.click_on_selection(selection_name=self.selection_name3)
        self.verify_ga_tracking_record(brand=self.expected_market_name.title(),
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id3,
                                       inplay_status=0,
                                       customer_built=0,
                                       location=self.site.sport_event_details.markets_tabs_list.current,
                                       module='edp',
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
                                       dimension177='No show',
                                       dimension180='normal',
                                       quantity=1,
                                       normalize_name=True)
