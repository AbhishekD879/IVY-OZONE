import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870208_PUSh_Verify_that_for_all_markets_use_is_able_to_see_Price_change_with_push_and_when_user_taps_on_odds_selection_is_clickable_changes_to_green_and_is_added_to_bet_slip_Verify_that_Market_drop_off_with_Push_at_the_right_time(Common):
    """
    TR_ID: C44870208
    NAME: PUSh : "Verify that for all markets, use is able to see Price change with push and when user taps on odds, selection is clickable (changes to green) and is added to bet slip. Verify that Market drop off with Push at the right time."
    DESCRIPTION: "Verify that for all markets, use is able to see Price change with push and when user taps on odds, selection is clickable (changes to green) and is added to bet slip.
    DESCRIPTION: Verify that Market drop off with Push at the right time."
    PRECONDITIONS: Price change , Market drop off with Push
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage is opened
        """
        pass

    def test_002_verify_price_change_for_all_inplay_events_on_homepage_sports_landing_page_and_edp(self):
        """
        DESCRIPTION: Verify Price change for all inplay events on HomePage, Sports landing page and EDP
        EXPECTED: Price change with Push successfully
        """
        pass

    def test_003_verify_when_user_taps_on_odds_selection_is_clickablechanges_to_green(self):
        """
        DESCRIPTION: Verify when user taps on odds, selection is clickable(changes to green)
        EXPECTED: Price is highlighted in green
        """
        pass

    def test_004_verify_selected_selections_are_added_to_quickbetbetslip(self):
        """
        DESCRIPTION: Verify selected selections are added to Quickbet/Betslip
        EXPECTED: Selections are added successfully
        """
        pass

    def test_005_verify_that_market_drop_off_with_push_at_the_right_time(self):
        """
        DESCRIPTION: Verify that Market drop off with Push at the right time
        EXPECTED: Market drop off successfully
        """
        pass
