import pytest
from tests.base_test import vtest
from time import sleep
from collections import OrderedDict
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create event hub on prod/beta
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9726378_Event_hub_Module_by_Race_TypeID__Price_Change(BaseRacing):
    """
    TR_ID: C9726378
    NAME: Event hub: Module by <Race> TypeID - Price Change
    DESCRIPTION: This test case verifies situation when price is changed for  the 'Primary market' on the 'Event hub' tab (mobile/tablet) on a module by <Race> TypeID
    """
    keep_browser_open = True
    start_prices = OrderedDict([(0, '1/2'),
                                (1, '1/3'),
                                (2, '1/4')])
    increased_price = '5/2'
    decreased_price = '1/7'
    new_prices = OrderedDict([(0, '12/5'),
                              (1, '13/5'),
                              (2, '14/5')])

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Event Hub is created in CMS > Sport pages > Event hub. Module by <Race> TypeID is created in Event Hub and contains events
        PRECONDITIONS: 2. User is on Homepage > Event hub tab
        PRECONDITIONS: 3. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=3, lp_prices=self.start_prices)
        self.__class__.event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_id = event.event_id
        self._logger.info(f'*** Created Horse racing event name "{self.event_name}"')
        self.__class__.selections = {selection_name: selection_id for selection_name, selection_id in event.selection_ids.items()}
        race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId', id=race_type_id,
                                                                             page_type='eventhub', page_id=index_number,
                                                                             events_time_from_hours_delta=-10,
                                                                             module_time_from_hours_delta=-10)['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
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
        EXPECTED: * The 'Price/Odds' button is displayed new price immediately and it changes its color to:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        EXPECTED: * Other buttons are not changed if they are available
        """
        self.ob_config.change_price(selection_id=list(self.selections.values())[0], price=self.increased_price)
        module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        event_content = module_content._items_as_ordered_dict
        if len(event_content) > 2:
            self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing', timeout=5)
            self.site.wait_content_state(state_name='RacingEventDetails')
            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section = list(sections.values())[0]
            selection = section.items_as_ordered_dict.get(list(self.selections.keys())[0])
            self.__class__.HR_landing_page = True
        else:
            selection = event_content[self.event_name if self.brand == 'bma' else self.event_name.upper()].items_as_ordered_dict.get(list(self.selections.keys())[0])
            self.__class__.HR_landing_page = False
        result = wait_for_result(lambda: selection.bet_button.outcome_price_text == self.increased_price, timeout=20,
                                 name='Changed price to be updated')
        self.assertTrue(result,
                        msg=f'Price was not updated for the selection "{list(self.selections.keys())[0]}"')

    def test_003_collapse_module_from_preconditions(self):
        """
        DESCRIPTION: Collapse module from Preconditions
        """
        if self.HR_landing_page:
            self.navigate_to_page('Homepage')
            self.test_001_expand_module_from_preconditions()
        self.event_hub_module.collapse()
        self.assertFalse(self.event_hub_module.is_expanded(timeout=2),
                         msg=f'Module: "{self.module_name}" not collapsed')

    def test_004_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        """
        self.ob_config.change_price(selection_id=list(self.selections.values())[0], price=self.decreased_price)

    def test_005_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Price / Odds button displays new prices without any highlighting
        """
        self.event_hub_module.expand()
        module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
        event_content = module_content._items_as_ordered_dict
        if len(event_content) > 2:
            self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing', timeout=5)
            self.site.wait_content_state(state_name='RacingEventDetails')
            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No one section was found')
            section = list(sections.values())[0]
            selection = section.items_as_ordered_dict.get(list(self.selections.keys())[0])
            self.HR_landing_page = True
        else:
            selection = event_content[self.event_name if self.brand == 'bma' else self.event_name.upper()].items_as_ordered_dict.get(list(self.selections.keys())[0])
            self.HR_landing_page = False
        result = wait_for_result(lambda: selection.bet_button.outcome_price_text == self.decreased_price, timeout=20,
                                 name='Changed price to be updated')
        self.assertTrue(result,
                        msg=f'Price was not updated for the selection "{list(self.selections.keys())[0]}"')
        if self.HR_landing_page:
            self.navigate_to_page('Homepage')
            self.test_001_expand_module_from_preconditions()

    def test_006_trigger_price_change_for_3_outcomes_of_any_event_from_module(self):
        """
        DESCRIPTION: Trigger price change for 3 outcomes of any event from Module
        EXPECTED: The 'Price/Odds' buttons are displayed new prices immediately and they change its color to:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        """
        for index, selection_id in enumerate(self.selections.values()):
            self.ob_config.change_price(selection_id=selection_id, price=self.new_prices[index])
            sleep(2)
            module_content = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(self.module_name)
            event_content = module_content._items_as_ordered_dict
            if len(event_content) > 2:
                self.navigate_to_edp(event_id=self.event_id, sport_name='horse-racing', timeout=5)
                self.site.wait_content_state(state_name='RacingEventDetails')
                sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
                self.assertTrue(sections, msg='No one section was found')
                section = list(sections.values())[0]
                selection = section.items_as_ordered_dict.get(list(self.selections.keys())[index])
                self.HR_landing_page = True
            else:
                selection = event_content[self.event_name if self.brand == 'bma' else self.event_name.upper()].items_as_ordered_dict.get(list(self.selections.keys())[index])
                self.HR_landing_page = False
            result = wait_for_result(lambda: selection.bet_button.outcome_price_text == self.new_prices[index],
                                     timeout=20, name='Changed price to be updated')
            self.assertTrue(result,
                            msg=f'Price was not updated for the selection "{list(self.selections.keys())[index]}"')
            if self.HR_landing_page:
                self.navigate_to_page('Homepage')
                self.test_001_expand_module_from_preconditions()
