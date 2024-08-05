import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.build_your_bet
@pytest.mark.build_your_bet_dashboard
@pytest.mark.banach
@pytest.mark.critical
@pytest.mark.mocked_data
@pytest.mark.desktop
@vtest
class Test_C2490491_Banach_Dashboard_in_expanded_state_selections_format_and_scroll(BaseBanachTest):
    """
    TR_ID: C2490491
    NAME: Banach Dashboard in expanded state selections format and scroll
    DESCRIPTION: Test case verifies dashboard header and selections list, close and open button
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Examples of combinable Banach markets with selections:**
    PRECONDITIONS: -  without switcher Both teams to score, Total Corners, Corners Match bet, Win Either half HOME
    PRECONDITIONS: -  with switcher Match Betting [HOME or DRAW], Double Chance [HOME OR DRAW or AWAY OR DRAW]
    PRECONDITIONS: **2 Banach selections are added to the dashboard**
    PRECONDITIONS: **Dashboard is expanded**
    """
    keep_browser_open = True
    initial_counter = 0
    team1, team2 = 'Test Team 1', 'Test Team 2'
    expected_dashboard_summary_all_markets_and_selections = []
    expected_dashboard_all_markets_and_selections = []
    expected_default_place_bet_text = vec.yourcall.PLACE_BET
    blocked_hosts = ['*spark-br.*']

    def verify_dashboard_selections(self) -> None:
        """
        Verifies BYB Dashboard selections: if they are the same as were added and if each selection has remove icon
        :return:
        """
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        self.assertTrue(dashboard_panel.is_expanded(), msg='BYB Dashboard is not expanded')
        result = wait_for_result(lambda: len(dashboard_panel.outcomes_section.items_as_ordered_dict.keys()) == len(self.expected_dashboard_all_markets_and_selections),
                                 timeout=5,
                                 name='All selection to be displayed')
        self.assertTrue(result,
                        msg=f'Not all selection are displayed on dashboard. Expected: {len(self.expected_dashboard_all_markets_and_selections)}'
                        f'Actual number {len(dashboard_panel.outcomes_section.items_as_ordered_dict.keys())}')
        selections = dashboard_panel.outcomes_section.items_as_ordered_dict
        dashboard_selections = list(selections.keys())
        self.assertEqual(dashboard_selections, self.expected_dashboard_all_markets_and_selections,
                         msg=f'Dashboard selections "{dashboard_selections}" are '
                             f'not the same as were added "{self.expected_dashboard_all_markets_and_selections}"')
        for selection_name, selection in selections.items():
            self.assertTrue(selection.has_remove_button(), msg=f'Outcome "{selection_name}" does not have remove icon')

    def test_000_preconditions(self):
        """
        DESCRIPTION: 2 Banach selections are added to the dashboard
        DESCRIPTION: Dashboard is expanded
        """
        self.__class__.eventID = self.create_ob_event_for_mock(team1=self.team1, team2=self.team2)
        self.navigate_to_edp(event_id=self.eventID)
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet, timeout=5),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

        # Match betting 90 mins selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        match_betting_default_switcher = match_betting.grouping_buttons.current
        match_betting_selection_names = match_betting.set_market_selection(selection_name=self.team1)
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        match_betting_market_and_selection_name = f'{self.expected_market_sections.match_betting.title()} ' \
                                                  f'{match_betting_default_switcher.lower()} ' \
                                                  f'{self.team1.upper()}'

        self.__class__.expected_dashboard_summary_all_markets_and_selections.append(
            match_betting_market_and_selection_name.upper())
        self.__class__.expected_dashboard_all_markets_and_selections.append(match_betting_market_and_selection_name)
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
        self.__class__.initial_counter += 1

        # Double chance 90 mins selection
        double_chance_market = self.get_market(market_name=self.expected_market_sections.double_chance)
        double_chance_default_switcher = double_chance_market.grouping_buttons.current
        double_chance_selection_names = double_chance_market.set_market_selection(count=1)
        self.assertTrue(double_chance_selection_names, msg='No one selection added to Dashboard')
        double_chance_market_and_selection_name = f'{self.expected_market_sections.double_chance.title()} ' \
                                                  f'{double_chance_default_switcher.lower()} ' \
                                                  f'{double_chance_selection_names[0].upper()}'

        self.__class__.expected_dashboard_all_markets_and_selections.append(double_chance_market_and_selection_name)
        self.__class__.expected_dashboard_summary_all_markets_and_selections.append(
            double_chance_market_and_selection_name.upper())

        self.__class__.initial_counter += 1

    def test_001_verify_dashboard_in_expanded_state(self):
        """
        DESCRIPTION: Verify dashboard in expanded state
        EXPECTED: 1.Dashboard header:
        EXPECTED: - icon with number of selections
        EXPECTED: - BUILD YOUR BET text
        EXPECTED: - name of selections (in the same order they were added, separated by comma)
        EXPECTED: - "Close" label with upside down arrow
        EXPECTED: 2.Odds area
        EXPECTED: 3.Dashboard selections:
        EXPECTED: - Selection lines are displayed in the same order they were added
        EXPECTED: - Delete button next to each selection
        """
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        self.assertTrue(dashboard_panel.is_expanded(), msg='BYB Dashboard is not expanded')
        summary_block = dashboard_panel.byb_summary
        self.assertTrue(summary_block.summary_counter.icon,
                        msg='Dashboard icon is not visible')
        self.assertEqual(int(summary_block.summary_counter.value), self.initial_counter,
                         msg=f'Dashboard counter "{summary_block.summary_counter.value}" '
                             f'is not the same as expected "{self.initial_counter}"')
        self.assertEquals(summary_block.summary_description.dashboard_title,
                          vec.yourcall.DASHBOARD_TITLE,
                          msg=f'Dashboard title "{summary_block.summary_description.dashboard_title}" '
                              f'is not the same as expected "{vec.yourcall.DASHBOARD_TITLE}"')

        dashboard_summary_markets = summary_block.summary_description.dashboard_market_text
        dashboard_summary_markets = dashboard_summary_markets.split(', ')
        self.assertEqual(dashboard_summary_markets, self.expected_dashboard_summary_all_markets_and_selections,
                         msg=f'List of markets selections: "{dashboard_summary_markets}" are not the same as expected '
                             f'"{self.expected_dashboard_summary_all_markets_and_selections}"')

        label = summary_block.open_close_toggle_button.name
        self.assertEqual(label, 'Close',
                         msg=f'Button name "{label}" is not the same as expected "Close"')
        self.assertTrue(summary_block.open_close_toggle_button.has_up_down_arrow(),
                        msg='There\'s no up/down arrow near button')

        odds = summary_block.place_bet.value
        self.assertTrue(odds, msg='Can not get odds for given selections')
        self.assertEqual(summary_block.place_bet.text, self.expected_default_place_bet_text,
                         msg=f'Place bet button text: "{summary_block.place_bet.text}" is not the same as expected:'
                             f' "{self.expected_default_place_bet_text}"')

        self.verify_dashboard_selections()

    def test_002_add_1_more_combinable_selection_from_marketswhere_select_1st_half_for_markets_with_switcherverify_selections_format(
            self):
        """
        DESCRIPTION: Add 1 more combinable selection from markets,
        DESCRIPTION: where select 1st Half for markets with switcher
        DESCRIPTION: Verify selections format
        EXPECTED: - For markets with 1st Half selection name consists of
        EXPECTED: [Market name 1st Half SELECTION NAME]
        """
        # Match betting 1st half selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        match_betting.grouping_buttons.click_button('1ST HALF')
        match_betting_default_switcher = '1st Half'
        match_betting_1st_half_selection_names = match_betting.set_market_selection(selection_name=self.team2)
        self.assertTrue(match_betting_1st_half_selection_names, msg='No one selection added to Dashboard')
        match_betting_market_1st_half_and_selection_name = f'{self.expected_market_sections.match_betting.title()} ' \
                                                           f'{match_betting_default_switcher} ' \
                                                           f'{self.team2.upper()}'
        self.__class__.expected_dashboard_summary_all_markets_and_selections.append(
            match_betting_market_1st_half_and_selection_name.upper())
        self.__class__.expected_dashboard_all_markets_and_selections.append(
            match_betting_market_1st_half_and_selection_name)
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
        self.__class__.initial_counter += 1

        self.verify_dashboard_selections()

    def test_003_add_1_more_combinable_selection_from_marketswhere_select_2nd_half_for_markets_with_switcher(self):
        """
        DESCRIPTION: Add 1 more combinable selection from markets,
        DESCRIPTION: where select 2nd Half for markets with switcher
        EXPECTED: - For markets with 2nd Half switcher selection name consists of
        EXPECTED: [Market name 2nd Half  SELECTION NAME]
        """
        # Double chance 2nd half mins selection
        double_chance_market = self.get_market(market_name=self.expected_market_sections.double_chance)
        double_chance_market.grouping_buttons.click_button('2ND HALF')
        double_chance_default_switcher = '2nd Half'
        double_chance_selection_names = double_chance_market.set_market_selection(count=1)
        self.assertTrue(double_chance_selection_names, msg='No one selection added to Dashboard')
        double_chance_market_2nd_half_and_selection_name = f'{self.expected_market_sections.double_chance.title()} ' \
                                                           f'{double_chance_default_switcher} ' \
                                                           f'{double_chance_selection_names[0].upper()}'

        self.__class__.expected_dashboard_all_markets_and_selections.append(
            double_chance_market_2nd_half_and_selection_name)
        self.__class__.expected_dashboard_summary_all_markets_and_selections.append(
            double_chance_market_2nd_half_and_selection_name.upper())

        self.__class__.initial_counter += 1

        self.verify_dashboard_selections()

    def test_004_add_1_2_more_combinable_selection_from_markets_without_switcher(self):
        """
        DESCRIPTION: Add 1-2 more combinable selection from markets without switcher
        EXPECTED: - For markets without switcher selection name consists of
        EXPECTED: [Market name SELECTION NAME]
        """
        # Both teams to score selection
        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        both_teams_to_score_selection_names = both_teams_to_score_market.set_market_selection(count=1)
        self.assertTrue(both_teams_to_score_selection_names, msg='No one selection added to Dashboard')
        both_teams_to_score_market_and_selection_name = f'{self.expected_market_sections.both_teams_to_score.title()} ' \
                                                        f'{both_teams_to_score_selection_names[0].upper()}'

        self.__class__.expected_dashboard_all_markets_and_selections.append(
            both_teams_to_score_market_and_selection_name)
        self.__class__.expected_dashboard_summary_all_markets_and_selections.append(
            both_teams_to_score_market_and_selection_name.upper())

        self.__class__.initial_counter += 1
        self.verify_dashboard_selections()

    def test_005_add_selection_from_player_bets_market_and_verify_format(self):
        """
        DESCRIPTION: Add selection from 'Player bets' market and verify format
        EXPECTED: Selection from 'Player bets' market consists of:
        EXPECTED: - selection in the format:
        EXPECTED: [Player name]to have[statistic value range][player statistic]
        EXPECTED: - edit and delete icons next to each selection
        """
        # TODO seems this step description was copied from DS tests, need to clarify with Oksana
        player_selection_name = self.add_byb_selection_to_dashboard(
            market_name=self.expected_market_sections.player_to_score_2plus_goals,
            switcher_name=self.team2.upper(), selection_index=1)

        self.assertTrue(player_selection_name, msg='No one selection added to Dashboard')
        player_to_score_2plus_goals_market_and_selection_name = f'{self.expected_market_sections.player_to_score_2plus_goals.title()} ' \
                                                                f'{player_selection_name[0].upper()}'

        self.__class__.expected_dashboard_all_markets_and_selections.append(
            player_to_score_2plus_goals_market_and_selection_name)
        self.__class__.expected_dashboard_summary_all_markets_and_selections.append(
            player_to_score_2plus_goals_market_and_selection_name.upper())

        self.__class__.initial_counter += 1
        self.verify_dashboard_selections()

    def test_006_verify_scroll(self):
        """
        DESCRIPTION: Verify scroll
        EXPECTED: - Selections list is scrollable (scroll appears for 5 and more selections in dashboard)
        EXPECTED: - Page content with markets is not scrollable (when focus is on dashboard)
        """
        # can only check indirectly, if selection becomes visible after scrolling with webdriver, cannot verify if scroll bar is there,
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        self.assertTrue(dashboard_panel.is_expanded(), msg='BYB Dashboard is not expanded')

        selections = dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(selections, msg='List of BYB dashboard selections is empty"')
        for selection_name, selection in selections.items():
            selection.scroll_to()
            self.assertTrue(selection.is_displayed(), msg=f'Selection "{selection_name}" is not displayed')
