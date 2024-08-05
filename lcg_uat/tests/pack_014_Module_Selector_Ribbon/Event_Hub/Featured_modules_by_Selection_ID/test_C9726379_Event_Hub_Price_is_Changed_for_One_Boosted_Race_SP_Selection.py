import pytest
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot edit the price change in beta TI
# @pytest.mark.hl
@pytest.mark.other
@pytest.mark.medium
@pytest.mark.mobile_only
@vtest
class Test_C9726379_Event_Hub_Price_is_Changed_for_One_Boosted_Race_SP_Selection(Common):
    """
    TR_ID: C9726379
    NAME: Event Hub: Price is Changed for One Boosted Race SP Selection
    DESCRIPTION: This test case verifies price change for one boosted Race SP selection.
    PRECONDITIONS: 1. CMS and OB TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2. To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXX - event ID
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. There should be an event with Boosted Race SP selection (on CMS event is added by **selection Id**) on 'Event Hub' tab
    PRECONDITIONS: 4. Make sure that 'Expanded by default' check box is checked for the module that contains tested selection
    PRECONDITIONS: 5. User is on Homepage > Event Hub tab
    """
    keep_browser_open = True
    new_price_1 = '5/2'
    new_price_2 = '1/7'

    def test_000_preconditions(self):
        event = self.ob_config.add_UK_racing_event(number_of_runners=1)
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

    def test_001_find_a_module_with_boosted_selection_from_preconditions(self):
        """
        DESCRIPTION: Find a module with Boosted Selection from preconditions
        EXPECTED: Module with a Boosted Selection is displayed with 'SP' outcome
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

    def test_002_trigger_price_change_for_the_outcome_of_the_boosted_selection(self):
        """
        DESCRIPTION: Trigger price change for the outcome of the Boosted Selection
        EXPECTED: The 'Price/Odds' button is NOT displaying new price and is NOT highlighted in any color because only 'SP' is shown instead of price/odds button
        """
        self.__class__.bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(self.bet_buttons_list, msg='No selections found')
        self.__class__.bet_button = self.bet_buttons_list[0]
        self.assertTrue(self.bet_button,
                        msg=f'selection bet button is not found within module')
        self.site.contents.scroll_to_we(self.bet_button)
        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price_1)
        result = wait_for_result(lambda: self.site.home.bet_buttons[0].text == self.new_price_1,
                                 name=f'Previous price {self.site.home.bet_buttons[0].text} to appear. '
                                      f'Current is {self.new_price_1}',
                                 timeout=10)
        self.assertFalse(result, msg='Price was changed')

    def test_003_collapsethe_module(self):
        """
        DESCRIPTION: Collapse the module
        EXPECTED: Module is collapsed
        """
        self.event_hub_module.collapse()
        self.assertFalse(self.event_hub_module.is_expanded(timeout=2),
                         msg=f'Module: "{self.module_name}" not collapsed')

    def test_004_trigger_price_change_for_the_outcome_of_the_boosted_selection_again(self):
        """
        DESCRIPTION: Trigger price change for the outcome of the Boosted Selection again
        EXPECTED: Nothing happens, no blinking or color changing on UI
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price_2)

    def test_005_expand_the_module(self):
        """
        DESCRIPTION: Expand the module
        EXPECTED: Module is expanded and the 'Price/Odds' button is NOT displaying new price and is NOT highlighted in any color because only 'SP' is shown instead of price/odds button
        """
        self.event_hub_module.expand()
        self.assertTrue(self.event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')
        result = wait_for_result(lambda: self.site.home.bet_buttons[0].text == self.new_price_2,
                                 name=f'Previous price {self.site.home.bet_buttons[0].text} to appear. '
                                      f'Current is {self.new_price_2}',
                                 timeout=10)
        self.assertFalse(result, msg='Price was changed')
