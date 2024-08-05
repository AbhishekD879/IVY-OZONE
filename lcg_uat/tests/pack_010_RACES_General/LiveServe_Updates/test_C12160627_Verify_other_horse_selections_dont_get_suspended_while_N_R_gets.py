import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # we can't trigger live updates on prod and hl
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C12160627_Verify_other_horse_selections_dont_get_suspended_while_N_R_gets(BaseSportTest):
    """
    TR_ID: C12160627
    NAME: Verify other horse selections don’t get suspended while N/R gets
    DESCRIPTION: This test case verifies other horse selections don’t get suspended while N/R gets
    """
    keep_browser_open = True
    markets = [('top_2_finish',)]
    expected_prices = {}
    actual_prices = {}

    def test_000_preconditions(self):
        """
         PRECONDITIONS: 1. Open horse racing event
         PRECONDITIONS: 2. Add market Top 2 Finish in TI tool for this event
         PRECONDITIONS: 3. Add selections to market
         PRECONDITIONS: 4. Set 1-2 selections as N/R
         PRECONDITIONS: 5. Repeat steps 3-4 for Win or Each Way market
        """
        self.__class__.event = self.ob_config.add_UK_racing_event(markets=self.markets, number_of_runners=3, lp=True)
        self.__class__.eventID = self.event.event_id

        win_or_each_way_selection_ids = self.event.selection_ids.get('win_or_each_way')
        top_2_finish_second_selection_ids = self.event.selection_ids.get('top_2_finish')

        selection_name, self.__class__.selection_id = list(win_or_each_way_selection_ids.items())[0]
        self.__class__.new_selection_name = f'{selection_name} N/R'
        self.ob_config.change_selection_name(selection_id=self.selection_id, new_selection_name=self.new_selection_name)

        selection_name, self.__class__.selection_id_02 = list(top_2_finish_second_selection_ids.items())[0]
        self.__class__.new_selection_name_02 = f'{selection_name} N/R'
        self.ob_config.change_selection_name(selection_id=self.selection_id_02,
                                             new_selection_name=self.new_selection_name_02)

    def test_001_suspend_nr_selection_for_win_or_each_way_market(self):
        """
        DESCRIPTION: Suspend N/R selection for Win or Each Way market
        EXPECTED: Only 1 N/R selection is suspended
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab('WIN OR E/W')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')
        for (index, (outcome_name, outcome)) in enumerate(outcomes.items()):
            self.expected_prices.update({outcome_name: outcome.output_price})
            self._logger.debug(f'Outcome: {0} "{outcome_name}"')
            if outcome_name in self.new_selection_name:
                self.assertFalse(outcome.bet_button.is_enabled(expected_result=False, timeout=10),
                                 msg=f'Price bet button is active for "{outcome_name}"')
            else:
                self.assertTrue(outcome.bet_button.is_enabled(), msg=f'Price is suspended for "{outcome_name}"')

        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)

        for (index, (outcome_name, outcome)) in enumerate(outcomes.items()):
            self.actual_prices.update({outcome_name: outcome.output_price})
            self._logger.debug(f'Outcome: {0} "{outcome_name}"')
            if outcome_name in self.new_selection_name:
                self.assertFalse(outcome.bet_button.is_enabled(expected_result=False, timeout=10),
                                 msg=f'Price is not suspended for "{outcome_name}"')
            else:
                self.assertTrue(outcome.bet_button.is_enabled(), msg=f'Price is suspended for "{outcome_name}"')

        self.assertEqual(self.actual_prices, self.expected_prices, msg=f'Actual "{self.actual_prices}" and expected "{self.expected_prices}" prices are changed')

    def test_002_suspend_nr_selection_for_top_2_finish_market(self):
        """
        DESCRIPTION: Suspend N/R selection for Top 2 Finish market
        EXPECTED: Only 1 N/R selection is suspended
        """
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.TOP_FINISH_MARKET_NAME)
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')
        for (index, (outcome_name, outcome)) in enumerate(outcomes.items()):
            self.expected_prices.update({outcome_name: outcome.output_price})
            self._logger.debug(f'Outcome: {0} "{outcome_name}"')
            if outcome_name in self.new_selection_name_02:
                self.assertFalse(outcome.bet_button.is_enabled(expected_result=False),
                                 msg=f'Price bet button is active for "{outcome_name}"')
            else:
                self.assertTrue(outcome.bet_button.is_enabled(), msg=f'Price is suspended for "{outcome_name}"')

        self.ob_config.change_selection_state(selection_id=self.selection_id_02, displayed=True, active=False)

        for (index, (outcome_name, outcome)) in enumerate(outcomes.items()):
            self.actual_prices.update({outcome_name: outcome.output_price})
            self._logger.debug(f'Outcome: {0} "{outcome_name}"')
            if outcome_name in self.new_selection_name:
                self.assertFalse(outcome.bet_button.is_enabled(expected_result=False),
                                 msg=f'Price is not suspended for "{outcome_name}"')
            else:
                self.assertTrue(outcome.bet_button.is_enabled(), msg=f'Price is suspended for "{outcome_name}"')

        self.assertEqual(self.actual_prices, self.expected_prices, msg=f'Actual "{self.actual_prices}" and expected "{self.expected_prices}" prices are changed')
