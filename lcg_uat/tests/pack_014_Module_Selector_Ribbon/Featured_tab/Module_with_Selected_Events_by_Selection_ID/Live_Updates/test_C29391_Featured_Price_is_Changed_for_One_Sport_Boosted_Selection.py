import pytest
from selenium.common.exceptions import StaleElementReferenceException

from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Live price updates cannot be tested on prod and hl
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.cms
@pytest.mark.slow
@pytest.mark.liveserv_updated
@pytest.mark.featured
@pytest.mark.module_ribbon
@pytest.mark.desktop
@vtest
class Test_C29391_Featured_Price_is_Changed_for_One_Sport_Boosted_Selection(BaseFeaturedTest):
    """
    TR_ID: C29391
    NAME: Featured: Price is Changed for One Sport Boosted Selection
    DESCRIPTION: This test case verifies price change for one Sport Boosted selection.
    PRECONDITIONS: 1. Featured Module by <Sport> Selection ID is created in CMS
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3. User is on Homepage > Featured tab
    """
    keep_browser_open = True
    new_price_1 = '11/17'
    new_price_2 = '33/5'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Preconditions
        DESCRIPTION: Featured Module by <Sport> Selection ID is created in CMS
        DESCRIPTION: User is on Homepage > Featured tab
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = event.selection_ids
        self.__class__.team2 = event.team2

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Selection', id=self.selection_ids[self.team2])['title'].upper()

        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)

        self.__class__.featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        )
        self.featured_module.scroll_to()
        self.__class__.section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(self.section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        self.section.scroll_to()

    def test_001_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Module is expanded
        """
        try:
            self.section.expand()
            self.assertTrue(self.section.is_expanded(bypass_exceptions=(), timeout=5), msg=f'{self.section.name} is not expanded')
        except (StaleElementReferenceException, VoltronException):
            self.__class__.section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
            self.assertTrue(self.section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        self.__class__.section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(self.section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        self.assertTrue(self.section.is_expanded(timeout=10), msg=f'{self.section.name} is not expanded')

    def test_002_trigger_price_change_for_an_outcome_in_this_module(self):
        """
        DESCRIPTION: Trigger price change for an outcome in this module
        EXPECTED: The 'Price/Odds' button is displayed new price immediately and it change its color to:
        EXPECTED: *   blue color if a price has decreased
        EXPECTED: *   pink color if a price has increased
        """
        self.__class__.section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        bet_buttons = self.section.get_available_prices()
        self.assertTrue(bet_buttons, msg='No selections found')
        bet_button = bet_buttons.get(self.team2)
        self.assertTrue(bet_button,
                        msg=f'"{self.team2}" selection bet button is not found within module "{self.section.name}"')
        bet_button.scroll_to()
        self.ob_config.change_price(selection_id=self.selection_ids[self.team2], price=self.new_price_1)

        price_update_received = self.wait_for_price_update_from_featured_ms(event_id=self.eventID,
                                                                            selection_id=self.selection_ids[self.team2],
                                                                            price=self.new_price_1)
        self.assertTrue(price_update_received, msg='Price update was not received')

        self.__class__.featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        )
        self.featured_module.scroll_to()

        self.__class__.section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(self.section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        bet_buttons = self.section.get_available_prices()
        self.assertTrue(bet_buttons, msg='No selections found')
        bet_button = bet_buttons.get(self.team2)
        self.assertTrue(bet_button,
                        msg=f'"{self.team2}" selection bet button is not found within module "{self.section.name}"')
        bet_button.scroll_to()
        self.assertTrue(bet_button.is_price_changed(expected_price=self.new_price_1, timeout=10), msg='Price was not changed')

    def test_003_collapse_event_section(self):
        """
        DESCRIPTION: Collapse event section
        EXPECTED: Section is collapsed
        """
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(expected_result=False), msg=f'{self.section.name} is not collapsed')

    def test_004_trigger_price_change_for_an_outcome_in_this_module(self):
        """
        DESCRIPTION: Trigger price change for an outcome in this module
        EXPECTED: Price is changed
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.team2], price=self.new_price_2)
        price_update_received = self.wait_for_price_update_from_featured_ms(event_id=self.eventID,
                                                                            selection_id=self.selection_ids[self.team2],
                                                                            price=self.new_price_2)
        self.assertTrue(price_update_received, msg='Price update was not received')

    def test_005_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: The 'Price/Odds' button is displayed new price without highlighting in any color
        """
        self.__class__.featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        )
        self.featured_module.scroll_to()
        self.__class__.section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(self.section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        self.section.scroll_to()
        self.test_001_expand_module_from_preconditions()
        try:
            bet_buttons = self.section.get_available_prices()
            self.assertTrue(bet_buttons, msg='No selections found')
            bet_button = bet_buttons.get(self.team2)
            self.assertTrue(bet_button,
                            msg=f'"{self.team2}" selection bet button is not found within module "{self.section.name}"')
        except (VoltronException, StaleElementReferenceException):
            self.__class__.section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
            self.assertTrue(self.section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
            bet_buttons = self.section.get_available_prices()
            self.assertTrue(bet_buttons, msg='No selections found')
            bet_button = bet_buttons.get(self.team2)
            self.assertTrue(bet_button,
                            msg=f'"{self.team2}" selection bet button is not found within module "{self.section.name}"')

        self.assertEqual(bet_button.name, self.new_price_2)
