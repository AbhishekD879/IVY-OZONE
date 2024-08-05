import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot add featured modules on prod
@pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@pytest.mark.google_analytics
@pytest.mark.featured
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.login
@pytest.mark.quick_bet
@vtest
class Test_C10669039_Featured_Bet_tracking_of_adding_selection_to_Betslip_from_Featured_module_by_Type_Id(BaseDataLayerTest, BaseFeaturedTest, BaseBetSlipTest):
    """
    TR_ID: C10669039
    VOL_ID: C13808809
    NAME: Featured Bet: tracking of adding selection to Betslip from Featured module by Type Id
    DESCRIPTION: This test case verifies GA tracking of adding selection from Featured module by Type Id on home page to Betslip
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Betslip GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    """
    keep_browser_open = True

    def click_on_selection(self, selection_name):
        featured_module = self.site.home.get_module_content(self.featured_tab_name)
        featured_module.scroll_to()
        self.__class__.section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_name.upper())
        self.assertTrue(self.section, msg=f'Section "{self.module_name.upper()}" is not found on FEATURED tab')
        events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found')
        event = events.get(self.event_name)
        self.assertTrue(event, msg=f'Event "{self.event_name}" is not found in "{events.keys()}"')

        bet_buttons = event.template.get_available_prices()
        self.assertTrue(bet_buttons, msg='No selections found')
        bet_button = bet_buttons.get(selection_name)

        bet_button.click()
        self.assertTrue(bet_button.is_selected(timeout=1), msg='Outcome button is not highlighted in green')

    def test_000_preconditions(self):
        """
        DESCRIPTION: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
        DESCRIPTION: - You should have a Featured module by Type Id
        DESCRIPTION: - You should be on Home page > Featured tab in application
        """
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category()[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            self.__class__.team2 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'A'), None)
            if not self.team1:
                raise SiteServeException('No Home team found')

            if not self.team2:
                raise SiteServeException('No Away team found')

            self.__class__.type_id = event['event']['typeId']
            self.__class__.market_name = next(((market['market']['name']) for market in event['event']['children']
                                               if market['market'].get('children') and
                                               market['market']['templateMarketName'] in ['Match Result', 'Match Betting']), None)
        else:
            event_params = self.ob_config.add_football_event_to_featured_autotest_league()
            self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
            self.__class__.eventID = event_params.event_id
            self.__class__.selection_ids = event_params.selection_ids
            self.__class__.type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id
            self.__class__.market_name = self.expected_market_sections.match_result

        self.__class__.selection_name1, self.__class__.selection_name2, self.__class__.selection_name3 = \
            list(self.selection_ids.keys())[:3]
        self.__class__.selection_id1, self.__class__.selection_id2, self.__class__.selection_id3 = \
            list(self.selection_ids.values())[:3]

        self.__class__.category_id = self.ob_config.backend.ti.football.category_id

        self.__class__.featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', show_all_events=True, show_expanded=True, id=self.type_id)['title']

        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name.upper())
        self.__class__.ga_module_name = self.module_name if self.brand != 'ladbrokes' else 'featured bet'

    def test_001_mobile__tap_odds_button_within_featured_module_by_type_id__tap_add_to_betslip_button__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Tap ODDS button within Featured module by Type Id > tap 'ADD TO BETSLIP' button
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
        EXPECTED: dimension65: "featured bet"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.click_on_selection(selection_name=self.selection_name1)

        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.verify_ga_tracking_record(brand=self.market_name.title(),
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id1,
                                       inplay_status=0, customer_built=0,
                                       location=f'HOME. {self.featured_tab_name}',
                                       module='featured bet',
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
                                       metric1=0)

    def test_002_mobile__tap_any_another_odds_button_within_featured_module_by_type_id__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Tap any another ODDS button within Featured module by Type Id
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
        EXPECTED: dimension65: "featured bet"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.click_on_selection(selection_name=self.selection_name2)
        self.verify_ga_tracking_record(brand=self.market_name.title(),
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id2,
                                       inplay_status=0, customer_built=0,
                                       location=f'HOME. {self.featured_tab_name}',
                                       module='featured bet',
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

    def test_003_mobile_login_and_go_to_right_menu__settings__disabled_allow_quick_bet_or_go_to_cms__system_configuration__structure__quickbet_disable_quick_bet_functionality__remove_all_selections_from_betslip__tap_odds_button_within_featured_module_by_type_id__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Login and go to Right Menu > Settings > disabled 'Allow Quick Bet' or go to CMS > System Configuration > Structure > quickBet disable Quick Bet functionality
        DESCRIPTION: - Remove all selections from betslip
        DESCRIPTION: - Tap ODDS button within Featured module by Type Id
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
        EXPECTED: dimension65: "featured bet"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """

        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.site.toggle_quick_bet()
        # Remove all selections from betslip
        self.site.header.bet_slip_counter.click()
        self.clear_betslip()

        self.click_on_selection(selection_name=self.selection_name3)

        self.verify_ga_tracking_record(brand=self.market_name.title(),
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id3,
                                       inplay_status=0, customer_built=0,
                                       location=f'HOME. {self.featured_tab_name}',
                                       module='featured bet',
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
