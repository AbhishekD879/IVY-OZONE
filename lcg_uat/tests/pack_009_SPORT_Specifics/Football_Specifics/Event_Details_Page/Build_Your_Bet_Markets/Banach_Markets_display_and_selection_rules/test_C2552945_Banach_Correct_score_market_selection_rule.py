import pytest
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from time import sleep


# @pytest.mark.tst2   # cannot get banach events in qa environments
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C2552945_Banach_Correct_score_market_selection_rule(BaseBanachTest):
    """
    TR_ID: C2552945
    NAME: Banach. Correct score market selection rule
    DESCRIPTION: Test case verifies rules of adding selections to dashboard in Correct score market
    DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
    DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    DESCRIPTION: Related to [Format of Correct score selections][2]
    DESCRIPTION: [2]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490706
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: To check error when selections cannot be combined check **price** request > "responseMessage" parameter
    PRECONDITIONS: **CORRECT SCORE is present on 'Build Your Bet(Coral)/Bet Builder (Ladbrokes)' tab**
    PRECONDITIONS: **Correct score market is expanded and no selections are added to dashboard**
    """
    keep_browser_open = True
    EXPECTED_CORRECT_SCORE_BUTTONS = ['90 mins', '1st Half', '2nd Half']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find event with Build Your Bet markets, open its EDP
        """
        self.__class__.proxy = None
        event_id = self.get_ob_event_with_byb_market()
        self.navigate_to_edp(event_id=event_id)
        self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.current,
                        msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.__class__.correct_score_market = self.get_market(market_name=self.expected_market_sections.correct_score)
        self.assertTrue(self.correct_score_market.is_expanded(),
                        msg=f'"{self.expected_market_sections.correct_score}" section is not expanded')
        correct_score_switchers = self.correct_score_market.grouping_buttons.items_names
        self.assertEqual(correct_score_switchers, self.EXPECTED_CORRECT_SCORE_BUTTONS,
                         msg=f'Actual market headers "{correct_score_switchers}" '
                             f'are not same as expected headers: "{self.EXPECTED_CORRECT_SCORE_BUTTONS}"')
        btn_90_min = self.correct_score_market.grouping_buttons.items_as_ordered_dict.get(
            self.EXPECTED_CORRECT_SCORE_BUTTONS[0])
        self.assertTrue(btn_90_min.is_selected(),
                        msg=f'"{self.EXPECTED_CORRECT_SCORE_BUTTONS[0]}" button is not selected by default')

    def test_001_in_90_mins_switcher_tab_inside_market_select_the_following_score_in_the_drop_downs_43_and_tap_add_to_bet_button(self):
        """
        DESCRIPTION: In "90 mins" switcher tab inside market select the following score in the drop-downs: 4:3 and tap ADD TO BET button
        EXPECTED: "4:3" selection is added to dashboard
        """
        self.correct_score_market.grouping_buttons.click_button(self.EXPECTED_CORRECT_SCORE_BUTTONS[0], timeout=3)
        team_a_scores = self.correct_score_market.team_away_scores
        team_h_scores = self.correct_score_market.team_home_scores
        team_h_scores.select_score_by_text(text='4')
        team_a_scores.select_score_by_text(text='3')
        sleep(2)
        self.correct_score_market.add_to_betslip_button.click()
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        outcomes = dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        dashboard_selections = list(outcomes.keys())
        self.assertIn("4-3", dashboard_selections[0],
                      msg=f' "4-3" is not in {dashboard_selections[0]}')

    def test_002_in_the_same_switcher_tab_select_the_following_score_in_the_drop_downs_42(self):
        """
        DESCRIPTION: In the same switcher tab select the following score in the drop-downs: "4:2"
        EXPECTED: Selection "4:3" is substituted with selection "4:2" in dashboard
        """
        team_a_scores = self.correct_score_market.team_away_scores
        team_h_scores = self.correct_score_market.team_home_scores
        team_a_scores.scroll_to()
        team_h_scores.select_score_by_text(text='4')
        team_a_scores.select_score_by_text(text='2')
        sleep(2)
        self.correct_score_market.add_to_betslip_button.click()
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        outcomes = dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        dashboard_selections = list(outcomes.keys())
        self.assertNotIn("4-3", dashboard_selections[0],
                         msg=f' "4-3" is still in {dashboard_selections[0]}')
        self.assertIn("4-2", dashboard_selections[0],
                      msg=f' "4-2" is not in {dashboard_selections[0]}')

    def test_003_tap_on_show_all_button_scroll_and_check_selected_values_in_the_grid(self):
        """
        DESCRIPTION: Tap on "Show All" button, scroll and check selected values in the Grid
        EXPECTED: - Selection "4:2" is highlighted
        EXPECTED: - Selection "4:3" is not highlighted
        """
        # OX.136.0.0 release- With new BYB template, Show All is removed
        # self.correct_score_market.show_all_button.click()
        # self.correct_score_market.scroll_to_we()
        # outcomes = self.correct_score_market.outcome_table.home_outcomes.items
        # for index in range(len(outcomes)):
        #     if outcomes[index].bet_button.name == "4 - 3":
        #         self.assertFalse(outcomes[index].bet_button.is_selected,
        #                          msg=f'{outcomes[index].bet_button.name} is still highlighted ')
        #     if outcomes[index].bet_button.name == "4 - 2":
        #         self.assertTrue(outcomes[index].bet_button.is_selected,
        #                         msg=f'{outcomes[index].bet_button.name} is not highlighted ')
        #         break

    def test_004_switch_to_1st_half_tab_and_select_the_following_value_from_the_selections_grid_34(self):
        """
        DESCRIPTION: Switch to "1st half" tab and select the following value from the selections Grid: "3:4"
        EXPECTED: Combination error message taken from the **price** request is displayed above dashboard
        """
        self.correct_score_market.grouping_buttons.click_button(self.EXPECTED_CORRECT_SCORE_BUTTONS[1], timeout=3)
        self.__class__.correct_score_default_switcher = self.correct_score_market.grouping_buttons.current
        team_a_scores = self.correct_score_market.team_away_scores
        team_h_scores = self.correct_score_market.team_home_scores
        team_a_scores.scroll_to()
        team_h_scores.select_score_by_text(text='2')
        team_a_scores.select_score_by_text(text='3')
        sleep(3)
        self.correct_score_market.add_to_betslip_button.click()
        sleep(3)
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        outcomes = wait_for_result(
            lambda: dashboard_panel.outcomes_section.items_as_ordered_dict,
            timeout=10,
            name='Outcomes to appear')
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        dashboard_selections = list(outcomes.keys())
        self.assertIn("3-2", dashboard_selections[1],
                      msg=f' "3-2" is not in {dashboard_selections[1]}')
        error_message_text = self.site.sport_event_details.tab_content.dashboard_panel.info_panel.text
        self.assertTrue(error_message_text, msg='Error message from provider is not shown')

    def test_005_select_the_following_value_from_the_1st_half_grid_32(self):
        """
        DESCRIPTION: Select the following value from the "1st half" Grid: "3:2"
        EXPECTED: - Selection "3:4" is substituted with selection ""3:2"
        EXPECTED: - Error message disappears
        """
        team_a_scores = self.correct_score_market.team_away_scores
        team_h_scores = self.correct_score_market.team_home_scores
        team_a_scores.scroll_to()
        team_h_scores.select_score_by_text(text='2')
        team_a_scores.select_score_by_text(text='1')
        sleep(3)
        self.correct_score_market.add_to_betslip_button.click()
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        outcomes = wait_for_result(
            lambda: dashboard_panel.outcomes_section.items_as_ordered_dict,
            timeout=10,
            name='Outcomes to appear')
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        dashboard_selections = list(outcomes.keys())
        self.assertIn("2-1", dashboard_selections[1],
                      msg=f' "2-1" is not in {dashboard_selections[1]}')
        self.assertFalse(
            self.site.sport_event_details.tab_content.dashboard_panel.wait_for_info_panel(
                expected_result=False, timeout=10),
            msg='Error message from provider is not hidden from Dashboard')
