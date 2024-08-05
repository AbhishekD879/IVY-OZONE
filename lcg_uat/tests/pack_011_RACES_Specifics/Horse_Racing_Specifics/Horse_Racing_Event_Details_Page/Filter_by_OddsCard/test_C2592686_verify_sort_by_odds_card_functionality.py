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
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C2592686_Verify_Sort_By_Odds_Cards_Functionality(BaseRacing):
    """
    TR_ID: C2592686
    NAME: Verify Sort by Odds/Card functionality
    DESCRIPTION: This test case verifies Filter by Odds/Card functionality.
    PRECONDITIONS: Filter by Odds/Card functionality toggle should be enabled in CMS.
    PRECONDITIONS: Odds display settings should be set to "Decimal".
    """
    keep_browser_open = True
    number_of_runners = 10
    non_runner_index = [8, 9]
    suspended_selection_index = 6
    number_of_sp_prices = 2
    selection_to_bet_without = 3
    prices = {0: '1/2', 1: '2/3', 2: '6/11', 3: '1/2', 4: None, 5: '1/3', 6: '2/5', 7: None, 8: '3/5', 9: '2/11'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Horse racing event( <Race event>) with following racer types:
        DESCRIPTION: * Ordinary runners
        DESCRIPTION: * SUSPENDED runners
        DESCRIPTION: * Non-runners
        DESCRIPTION: * SP runners
        DESCRIPTION: * Unnamed favorite, Unnamed 2nd Favorite.
        DESCRIPTION: Go to Oxygen application and navigate to Horse racing landing page.
        DESCRIPTION: Go to <Race event> event details page
        """
        self.__class__.default_market_tab = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        place_insurance = 'insurance_4_places' if self.brand == 'bma' else 'place_insurance_4'
        markets = [
            ('win_only', {'cashout': True}),
            ('betting_without', {'without_runner': self.selection_to_bet_without}),
            ('to_finish_second',),
            (place_insurance,),
            ('top_3_finish',),
        ]

        event = self.ob_config.add_UK_racing_event(markets=markets, number_of_runners=self.number_of_runners,
                                                   unnamed_favorites=True, lp_prices=self.prices)
        sp_event = self.ob_config.add_UK_racing_event(markets=markets, number_of_runners=self.number_of_runners,
                                                      unnamed_favorites=True)
        ft_params = self.ob_config.add_UK_racing_event(number_of_runners=self.number_of_runners,
                                                       forecast_available=True, tricast_available=True)
        self.__class__.eventID = event.event_id
        self.__class__.sp_eventID = sp_event.event_id
        self.__class__.ft_eventID = ft_params.event_id
        self.__class__.selections = list(event.selection_ids['win_or_each_way'].keys())
        prices = dict(self.prices)

        markets.append(('win_or_each_way',))

        for market in markets:
            if market[0] == 'betting_without':
                continue
            # Non Runner
            for index in self.non_runner_index:
                nr_selection_name = list(event.selection_ids[market[0]].keys())[index]
                nr_selection_id = list(event.selection_ids[market[0]].values())[index]

                new_selection_name = f'{nr_selection_name} N/R'
                self.ob_config.change_selection_name(selection_id=nr_selection_id,
                                                     new_selection_name=new_selection_name)
                self.__class__.selections[index] = new_selection_name

            # Suspended
            suspended_selection_id = list(event.selection_ids[market[0]].values())[
                self.suspended_selection_index]
            self.ob_config.change_selection_state(selection_id=suspended_selection_id, displayed=True)

        self.__class__.expected_selections = self.sort_selections_by_price(selections=self.selections, prices=prices,
                                                                           non_runners=self.non_runner_index)

        # Betting Without case
        self.prices.pop(self.selection_to_bet_without - 1)
        bw_prices = dict(self.prices)
        # playing with indexes after popping one price
        for index in range(len(bw_prices.keys())):
            price = bw_prices.pop(list(bw_prices.keys())[0])
            bw_prices[index] = price
        self.__class__.bw_selections = list(event.selection_ids['betting_without'].keys())
        bw_non_runner_index = []
        # Non Runner
        for index in self.non_runner_index:
            index = index - 1 if index > self.selection_to_bet_without - 1 else index
            bw_non_runner_index.append(index)
            nr_selection_name = list(event.selection_ids['betting_without'].keys())[index]
            nr_selection_id = list(event.selection_ids['betting_without'].values())[index]

            new_selection_name = f'{nr_selection_name} N/R'
            self.ob_config.change_selection_name(selection_id=nr_selection_id,
                                                 new_selection_name=new_selection_name)
            self.__class__.bw_selections[index] = new_selection_name

        # Suspended
        suspended_selection_index = self.suspended_selection_index - 1 \
            if self.suspended_selection_index > self.selection_to_bet_without - 1 else self.suspended_selection_index
        suspended_bw_selection_id = list(event.selection_ids['betting_without'].values())[suspended_selection_index]
        self.ob_config.change_selection_state(selection_id=suspended_bw_selection_id, displayed=True)
        self.__class__.expected_bw_selections = self.sort_selections_by_price(selections=self.bw_selections,
                                                                              prices=bw_prices,
                                                                              non_runners=bw_non_runner_index)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_001_navigate_to_filter_by_odds_card_toggle(self):
        """
        DESCRIPTION: Navigate to Filter by Odds/Card toggle
        EXPECTED: <Race event> event details page
        EXPECTED: First available market tab is selected
        EXPECTED: Toggle default value is:'SORT BY: PRICE'
        """
        self.__class__.market_tabs = self.site.racing_event_details.tab_content.event_markets_list.\
            market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found')
        active_tab = self.site.racing_event_details.tab_content.event_markets_list.current_market_tab_name
        self.assertEqual(active_tab, list(self.market_tabs.keys())[0],
                         msg=f'Incorrect market tab which is active.'
                             f'\nActual: "{active_tab}"\nExpected: "{list(self.market_tabs.keys())[0]}"')
        self.assertTrue(self.site.racing_event_details.tab_content.has_sorting_toggle(timeout=20),
                        msg='Failed to display Sorting Toggle')
        self.assertEqual(self.site.racing_event_details.tab_content.sorting_toggle.selected_option,
                         vec.racing.PRICE_SORTING_OPTION_SELECTED.upper(),
                         msg=f'Incorrect sorting toggle default value.\n'
                             f'Actual: "{self.site.racing_event_details.tab_content.sorting_toggle.selected_option}"\n'
                             f'Expected: "{vec.racing.PRICE_SORTING_OPTION_SELECTED.upper()}"')

    def test_002_check_sorting_by_price(self):
        """
        DESCRIPTION: Check race runners sorting.
        DESCRIPTION: Verify race runners sorting order by Price
        EXPECTED: Race runners list is sorted in ascending order by price
        EXPECTED: In case of the same price for 2 or more runners, they are sorted by card number within each other
        EXPECTED: Non-runners are always displayed at the bottom of the runner list
        EXPECTED: Sort by order does not changed after selection suspending
        EXPECTED: SP runners appear at the bottom of the list(but before unnamed favorites)
        EXPECTED: Unnamed Favorites are always displayed last at the bottom of the list
        EXPECTED:                                       (Firstly goes "Unnamed Favorite" then "Unnamed 2nd Favorite"...)
        """
        tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(tab, msg='Events are not found')
        tab_name, tab_content = list(tab.items())[0]
        outcomes = tab_content.items_as_ordered_dict
        actual_selections = list(outcomes.keys())
        self.__class__.expected = ([s.replace(' N/R', '') for s in self.expected_selections])
        self.assertListEqual(actual_selections[:-2], self.expected,
                             msg=f'Incorrect order of selection when sorting by price.\n'
                             f'Actual: {actual_selections[:-2]}\nExpected: {self.expected}')
        self.assertListEqual(actual_selections[-2:], [vec.racing.UNNAMED_FAVORITE, vec.racing.UNNAMED_FAVORITE_2ND],
                             msg=f'Unnamed Favorites should be displayed at the very bottom when sorting by price.\n'
                             f'Actual last displayed selections are: {actual_selections[-2:]}')

    def test_003_check_sorting_by_price_for_different_markets(self):
        """
        DESCRIPTION: Go to other markets like race winner, betting without, win only, etc within <Race event> EDP.
        DESCRIPTION: Verify race runners sorting by price.
        EXPECTED: Race runners list is sorted in ascending order by price
        EXPECTED: In case of the same price for 2 or more runners, they are sorted by card number within each other
        EXPECTED: Non-runners are always displayed at the bottom of the runner list
        EXPECTED: Sort by order does not changed after selection suspending
        EXPECTED: SP runners appear at the bottom of the list(but before unnamed favorites)
        EXPECTED: Unnamed Favorites are always displayed last at the bottom of the list
        EXPECTED: (Firstly goes "Unnamed Favorite" then "Unnamed 2nd Favorite"...)
        """
        for market_tab in self.market_tabs:
            if market_tab == self.default_market_tab:
                continue  # verified in the previous step

            self.market_tabs[market_tab].click()
            self.assertTrue(self.site.racing_event_details.tab_content.has_sorting_toggle(),
                            msg='Failed to display Sorting Toggle')
            self.assertEqual(self.site.racing_event_details.tab_content.sorting_toggle.selected_option,
                             vec.racing.PRICE_SORTING_OPTION_SELECTED.upper(),
                             msg=f'Incorrect sorting toggle default value.\n'
                                 f'Actual: "{self.site.racing_event_details.tab_content.sorting_toggle.selected_option}"'
                                 f'\nExpected: "{vec.racing.PRICE_SORTING_OPTION_SELECTED.upper()}"')

            tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(tab, msg='Events are not found')
            tab_name, tab_content = list(tab.items())[0]
            outcomes = tab_content.items_as_ordered_dict
            actual_selections = list(outcomes.keys())

            self.__class__.betting_without = vec.racing.RACING_EDP_BETTING_WITHOUT_SHORTCUT

            if self.betting_without not in market_tab:
                self.assertListEqual(actual_selections, self.expected,
                                     msg=f'Incorrect order of selection when sorting by price. Market is {market_tab}\n'
                                         f'Actual: {actual_selections}\nExpected: {self.expected}')
            else:
                bet_without_list = ([s.replace(' N/R', '') for s in self.expected_bw_selections])
                self.assertListEqual(actual_selections, bet_without_list,
                                     msg=f'Incorrect order of selection when sorting by price. Market is "BETTING W/O"\n'
                                     f'Actual: {actual_selections}\nExpected: {bet_without_list}')

    def test_004_check_sorting_by_price_for_forecast_tricast_markets(self):
        """
        DESCRIPTION: Go to markets like forecast & tricast within <Race event> event details page.
        DESCRIPTION: Verify that Filter by Odds/Card toggle is not applied there
        EXPECTED: Filter by Odds/Card toggle is not applied for forecast & tricast markets
        """
        self.navigate_to_edp(event_id=self.ft_eventID, sport_name='horse-racing')
        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found')

        for market_tab_name, market_tab in market_tabs.items():
            if market_tab_name in [vec.racing.RACING_EDP_FORECAST_MARKET_TAB, vec.racing.RACING_EDP_TRICAST_MARKET_TAB]:
                market_tab.click()
                self.assertFalse(self.site.racing_event_details.tab_content.has_sorting_toggle(expected_result=False),
                                 msg=f'Sorting Toggle is unexpectedly displayed for "{market_tab_name}" market ')

    def test_005_select_sort_by_race_card(self):
        """
        DESCRIPTION: Navigate to event market from step 2 -> navigate to Filter by Odds/Card toggle and set value to
        DESCRIPTION: "'SORT BY: RACECARD'"
        EXPECTED: Toggle value is:'SORT BY: RACECARD'
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        self.site.racing_event_details.tab_content.choose_sorting_option(option=vec.racing.CARD_SORTING_OPTION)
        self.assertEqual(self.site.racing_event_details.tab_content.sorting_toggle.selected_option,
                         vec.racing.CARD_SORTING_OPTION_SELECTED.upper(),
                         msg=f'Incorrect sorting toggle default value.\n'
                             f'Actual: "{self.site.racing_event_details.tab_content.sorting_toggle.selected_option}"\n'
                             f'Expected: "{vec.racing.CARD_SORTING_OPTION_SELECTED.upper()}"')

    def test_006_check_sorting_by_race_card(self):
        """
        DESCRIPTION: Verify race runners sorting order by Racecard.
        EXPECTED: Toggle value is 'SORT BY: RACECARD' in other market race card
        EXPECTED: Race runners list is sorted in ascending order by racecard(card number)
        EXPECTED: SP runners, SUSPENDED & Non-runners are displaying in racecard number order
        EXPECTED: Unnamed Favorites are always displayed last at the bottom of the list
        EXPECTED: (Firstly goes "Unnamed Favorite" then "Unnamed 2nd Favorite"...)
        """
        tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(tab, msg='Events are not found')
        tab_name, tab_content = list(tab.items())[0]
        outcomes = tab_content.items_as_ordered_dict
        actual_selections = list(outcomes.keys())
        self.__class__.expected_selectionslist = ([s.replace(' N/R', '') for s in self.selections])
        self.assertListEqual(actual_selections, self.expected_selectionslist,
                             msg=f'Incorrect order of selection when sorting by race card.\n'
                             f'Actual: {actual_selections}\nExpected: {self.expected_selectionslist}')

    def test_007_check_sorting_by_race_card_for_different_markets(self):
        """
        DESCRIPTION: Go to other markets like race winner, betting without, win only, etc within <Race event> EDP.
        DESCRIPTION: Verify race runners sorting by race card.
        EXPECTED: Toggle value is 'SORT BY: RACECARD' in other market race card
        EXPECTED: Race runners list is sorted in ascending order by racecard(card number)
        EXPECTED: SP runners, SUSPENDED & Non-runners are displaying in racecard number order
        EXPECTED: Unnamed Favorites are always displayed last at the bottom of the list
        EXPECTED: (Firstly goes "Unnamed Favorite" then "Unnamed 2nd Favorite"...)
        """
        self.__class__.market_tabs = \
            self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found')

        for market_tab in self.market_tabs:
            if market_tab == self.default_market_tab:
                continue  # verified in the previous step

            self.market_tabs[market_tab].click()
            self.assertTrue(self.site.racing_event_details.tab_content.has_sorting_toggle(),
                            msg='Failed to display Sorting Toggle')
            self.assertEqual(self.site.racing_event_details.tab_content.sorting_toggle.selected_option,
                             vec.racing.CARD_SORTING_OPTION_SELECTED.upper(),
                             msg=f'Incorrect sorting toggle default value.\n'
                                 f'Actual: "{self.site.racing_event_details.tab_content.sorting_toggle.selected_option}"\n'
                                 f'Expected: "{vec.racing.CARD_SORTING_OPTION_SELECTED.upper()}"')

            tab = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(tab, msg='Events are not found')
            tab_name, tab_content = list(tab.items())[0]
            outcomes = tab_content.items_as_ordered_dict
            actual_selections = list(outcomes.keys())

            if self.betting_without not in market_tab:
                self.assertListEqual(actual_selections, self.expected_selectionslist[:-2],
                                     msg=f'Incorrect order of selection when sorting by price. Market is {market_tab}\n'
                                     f'Actual: {actual_selections}\nExpected: {self.expected_selectionslist[:-2]}')
            else:
                racecard_bet_without_list = ([s.replace(' N/R', '') for s in self.bw_selections])
                self.assertListEqual(actual_selections, racecard_bet_without_list,
                                     msg=f'Incorrect order of selection when sorting by price. Market is "BETTING W/O"\n'
                                     f'Actual: {actual_selections}\nExpected: {racecard_bet_without_list}')

    def test_008_check_sorting_by_race_card_for_different_markets(self):
        """
        DESCRIPTION: Navigate to the race where all prices are SP
        DESCRIPTION: Verify that it is no sorting toggle available if all prices are SP
        EXPECTED: Sorting toggle is unavailable if all prices are SP.
        """
        self.navigate_to_edp(event_id=self.sp_eventID, sport_name='horse-racing')

        self.__class__.market_tabs = \
            self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No market tabs found')

        active_tab = self.site.racing_event_details.tab_content.event_markets_list.current_market_tab_name
        self.assertEqual(active_tab, list(self.market_tabs.keys())[0],
                         msg=f'Incorrect market tab which is active.'
                             f'\nActual: "{active_tab}"\nExpected: "{list(self.market_tabs.keys())[0]}"')

        for market_tab in self.market_tabs:
            self.market_tabs[market_tab].click()
            self.assertFalse(self.site.racing_event_details.tab_content.has_sorting_toggle(expected_result=False),
                             msg=f'Sorting Toggle is unexpectedly displayed for event with all SP prices. '
                                 f'Market is {market_tab}')

    def test_009_check_sorting_by_price_for_decimal_format(self):
        """
        DESCRIPTION: Switch to Decimal format of prices
        EXPECTED: Sorting is the same as for Fractional
        """
        self.site.login()
        self.site.wait_logged_in()
        self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.test_001_navigate_to_filter_by_odds_card_toggle()
        self.test_002_check_sorting_by_price()
        self.test_003_check_sorting_by_price_for_different_markets()
