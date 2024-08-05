import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #Cannot create event hub on prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C9726371_Event_Hub_Module_by_Sport_TypeID__Price_Change(Common):
    """
    TR_ID: C9726371
    NAME: Event Hub: Module by <Sport> TypeID - Price Change
    DESCRIPTION: This test case verifies situation when price is changed for outcomes of  the 'Primary market' on the 'Event Hub' tab (mobile/tablet) of a Featured Events module by <Sport> TypeID
    PRECONDITIONS: 1. Event Hub is created in CMS. Module by <Sport> TypeID is created in CMS and contains events
    PRECONDITIONS: 2. User is on Homepage > Event Hub tab
    PRECONDITIONS: 3. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    """
    keep_browser_open = True

    prices = ['4/6', '3/4', '6/5']

    def test_000_preconditions(self):
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = list(event.selection_ids.values())
        type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='Type', id=type_id,
                                                                             page_type='eventhub', page_id=index_number,
                                                                             events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'

        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub', internal_id=internal_id,
                                                                           hub_index=index_number, display_date=True)

        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

        result = wait_for_result(lambda: self.event_hub_tab_name in [module.get('title').upper() for module in
                                                                     self.cms_config.get_initial_data().get(
                                                                         'modularContent', [])
                                                                     if module['@type'] == 'COMMON_MODULE'],
                                 name=f'Event_hub tab "{self.event_hub_tab_name}" appears',
                                 timeout=200,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result, msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')

    def test_001_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED:
        """
        self.site.wait_content_state(state_name='Homepage')
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.event_hub_items_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        self.__class__.event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(self.event_hub_module,
                        msg=f'Module "{self.module_name}" was not found on "{self.event_hub_tab_name}" tab')
        self.assertTrue(self.event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')

    def test_002_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        EXPECTED: The 'Price/Odds' button is displayed new price immediately and it changes its color to:
        EXPECTED: *   blue color if a price has decreased
        EXPECTED: *   pink color if a price has increased
        EXPECTED: Other buttons are not changed if they are available
        """
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No selections found')
        bet_button = bet_buttons_list[0]
        self.assertTrue(bet_button,
                        msg=f'selection bet button is not found within module')
        self.site.contents.scroll_to_we(bet_button)
        self.ob_config.change_price(selection_id=self.selection_ids[0], price=self.prices[0])
        result = wait_for_result(lambda: self.site.home.bet_buttons[0].text == self.prices[0],
                                 name=f'Previous price {self.site.home.bet_buttons[0].text} to appear. '
                                      f'Current is {self.prices[0]}',
                                 timeout=30)
        self.assertTrue(result, msg='Price was not changed')

    def test_003_collapse_module_from_preconditions(self):
        """
        DESCRIPTION: Collapse module from Preconditions
        EXPECTED:
        """
        self.event_hub_module.collapse()
        self.assertFalse(self.event_hub_module.is_expanded(timeout=2),
                         msg=f'Module: "{self.module_name}" not collapsed')

    def test_004_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        EXPECTED:
        """
        self.ob_config.change_price(selection_id=self.selection_ids[1], price=self.prices[1])

    def test_005_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Price / Odds button displays new prices without any highlighting
        """
        self.event_hub_module.expand()
        self.assertTrue(self.event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')
        result = wait_for_result(lambda: self.site.home.bet_buttons[2].text == self.prices[1],
                                 name=f'Previous price {self.site.home.bet_buttons[2].text} to appear. '
                                      f'Current is {self.prices[1]}',
                                 timeout=10)
        self.assertTrue(result, msg='Price was not changed')

    def test_006_trigger_price_change_for_a_few_outcomes_from_the_same_market(self):
        """
        DESCRIPTION: Trigger price change for a few outcomes from the same market
        EXPECTED: All 'Price/Odds' buttons display new price immediately and it changes its color to:
        EXPECTED: *   blue color if a price has decreased
        EXPECTED: *   pink color if a price has increased
        """
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No selections found')
        bet_button = bet_buttons_list[1]
        self.assertTrue(bet_button,
                        msg=f'selection bet button is not found within module')
        self.site.contents.scroll_to_we(bet_button)
        self.ob_config.change_price(selection_id=self.selection_ids[2], price=self.prices[2])
        result = wait_for_result(lambda: self.site.home.bet_buttons[1].text == self.prices[2],
                                 name=f'Previous price {self.site.home.bet_buttons[1].text} to appear. '
                                      f'Current is {self.prices[2]}',
                                 timeout=10)
        self.assertTrue(result, msg='Price was not changed')
