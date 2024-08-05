import pytest
import tests
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from datetime import datetime
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create event hub in prod/beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C9726396_Event_hub_Verify_Module_with_Selected_Events_by_Enhanced_Multiples(BaseBetSlipTest):
    """
    TR_ID: C9726396
    NAME: Event hub: Verify Module with Selected Events by Enhanced Multiples
    DESCRIPTION: This test case verifies Events Retrieving by Enhanced Multiples type ID and configured module itself.
    DESCRIPTION: Note: Test Case should cover all supporting Sports (Football for now)
    DESCRIPTION: **Jira tickets:** BMA-5106
    PRECONDITIONS: 1) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 2) For retrieving all Class ID's use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) For retrieving Type ID's for verified Class ID (Sport) use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Class ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) Event Hub is created in CMS > Sport Pages > Event Hub. Module by Enhanced multiples is created in this Event Hub.
    PRECONDITIONS: 5) User is on Homepage > Evernt Hub tab.
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True
    selection_type = "all to win in 90 Mins"
    stake_bet_amounts = 0.1

    def wait_event_disappearance(self) -> bool:
        """
        DESCRIPTION: this is fix for event disappearance
        :return: True if selection name is not in section
        """
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        sections = event_hub_content.accordions_list.items_as_ordered_dict
        if not sections:
            return True
        section = sections.get(self.module_name)
        if not section:
            return True
        return self.selection_name not in section.items_as_ordered_dict.keys()

    def verify_price_format(self, event_id, selection_name, selection_id, fraction=True) -> None:
        """
        DESCRIPTION: Verify data of 'Price/Odds' buttons for verified selection
        :param event_id: event id
        :param selection_id: selection id
        :param selection_name: selection name
        :param fraction: 'Price/Odds' buttons format
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        outcomes_resp = resp[0]['event']['children'][0]['market']['children'][0]
        price_resp = outcomes_resp["outcome"]["children"][0]["price"]
        self.assertTrue(price_resp, msg=f'Price is not found in Siteserve response "{outcomes_resp}"')
        module = self.get_section(section_name=self.module_name)
        bet_button = module.get_bet_button_by_selection_id(selection_id)
        self.assertIsNotNone(bet_button,
                             msg=f'"{selection_name}" selection bet button is not found within module "{self.module_name}""')

        if fraction:
            fraction_price_resp = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}'
            self.assertEqual(bet_button.outcome_price_text, fraction_price_resp,
                             msg=f'Price "{bet_button.outcome_price_text}" is '
                                 f'not the same as in response "{fraction_price_resp}"')
        else:
            decimal_price_resp = f'{price_resp["priceDec"]}'
            self.assertEqual(bet_button.outcome_price_text, decimal_price_resp,
                             msg=f'Price "{bet_button.outcome_price_text}" is '
                                 f'not the same as in response "{decimal_price_resp}"')

    def test_000_preconditions(self):
        """
                PRECONDITIONS: Event Hub is created in CMS > Sport Pages > Event Hub.
        """
        self.__class__.module_id = self.ob_config.football_config.specials.enhanced_multiples.type_id
        start_time = self.get_date_time_formatted_string(hours=3)
        event = self.ob_config.add_football_event_enhanced_multiples(start_time=start_time)
        self.__class__.event_name = f'{event.team1} v {event.team2}'
        self.__class__.selection_name = f'{event.team1}, {event.team2} {self.selection_type}'
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = event.selection_ids
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Enhanced Multiples', id=self.module_id, page_type='eventhub', page_id=index_number,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10, show_expanded=True)['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)

        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.site.wait_content_state(state_name='Homepage')
        self.site.login(username=tests.settings.betplacement_user)

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_expandcollapse_module_from_preconditions_and_verify_header_name_and_selection_name(self):
        """
        DESCRIPTION: Expand/Collapse Module from preconditions and verify Header Name and Selection Name
        EXPECTED: *   Header name is collapsible
        EXPECTED: *   Selection name corresponds to '**name**' attribute on Outcome level OR to <name> set in CMS if name was overridden
        """
        self.site.wait_content_state(state_name='Homepage')
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(event_hub_module,
                        msg=f'Module "{self.module_name}" was not found on "{self.event_hub_tab_name}" tab')
        self.assertTrue(event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')
        self.__class__.module = self.get_section(section_name=self.module_name)
        self.module.collapse()
        self.assertFalse(self.module.is_expanded(expected_result=False),
                         msg=f'Section "{self.module_name}" is expanded')
        self.module.expand()
        self.assertTrue(self.module.is_expanded(), msg=f'Section "{self.module_name}" is not expanded')
        events_filter = self.basic_active_events_filter().add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_NAME, OPERATORS.EQUALS, "|Enhanced Multiples|"))
        self.__class__.resp = self.ss_req.ss_event_for_type(type_id=self.module_id, query_builder=events_filter)
        self.assertTrue(self.resp,
                        msg='There are no outcomes of events with attribute **typeName="Enhanced Multiples****"')
        selections_names = [selection['event']['name'] for selection in self.resp]
        self.assertIn(self.event_name, selections_names,
                      msg=f'Selection name "{self.event_name}" does not correspond to "**name**" attribute '
                          f'on Outcome level: {selections_names}')

    def test_002_verify_outcome_start_time(self):
        """
        DESCRIPTION: Verify Outcome Start Time
        EXPECTED: *   Outcome start time corresponds to **startTime** attribute of event it belongs to
        EXPECTED: *   Outcome Start Time is shown below Sport icon
        EXPECTED: *   For outcomes that occur Today date format is '12 hours' AM/PM (HH:MM AM/PM)
        EXPECTED: *   For outcomes that occur in the future (but NOT over 24 hours) date format is '12 hours' AM/PM (HH:MM AM/PM)
        EXPECTED: *   For outcomes that occur in the future (over 24 hours away) date format is 'DD Month HH:MM' AM/PM
        """
        actual_events = self.module.items_as_ordered_dict
        self.assertTrue(actual_events, msg=f'No events found in "{self.module_name}" module')
        self.__class__.event = next(iter(actual_events.values()))
        self.assertTrue(self.event, msg=f'The first vent not found among events "{actual_events.keys()}"')
        event_time_ui = self.event.event_time
        self.assertTrue(event_time_ui, msg='Outcome Start Time is not shown below Sport icon')
        event_time_resp = self.resp[0]['event']['startTime']
        event_time_resp_converted = \
            datetime.strptime(event_time_resp, self.ob_format_pattern).strftime(
                self.event_card_today_time_format_pattern)
        self.assertTrue(event_time_resp_converted,
                        msg=f'Date format is not in "{self.event_card_today_time_format_pattern}" format')

    def test_003_tapanywhere_on_outcome_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Outcome section (except for price buttons)
        EXPECTED: Outcome section is not clickable
        """
        self.event.click()
        current_tab_name = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(current_tab_name,
                         self.event_hub_tab_name,
                         msg=f'Selected tab is "{current_tab_name}" instead of {self.event_hub_tab_name} tab')

    def test_004_verify_data_of_priceodds_button_for_verified_outcome_in_fraction_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button for verified outcome in fraction format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if **eventStatusCode="S"**
        """
        self.verify_price_format(event_id=self.eventID, selection_name=self.selection_name,
                                 selection_id=self.selection_ids[self.selection_name])

    def test_005_verify_data_of_priceodds_for_verified_outcome_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified outcome in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if **eventStatusCode="S"**
        """
        format_changed = self.site.change_odds_format(odds_format='DECIMAL')
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.site.back_button_click()
        self.site.wait_content_state('Homepage')
        self.site.home.get_module_content(self.event_hub_tab_name)
        self.verify_price_format(event_id=self.eventID, selection_name=self.selection_name,
                                 selection_id=self.selection_ids[self.selection_name],
                                 fraction=False)

    def test_006_add_selection_to_the_betslip_from_module_selector_ribbon(self):
        """
        DESCRIPTION: Add selection to the Betslip from Module Selector Ribbon
        EXPECTED: Bet indicator displays 1.
        """
        module = self.get_section(section_name=self.module_name)
        self.assertTrue(module, msg=f'Section "{self.module_name}" is not found on Featured tab')
        selections = module.items_as_ordered_dict
        self.assertTrue(selections, msg='No selections found')
        selection = selections.get(self.selection_name)
        self.assertTrue(selection, msg=f'"{self.selection_name}" not found in {list(selections.keys())}')
        betslip_counter_value = self.get_betslip_counter_value()
        selection.bet_button.click()
        self.site.wait_for_quick_bet_panel()
        self.site.quick_bet_panel.add_to_betslip_button.click()
        self.site.wait_quick_bet_overlay_to_hide()
        self.verify_betslip_counter_change(expected_value=str(int(betslip_counter_value) + 1))

    def test_007_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertEqual(stake_name, self.selection_name,
                         msg=f'Selection "{self.selection_name}" should be present in betslip')
        self.assertEqual(len(singles_section.items()), 1,
                         msg='Only one selection should be present in betslip')

    def test_008_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by tapping 'Bet Now' button
        EXPECTED: *   Bet is placed succesfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        self.place_single_bet(stake_bet_amounts={self.selection_name: self.stake_bet_amounts})
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_009_repeat_steps_1_7___triggerwait_until_for_verified_event_isstartedtrue_attribute_will_be_set__refresh_page(
            self):
        """
        DESCRIPTION: Repeat steps 1-7 -> Trigger/wait until for verified event '**isStarted="true"**' attribute will be set -> Refresh page
        EXPECTED: All outcomes of verified event are no more shown within 'Featured' tab
        """
        start_time = self.get_date_time_formatted_string(hours=-1)
        self.ob_config.update_event_start_time(eventID=self.eventID, start_time=start_time)
        result = wait_for_result(lambda: self.wait_event_disappearance(),
                                 timeout=30,
                                 poll_interval=3,
                                 name=f'Event "{self.event_name}" is present in section "{self.module_name}"')
        self.assertTrue(result, msg=f'Event "{self.event_name}" is still present')
