import pytest
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_fixed

from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl # Live updates cannot be tested on prod and hl
@pytest.mark.medium
@pytest.mark.featured
@pytest.mark.desktop
@pytest.mark.liveserv_updates
@vtest
class Test_C9701561_Verify_behavior_of_collapsed_Featured_module_after_live_update_receiving(BaseFeaturedTest):
    """
    TR_ID: C9701561
    NAME: Verify behavior of collapsed Featured module after live update receiving
    DESCRIPTION: This test cases verifies behavior of collapsed Featured module after live update receiving.
    PRECONDITIONS: * Module by <Sport> TypeID is created in CMS and contains events
    PRECONDITIONS: * Module is collapsed
    PRECONDITIONS: * User is on Homepage > Featured tab
    PRECONDITIONS: * CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    """
    keep_browser_open = True
    event_params = {}
    module = None
    new_price = '2/1'

    @retry(stop=stop_after_attempt(3),
           retry=retry_if_exception_type(StaleElementReferenceException),
           reraise=True,
           wait=wait_fixed(wait=5))
    def get_featured_section(self, module_title: str):
        """
        DESCRIPTION: Get featured section
        :param module_title: featured module name
        :return: section object
        """
        home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        featured_module = self.site.home.get_module_content(home_featured_tab_name)
        featured_module.scroll_to()
        section = featured_module.accordions_list.items_as_ordered_dict.get(module_title)
        self.assertTrue(section, msg=f'Section "{module_title}" is not found on FEATURED tab')
        return section

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        DESCRIPTION: Create Featured modules in CMS by Sport Type ID, Race Type ID, Selection ID and Enhanced Multiples
        """
        params = self.ob_config.add_football_event_to_featured_autotest_league()
        football_type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

        module_title1 = self.cms_config.add_featured_tab_module(
            select_event_by='Type', id=football_type_id, show_expanded=False, show_all_events=True)['title'].upper()

        params1 = self.ob_config.add_football_event_to_autotest_league2()
        self.__class__.event_id = params1.event_id
        self.__class__.selection_id = params1.selection_ids[params1.team1]
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_league2.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.market_id = self.ob_config.market_ids[self.event_id][market_short_name]

        self.__class__.module_title = self.cms_config.add_featured_tab_module(
            select_event_by='Selection', id=self.selection_id, show_expanded=False)['title'].upper()

        params2 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '3/5'})
        race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        self.__class__.module_title2 = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', show_expanded=False, id=race_type_id)['title'].upper()

        params3 = self.ob_config.add_football_event_enhanced_multiples()
        module_id = self.ob_config.football_config.specials.enhanced_multiples.type_id

        module_title3 = self.cms_config.add_featured_tab_module(
            select_event_by='Enhanced Multiples', id=module_id, show_expanded=False)['title'].upper()

        self.event_params.update({module_title1: params, self.module_title2: params2, module_title3: params3})
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(self.module_title)
        section = self.get_featured_section(self.module_title)
        self.assertFalse(section.is_expanded(expected_result=False), msg=f'Featured section is expanded')

    def test_001_trigger_price_change_for_some_outcome(self, selection_id=None, module=None):
        """
        DESCRIPTION: Trigger price change for some outcome
        EXPECTED: Collapsed Featured module remains collapsed
        """
        self.__class__.selection_id, self.__class__.module = (selection_id, module) if selection_id and module \
            else (self.selection_id, self.module_title)
        self.__class__.section = self.get_featured_section(self.module)
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(expected_result=False),
                         msg=f'Featured "{self.module}" section is expanded after collapse')

        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price)
        self.assertFalse(self.section.is_expanded(expected_result=False),
                         msg=f'Featured "{self.module}" section is expanded')

    def test_002_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Price / Odds button displays new prices without any highlighting
        """
        try:
            self.section.expand()
        except StaleElementReferenceException:
            self.__class__.section = self.get_featured_section(self.module)
            self.section.expand()

        self.__class__.section = self.get_featured_section(self.module)
        result = self.section.is_expanded(timeout=5)
        self.assertTrue(result, msg=f'Featured section "{self.module}" is not expanded')
        bet_button = self.section.get_bet_button_by_selection_id(selection_id=self.selection_id)
        self.assertTrue(bet_button, msg=f'Bet button for selection "{self.selection_id}" is not found')
        initial_price = bet_button.name
        result = wait_for_result(lambda: bet_button.name == self.new_price,
                                 name=f'Price to changed in "{self.module}" from "{initial_price}" to "{self.new_price}"',
                                 timeout=15)
        self.assertTrue(result, msg=f'Price is not changed in "{self.module}"')
        self.assertFalse(bet_button.is_selected(expected_result=False), msg=f'Bet button is highlighted in "{self.module}"')

    def test_003_trigger_suspension_unsuspension_for_some_outcome_market_event(self, event_id=None, market_id=None):
        """
        DESCRIPTION: Trigger suspension/unsuspension for some outcome (market/event)
        EXPECTED: Collapsed Featured module remains collapsed
        """
        event_id, market_id = (event_id, market_id) if event_id and market_id \
            else (self.event_id, self.market_id)
        self.section.collapse()
        self.assertFalse(self.section.is_expanded(expected_result=False, timeout=2), msg=f'Featured section is expanded')
        self.ob_config.change_market_state(event_id=event_id, market_id=market_id, displayed=True)
        self.assertFalse(self.section.is_expanded(expected_result=False), msg=f'Featured section is expanded')

    def test_004_expand_module(self):
        """
        DESCRIPTION: Expand module
        EXPECTED: Price / Odds button displays suspended
        """
        try:
            self.section.expand()
        except StaleElementReferenceException:
            self.__class__.section = self.get_featured_section(self.module)
            self.section.expand()
        self.assertTrue(self.section.is_expanded(), msg=f'Featured section is not expanded')
        bet_button = self.section.get_bet_button_by_selection_id(selection_id=self.selection_id)
        prince_status_changed = bet_button.is_enabled(expected_result=False, timeout=15)
        self.assertFalse(prince_status_changed, msg='Bet button is not suspended')

    def test_005_repeat_steps_1_4_for_module_by_sport_type_id_module_by_race_type_id_module_by_selection_id_module_by_enhanced_multiples(self):
        """
        DESCRIPTION: Repeat steps 1-4 for:
        DESCRIPTION: * Module by Sport Type ID
        DESCRIPTION: * Module by Race Type ID
        DESCRIPTION: * Module by Selection ID
        DESCRIPTION: * Module by Enhanced Multiples
        """
        for module, params in self.event_params.items():
            self._logger.info(f'*** Repeating steps for Module "{module}"')
            self.test_001_trigger_price_change_for_some_outcome(
                selection_id=list(params.selection_ids.values())[0],
                module=module)
            self.test_002_expand_module_from_preconditions()
            self.test_003_trigger_suspension_unsuspension_for_some_outcome_market_event(
                event_id=params.event_id,
                market_id=params.market_id if module == self.module_title2 else list(self.ob_config.market_ids[params.event_id].values())[0])
            self.test_004_expand_module()
