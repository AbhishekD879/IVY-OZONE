import pytest
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot edit the price change in beta TI
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C9726382_Event_Hub_Price_is_Changed_for_One_Sport_Boosted_Selection(Common):
    """
    TR_ID: C9726382
    NAME: Event Hub: Price is Changed for One Sport Boosted Selection
    DESCRIPTION: This test case verifies price change for one Sport Boosted selection on Event Hub.
    PRECONDITIONS: 1. Event Hub is created on CMS > Sport Page > Event Hub. Featured Module by <Sport> Selection ID is created in it.
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3. User is on Homepage > Event Hub tab
    """
    keep_browser_open = True
    prices = ['4/6', '3/4']

    def test_000_preconditions(self):
        event = self.ob_config.add_american_football_outright_event_to_autotest_league(selections_number=3)
        self.__class__.selection_id = list(event.selection_ids.items())[0][1]
        self.__class__.eventID = event.event_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
                                        select_event_by='Selection',
                                        id=self.selection_id,
                                        page_type='eventhub',
                                        page_id=index_number,
                                        events_time_from_hours_delta=-10,
                                        module_time_from_hours_delta=-10)['title'].upper()
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

    def test_001_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Module is expanded
        """
        self.site.wait_content_state(state_name='Homepage')
        self.__class__.event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(self.event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        self.__class__.event_hub_modules = self.event_hub_content.event_hub_items_dict
        self.assertTrue(self.event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        self.__class__.event_hub_module = self.event_hub_modules.get(self.module_name)
        self.assertTrue(self.event_hub_module,
                        msg=f'Module "{self.module_name}" was not found on "{self.event_hub_tab_name}" tab')
        self.assertTrue(self.event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')

    def test_002_trigger_price_change_for_an_outcome_in_this_module(self):
        """
        DESCRIPTION: Trigger price change for an outcome in this module
        EXPECTED: The 'Price/Odds' button is displayed new price immediately and it change its color to:
        EXPECTED: *   blue color if a price has decreased
        EXPECTED: *   pink color if a price has increased
        """
        self.__class__.bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(self.bet_buttons_list, msg='No selections found')
        self.__class__.bet_button = self.bet_buttons_list[0]
        self.assertTrue(self.bet_button,
                        msg=f'selection bet button is not found within module')
        self.site.contents.scroll_to_we(self.bet_button)
        self.ob_config.change_price(selection_id=self.selection_id, price=self.prices[0])
        result = wait_for_result(lambda: self.site.home.bet_buttons[0].text == self.prices[0],
                                 name=f'Previous price {self.site.home.bet_buttons[0].text} to appear. '
                                      f'Current is {self.prices[0]}',
                                 timeout=10)
        self.assertTrue(result, msg='Price was not changed')

    def test_003_collapseevent_section(self):
        """
        DESCRIPTION: Collapse event section
        EXPECTED: Section is collapsed
        """
        self.event_hub_module.collapse()
        self.assertFalse(self.event_hub_module.is_expanded(timeout=2),
                         msg=f'Module: "{self.module_name}" not collapsed')

    def test_004_trigger_price_change_for_an_outcome_in_this_module(self):
        """
        DESCRIPTION: Trigger price change for an outcome in this module
        EXPECTED: Price is changed
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.prices[1])

    def test_005_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: The 'Price/Odds' button is displayed new price without highlighting in any color
        """
        self.event_hub_module.expand()
        self.assertTrue(self.event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')
        result = wait_for_result(lambda: self.site.home.bet_buttons[0].text == self.prices[1],
                                 name=f'Previous price {self.site.home.bet_buttons[0].text} to appear. '
                                      f'Current is {self.prices[1]}',
                                 timeout=10)
        self.assertTrue(result, msg='Price was not changed')
