import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.medium
@pytest.mark.safari
@vtest
class Test_C1056147_Verify_Racing_Post_Silks_Form_Information_when_silks_are_not_available(BaseRacing):
    """
    TR_ID: C1056147
    NAME: Verify Racing Post Silks/Form Information when silks are not available
    DESCRIPTION: This test case verifies how racing post info will be displayed for each event when silks are not available for the event.
    """
    keep_browser_open = True
    runner_numbers = [1, '-', 3, '-']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Horse Racing event without available silks and open event details page
        """
        event_params = self.ob_config.add_UK_racing_event(runner_numbers=self.runner_numbers)
        self.__class__.eventID = event_params.event_id
        self.__class__.selections_with_runner_num = {selection_name: self.runner_numbers[i] for i, selection_name
                                                     in enumerate(event_params.selection_ids.keys())}

    def test_002_open_event_details_page(self):
        """
        DESCRIPTION: Open event details page
        EXPECTED: 'Horse Racing' landing page is opened
        EXPECTED: 'Win or E/W' tab is opened by default
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        current_tab_name = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.current
        tab_name = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        self.assertEqual(current_tab_name, tab_name,
                         msg=f'Current tab "{current_tab_name}" is not the same '
                             f'as expected "{tab_name}"')

    def test_003_verify_silk_icon(self):
        """
        DESCRIPTION: Verify silk icon
        EXPECTED: Generic silk images are displayed
        EXPECTED: Only runner numbers are displayed
        EXPECTED: Runner numbers are NOT displayed and selection (horse) names without runnerNumber attribute are aligned with the other horse names
        """
        markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets with outcomes found')
        for market_name, market in markets.items():
            outcomes = market.items_as_ordered_dict
            self.assertTrue(outcomes, msg=f'No outcomes found for "{market_name}"')
            for outcome_name, outcome in outcomes.items():
                self.assertTrue(outcome.is_silk_generic, msg=f'Silk icon is not generic for outcome: "{outcome_name}"')
                self.assertIn(outcome_name, self.selections_with_runner_num,
                              msg=f'Outcome "{outcome_name}" is not in '
                                  f'list of created outcomes "{self.selections_with_runner_num}"')

                runner_number = self.selections_with_runner_num[outcome_name]
                if runner_number != '-':
                    self.assertEqual(int(outcome.runner_number), int(runner_number),
                                     msg=f'Runner number "{outcome.runner_number}" for outcome: "{outcome_name}" '
                                         f'is not the same as expected "{runner_number}"')
                else:
                    self.assertFalse(outcome.runner_number,
                                     msg=f'Runner number is displayed for outcome "{outcome_name}"')
