import pytest

from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl # Live updates cannot be tested on prod and hl
@pytest.mark.module_ribbon
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.liveserv_updates
@pytest.mark.featured
@pytest.mark.football
@vtest
class Test_C29386_Featured_Module_by_Sport_TypeID_Price_Change(BaseFeaturedTest):
    """
    TR_ID: C29386
    NAME: Featured Module by Sport TypeID - Price Change
    DESCRIPTION: This test case verifies situation when price is changed for outcomes of  the 'Primary market'
    DESCRIPTION: on the 'Featured' tab (mobile/tablet)/ Featured section (desktop) of a module by <Sport> TypeID
    PRECONDITIONS: 1. Module by <Sport> TypeID is created in CMS and contains events
    PRECONDITIONS: 2. User is on Homepage > Featured tab
    PRECONDITIONS: 3. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    """
    keep_browser_open = True
    expected_price = '1/7'
    lp = OrderedDict([('odds_home', expected_price),
                      ('odds_draw', expected_price),
                      ('odds_away', expected_price)])
    new_price_1 = '1/3'
    new_price_2 = '1/4'
    featured_tab_name = ''

    def get_section(self):
        sections = self.site.home.get_module_content(
            module_name=self.featured_tab_name
        ).accordions_list.items_as_ordered_dict
        self.assertIn(self.module_name, sections, msg=f'"{self.module_name}" module is not in sections')
        return sections[self.module_name]

    def test_000_preconditions(self):
        """
        DESCRIPTION: create event and add to the featured tab
        """
        type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id
        start_time = self.get_date_time_formatted_string(hours=2)
        event_params = self.ob_config.add_football_event_to_featured_autotest_league(start_time=start_time, lp=self.lp)
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        self.__class__.event_id = event_params.event_id
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.team1 = event_params.team1
        self.__class__.team2 = event_params.team2

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', id=type_id, show_expanded=False, show_all_events=True)['title'].upper()

        self.__class__.featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)

    def test_001_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)

        section = self.get_section()
        section.expand()

    def test_002_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        EXPECTED: The 'Price/Odds' button is displayed new price immediately and it changes its color to:
        EXPECTED: *   blue color if a price has decreased
        EXPECTED: *   pink color if a price has increased
        EXPECTED: Other buttons are not changed if they are available
        """
        section = self.get_section()

        bet_button = section.get_bet_button_by_selection_id(selection_id=self.selection_ids[self.team1])
        self.assertTrue(bet_button,
                        msg=f'"{self.team1}" selection bet button is not found within module "{section.name}"')

        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.new_price_1)
        result = self.wait_for_price_update_from_featured_ms(event_id=self.event_id,
                                                             selection_id=self.selection_ids[self.team1],
                                                             price=self.new_price_1)
        self.assertTrue(result,
                        msg=f'Price updates are not received for event "{self.event_name}", event id "{self.event_id}"')

        section = self.get_section()
        section.expand()

        bet_button = section.get_bet_button_by_selection_id(selection_id=self.selection_ids[self.team1])
        try:
            new_prince_changed = wait_for_result(lambda: bet_button.name == self.new_price_1,
                                                 timeout=4,
                                                 name='Price to change')
        except (VoltronException, AttributeError):
            section = self.get_section()

            bet_button = section.get_bet_button_by_selection_id(selection_id=self.selection_ids[self.team1])
            new_prince_changed = wait_for_result(lambda: bet_button.name == self.new_price_1,
                                                 timeout=4,
                                                 name='Price to change')
        self.assertTrue(new_prince_changed, msg='Price was not changed')

        bet_button_team2 = section.get_bet_button_by_selection_id(selection_id=self.selection_ids[self.team2])
        self.assertTrue(bet_button,
                        msg=f'"{self.team2}" selection bet button is not found within module "{section.name}"')
        self.assertEqual(bet_button_team2.name, self.expected_price, f'Price for {self.team2} was changed')

        bet_button_draw = section.get_bet_button_by_selection_id(selection_id=self.selection_ids['Draw'])
        self.assertTrue(bet_button,
                        msg=f'"Draw" selection bet button is not found within module "{section.name}"')
        self.assertEqual(bet_button_draw.name, self.expected_price, f'Price for Draw was changed')

    def test_003_collapse_module_from_preconditions(self):
        """
        DESCRIPTION: Collapse module from Preconditions
        """
        section = self.get_section()
        section.collapse()

    def test_004_trigger_price_change_for_one_outcome(self):
        """
        DESCRIPTION: Trigger price change for one outcome
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.new_price_2)
        result = self.wait_for_price_update_from_featured_ms(event_id=self.event_id,
                                                             selection_id=self.selection_ids[self.team1],
                                                             price=self.new_price_2)
        self.assertTrue(result,
                        msg=f'Price updates are not received for event "{self.event_name}", event id "{self.event_id}"')

    def test_005_expand_module_from_preconditions(self):
        """
        DESCRIPTION: Expand module from Preconditions
        EXPECTED: Price / Odds button displays new prices without any highlighting
        """
        section = self.get_section()
        section.expand()

        section = self.get_section()

        bet_button = section.get_bet_button_by_selection_id(selection_id=self.selection_ids[self.team1])
        self.assertTrue(bet_button,
                        msg=f'"{self.team1}" selection bet button is not found within module "{section.name}"')

        new_prince_changed = wait_for_result(lambda: bet_button.name == self.new_price_2,
                                             timeout=2,
                                             name='Price to change')
        self.assertTrue(new_prince_changed, msg='Price was not changed')

    def test_006_trigger_price_change_for_a_few_outcomes_from_the_same_market(self):
        """
        DESCRIPTION: Trigger price change for a few outcomes from the same market
        EXPECTED: All 'Price/Odds' buttons display new price immediately and it changes its color to:
        EXPECTED: *   blue color if a price has decreased
        EXPECTED: *   pink color if a price has increased
        """
        pass  # There is no possibility to change prices for two outcomes simultaneously
