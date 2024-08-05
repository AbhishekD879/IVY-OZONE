from collections import OrderedDict

import pytest
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.module_ribbon
@pytest.mark.featured
@pytest.mark.cms
@pytest.mark.racing
@vtest
class Test_C2511060_Featured_Module_by_Race_TypeID_Price_Change(BaseFeaturedTest, BaseRacing):
    """
    TR_ID: C2511060
    NAME: Featured: Module by <Race> TypeID - Price Change
    DESCRIPTION: This test case verifies situation when price is changed for the 'Primary market' on the 'Featured' tab (mobile/tablet)/ Featured section (desktop) of a module by <Race> TypeID
    PRECONDITIONS: 1. Module by <Race> TypeID is created in CMS and contains events
    PRECONDITIONS: 2. User is on Homepage > Featured tab
    PRECONDITIONS: 3. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
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

    def compare_prices(self, price_buttons_list: list, expected_prices: list):
        """
        Help function which compares expected and actual value of price / odds buttons of event
        :param price_buttons_list: list of price buttons objects
        :param expected_prices: expected prices / odds buttons values
        """
        for index, price_button in enumerate(price_buttons_list):
            self.assertEquals(price_button.outcome_price_text, expected_prices[index],
                              msg=f'Price is: "{price_button.outcome_price_text}", '
                                  f'not as expected: "{expected_prices[index]}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Module by <Race> TypeID is created in CMS and contains events
        DESCRIPTION: Related event for module is created
        DESCRIPTION: User is on Homepage > Featured tab
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=3, lp_prices=self.start_prices)
        self.__class__.event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'
        self._logger.info(f'*** Created Horse racing event name "{self.event_name}"')
        self.__class__.selection_ids = list(event.selection_ids.values())
        self.__class__.first_selection_id = self.selection_ids[0]
        self.__class__.eventID = event.event_id

        race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        self.__class__.race_module_name = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=race_type_id, show_expanded=False, show_all_events=True)['title'].upper()

        self._logger.info(f'*** Created Module "{self.race_module_name}"')

        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.race_module_name)

        self.__class__.featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        )
        self.featured_module.scroll_to()
        self.__class__.section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.race_module_name)
        self.assertTrue(self.section, msg=f'Section "{self.race_module_name}" is not found on FEATURED tab')

    def test_001_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Module is expanded
        EXPECTED: Created in preconditions event is present in module
        """
        self.section.expand()
        self.assertTrue(self.section.is_expanded(timeout=5),
                        msg=f'Section "{self.race_module_name}" is not expanded')

        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.race_module_name)
        self.assertIsNotNone(section, msg=f'"{self.race_module_name}" module is not present')
        self.__class__.cards = section.items_as_ordered_dict
        self.assertTrue(self.cards, msg=f'No Cards found on {self.race_module_name} module')
        self.assertIn(self.event_name, list(self.cards.keys()),
                      msg=f'"{self.event_name}" is not in "{list(self.cards.keys())}"')

    def test_002_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        EXPECTED: * The 'Price/Odds' button is displayed new price immediately and it changes its color to:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        EXPECTED: * Other buttons are not changed if they are available
        """
        self.ob_config.change_price(selection_id=self.first_selection_id, price=self.increased_price)

        result = self.wait_for_price_update_from_featured_ms(event_id=self.eventID, selection_id=self.first_selection_id, price=self.increased_price)
        self.assertTrue(result,
                        msg=f'Price update for selection with id "{self.first_selection_id}" is not received')
        list(self.cards.values())[0].scroll_to()

        # For navigating to event in case if there are several events
        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.race_module_name)
        self.assertIsNotNone(section, msg=f'"{self.race_module_name}" module is not present')
        price_button = section.get_bet_button_by_selection_id(self.first_selection_id)
        price_button.scroll_to_we()
        wait_for_result(lambda:
                        section.get_bet_button_by_selection_id(
                            self.selection_ids[0]).outcome_price_text != list(self.start_prices.values())[0],
                        name=f'Price to change from {list(self.start_prices.values())[0]} to {self.increased_price}',
                        bypass_exceptions=(StaleElementReferenceException, NoSuchElementException, VoltronException, AttributeError),
                        timeout=10)

        price_buttons = [section.get_bet_button_by_selection_id(selection_id) for selection_id in self.selection_ids]
        self.compare_prices(price_buttons, [self.increased_price, self.start_prices[1], self.start_prices[2]])

        self.ob_config.change_price(selection_id=self.first_selection_id, price=self.decreased_price)
        result = self.wait_for_price_update_from_featured_ms(event_id=self.eventID, selection_id=self.first_selection_id,
                                                             price=self.decreased_price)
        self.assertTrue(result,
                        msg=f'Price update for selection with id "{self.first_selection_id}" is not received')

        wait_for_result(lambda:
                        section.get_bet_button_by_selection_id(
                            self.selection_ids[0]).outcome_price_text == self.increased_price,
                        name=f'Price to change from {self.increased_price} to {self.decreased_price}',
                        bypass_exceptions=(StaleElementReferenceException, NoSuchElementException, VoltronException, AttributeError),
                        timeout=10)

        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.race_module_name)
        self.assertIsNotNone(section, msg=f'"{self.race_module_name}" module is not present')
        price_buttons = [section.get_bet_button_by_selection_id(selection_id) for selection_id in self.selection_ids]
        price_buttons[0].scroll_to_we()
        self.compare_prices(price_buttons, [self.decreased_price, self.start_prices[1], self.start_prices[2]])

    def test_003_collapse_module_from_preconditions(self):
        """
        DESCRIPTION: Collapse module from Preconditions
        EXPECTED: Module is collapsed
        """
        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.race_module_name)
        self.assertIsNotNone(section, msg=f'"{self.race_module_name}" module is not present')
        section.collapse()
        self.assertFalse(section.is_expanded(expected_result=False, timeout=2),
                         msg=f'Section "{self.race_module_name}" is not collapsed')

    def test_004_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        EXPECTED: Price change was triggered
        """
        self.ob_config.change_price(selection_id=self.first_selection_id, price=self.increased_price)
        result = self.wait_for_price_update_from_featured_ms(event_id=self.eventID, selection_id=self.first_selection_id,
                                                             price=self.increased_price)
        self.assertTrue(result,
                        msg=f'Price update for selection with id "{self.first_selection_id}" is not received')

    def test_005_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Price / Odds button displays new prices without any highlighting
        """
        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.race_module_name)
        self.assertIsNotNone(section, msg=f'"{self.race_module_name}" module is not present')
        section.expand()
        self.assertTrue(section.is_expanded(timeout=10),
                        msg=f'Section "{self.race_module_name}" is not expanded')

        wait_for_result(lambda:
                        section.get_bet_button_by_selection_id(
                            self.selection_ids[0]).outcome_price_text == self.decreased_price,
                        name=f'Price to change from {self.decreased_price} to {self.increased_price}',
                        timeout=10)
        price_buttons = [section.get_bet_button_by_selection_id(selection_id) for selection_id in self.selection_ids]
        price_buttons[0].scroll_to_we()
        self.compare_prices(price_buttons, [self.increased_price, self.start_prices[1], self.start_prices[2]])

    def test_006_trigger_price_change_for_three_outcomes_of_any_event_from_module(self):
        """
        DESCRIPTION: Trigger price change for 3 outcomes of any event from Module
        EXPECTED: The 'Price/Odds' buttons are displayed new prices immediately and they change its color to:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        """
        for index, selection_id in enumerate(self.selection_ids):
            self.ob_config.change_price(selection_id=selection_id, price=self.new_prices[index])
            result = self.wait_for_price_update_from_featured_ms(event_id=self.eventID,
                                                                 selection_id=selection_id,
                                                                 price=self.new_prices[index])
            self.assertTrue(result,
                            msg=f'Price update for selection with id "{self.first_selection_id}" is not received')

        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.race_module_name)
        self.assertIsNotNone(section, msg=f'"{self.race_module_name}" module is not present')
        wait_for_result(lambda:
                        section.get_bet_button_by_selection_id(
                            self.selection_ids[0]).outcome_price_text == self.new_prices[0],
                        name=f'Price to change from {self.decreased_price} to {self.new_prices[0]}',
                        timeout=10)
        price_buttons = [section.get_bet_button_by_selection_id(selection_id) for selection_id in self.selection_ids]
        price_buttons[0].scroll_to_we()
        self.compare_prices(price_buttons, list(self.new_prices.values()))
