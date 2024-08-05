import pytest
import tests
from voltron.environments import constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@pytest.mark.google_analytics
@pytest.mark.event_details
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.safari
@pytest.mark.login
@pytest.mark.quick_bet
@pytest.mark.reg156_fix
@vtest
class Test_C10669035_Race_Card_tracking_of_adding_selection_to_Betslip_on_race_details_page(BaseDataLayerTest, BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C10669035
    VOL_ID: C13815464
    NAME: Race Card: tracking of adding selection to Betslip on race details page
    DESCRIPTION: This test case verifies GA tracking of adding selection from <race> event details page to Betslip
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Betslip GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    """
    keep_browser_open = True

    def click_on_selection(self, selection_name):
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No one outcome was found in section: "%s"' % section_name)
        if selection_name:
            self.assertIn(selection_name, outcomes.keys())
        outcome = outcomes[selection_name] if selection_name else list(outcomes.values())[0]
        outcome.bet_button.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
        DESCRIPTION: - You should be on <race> event details page in application
        """
        quick_bet = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet:
            quick_bet = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')

        self.__class__.category_id = self.ob_config.horseracing_config.category_id
        if tests.settings.backend_env == 'prod':
            additional_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_LIVE_NOW_EVENT, OPERATORS.IS_FALSE)
            event = self.get_active_events_for_category(category_id=self.category_id,
                                                        additional_filters=additional_filter)[0]
            self.__class__.eventID = event['event']['id']
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.time = event['event']['name'].split()[0]
            market = next(market['market'] for market in event['event']['children'])
            outcomes = market['children']

            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            if not selection_ids:
                raise SiteServeException(f'Outcomes list is empty for event "{self.event_name}""')
            self.__class__.selection_name1, self.__class__.selection_name2, self.__class__.selection_name3 = \
                list(selection_ids.keys())[:3]
            self.__class__.selection_id1, self.__class__.selection_id2, self.__class__.selection_id3 = \
                list(selection_ids.values())[:3]
            self.__class__.type_id = event['event']['typeId']
            self.__class__.market_name = market['name']
        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=3)
            self.__class__.time = event.event_off_time
            self.__class__.eventID = event.event_id
            self.__class__.event_name = '%s %s' % (event.event_off_time, self.horseracing_autotest_uk_name_pattern)
            self.__class__.market_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.market_name. \
                replace('|', '')

            self.__class__.selection_name1, self.__class__.selection_name2, self.__class__.selection_name3 = \
                list(event.selection_ids.keys())[:3]
            self.__class__.selection_id1, self.__class__.selection_id2, self.__class__.selection_id3 = \
                list(event.selection_ids.values())[:3]
            self.__class__.type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        self.assertTrue(tab_opened, msg='Win or Each way tab is not opened')

    def test_001_tap_any_odds_button_tap_add_to_betslip_button(self):
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
        EXPECTED: dimension65: "racecard"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.add_selection_to_quick_bet(outcome_name=self.selection_name1)
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.verify_ga_tracking_record(brand=self.market_name,
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id1,
                                       inplay_status=0, customer_built=0,
                                       location=self.time,
                                       module='racecard',
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
                                       dimension166="normal",
                                       dimension177="No show",
                                       dimension180="normal",
                                       metric1=0)

    def test_002_tap_any_another_odds_button(self):
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
        EXPECTED: dimension65: "racecard"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.click_on_selection(selection_name=self.selection_name2)
        self.verify_ga_tracking_record(brand=self.market_name,
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id2,
                                       inplay_status=0, customer_built=0,
                                       location=self.time,
                                       module='racecard',
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
                                       dimension177="No show",
                                       dimension180="normal",
                                       quantity=1)

    def test_003_login_and_go_to_right_menu_settings_disabled_allow_quick_bet(self):
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
        EXPECTED: dimension65: "racecard"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.site.toggle_quick_bet()

        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
        self.assertTrue(tab_opened, msg='Win or Each way tab is not opened')
        # Remove all selections from betslip
        self.site.header.bet_slip_counter.click()
        self.clear_betslip()

        self.click_on_selection(selection_name=self.selection_name3)
        self.verify_ga_tracking_record(brand=self.market_name,
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id3,
                                       inplay_status=0, customer_built=0,
                                       location=self.time,
                                       module='racecard',
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
                                       dimension177="No show",
                                       dimension180="normal",
                                       quantity=1)
