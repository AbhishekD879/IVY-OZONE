import pytest
from fractions import Fraction
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot configure featured tab events in prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C11386067_Event_hub_Verify_module_created_by_market_ID_of_Outright_Sport_event(Common):
    """
    TR_ID: C11386067
    NAME: Event hub: Verify module created by market ID of Outright <Sport> event
    DESCRIPTION: This test case verifies featured module created by market ID of Outright <Sport> event
    PRECONDITIONS: 1. CMS, TI:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 2. Outright event created in TI
    PRECONDITIONS: 3. Event Hub is created and configured to be displayed on FE in CMS >  Sport Pages > Event Hub
    PRECONDITIONS: 4. Featured module by Market Id is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
    PRECONDITIONS: 5. User is on Homepage > Event Hub tab
    """
    keep_browser_open = True
    prices = ['1/3', '4/6', '3/4']

    def test_000_preconditions(self):
        event = self.ob_config.add_american_football_outright_event_to_autotest_league(selections_number=3)
        self.__class__.event_name, event_time = event.ss_response['event']['name'], event.ss_response['event'][
            'startTime']
        self.__class__.event_time_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                                         date_time_str=event_time,
                                                                         ui_format_pattern=self.event_card_today_time_format_pattern,
                                                                         future_datetime_format=self.event_card_coupon_and_competition_future_time_format_pattern,
                                                                         ss_data=True).split(" ")[0]
        market_id = event.default_market_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Market',
                                                              id=market_id,
                                                              page_type='eventhub',
                                                              page_id=index_number,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10)
        self.__class__.module_name = module_data['title'].upper()

        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

        result = wait_for_result(lambda: self.event_hub_tab_name in [module.get('title').upper() for module in
                                                                     self.cms_config.get_initial_data().get(
                                                                         'modularContent', [])
                                                                     if module['@type'] == 'COMMON_MODULE'],
                                 name=f'Event_hub tab "{self.event_hub_tab_name}" appears',
                                 timeout=200,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result, msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')

    def test_001_navigate_to_module_from_preconditions_make_sure_its_expanded_and_verify_its_contents(self):
        """
        DESCRIPTION: Navigate to Module from preconditions. Make sure it's expanded and verify it's contents
        EXPECTED: * Module name corresponds to Name set in CMS
        EXPECTED: * Selections are ordered by:
        EXPECTED: Price / Odds in ascending order
        EXPECTED: Alphabetically by selection name - if prices are the same
        EXPECTED: * Price buttons located at the right of each selection containing prices set in TI
        EXPECTED: * No info about event name/start time present in the module
        """
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(event_hub_module,
                        msg=f'Module "{self.module_name}" was not found on "{self.event_hub_tab_name}" tab')
        self.assertTrue(event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')
        events = list(event_hub_module.items_as_ordered_dict.keys())
        odds = []
        for event in events:
            odd = event.split('\n')[1]
            self.assertIn(odd, self.prices, msg='Prices are not displayed as per TI settings')
            odds.append(round(float(Fraction(odd)), 2))
        self.assertTrue(all(odds[i] <= odds[i + 1] for i in range(len(odds) - 1)),
                        msg=f'Odds: "{odds}" should be sorted in ascending order')
        module = str(list(event_hub_content.event_hub_items_dict.keys())[0])
        self.assertFalse(self.event_name in module, msg=f'Event name "{self.event_name}" is displayed on module')
        self.assertFalse(self.event_time_converted in module,
                         msg=f'Event time "{self.event_time_converted}" is displayed on module')
