import pytest
import tests
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
import voltron.environments.constants as vec


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.build_your_bet
@pytest.mark.build_your_bet_dashboard
@pytest.mark.banach
@pytest.mark.critical
@pytest.mark.desktop
@vtest
class Test_C1894879_BYB_Banach_Dashboard_layout(BaseBanachTest):
    """
    TR_ID: C1894879
    NAME: BYB Banach Dashboard layout
    DESCRIPTION: This test case verifies triggering selections dashboard and price generation
    DESCRIPTION: Note: some selections are not allowed for combos or require additional selections to place bet, those rules are covered in related TC's.For this test case use only valid combos of selections.
    PRECONDITIONS: *CMS config*:
    PRECONDITIONS: 1. Build Your Bet tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: a. Banach leagues are added and enabled in CMS -> YourCall -> YourCall Leagues
    PRECONDITIONS: b. Event belonging to Banach league is mapped (on Banach side)
    PRECONDITIONS: 2. BYB markets are added in CMS -> BYB -> BuildYourBet Markets Page
    PRECONDITIONS: *Requests*:
    PRECONDITIONS: Request for Banach leagues : https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues
    PRECONDITIONS: Request for Banach event data: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/events/obEventId=xxxxx
    PRECONDITIONS: Request for Banach market groups: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v2/markets-grouped?obEventId=xxxxx
    PRECONDITIONS: Request for Banach selections: https://buildyourbet-dev0.coralsports.dev.cloud.ladbrokescoral.com/api/v1/selections?marketIds=[ids]&obEventId=xxxxx
    PRECONDITIONS: Build Your Bet tab on event details page is loaded
    """
    keep_browser_open = True
    dashboard_panel = None
    dashboard_markets_list = []
    match_betting_market_and_selection_name, correct_score_market_and_selection_name = str, str
    expected_default_place_bet_text = vec.yourcall.PLACE_BET
    blocked_hosts = ['*spark-br.*']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get OB event with Banach markets or create one to use in mock service
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.proxy = None
            self.__class__.eventID = self.get_ob_event_with_byb_market()
        else:
            self.__class__.eventID = self.create_ob_event_for_mock(team1='Test team 1', team2='Test team 2')

    def test_001_navigate_to_event_detail_page(self):
        """
        DESCRIPTION: Navigate to Build Your Bet tab (phase #2) on Event Details page of event mapped with Banach with available Banach markets
        EXPECTED: Static block with market accordions (for markets that are received from Banach or mock) are displayed
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.open_tab(
            self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_002_add_few_combinable_selections_to_byb_dashboard_from_different_markets_accordions(self):
        """
        DESCRIPTION: Add few combinable selections to BYB Dashboard from different markets accordions:
        DESCRIPTION: * Match Result or Both teams to score
        DESCRIPTION: * Double Chance
        DESCRIPTION: * Anytime goalscorer
        DESCRIPTION: * Over/Under markets
        DESCRIPTION: * Correct Score
        EXPECTED: * Selected selections are highlighted within accordions
        EXPECTED: * BYB Dashboard appears with slide animation and is displayed in an expanded state (only when the page is accessed and selections are added for the first time):
        EXPECTED: *  **on mobile** in the bottom of the screen over footer menu
        EXPECTED: *  **on tablet/desktop** in the bottom of the market area and above footer menu (if market area is too long to be shown within screen)
        EXPECTED: * User is able to collapse the Dashboard
        """
        # Match betting selection
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting, msg=f'Can not get market "{self.expected_market_sections.match_result}"')
        match_betting_selection_name = match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_name, msg='No one selection added to Dashboard')
        match_betting_default_switcher_tab= match_betting.time_period_outcomes_list.current
        self.__class__.match_betting_default_switcher = "90 MINS" if match_betting_default_switcher_tab == "90 Minutes" else match_betting_default_switcher_tab
        team_name = match_betting.outcomes.items[0].name
        match_betting_selection_name = match_betting.outcomes.items_as_ordered_dict[team_name].is_selected()
        if match_betting_selection_name:
            match_betting_selection_names = team_name
        else:
            match_betting.outcomes.items_as_ordered_dict[team_name].click()
            match_betting_selection_names = team_name
        match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            initial_counter=self.initial_counter, timeout=15)
        self.__class__.initial_counter += 1

        self.__class__.team1 = ''.join(match_betting_selection_names.replace("Fc", "").strip())
        self.__class__.match_betting_market_and_selection_name =\
            f'{self.expected_market_sections.match_betting} {self.match_betting_default_switcher} {self.team1.upper()}'

        # Correct score selection
        correct_score_market = self.get_market(market_name=self.expected_market_sections.correct_score)
        self.__class__.correct_score_default_switcher = correct_score_market.grouping_buttons.current
        team_a_scores = correct_score_market.team_away_scores
        team_h_scores = correct_score_market.team_home_scores

        team_a_scores.select_score_by_text(text='0')
        team_h_scores.select_score_by_text(text='1')
        self.__class__.correct_score_selection = \
            f'{self.team1.title()} 1-0' if self.brand == 'ladbrokes' else f'{self.team1.upper()} 1-0'
        self._logger.debug(f'*** Correct score selection: "{self.correct_score_selection}"')

        self.__class__.correct_score_market_and_selection_name = \
            f'{self.expected_market_sections.correct_score} {self.correct_score_default_switcher} ' \
            f'{self.correct_score_selection}'
        correct_score_market.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1

        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded()
        self.assertTrue(is_expanded, msg='Dashboard is not expanded')
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.open_close_toggle_button.click()
        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded(
            expected_result=False, timeout=15)
        self.assertFalse(is_expanded, msg='Dashboard is not collapsed')

    def test_003_verify_the_byb_dashboard_content_in_collapsed_state(self):
        """
        DESCRIPTION: Verify the BYB Dashboard content in collapsed state
        EXPECTED: BYB Dashboard consists of
        EXPECTED: * Dashboard touchable area
        EXPECTED: * Odds touchable area
        """
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB dashboard is not available')

    def test_004_verify_the_dashboard_touchable_area_content(self):
        """
        DESCRIPTION: Verify the dashboard touchable area content
        EXPECTED: The following information is displayed:
        EXPECTED: * icon with number of selections
        EXPECTED: * **BUILD A BET** text
        EXPECTED: * name of selections (in the same order they were added, separated by comma)
        EXPECTED: * 'Open' label with arrow
        """
        self.__class__.dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        self.__class__.summary_block = self.dashboard_panel.byb_summary
        self.assertTrue(self.summary_block.summary_counter.icon, msg="Dashboard icon is not visible")
        self.assertTrue(self.summary_block.summary_counter.value, msg="Dashboard counter is not visible")
        self.assertEquals(self.summary_block.summary_description.dashboard_title, vec.yourcall.DASHBOARD_TITLE,
                          msg=f'Dashboard title "{self.summary_block.summary_description.dashboard_title}" '
                              f'is not the same as expected "{ vec.yourcall.DASHBOARD_TITLE}"')
        self.__class__.dashboard_markets_list = self.summary_block.summary_description.dashboard_market_text
        self._logger.debug(f'*** Dashboard Markets and selection list: "{self.dashboard_markets_list}"')
        self.assertTrue(self.dashboard_markets_list,
                        msg=f'Dashboard Market text is not visible "{self.dashboard_markets_list}"')

        actual_button_name = \
            self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.open_close_toggle_button.name
        self.assertEqual(actual_button_name, vec.yourcall.OPEN,
                         msg=f'Button name: "{actual_button_name}" is not the same as expected: "{vec.yourcall.OPEN}"')

        self.assertTrue(self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.open_close_toggle_button.
                        has_up_down_arrow(), msg='There\'s no up/down arrow near button')

    def test_005_verify_selections_name(self):
        """
        DESCRIPTION: Verify selections name
        EXPECTED: Name of selection is displayed in the following formats:
        EXPECTED: * For Match Result, Both teams to score, Player to be carded and Anytime goalscorer - **<Market Name> <Selection Name>** (e.g. Both Teams to score YES or Player to be carded CRISTIANO RONALDO)
        EXPECTED: * For Over/Under markets - **Total <Statistic name> OVER or UNDER XX.X** (e.g. Total Booking Points OVER 33.5)
        """
        expected_all_markets_and_selections = f'{self.match_betting_market_and_selection_name.upper()}, ' \
                                              f'{self.correct_score_market_and_selection_name.upper()}'

        self.assertEqual(self.dashboard_markets_list, expected_all_markets_and_selections,
                         msg=f'List of markets selections: "{self.dashboard_markets_list}" \n'
                             f'are not the same as expected "{expected_all_markets_and_selections}"')

        dashboard_market_text = self.dashboard_panel.byb_summary.summary_description
        self.assertTrue(dashboard_market_text.is_element_truncated(), msg='Dashboard market text is not truncated')

    def test_006_verify_odds_touchable_area_content(self):
        """
        DESCRIPTION: Verify Odds touchable area content
        EXPECTED: The following information is displayed:
        EXPECTED: * <Corresponding Odds value> with corresponding user format (decimal or fractional)
        EXPECTED: * **PLACE BET** text below
        """
        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')
        odds = self.summary_block.place_bet.value
        self.assertTrue(odds, msg='Can not get odds for given selections')
        self.assertEqual(self.summary_block.place_bet.text, self.expected_default_place_bet_text,
                         msg=f'Place bet button text: "{self.summary_block.place_bet.text}" '
                             f'is not the same as expected: "{self.expected_default_place_bet_text}"')

    def test_007_click_within_dashboard_touchable_area(self):
        """
        DESCRIPTION: Click within Dashboard touchable area
        EXPECTED: * Dashboard touchable area is shown with the following change: 'Close' label with upside down arrow
        EXPECTED: * Dashboard expands with slide animation
        EXPECTED: * Selection lines with information about added selections are displayed below the Dashboard touchable area in the same order they were added
        """
        self.dashboard_panel.byb_summary.open_close_toggle_button.click()
        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded(timeout=13)
        self.assertTrue(is_expanded, msg='Dashboard is not expanded')
        label = self.dashboard_panel.byb_summary.open_close_toggle_button.name
        self.assertEqual(label, vec.yourcall.CLOSE,
                         msg=f'Toggle button label "{label}" is not the same as expected "{vec.yourcall.CLOSE}"')

        self.__class__.outcomes = self.dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'List of outcomes is empty: "{self.outcomes}"')
        dashboard_selections = list(self.outcomes.keys())
        self._logger.debug(f'*** List of outcomes: "{dashboard_selections}"')
        if self.brand == 'ladbrokes':
            self.__class__.match_betting_market_and_selection_name = \
                f'{self.expected_market_sections.match_betting.title()} ' \
                f'{self.match_betting_default_switcher.lower()} - {self.team1.title()}'

            self.__class__.correct_score_market_and_selection_name = \
                f'{self.expected_market_sections.correct_score.title()} ' \
                f'{self.correct_score_default_switcher.lower()} - {self.correct_score_selection}'
        else:
            self.__class__.match_betting_market_and_selection_name = \
                f'{self.expected_market_sections.match_betting.title()} ' \
                f'{self.match_betting_default_switcher.lower()} {self.team1.upper()}'

            self.__class__.correct_score_market_and_selection_name = \
                f'{self.expected_market_sections.correct_score.title()} ' \
                f'{self.correct_score_default_switcher.lower()} {self.correct_score_selection}'

        expected_added_selections = [
            self.match_betting_market_and_selection_name, self.correct_score_market_and_selection_name]
        self._logger.debug(f'*** List of added selections is: "{expected_added_selections}"')

        self.assertListEqual(dashboard_selections, expected_added_selections,
                             msg=f'Lists with outcomes "{dashboard_selections}" are not equal \n'
                                 f'to list of added selections "{expected_added_selections}"')

    def test_008_verify_content_of_selection_lines(self):
        """
        DESCRIPTION: Verify content of selection lines
        EXPECTED: * Name of selection is displayed in the same formats as in step #4
        EXPECTED: * 'Remove' icon is shown on the right
        """
        # content of selections are verified in step 007
        for outcome_name, outcome in self.outcomes.items():
            self.assertTrue(outcome.has_remove_button(), msg=f'Outcome "{outcome_name}" does not have remove icon')

    def test_009_scroll_market_area(self):
        """
        DESCRIPTION: Scroll market area
        EXPECTED: * Market area scrollable
        EXPECTED: * **on mobile** dashboard is sticked to the bottom of the screen
        EXPECTED: * **on tablet/desktop** is sticked to the bottom of market area
        """
        # cannot verify scrolling, it is done implicitly while looking for outcomes in section
        pass

    def test_010_add_one_more_valid_selection_to_dashboard(self):
        """
        DESCRIPTION: Add one more valid selection to Dashboard
        EXPECTED: * Added selections lines are shown
        EXPECTED: * Icon with number of selections is updated
        EXPECTED: * Odds touchable area is updated with odds value
        EXPECTED: * Scroll appears (for 5 and more selections in dashboard)
        """
        # Double chance selection
        double_chance_market = self.get_market(market_name=self.expected_market_sections.double_chance)
        double_chance_selection_names = double_chance_market.set_market_selection(count=1)
        self.assertTrue(double_chance_selection_names, msg='No one selection added to Dashboard')
        self.__class__.initial_counter += 1
        result = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        counter_value = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.summary_counter.value
        self.assertTrue(result, msg=f'Number of added selections "{counter_value}" '
                                    f'is not the same as added "{self.initial_counter}"')

    def test_011_scroll_up_and_down_within_section_with_selections_lines(self):
        """
        DESCRIPTION: Scroll up and down within section with selections lines
        EXPECTED: * Section with selections lines is scrollable
        EXPECTED: * Page content with markets is NOT scrollable
        """
        # cannot verify scrolling, it is done implicitly while looking for outcomes in section
        pass

    def test_012_click_remove_icon_for_the_any_selection_line(self):
        """
        DESCRIPTION: Click 'Remove' icon for the any selection line
        EXPECTED: * Selection is not highlighted within market accordion
        EXPECTED: * Selection is removed from Dashboard
        EXPECTED: * Odds touchable area is shown with updated odds value
        EXPECTED: * Icon with number of selections is updated
        """
        self.__class__.outcomes = self.dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'List of outcomes is empty: "{self.outcomes}"')
        outcome_name, outcome = list(self.outcomes.items())[0]
        outcome.remove_button.click()
        self.__class__.initial_counter -= 1
        result = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        counter_value = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.summary_counter.value
        self.assertTrue(result, msg=f'Number of added selections "{counter_value}" '
                                    f'is not the same as added "{self.initial_counter}"')

    def test_013_click_within_dashboard_touchable_area(self):
        """
        DESCRIPTION: Click within Dashboard touchable area
        EXPECTED: * Dashboard collapses with slide animation
        """
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.open_close_toggle_button.click()
        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded(
            expected_result=False, timeout=15)
        self.assertFalse(is_expanded, msg='Dashboard is not collapsed')

    def test_014_remove_remaining_selections_from_dashboard(self):
        """
        DESCRIPTION: Remove remaining selections from Dashboard
        EXPECTED: * Dashboard disappears with slide animation
        """
        self.dashboard_panel.byb_summary.open_close_toggle_button.click()
        is_expanded = self.site.sport_event_details.tab_content.dashboard_panel.is_expanded(timeout=15)
        self.assertTrue(is_expanded, msg='Dashboard is not expanded')
        self.__class__.outcomes = self.dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'List of outcomes is empty: "{self.outcomes}"')
        self.remove_all_selections_from_dashboard()
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(expected_result=False),
                         msg='Build Your Bet dashboard is still shown')

    def test_015_add_only_one_selection_to_dashboard(self):
        """
        DESCRIPTION: Add only ONE selection to dashboard
        EXPECTED: * Selection appears on sliding dashboard
        EXPECTED: * 'Please add another selection to place the bet' notification is shown above the dashboard as per GD
        """
        self.test_010_add_one_more_valid_selection_to_dashboard()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='Yourcall dashboard is not available')
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        self.assertEqual(dashboard_panel.info_panel.text, vec.yourcall.DASHBOARD_ALERT,
                         msg=f'Infopanel text: "{dashboard_panel.info_panel.text}" '
                         f'is not the same as expected: "{vec.yourcall.DASHBOARD_ALERT}"')
