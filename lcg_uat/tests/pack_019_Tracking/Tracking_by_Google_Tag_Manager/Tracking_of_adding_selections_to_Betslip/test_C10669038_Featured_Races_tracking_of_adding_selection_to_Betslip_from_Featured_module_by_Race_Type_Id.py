import pytest
from selenium.common.exceptions import StaleElementReferenceException

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.low
@pytest.mark.betslip
@pytest.mark.google_analytics
@pytest.mark.featured
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.login
@pytest.mark.quick_bet
@vtest
class Test_C10669038_Featured_Races_tracking_of_adding_selection_to_Betslip_from_Featured_module_by_Race_Type_Id(BaseDataLayerTest, BaseRacing, BaseFeaturedTest, BaseBetSlipTest):
    """
    TR_ID: C10669038
    VOL_ID: C13802084
    NAME: Featured Races: tracking of adding selection to Betslip from Featured module by Race Type Id
    DESCRIPTION: This test case verifies GA tracking of adding selection from Featured module by Race Type Id on home page to Betslip
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Betslip GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    """
    keep_browser_open = True

    def click_on_selection(self, selection_number):
        featured_module = self.site.home.get_module_content(self.featured_tab_name)
        try:
            self.__class__.section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        except StaleElementReferenceException:
            self.__class__.section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(self.section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        try:
            events = self.section.items_as_ordered_dict
        except StaleElementReferenceException:
            self.__class__.section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
            events = self.section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found')
        event = events[self.event_name if self.brand != "ladbrokes" else self.event_name.upper()]
        outcomes = event.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in event: "{self.event_name}"')
        selection_name, outcome = list(outcomes.items())[selection_number]
        self.__class__.selection_id = self.selections[selection_name]
        outcome.bet_button.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
        DESCRIPTION: - You should have a Featured module by Race Type Id
        DESCRIPTION: - You should be on Home page > Featured tab in application
        """
        quick_bet_config = self.get_initial_data_system_configuration().get('quickBet', {})
        if not quick_bet_config:
            quick_bet_config = self.cms_config.get_system_configuration_item('quickBet')
        if not quick_bet_config.get('EnableQuickBet'):
            raise CmsClientException('Quick Bet is disabled in CMS')
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.category_id)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.eventID = event['event']['id']
            self.__class__.type_id = event['event']['typeId']
            self.__class__.market_name = self.ob_config.horseracing_config.default_market_name.replace('|', '')
            self.__class__.market = next((market['market'] for market in event['event']['children']
                                         if market['market']['templateMarketName'] == self.market_name), None)
            if self.market is None:
                raise SiteServeException(f'Horseracing events with market {self.market_name} were not found')
            self.__class__.selections = {i['outcome']['name']: i['outcome']['id'] for i in self.market['children']}
            self._logger.info(f'*** Found Event "{self.event_name}" with id {self.eventID}')
        else:
            event = self.ob_config.add_UK_racing_event(number_of_runners=3)
            self.__class__.eventID = event.event_id
            self.__class__.event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
            self.__class__.market_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.\
                market_name.replace('|', '')

            self.__class__.selections = event.selection_ids
            self.__class__.type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id

        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId',
                                                                             show_all_events=True,
                                                                             show_expanded=True,
                                                                             id=self.type_id).get('title', '').upper()
        self.__class__.featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)

    def test_001_mobile__tap_any_odds_button_within_featured_module_by_race_type_id__tap_add_to_betslip_button__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Tap any ODDS button within Featured module by Race Type Id > tap 'ADD TO BETSLIP' button
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
        EXPECTED: dimension65: "featured races"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.click_on_selection(selection_number=0)
        self.site.add_first_selection_from_quick_bet_to_betslip()

        self.verify_ga_tracking_record(brand=self.market_name,
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id,
                                       inplay_status=0, customer_built=0,
                                       location=f'HOME. {self.featured_tab_name}',
                                       module='featured races',
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

    def test_002_mobile__tap_odds_button_on_another_selection_within_featured_module_by_race_type_id__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Tap ODDS button on another selection within Featured module by Race Type Id
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
        EXPECTED: dimension65: "featured races"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.click_on_selection(selection_number=1)
        self.verify_ga_tracking_record(brand=self.market_name,
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id,
                                       inplay_status=0, customer_built=0,
                                       location=f'HOME. {self.featured_tab_name}',
                                       module='featured races',
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

    def test_003_mobile_login_and_go_to_right_menu__settings__disabled_allow_quick_bet_or_go_to_cms__system_configuration__structure__quickbet_disable_quick_bet_functionality__remove_all_selections_from_betslip__tap_odds_button_within_featured_module_by_race_type_id__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: **Mobile**
        DESCRIPTION: - Login and go to Right Menu > Settings > disabled 'Allow Quick Bet' or go to CMS > System Configuration > Structure > quickBet disable Quick Bet functionality
        DESCRIPTION: - Remove all selections from betslip
        DESCRIPTION: - Tap ODDS button within Featured module by Race Type Id
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
        EXPECTED: dimension65: "featured races"
        EXPECTED: name: "<<EVENT_NAME>>"
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>"
        EXPECTED: }}
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.site.toggle_quick_bet()

        self.click_on_selection(selection_number=2)

        self.verify_ga_tracking_record(brand=self.market_name,
                                       category=self.category_id,
                                       event_id=self.eventID,
                                       selection_id=self.selection_id,
                                       inplay_status=0, customer_built=0,
                                       location=f'HOME. {self.featured_tab_name}',
                                       module='featured races',
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
