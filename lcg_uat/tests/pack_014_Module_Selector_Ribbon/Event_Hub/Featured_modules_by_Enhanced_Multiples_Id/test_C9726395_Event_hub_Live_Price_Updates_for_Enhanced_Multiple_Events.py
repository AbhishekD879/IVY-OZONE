import pytest
from tests.base_test import vtest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl # Live updates cannot be tested on prod and hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C9726395_Event_hub_Live_Price_Updates_for_Enhanced_Multiple_Events(BaseFeaturedTest, BaseBetSlipTest):
    """
    TR_ID: C9726395
    NAME: Event hub: Live Price Updates for Enhanced Multiple Events
    DESCRIPTION: This test case verified live price updates for Enhanced Multiple events which are added to the 'Event Hub' tab (mobile/tablet)
    DESCRIPTION: **NOTE** : Live price updates are NOT applicable to Football Enhanced Multiples Events.
    PRECONDITIONS: 1) To get into SiteServer use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Make sure on 'Event Hub' tab there are a Football Enhanced Multiples Events
    PRECONDITIONS: 3) To verify suspension and price changes check received data using Dev Tools-> Network -> Web Sockets -> ?module=featured&EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCN depend on level of triggering suspension event/market/selection and response with type: PRICE when trigger price changes
    PRECONDITIONS: 4) User is on Event hub tab
    """
    keep_browser_open = True
    selection_type = "all to win in 90 Mins"
    new_price = '1/5'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create football and horse race test events
        """
        module_id = self.ob_config.football_config.specials.enhanced_multiples.type_id
        start_time = self.get_date_time_formatted_string(hours=3)
        self.ob_config.add_football_event_enhanced_multiples(start_time=start_time)
        event = self.ob_config.add_football_event_enhanced_multiples(start_time=start_time)
        self.__class__.event_name = f'{event.team1} v {event.team2}'
        self.__class__.selection_name = f'{event.team1}, {event.team2} {self.selection_type}'
        self.__class__.eventID = event.event_id
        self.__class__.market_id = event.default_market_id
        self.__class__.selection_ids = event.selection_ids
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Enhanced Multiples', id=module_id, page_type='eventhub', page_id=index_number,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10, show_expanded=True)['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.site.wait_content_state(state_name='Homepage')
        event_hub_content = self.site.home.get_module_content(event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(module_name)
        self.assertTrue(event_hub_module,
                        msg=f'Module "{module_name}" was not found on "{event_hub_tab_name}" tab')
        self.assertTrue(event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{module_name}" not expanded')
        self.__class__.module = self.get_section(section_name=module_name)
        self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'Section "{module_name}" is expanded')
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'Section "{module_name}" is not expanded')
        events_filter = self.basic_active_events_filter().add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_NAME, OPERATORS.EQUALS, "|Enhanced Multiples|"))
        resp = self.ss_req.ss_event_for_type(type_id=module_id, query_builder=events_filter)
        self.assertTrue(resp,
                        msg='There are no outcomes of events with attribute **typeName="Enhanced Multiples****"')
        selections_names = [selection['event']['name'] for selection in resp]
        self.assertIn(self.event_name, selections_names,
                      msg=f'Selection name "{self.event_name}" does not correspond to "**name**" attribute '
                          f'on Outcome level: {selections_names}')

    def test_001_trigger_price_change_for_this_outcome_for_this_event(self):
        """
        DESCRIPTION: Trigger price change for this outcome for this event
        EXPECTED: * The 'Price/Odds' button is displayed new prices immediately and it changes the color:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        EXPECTED: * Updates are received in WS
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.selection_name], price=self.new_price)

        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.module.get_bet_button_by_selection_id(selection_id)
            wait_for_result(lambda: bet_button.outcome_price_text == self.new_price,
                                          timeout=20, name='Changed price to be updated')
            self.assertTrue(bet_button.outcome_price_text == self.new_price,
                            msg=f'Selection price is not changed to {self.new_price}')
            self.assertTrue(bet_button.is_displayed(timeout=3, expected_result=True),
                            msg=f'"{selection_name}" selection is not displayed for "{self.event_name}" event')

    def test_002_trigger_the_following_situation_for_the_eventeventstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for the event:
        DESCRIPTION: **eventStatusCode='S'**
        EXPECTED: * Price/Odds buttons of this event immediately start to be displayed as greyed out
        EXPECTED: * Price/Odds buttons are disabled
        EXPECTED: * Updates are received in WS
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.module.get_bet_button_by_selection_id(selection_id)
            self.assertFalse(bet_button.is_enabled(timeout=40, expected_result=False),
                             msg=f'"{selection_name}" selection is not suspended for "{self.event_name}" event')

            self.assertTrue(bet_button.is_displayed(timeout=3, expected_result=True),
                            msg=f'"{selection_name}" selection is not displayed for "{self.event_name}" event')

    def test_003_trigger_the_following_situation_for_the_event_primary_marketmarketstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for the event primary market:
        DESCRIPTION: **marketStatusCode='S'**
        EXPECTED: * Price/Odds buttons of this market immediately start to be displayed as greyed out
        EXPECTED: * Price/Odds buttons are disabled
        EXPECTED: * Updates are received in WS
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.market_id, displayed=True,
                                           active=False)
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.module.get_bet_button_by_selection_id(selection_id)
            self.assertFalse(bet_button.is_enabled(timeout=40, expected_result=False),
                             msg=f'"{selection_name}" selection is not suspended for "{self.event_name}" event')

            self.assertTrue(bet_button.is_displayed(timeout=3, expected_result=True),
                            msg=f'"{selection_name}" selection is not displayed for "{self.event_name}" event')

    def test_004_trigger_the_following_situation_for_the_selection_from_the_eventoutcomestatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for the selection from the event:
        DESCRIPTION: **outcomeStatusCode='S'**
        EXPECTED: * Price/Odds button of this outcome immediately start to C884423be displayed as greyed out
        EXPECTED: * Price/Odds buttons are disabled
        EXPECTED: * Updates are received in WS
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.selection_name], displayed=True,
                                              active=True)
        for selection_name, selection_id in self.selection_ids.items():
            bet_button = self.module.get_bet_button_by_selection_id(selection_id)
            self.assertFalse(bet_button.is_enabled(timeout=40, expected_result=False),
                             msg=f'"{selection_name}" selection is not suspended for "{self.event_name}" event')

            self.assertTrue(bet_button.is_displayed(timeout=3, expected_result=True),
                            msg=f'"{selection_name}" selection is not displayed for "{self.event_name}" event')
