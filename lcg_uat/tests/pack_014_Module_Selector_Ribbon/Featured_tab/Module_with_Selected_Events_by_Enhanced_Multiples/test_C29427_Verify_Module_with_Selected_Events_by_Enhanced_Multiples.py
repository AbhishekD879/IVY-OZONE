from datetime import datetime

import pytest
from crlat_ob_client.utils.waiters import wait_for_result
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.medium
@pytest.mark.homepage
@pytest.mark.module_ribbon
@pytest.mark.featured
@pytest.mark.enhanced_multiples
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C29427_Verify_Module_with_Selected_Events_by_Enhanced_Multiples(BaseFeaturedTest, BaseBetSlipTest):
    """
    TR_ID: C29427
    NAME: Verify Module with Selected Events by Enhanced Multiples
    DESCRIPTION: This test case verifies Events Retrieving by Enhanced Multiples type ID and configured module itself.
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) For retrieving all Class ID's use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) For retrieving Type ID's for verified Class ID (Sport) use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Class ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4) Go to CMS -> Featured Tab Modules -> Tap 'Create Feature Tab Module' button -> Fill in all required fields with valid data -> Go to 'Select Events by' field and select **Enhanced Multiples** -> Set valid Type ID of Enhanced Multiples -> Tap 'Load Selection'->'Confirm Selection'->'Save Module' button
    PRECONDITIONS: **NOTE: **Sport icon is CMS configurable - https://CMS_ENDPOINT/keystone/sport-categories (check CMS_ENDPOINT via *devlog *function)
    PRECONDITIONS: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True
    selection_type = "all to win in 90 Mins"
    stake_bet_amounts = 0.1

    @classmethod
    def custom_setUp(cls):
        cls._com = Common()
        ob_config = cls.get_ob_config()
        events_filter = cls._com.basic_active_events_filter().add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A'))
        resp = cls.get_ss_config().ss_event_for_type(
            type_id=ob_config.football_config.specials.enhanced_multiples.type_id,
            query_builder=events_filter)
        if resp:
            event_ids = [event['event']['id'] for event in resp]
            for event_id in event_ids:
                ob_config.change_event_state(event_id)

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

        self.get_enhanced_section()
        bet_button = self.section.get_bet_button_by_selection_id(selection_id)
        self.assertIsNotNone(bet_button,
                             msg=f'"{selection_name}" selection bet button is not found within module "{self.module_name}""')

        if fraction:
            fraction_price_resp = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}'
            self.assertEqual(bet_button.outcome_price_text, fraction_price_resp,
                             msg=f'Price "{bet_button.outcome_price_text}" is '
                                 f'not the same as in response "{fraction_price_resp }"')
        else:
            decimal_price_resp = f'{price_resp["priceDec"]}'
            self.assertEqual(bet_button.outcome_price_text, decimal_price_resp,
                             msg=f'Price "{bet_button.outcome_price_text}" is '
                                 f'not the same as in response "{decimal_price_resp}"')

    def wait_event_disappearance(self) -> bool:
        """
        DESCRIPTION: this is fix for event disappearance
        :return: True if selection name is not in section
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        featured_name = self.get_ribbon_tab_name(
            self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured) if self.device_type == 'mobile' \
            else vec.sb_desktop.FEATURED_MODULE_NAME
        module = self.site.home.get_module_content(module_name=featured_name)
        sections = module.accordions_list.items_as_ordered_dict
        if not sections:
            return True
        section = sections.get(self.module_name)
        if not section:
            return True
        return self.selection_name not in section.items_as_ordered_dict.keys()

    def get_enhanced_section(self) -> None:
        """
        DESCRIPTION: Get enhanced multiples section
        """
        featured_module = self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        featured_module.scroll_to()
        self.__class__.section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(self.section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create football enhanced multiples events
        DESCRIPTION: Create Featured module in CMS by Type ID of Enhanced Multiples
        DESCRIPTION: Login
        """
        self.__class__.module_id = self.ob_config.football_config.specials.enhanced_multiples.type_id
        start_time = self.get_date_time_formatted_string(hours=3)
        event_params = self.ob_config.add_football_event_enhanced_multiples(start_time=start_time)
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.selection_name = f'{event_params.team1}, {event_params.team2} {self.selection_type}'
        self.__class__.event_id, self.__class__.selection_ids1 = event_params.event_id, event_params.selection_ids

        event_params2 = self.ob_config.add_football_event_enhanced_multiples()
        self.__class__.event_name2 = f'{event_params2.team1} v {event_params2.team2}'
        self.__class__.selection_name2 = f'{event_params2.team1}, {event_params2.team2} {self.selection_type}'
        self.__class__.event_id2, self.__class__.selection_ids2 = event_params2.event_id, event_params2.selection_ids

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Enhanced Multiples', id=self.module_id, show_expanded=True)['title'].upper()

        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.site.login(username=tests.settings.betplacement_user, password=tests.settings.default_password,
                        async_close_dialogs=False, timeout_close_dialogs=5)

    def test_001_load_oxygen_application_and_verify_selection_within_created_module(self):
        """
        DESCRIPTION: Load Oxygen application and verify selection within created Module
        EXPECTED: Created module with Enhanced Multiples outcomes which have same TypeId is displayed:
        EXPECTED: *   Just outcomes of events with attribute **typeName="Enhanced Multiples****" **are shown
        EXPECTED: *   Just outcomes of events with **NO isStarted="true"** attribute are shown
        EXPECTED: *   **Each outcome is shown separately **(of events with more then one market and more than one outcome, of  events one market and more than one outcome, of  events with one market and one outcome)
        """
        self.get_enhanced_section()
        events_filter = self.basic_active_events_filter().add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.TYPE_NAME, OPERATORS.EQUALS, "|Enhanced Multiples|"))
        self.__class__.resp = self.ss_req.ss_event_for_type(type_id=self.module_id, query_builder=events_filter)
        self.assertTrue(self.resp,
                        msg='There are no outcomes of events with attribute **typeName="Enhanced Multiples****"')

        events_filter2 = self.basic_active_events_filter().add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.EQUALS, OPERATORS.IS_TRUE))
        resp2 = self.ss_req.ss_event_for_type(type_id=self.module_id, query_builder=events_filter2)
        events = [event['event']['name'] for event in resp2]
        self.assertNotIn(self.event_name, events, msg=f'Outcomes of {self.event_name} event with'
                                                      f' **isStarted="true"** attribute is shown')
        self.assertNotIn(self.event_name2, events, msg=f'Outcomes of {self.event_name2} event with '
                                                       f'**isStarted="true"** attribute is shown')

    def test_002_expand_collapse_module_and_verify_header_name_and_selection_name(self):
        """
        DESCRIPTION: Expand/Collapse Module and verify Header Name and Selection Name
        EXPECTED: *   Header is collapsible
        EXPECTED: *   Selection name corresponds to '**name**' attribute on Outcome level OR to <name> set in CMS if name was overridden
        """
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(expected_result=False), msg=f'Section "{self.module_name}" is expanded')
        self.section.expand()
        self.assertTrue(self.section.is_expanded(), msg=f'Section "{self.module_name}" is not expanded')

        selections_names = [selection['event']['name'] for selection in self.resp]
        self.assertIn(self.event_name2, selections_names,
                      msg=f'Selection name "{self.event_name2}" does not correspond to "**name**" attribute '
                          f'on Outcome level: {selections_names}')
        self.assertIn(self.event_name, selections_names,
                      msg=f'Selection name "{self.event_name}" does not correspond to "**name**" attribute '
                          f'on Outcome level: {selections_names}')

    def test_003_verify_outcome_start_time(self):
        """
        DESCRIPTION: Verify Outcome Start Time
        EXPECTED: *   Outcome start time corresponds to **startTime** attribute of event it belongs to
        EXPECTED: *   Outcome Start Time is shown below Sport icon
        EXPECTED: *   For outcomes that occur Today date format is '12 hours' AM/PM (HH:MM AM/PM)
        EXPECTED: *   For outcomes that occur in the future (but NOT over 24 hours) date format is '12 hours' AM/PM (HH:MM AM/PM)
        EXPECTED: *   For outcomes that occur in the future (over 24 hours away) date format is 'DD Month HH:MM' AM/PM
        """
        actual_events = self.section.items_as_ordered_dict
        self.assertTrue(actual_events, msg=f'No events found in "{self.module_name}" module')
        self.__class__.event = next(iter(actual_events.values()))
        self.assertTrue(self.event, msg=f'The first vent not found among events "{actual_events.keys()}"')
        event_time_ui = self.event.event_time
        self.assertTrue(event_time_ui, msg='Outcome Start Time is not shown below Sport icon')
        event_time_resp = self.resp[0]['event']['startTime']
        event_time_resp_converted = \
            datetime.strptime(event_time_resp, self.ob_format_pattern).strftime(self.event_card_today_time_format_pattern)
        self.assertTrue(event_time_resp_converted, msg=f'Date format is not in "{self.event_card_today_time_format_pattern}" format')

    def test_004_tap_anywhere_on_outcome_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Outcome section (except for price buttons)
        EXPECTED: Outcome section is not clickable
        """
        self.event.click()
        if self.device_type == 'mobile':
            current_tab_name = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEqual(current_tab_name, self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured),
                             msg=f'Selected tab is "{current_tab_name}" instead of {self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)} tab')
        else:
            self.site.wait_content_state('HomePage')

    def test_005_verify_data_of_price_odds_button_for_verified_outcome_in_fraction_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds button for verified outcome in fraction format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if **eventStatusCode="S"**
        """
        self.ob_config.change_event_state(event_id=self.event_id, displayed=True, active=False)
        self.verify_price_format(event_id=self.event_id, selection_name=self.selection_name,
                                 selection_id=self.selection_ids1[self.selection_name])
        self.verify_price_format(event_id=self.event_id2, selection_name=self.selection_name2,
                                 selection_id=self.selection_ids2[self.selection_name2])

    def test_006_verify_data_of_priceodds_for_verified_outcome_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds for verified outcome in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if **eventStatusCode="S"**
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        if self.brand == 'bma':
            self.navigate_to_page(name='')
            self.site.wait_content_state(state_name='Home')
        else:
            if self.device_type == 'mobile':
                self.site.settings.back_button_click()
                self.site.wait_content_state(state_name='Home')
                self.site.right_menu.close_icon.click()

        self.verify_price_format(event_id=self.event_id, selection_name=self.selection_name,
                                 selection_id=self.selection_ids1[self.selection_name],
                                 fraction=False)
        self.verify_price_format(event_id=self.event_id2, selection_name=self.selection_name2,
                                 selection_id=self.selection_ids2[self.selection_name2],
                                 fraction=False)

    def test_007_add_selection_to_the_betslip_from_module_selector_ribbon(self):
        """
        DESCRIPTION: Add selection to the Betslip from Module Selector Ribbon
        EXPECTED: Bet indicator displays 1.
        """
        featured_name = self.get_ribbon_tab_name(
            internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured) if self.device_type == 'mobile' \
            else vec.sb_desktop.FEATURED_MODULE_NAME
        module = self.site.home.get_module_content(module_name=featured_name)
        sections = module.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No section was found in module')
        section = sections.get(self.module_name)
        self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on Featured tab')
        selections = section.items_as_ordered_dict
        self.assertTrue(selections, msg='No selections found')
        selection = selections.get(self.selection_name2)
        self.assertTrue(selection, msg=f'"{self.selection_name2}" not found in {list(selections.keys())}')
        selection.bet_button.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()

        self.verify_betslip_counter_change(expected_value=1)

    def test_008_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: *   Selection is added to the Betslip
        EXPECTED: *   All information is displayed correctly
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertEqual(stake_name, self.selection_name2,
                         msg=f'Selection "{self.selection_name2}" should be present in betslip')
        self.assertEqual(len(singles_section.items()), 1,
                         msg='Only one selection should be present in betslip')

    def test_009_place_a_bet_by_tapping_bet_now_button(self):
        """
        DESCRIPTION: Place a bet by tapping 'Bet Now' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   User's balance is decremented by entered stake
        """
        self.place_single_bet(stake_bet_amounts={self.selection_name2: self.stake_bet_amounts})
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_010_repeat_steps_1_7_trigger_wait_until_for_verified_event_isstartedtrue_attribute_will_be_set__refresh_page(self):
        """
        DESCRIPTION: Repeat steps 1-7 -> Trigger/wait until for verified event '**isStarted="true"**' attribute will be set -> Refresh page
        EXPECTED: All outcomes of verified event are no more shown within 'Featured' tab
        """
        start_time = self.get_date_time_formatted_string(hours=-1)
        self.ob_config.update_event_start_time(eventID=self.event_id, start_time=start_time)
        result = wait_for_result(lambda: self.wait_event_disappearance(),
                                 timeout=30,
                                 poll_interval=3,
                                 name=f'Event "{self.event_name}" is present in section "{self.module_name}"')
        self.assertTrue(result, msg=f'Event "{self.event_name}" is still present')
