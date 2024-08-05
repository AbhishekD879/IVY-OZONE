import pytest
from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # can not create events and suspend the events
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.football
@pytest.mark.event_details
@pytest.mark.markets
@pytest.mark.sports
@pytest.mark.slow
@pytest.mark.medium
@vtest
class Test_C822274_Verify_Correct_Score_market_with_incomplete_data(BaseSportTest):
    """
    TR_ID: C822274
    NAME: Verify Correct Score market with incomplete data
    DESCRIPTION: This test case verifies Correct Score market on Football event details page in the following cases:
    DESCRIPTION: * if all selections for Team 1 have been disabled (undisplayed or deleted)
    DESCRIPTION: * if all selections for Team 2 have been disabled (undisplayed or deleted)
    DESCRIPTION: * if all selections for both teams have been disabled (undisplayed or deleted)
    DESCRIPTION: * if all "Draw" selections have been disabled (undisplayed or deleted)
    PRECONDITIONS: There has to be a Football event with Correct Score market.
    PRECONDITIONS: Data should be available for Correct Score with H/D/A - Any other.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: In TI create football sport event
        EXPECTED: Event was created
        """
        event = self.ob_config.add_autotest_premier_league_football_event(markets=[('correct_score',
                                                                                    {'cashout': True})],
                                                                          selections_number=4)
        self.__class__.eventID = event.event_id
        self.__class__.event_name = '%s v %s' % (event.team1, event.team2)
        self.__class__.selection_ids = list(event.selection_ids['correct_score'].values())
        self.__class__.home_selection_id = list(event.selection_ids['correct_score'].values())[:4]
        self.__class__.away_selection_id = list(event.selection_ids['correct_score'].values())[4:8]
        self.__class__.draw_selection_id = list(event.selection_ids['correct_score'].values())[8:]

        correct_score_prices = self.ob_config.event.correct_score_prices

        home_score_prices = correct_score_prices[0]
        sorted_home_score_prices = OrderedDict(sorted(home_score_prices[1].items()))
        self.__class__.home_prices = list(sorted_home_score_prices.values())

        away_score_prices = correct_score_prices[1]
        sorted_away_score_prices = OrderedDict(sorted(away_score_prices[1].items()))
        self.__class__.away_prices = list(sorted_away_score_prices.values())

        draw_score_prices = correct_score_prices[2]
        sorted_draw_score_prices = OrderedDict(sorted(draw_score_prices[1].items()))
        self.__class__.draw_prices = list(sorted_draw_score_prices.values())

        expected_goals = []
        for result in correct_score_prices:
            for score in list(result[1].keys()):
                expected_goals.append(score[0])
        self.__class__.expected_goals_quantity = sorted(list(set(expected_goals)))

    def test_001_open_event_details_page_of_the_event_from_preconditions(self):
        """
        DESCRIPTION: Open event details page of the event from Preconditions
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(self.markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)

    def test_002_select_all_markets_tab(self):
        """
        DESCRIPTION: Select "All Markets" tab
        EXPECTED: "MAIN MARKETS" ( **Mobile** ) / "MAIN" ( **Desktop** ) tab is opened
        EXPECTED: First 2 sections ( **Mobile** ) / 4 sections ( **Desktop** ) are expanded by default
        """
        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')
        if self.device_type == 'mobile':
            for market_name, market in list(self.markets_list.items())[:2]:
                market.scroll_to()
                self.assertTrue(market.is_expanded(),
                                msg=f'The section "{market_name}" is not expanded by default')
        else:
            expanded_markets = len(
                [market_name for market_name, market in self.markets_list.items() if market.is_expanded()])
            expected_count = len(self.markets_list.items()) if len(self.markets_list.items()) < 2 else 2
            self.assertEqual(expanded_markets, expected_count,
                             msg=f'Found "{expanded_markets}" expanded markets while expected "{expected_count}"')
        self.__class__.market_name = self.expected_market_sections.correct_score

    def test_003_verify_correct_score_section(self):
        """
        DESCRIPTION: Verify "Correct Score" section
        EXPECTED: * Pickers for Home Team and Away Team are present, active and contain data in them;
        EXPECTED: * Price/odds button next to the pickers shows valid odds;
        EXPECTED: * After expanding the section, there are 3 columns with corresponding results for "Home", "Draw" and "Away" selections
        """
        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.correct_score = self.markets_list.get(self.market_name)
        self.assertTrue(self.correct_score,
                        msg=f'"{self.market_name}" section is not found in "{self.markets_list.keys()}"')
        self.assertTrue(self.correct_score.team_home_scores, msg='Home team result drop-down is not present')
        self.assertTrue(self.correct_score.team_away_scores, msg='Away team result drop-down is not present')

        self.assertEquals(self.correct_score.team_home_scores.selected_item, '0',
                          msg='Default value for home team result drop-down is not "0"')
        self.assertEquals(self.correct_score.team_away_scores.selected_item, '0',
                          msg='Default value for away team result drop-down is not "0"')

        self.assertEquals(self.correct_score.combined_outcome_button.name, self.draw_prices[0],
                          msg=f'Outcome price "{self.correct_score.combined_outcome_button.name}" '
                              f'is not the same as expected "{self.draw_prices[0]}" in case of invalid result selection')

        self.assertTrue(self.correct_score.has_show_all_button, msg='"SHOW ALL" button is not present')

        self.correct_score.show_all_button.click()
        self.assertTrue(self.correct_score.has_show_less_button(), msg='"SHOW LESS" button is not present')

        self.__class__.correct_score = self.markets_list.get(self.market_name)

        home_actual_prices = self.correct_score.outcome_table.home_outcomes.outcomes_prices
        self.assertEquals(self.home_prices, home_actual_prices,
                          msg=f'Expected prices for home team: "{self.home_prices}"'
                              f' are not equal to actual: "{home_actual_prices}"')

        draw_actual_prices = self.correct_score.outcome_table.draw_outcomes.outcomes_prices
        self.assertEquals(self.draw_prices, draw_actual_prices,
                          msg=f'Expected prices for home team: "{self.draw_prices}"'
                              f' are not equal to actual: "{draw_actual_prices}"')

        away_actual_prices = self.correct_score.outcome_table.away_outcomes.outcomes_prices
        self.assertEquals(self.away_prices, away_actual_prices,
                          msg=f'Expected prices for home team: "{self.away_prices}"'
                              f' are not equal to actual: "{away_actual_prices}"')

    def test_004_undisplay_all_available_selections_related_to_home_team_in_ti_and_save(self, status=False, team=None):
        """
        DESCRIPTION: Undisplay **all** available selections related to Home Team in TI and save
        EXPECTED: Selections are undisplayed in TI
        """
        if not status and team is None:
            team = self.home_selection_id
        for index in team:
            self.ob_config.change_selection_state(selection_id=index, displayed=status, active=True)

    def test_005_reload_the_event_details_page_and_verify_correct_score_section(self, team=None):
        """
        DESCRIPTION: Reload the event details page and verify "Correct Score" section
        EXPECTED: * Pickers for both teams are still present and populated with data
        EXPECTED: * After expanding the section, there are only 2 columns with price/odds buttons ("Draw" and "Away Team" correspondingly)
        """
        self.test_001_open_event_details_page_of_the_event_from_preconditions()
        self.test_002_select_all_markets_tab()

        self.__class__.correct_score = self.markets_list.get(self.market_name)
        self.assertTrue(self.correct_score,
                        msg=f'"{self.market_name}" section is not found in "{self.markets_list.keys()}"')
        self.assertTrue(self.correct_score.team_away_scores, msg='Away team result drop-down is not present')
        self.assertEquals(self.correct_score.team_away_scores.selected_item, '0',
                          msg='Default value for away team result drop-down is not "0"')

        if team is None:
            self.assertEquals(self.correct_score.combined_outcome_button.name, self.draw_prices[0],
                              msg=f'Outcome price "{self.correct_score.combined_outcome_button.name}" '
                                  f'is not the same as expected "{self.draw_prices[0]}" in case of invalid result '
                                  f'selection')

        self.assertTrue(self.correct_score.has_show_all_button, msg='"SHOW ALL" button is not present')

        self.correct_score.show_all_button.click()
        self.assertTrue(self.correct_score.has_show_less_button(), msg='"SHOW LESS" button is not present')

    def test_006_select_in_the_drop_down_picker_any_value_for_home_team_and_a_value_for_away_team_which_satisfies_the_following_conditions_it_should_not_be_a_draw_eg_not_1_1_or_2_2_etc_value_selected_for_away_team_should_be_smaller_than_value_selected_for_the_home_team_eg_not_1_5_but_5_1(
            self, team=None):
        """
        DESCRIPTION: Select in the drop-down picker any value for Home Team and a value for Away Team which satisfies the following conditions:
        DESCRIPTION: * It should **not** be a draw (e.g., NOT 1-1 or 2-2 etc.)
        DESCRIPTION: * Value selected for Away Team should be **smaller** than value selected for the Home Team (e.g., NOT 1-5 BUT 5-1)
        EXPECTED: Values are selected
        """
        self.__class__.team_a_scores = self.correct_score.team_away_scores
        self.__class__.team_h_scores = self.correct_score.team_home_scores
        if team is None or team == "home":
            self.team_h_scores.select_score_by_text(text='3')
            self.team_a_scores.select_score_by_text(text='2')
            self.__class__.correct_score = self.markets_list.get(self.market_name)
            self.assertEquals(self.correct_score.team_home_scores.selected_item, '3',
                              msg='Default value for home team result drop-down is not "3"')
            self.assertEquals(self.correct_score.team_away_scores.selected_item, '2',
                              msg='Default value for away team result drop-down is not "2"')
        elif team == "away":
            self.team_h_scores.select_score_by_text(text='2')
            self.team_a_scores.select_score_by_text(text='3')
            self.__class__.correct_score = self.markets_list.get(self.market_name)
            self.assertEquals(self.correct_score.team_away_scores.selected_item, '3',
                              msg='Default value for home team result drop-down is not "3"')
            self.assertEquals(self.correct_score.team_home_scores.selected_item, '2',
                              msg='Default value for away team result drop-down is not "2"')
        else:
            self.team_h_scores.select_score_by_text(text='1')
            self.team_a_scores.select_score_by_text(text='2')
            self.__class__.correct_score = self.markets_list.get(self.market_name)
            self.assertEquals(self.correct_score.team_home_scores.selected_item, '1',
                              msg='Default value for away team result drop-down is not "1"')
            self.assertEquals(self.correct_score.team_away_scores.selected_item, '2',
                              msg='Default value for home team result drop-down is not "2"')

    def test_007_check_the_priceodds_button_next_to_the_pickers(self):
        """
        DESCRIPTION: Check the price/odds button next to the pickers
        EXPECTED: * Price/odds button is disabled
        EXPECTED: * Price/odds button shows 'N/A' text
        """
        add_to_betslip_button = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict[
            self.market_name].add_to_betslip_button.name
        self.assertEqual(add_to_betslip_button, "N/A",
                         msg=f'Add to Betslip button is not disabled "{add_to_betslip_button}"')

    def test_008_change_the_value_for_home_team_or_away_team_to_make_a_draw(self):
        """
        DESCRIPTION: Change the value for Home Team or Away Team to make a draw
        EXPECTED: Values are changed
        """
        self.team_h_scores.select_score_by_text(text='1')
        self.team_a_scores.select_score_by_text(text='1')

    def test_009_check_the_priceodds_button_next_to_the_pickers(self):
        """
        DESCRIPTION: Check the price/odds button next to the pickers
        EXPECTED: * Price/odds button is enabled
        EXPECTED: * Price/odds button shows correct price (the same as for the corresponding draw in the table below the picker when all selections are shown)
        EXPECTED: * Price/odds button can be selected and corresponding selection is added to the betslip
        """
        self.__class__.correct_score = self.markets_list.get(self.market_name)
        self.assertEquals(self.correct_score.team_home_scores.selected_item, '1',
                          msg='Default value for home team result drop-down is not "1"')
        self.assertEquals(self.correct_score.team_away_scores.selected_item, '1',
                          msg='Default value for away team result drop-down is not "1"')
        add_to_betslip_button = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict[
            self.market_name].add_to_betslip_button.name
        self.assertNotEqual(add_to_betslip_button, "N/A",
                            msg=f'Add to Betslip button is not disabled "{add_to_betslip_button}"')

    def test_010_change_the_value_for_away_team_to_be_greater_than_value_for_home_team(self, team=None):
        """
        DESCRIPTION: Change the value for Away Team to be **greater** than value for Home Team
        EXPECTED: Values are changed
        """
        if team is None:
            self.team_h_scores.select_score_by_text(text='1')
            self.team_a_scores.select_score_by_text(text='3')
            self.__class__.correct_score = self.markets_list.get(self.market_name)
            self.assertEquals(self.correct_score.team_home_scores.selected_item, '1',
                              msg='Default value for home team result drop-down is not "1"')
            self.assertEquals(self.correct_score.team_away_scores.selected_item, '3',
                              msg='Default value for away team result drop-down is not "3"')
        else:
            self.team_h_scores.select_score_by_text(text='2')
            self.team_a_scores.select_score_by_text(text='2')
            self.__class__.correct_score = self.markets_list.get(self.market_name)
            self.assertEquals(self.correct_score.team_home_scores.selected_item, '2',
                              msg='Default value for home team result drop-down is not "2"')
            self.assertEquals(self.correct_score.team_away_scores.selected_item, '2',
                              msg='Default value for away team result drop-down is not "2"')

    def test_011_check_the_priceodds_button_next_to_the_pickers(self):
        """
        DESCRIPTION: Check the price/odds button next to the pickers
        EXPECTED: * Price/odds button is enabled
        EXPECTED: * Price/odds button shows correct price (the same as for the corresponding selection in the table below the picker when all selections are shown)
        EXPECTED: * Price/odds button can be selected and corresponding selection is added to the betslip
        """
        add_to_betslip_button = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict[self.market_name].add_to_betslip_button.name
        self.assertNotEqual(add_to_betslip_button, "N/A",
                            msg=f'Add to Betslip button is not disabled "{add_to_betslip_button}"')

    def test_012_display_back_the_selections_for_the_home_team_in_ti_and_reload_the_event_details_pageverify_correct_score_section(
            self, selection_id=None):
        """
        DESCRIPTION: Display back the selections for the Home Team in TI and reload the event details page
        DESCRIPTION: Verify "Correct Score" section
        EXPECTED: * 3 columns are shown again in the table with all selections
        EXPECTED: * "N/A" text on the price/odds button next to the pickers is shown only in that case when selection is not present in the table
        EXPECTED: * Everything works in the same way as it used to work before selections were undisplayed
        """
        if selection_id is None:
            selection_id = self.home_selection_id
        self.test_004_undisplay_all_available_selections_related_to_home_team_in_ti_and_save(status=True,
                                                                                             team=selection_id)
        self.test_001_open_event_details_page_of_the_event_from_preconditions()
        self.test_002_select_all_markets_tab()

    def test_013_repeat_steps_4_12_for_away_team(self):
        """
        DESCRIPTION: Repeat steps 4-12 for Away Team
        EXPECTED:
        """
        self.test_004_undisplay_all_available_selections_related_to_home_team_in_ti_and_save(status=False,
                                                                                             team=self.away_selection_id)
        self.test_005_reload_the_event_details_page_and_verify_correct_score_section()
        self.test_006_select_in_the_drop_down_picker_any_value_for_home_team_and_a_value_for_away_team_which_satisfies_the_following_conditions_it_should_not_be_a_draw_eg_not_1_1_or_2_2_etc_value_selected_for_away_team_should_be_smaller_than_value_selected_for_the_home_team_eg_not_1_5_but_5_1(
            team="away")
        self.test_007_check_the_priceodds_button_next_to_the_pickers()
        self.test_008_change_the_value_for_home_team_or_away_team_to_make_a_draw()
        self.test_009_check_the_priceodds_button_next_to_the_pickers()
        self.test_010_change_the_value_for_away_team_to_be_greater_than_value_for_home_team()
        self.test_011_check_the_priceodds_button_next_to_the_pickers()
        self.test_012_display_back_the_selections_for_the_home_team_in_ti_and_reload_the_event_details_pageverify_correct_score_section(
            selection_id=self.away_selection_id)

    def test_014_repeat_steps_4_12_for_both_teams_at_the_same_time(self):
        """
        DESCRIPTION: Repeat steps 4-12 for both teams at the same time
        EXPECTED:
        """
        self.test_004_undisplay_all_available_selections_related_to_home_team_in_ti_and_save(status=False,
                                                                                             team=self.home_selection_id)
        self.test_004_undisplay_all_available_selections_related_to_home_team_in_ti_and_save(status=False,
                                                                                             team=self.away_selection_id)
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=30)
        self.test_005_reload_the_event_details_page_and_verify_correct_score_section()
        if self.device_type != 'mobile':
            self.test_006_select_in_the_drop_down_picker_any_value_for_home_team_and_a_value_for_away_team_which_satisfies_the_following_conditions_it_should_not_be_a_draw_eg_not_1_1_or_2_2_etc_value_selected_for_away_team_should_be_smaller_than_value_selected_for_the_home_team_eg_not_1_5_but_5_1(
                team="draw")
        else:
            self.test_006_select_in_the_drop_down_picker_any_value_for_home_team_and_a_value_for_away_team_which_satisfies_the_following_conditions_it_should_not_be_a_draw_eg_not_1_1_or_2_2_etc_value_selected_for_away_team_should_be_smaller_than_value_selected_for_the_home_team_eg_not_1_5_but_5_1(
                team="home")
        self.test_007_check_the_priceodds_button_next_to_the_pickers()
        self.test_008_change_the_value_for_home_team_or_away_team_to_make_a_draw()
        self.test_009_check_the_priceodds_button_next_to_the_pickers()
        self.test_010_change_the_value_for_away_team_to_be_greater_than_value_for_home_team(team="draw")
        self.test_011_check_the_priceodds_button_next_to_the_pickers()
        self.test_012_display_back_the_selections_for_the_home_team_in_ti_and_reload_the_event_details_pageverify_correct_score_section(
            selection_id=self.home_selection_id)
        self.test_012_display_back_the_selections_for_the_home_team_in_ti_and_reload_the_event_details_pageverify_correct_score_section(
            selection_id=self.away_selection_id)

    def test_015_repeat_steps_4_12_for_draw_selections(self):
        """
        DESCRIPTION: Repeat steps 4-12 for Draw selections
        EXPECTED:
        """
        self.test_004_undisplay_all_available_selections_related_to_home_team_in_ti_and_save(status=False,
                                                                                             team=self.draw_selection_id)
        self.device.refresh_page()
        self.site.wait_content_state_changed(timeout=30)
        self.test_005_reload_the_event_details_page_and_verify_correct_score_section(team="draw")
        if self.device_type != 'mobile':
            self.test_006_select_in_the_drop_down_picker_any_value_for_home_team_and_a_value_for_away_team_which_satisfies_the_following_conditions_it_should_not_be_a_draw_eg_not_1_1_or_2_2_etc_value_selected_for_away_team_should_be_smaller_than_value_selected_for_the_home_team_eg_not_1_5_but_5_1(
                team="home")
        else:
            self.test_006_select_in_the_drop_down_picker_any_value_for_home_team_and_a_value_for_away_team_which_satisfies_the_following_conditions_it_should_not_be_a_draw_eg_not_1_1_or_2_2_etc_value_selected_for_away_team_should_be_smaller_than_value_selected_for_the_home_team_eg_not_1_5_but_5_1(
                team="draw")
        self.test_007_check_the_priceodds_button_next_to_the_pickers()
        self.test_008_change_the_value_for_home_team_or_away_team_to_make_a_draw()
        self.test_009_check_the_priceodds_button_next_to_the_pickers()
        self.test_010_change_the_value_for_away_team_to_be_greater_than_value_for_home_team(team="home")
        self.test_011_check_the_priceodds_button_next_to_the_pickers()
        self.test_012_display_back_the_selections_for_the_home_team_in_ti_and_reload_the_event_details_pageverify_correct_score_section()

    def test_016_repeat_this_test_case_all_over_again_but_this_time_delete_selections_in_ti_instead_of_undisplaying_them(
            self):
        """
        DESCRIPTION: Repeat this test case all over again, but this time **delete** selections in TI instead of undisplaying them
        EXPECTED:
        """
        for index in self.selection_ids:
            self.ob_config.change_selection_state(selection_id=index, displayed=False, active=True)
        # cannot automate further steps after market selections deleted market will no longer be available on UI
