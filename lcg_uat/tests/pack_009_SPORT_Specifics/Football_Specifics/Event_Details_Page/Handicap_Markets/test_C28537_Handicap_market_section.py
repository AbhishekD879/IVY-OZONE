import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.markets
@pytest.mark.handicap
@pytest.mark.ob_smoke
@pytest.mark.sports
@vtest
class Test_C28537_Handicap_market_section(BaseSportTest):
    """
    TR_ID: C28537
    VOL_ID: C9698000
    NAME: Handicap market section
    """
    keep_browser_open = True
    sport_name = 'Football'

    def test_000_create_event(self):
        """
        DESCRIPTION: Create test event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[('handicap', {'cashout': True})])
        self.__class__.eventID = event_params.event_id
        self.__class__.created_event_name = event_params.team1 + ' v ' + event_params.team2

    def test_001_navigate_to_edp(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name=self.sport_name)

    def test_002_verify_handicap_results_market_section(self):
        """
        DESCRIPTION: Verify Handicap results market section
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        handicap = markets_list.get(self.expected_market_sections.handicap_results)
        self.assertTrue(handicap, msg=f'*** Can not find "{self.expected_market_sections.handicap_results}" market accordion')
        handicap.expand()
        self.assertTrue(handicap.is_expanded(),
                        msg=f'Market accordion "{self.expected_market_sections.handicap_results}" is not expanded')
        handicap.show_all_button.click()
        self.assertTrue(handicap.has_show_less_button(timeout=5), msg='There\'s no \'Show Less\' button')

        market_grouping_buttons = handicap.grouping_buttons.items_as_ordered_dict
        self.assertTrue(market_grouping_buttons, msg=f'Grouping button not found for '
                        f'"{self.expected_market_sections.handicap_results}" market')

        btn_90_min = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.ninety_mins)
        self.assertTrue(btn_90_min, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.ninety_mins}" not found')
        self.assertTrue(btn_90_min.is_selected(), msg=f'"{vec.sb.HANDICAP_SWITCHERS.ninety_mins}" is not selected by default')
        outcome_groups = handicap.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg='Outcome groups is empty')
        outcome_group_name, outcome_group = list(outcome_groups.items())[0]
        outcomes = outcome_group.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{outcome_group_name}"')
        outcome_name, outcome = list(outcomes.items())[1]
        outcome.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()

        handicap.grouping_buttons.click_button(vec.sb.HANDICAP_SWITCHERS.first_half)
        btn_1st_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.first_half)
        self.assertTrue(btn_1st_half, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.first_half}" not found')
        self.assertTrue(btn_1st_half.is_selected(), msg=f'"{vec.sb.HANDICAP_SWITCHERS.first_half}" button is not selected')

        outcome_groups = handicap.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg='Outcome groups is empty')
        outcome_group_name, outcome_group = list(outcome_groups.items())[1]
        outcomes = outcome_group.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{outcome_group_name}"')
        outcome_name, outcome = list(outcomes.items())[2]
        outcome.click()

        handicap.grouping_buttons.click_button(vec.sb.HANDICAP_SWITCHERS.second_half)
        btn_2nd_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.second_half)
        self.assertTrue(btn_2nd_half, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.second_half}" not found')
        self.assertTrue(btn_2nd_half.is_selected(),
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.second_half}" button is not selected')

        outcome_groups = handicap.outcomes.items_as_ordered_dict
        self.assertTrue(outcome_groups, msg='Outcome groups is empty')
        outcome_group_name, outcome_group = list(outcome_groups.items())[2]
        outcomes = outcome_group.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{outcome_group_name}"')
        outcome_name, outcome = list(outcomes.items())[1]
        outcome.click()

        self.verify_betslip_counter_change(expected_value=3)
