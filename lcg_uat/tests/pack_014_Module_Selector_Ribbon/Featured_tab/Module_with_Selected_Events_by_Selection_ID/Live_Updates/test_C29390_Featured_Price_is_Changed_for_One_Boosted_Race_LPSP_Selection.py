import pytest
from tests.base_test import vtest
from selenium.common.exceptions import StaleElementReferenceException
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Live price updates cannot be tested on prod and hl
# @pytest.mark.hl
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.liveserv_updated
@pytest.mark.module_ribbon
@pytest.mark.desktop
@vtest
class Test_C29390_Featured_Price_is_Changed_for_One_Boosted_Race_LPSP_Selection(BaseFeaturedTest, BaseRacing):
    """
    TR_ID: C29390
    NAME: Featured: Price is Changed for One Boosted Race LP,SP Selection
    DESCRIPTION: This test case verifies price change for one boosted Race LP, SP selection.
    DESCRIPTION: NOTE, **User Story** BMA-2451 Feature tab: Live serve price updates
    PRECONDITIONS: 1. CMS and OB TI: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2. To retrieve markets and outcomes for event use: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXX - event ID
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 3. There should be an event with Boosted Race LP, SP selection (in CMS event is added by **selection Id**, in BO TI the event's primary market has 'LP Available' & 'SP Available' check boxes checked) on 'Featured' tab
    PRECONDITIONS: 4. Make sure that 'Expanded by default' check box is checked for the module that contains tested selection
    """
    keep_browser_open = True
    new_price_1 = '5/2'
    new_price_2 = '1/7'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Preconditions
        DESCRIPTION: Featured Module by <Race> Selection ID is created in CMS
        DESCRIPTION: User is on Homepage > Featured tab
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=['1/2'])
        self.__class__.selection_id = list(event.selection_ids.values())[0]
        self.__class__.eventID = event.event_id

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Selection',
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10,
            show_expanded=False,
            id=self.selection_id)['title'].upper()

    def test_001_go_to_home_page__featured_module(self):
        """
        DESCRIPTION: Go to Home page > Featured module
        EXPECTED: Home page with Featured module is displayed
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)

        self.__class__.featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        )
        self.featured_module.scroll_to()

    def test_002_find_a_module_with_boosted_selection_from_preconditions(self):
        """
        DESCRIPTION: Find a module with Boosted Selection from preconditions
        EXPECTED: Module with Boosted Selection is displayed with correct outcome
        """
        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        section.scroll_to()
        try:
            section.expand()
            self.assertTrue(section.is_expanded(bypass_exceptions=(), timeout=5), msg=f'{section.name} is not expanded')
        except (StaleElementReferenceException, VoltronException):
            section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
            self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        self.assertTrue(section.is_expanded(timeout=10), msg=f'{section.name} is not expanded')

    def test_003_trigger_price_change_for_the_outcome_of_the_boosted_selection(self):
        """
        DESCRIPTION: Trigger price change for the outcome of the Boosted Selection
        EXPECTED: Only **LP **part for price/odds button is shown
        EXPECTED: The 'Price/Odds' button is displaying a new price immediately and it changes its color to:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        """
        self.__class__.section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        bet_buttons = self.section.get_available_prices()
        self.assertTrue(bet_buttons, msg='No selections found')
        _, bet_button = list(bet_buttons.items())[0]
        self.assertTrue(bet_button,
                        msg=f'selection bet button is not found within module "{self.section.name}"')
        bet_button.scroll_to()
        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price_1)

        price_update_received = self.wait_for_price_update_from_featured_ms(event_id=self.eventID,
                                                                            selection_id=self.selection_id,
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
        _, bet_button = list(bet_buttons.items())[0]
        self.assertTrue(bet_button,
                        msg=f'selection bet button is not found within module "{self.section.name}"')
        bet_button.scroll_to()
        self.assertTrue(bet_button.is_price_changed(expected_price=self.new_price_1, timeout=10), msg='Price was not changed')

    def test_004_collapsethe_module(self):
        """
        DESCRIPTION: Collapse the module
        EXPECTED: Module is collapased
        """
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(expected_result=False), msg=f'{self.section.name} is not collapsed')

    def test_005_trigger_price_change_for_the_outcome_of_the_boosted_selection_again(self):
        """
        DESCRIPTION: Trigger price change for the outcome of the Boosted Selection again
        EXPECTED: Nothing happens, no blinking or color changing on UI
        """
        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price_2)
        price_update_received = self.wait_for_price_update_from_featured_ms(event_id=self.eventID,
                                                                            selection_id=self.selection_id,
                                                                            price=self.new_price_2)
        self.assertTrue(price_update_received, msg='Price update was not received')

    def test_006_expand_the_module_in_a_few_seconds_after_price_changing(self):
        """
        DESCRIPTION: Expand the module in a few seconds after price changing
        EXPECTED: Only **LP **part for price/odds button is shown
        EXPECTED: The module is expanded and the 'Price/Odds' button is displaying a new price, no color changings on UI
        """
        featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        )
        featured_module.scroll_to()
        section = featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
        self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
        self.section.scroll_to()
        self.test_002_find_a_module_with_boosted_selection_from_preconditions()
        try:
            bet_buttons = self.section.get_available_prices()
            self.assertTrue(bet_buttons, msg='No selections found')
            _, bet_button = list(bet_buttons.items())[0]
            self.assertTrue(bet_button,
                            msg=f' selection bet button is not found within module "{self.section.name}"')
        except (VoltronException, StaleElementReferenceException):
            section = self.featured_module.accordions_list.items_as_ordered_dict.get(self.module_name)
            self.assertTrue(section, msg=f'Section "{self.module_name}" is not found on FEATURED tab')
            bet_buttons = section.get_available_prices()
            self.assertTrue(bet_buttons, msg='No selections found')
            _, bet_button = list(bet_buttons.items())[0]
            self.assertTrue(bet_button,
                            msg=f'selection bet button is not found within module "{section.name}"')
        self.assertEqual(bet_button.name, self.new_price_2)
