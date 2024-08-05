import pytest
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


# @pytest.mark.tst2  # cannot get banach events in qa environments
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.build_your_bet
@pytest.mark.desktop
@vtest
class Test_C2490706_Banach_Format_of_Correct_score_selection_on_dashboard(BaseBanachTest):
    """
    TR_ID: C2490706
    NAME: Banach. Format of Correct score selection on dashboard
    DESCRIPTION: Test case verifies Correct Score selections format in dashboard
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > markets-grouped request
    PRECONDITIONS: Response of selections for specific markets is to be taken from selections request when the market is expanded
    PRECONDITIONS: Correct Score market should be available
    PRECONDITIONS: BYB **Coral**/Bet Builder **Ladbrokes** tab is opened
    """
    keep_browser_open = True
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find event with Banach markets
        """
        self.__class__.event_id = self.get_ob_event_with_byb_market()
        self.navigate_to_edp(event_id=self.event_id, timeout=50)
        self.site.wait_content_state(state_name='EventDetails')
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_001_make_the_following_selection_in_the_correct_score_market_accordion90_mins_home_team_1___away_team_3_and_tap_add_to_bet(self):
        """
        DESCRIPTION: Make the following selection in the Correct Score market accordion:
        DESCRIPTION: 90 mins HOME team 1 - AWAY team 3 and tap ADD TO BET
        EXPECTED: Selection has the following name format in dashboard:
        EXPECTED: Correct Score 90 mins [AWAY team] 3-1 - Coral
        EXPECTED: ![](index.php?/attachments/get/114303314)
        EXPECTED: (!) Team which has higher score is displayed in Dashboard.
        """
        self.__class__.correct_score_market = self.get_market(market_name=self.expected_market_sections.correct_score)
        self.__class__.correct_score_default_switcher = self.correct_score_market.grouping_buttons.current
        self.__class__.team_a_scores = self.correct_score_market.team_away_scores
        self.__class__.team_h_scores = self.correct_score_market.team_home_scores
        self.team_h_scores.select_score_by_text(text='1')
        self.team_a_scores.select_score_by_text(text='3')
        self.__class__.expected_market = \
            f'{self.expected_market_sections.correct_score.upper()} {self.correct_score_default_switcher.upper()}'

        self.correct_score_market.add_to_betslip_button.click()
        self.__class__.dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        self.__class__.summary_block = self.dashboard_panel.byb_summary
        self.__class__.actual_correct_score_market_and_selection_name = \
            self.summary_block.summary_description.dashboard_market_text
        away_team_split = self.team2.title().split()
        length = len(away_team_split)
        result = None
        for i in range(0, length):
            team_name = away_team_split[i].upper()
            if team_name in self.actual_correct_score_market_and_selection_name:
                result = True
                break
            else:
                result = False
        self.assertTrue(result, msg=f'Team name "{self.team2.title()}" not present Dashboard selection name '
                                    f'"{self.actual_correct_score_market_and_selection_name}"')
        result = True if self.expected_market in self.actual_correct_score_market_and_selection_name else False
        self.assertTrue(result, msg=f'Market name not present in Dashboard selection name')

        result = True if '3-1' in self.actual_correct_score_market_and_selection_name else False
        self.assertTrue(result, msg=f'Score not present in Dashboard selection name')

        self.__class__.outcomes = self.dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'List of outcomes is empty: "{self.outcomes}"')
        dashboard_selection = list(self.outcomes.keys())[0]
        correct_score_dashboard_outcome = self.get_byb_dashboard_outcome(name=dashboard_selection)
        correct_score_dashboard_outcome.remove_button.click()

    def test_002_make_the_following_selection_in_the_correct_score_market_accordion90_mins_home_team_3___away_team_1_and_tap_add_to_bet(self):
        """
        DESCRIPTION: Make the following selection in the Correct Score market accordion:
        DESCRIPTION: 90 mins HOME team 3 - AWAY team 1 and tap ADD TO BET
        EXPECTED: Selection has the following name format in dashboard:
        EXPECTED: Correct Score 90 mins [Home team] 3-1 - Ladbrokes
        EXPECTED: ![](index.php?/attachments/get/114303315)
        EXPECTED: (!) Team which has higher score is displayed in Dashboard.
        """
        self.team_h_scores.select_score_by_text(text='3')
        self.team_a_scores.select_score_by_text(text='1')
        self.correct_score_market.add_to_betslip_button.click()
        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded(timeout=13)
        if not is_expanded:
            self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.open_close_toggle_button.click()
        self.actual_correct_score_market_and_selection_name = \
            self.summary_block.summary_description.dashboard_market_text
        home_team_split = self.team1.title().split()
        length = len(home_team_split)
        result = None
        for i in range(0, length):
            team_name = home_team_split[i].upper()
            if team_name in self.actual_correct_score_market_and_selection_name:
                result = True
                break
            else:
                result = False
        self.assertTrue(result, msg=f'Team name "{self.team1.title()}" not present Dashboard selection name '
                                    f'"{self.actual_correct_score_market_and_selection_name}"')
        result = True if self.expected_market in self.actual_correct_score_market_and_selection_name else False
        self.assertTrue(result, msg=f'Market name not present in Dashboard selection name')
        result = True if '3-1' in self.actual_correct_score_market_and_selection_name else False
        self.assertTrue(result, msg=f'Score not present in Dashboard selection name')
