import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2592686_Verify_Sort_by_Odds_Card_functionality(Common):
    """
    TR_ID: C2592686
    NAME: Verify Sort by Odds/Card functionality
    DESCRIPTION: This test case verifies Filter by Odds/Card functionality.
    PRECONDITIONS: 1. Filter by Odds/Card functionality toggle should be enabled in CMS
    PRECONDITIONS: 2. Odds display settings should be set to "Decimal"
    PRECONDITIONS: 3. Create Horse racing event( <Race event>) with following racer types :
    PRECONDITIONS: - Ordinary runners
    PRECONDITIONS: - SUSPENDED runners
    PRECONDITIONS: - Non-runners
    PRECONDITIONS: - SP runners
    PRECONDITIONS: - Unnamed favorite, Unnamed 2nd Favorite.
    PRECONDITIONS: 4. Go to Oxygen application and navigate to Horse racing landing page
    PRECONDITIONS: 5. Go to <Race event> event details page
    """
    keep_browser_open = True

    def test_001_navigate_to_filter_by_oddscard_toggle(self):
        """
        DESCRIPTION: Navigate to Filter by Odds/Card toggle
        EXPECTED: * <Race event> event details page
        EXPECTED: * First available market tab is selected
        EXPECTED: * Toggle default value is: 'SORT BY: PRICE'
        """
        pass

    def test_002_check_race_runners_sortingverify_race_runners_sorting_order_by_price(self):
        """
        DESCRIPTION: Check race runners sorting.
        DESCRIPTION: Verify race runners sorting order by Price
        EXPECTED: * Race runners list is sorted in ascending order by price
        EXPECTED: * In case of the same price for 2 or more runners, they are sorted by card number within each other
        EXPECTED: * Non-runners are always displayed at the bottom of the runner list (if there are several non-runners they are sorted by cardnumber)
        EXPECTED: * Sort by order does not changed after selection suspending
        EXPECTED: * SP runners appear at the bottom of the list(but before unnamed favorites )
        EXPECTED: * Unnamed Favorites are always displayed last at the bottom of the list(Firstly goes "Unnamed Favorite" then "Unnamed 2nd Favorite"...)
        """
        pass

    def test_003_go_to_other_markets_like_race_winner_betting_without_win_only_etc_within_race_event_event_details_pageverify_race_runners_sorting_by_price(self):
        """
        DESCRIPTION: Go to other markets like race winner, betting without, win only, etc within <Race event> event details page
        DESCRIPTION: Verify race runners sorting by price
        EXPECTED: * Toggle value is 'SORT BY: PRICE' in other market race card
        EXPECTED: * Race runners list is sorted in ascending order by price
        EXPECTED: * In case of the same price for 2 or more runners, they are sorted by card number within each other
        EXPECTED: * Non-runners are always displayed at the bottom of the runner list
        EXPECTED: * Sort by order does not changed after selection suspending
        EXPECTED: * SP runners appear at the bottom of the list(but before unnamed favorites )
        EXPECTED: * Unnamed Favorites are always displayed last at the bottom of the list(Firstly goes "Unnamed Favorite" then "Unnamed 2nd Favorite"...)
        EXPECTED: If there are not prices, race runners should be sorted by following order:
        EXPECTED: 1. LP
        EXPECTED: 2. SP
        EXPECTED: 3, NR
        EXPECTED: 4. Fav
        """
        pass

    def test_004_to_be_implemented_go_to_markets_like_forecast__tricast_within_race_event_event_details_pageverify_that_filter_by_oddscard_toggle_is_not_applied_there(self):
        """
        DESCRIPTION: [To be implemented] Go to markets like forecast & tricast within <Race event> event details page
        DESCRIPTION: Verify that Filter by Odds/Card toggle is not applied there
        EXPECTED: * Filter by Odds/Card toggle is not applied for forecast & tricast markets
        """
        pass

    def test_005_navigate_to_event_market_from_step_2___navigate_to_filter_by_oddscard_toggle_and_set_value_to_sort_by_racecard(self):
        """
        DESCRIPTION: Navigate to event market from step 2 -> navigate to Filter by Odds/Card toggle and set value to "'SORT BY: RACECARD'"
        EXPECTED: * Toggle value is: 'SORT BY: RACECARD'
        """
        pass

    def test_006_verify_race_runners_sorting_order_by_racecard(self):
        """
        DESCRIPTION: Verify race runners sorting order by Racecard
        EXPECTED: * Toggle value is 'SORT BY: RACECARD' in other market race card
        EXPECTED: * Race runners list is sorted in ascending order by racecard(card number)
        EXPECTED: * SP runners, SUSPENDED & Non-runners are displaying in racecard number order
        EXPECTED: * Unnamed Favorites are always displayed last at the bottom of the list(Firstly goes "Unnamed Favorite" then "Unnamed 2nd Favorite"...)
        """
        pass

    def test_007_go_to_other_markets_like_race_winner_betting_without_win_only_etcverify_sorting_by_racecard_on_other_market_tabs(self):
        """
        DESCRIPTION: Go to other markets like race winner, betting without, win only, etc
        DESCRIPTION: Verify sorting by racecard on other market tabs
        EXPECTED: * Race runners list is sorted in ascending order by racecard(card number)
        EXPECTED: * SP runners, SUSPENDED & Non-runners are always displayed at the bottom of the runner list
        EXPECTED: * Unnamed Favorites are always displayed last at the bottom of the list(Firstly goes "Unnamed Favorite" then "Unnamed 2nd Favorite"...)
        """
        pass

    def test_008_navigate_to_the_race_where_all_prices_are_spverify_that_it_is_no_sorting_toggle_available_if_all_prices_are_sp(self):
        """
        DESCRIPTION: Navigate to the race where all prices are SP
        DESCRIPTION: Verify that it is no sorting toggle available if all prices are SP
        EXPECTED: * Sorting toggle is unavailable if all prices are SP
        """
        pass

    def test_009_switch_to_decimal_format_of_prices(self):
        """
        DESCRIPTION: Switch to Decimal format of prices
        EXPECTED: Sorting is the same as for Fractional
        """
        pass
