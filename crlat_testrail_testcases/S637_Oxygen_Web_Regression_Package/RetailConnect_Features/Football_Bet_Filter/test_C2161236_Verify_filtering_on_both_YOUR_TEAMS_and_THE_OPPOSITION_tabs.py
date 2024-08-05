import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2161236_Verify_filtering_on_both_YOUR_TEAMS_and_THE_OPPOSITION_tabs(Common):
    """
    TR_ID: C2161236
    NAME: Verify filtering on both YOUR TEAMS and THE OPPOSITION tabs
    DESCRIPTION: This test case verifies filtering from a few tabs simultaneously
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: 1. Load SportBook
    PRECONDITIONS: 2. Select 'Connect' from header ribbon
    PRECONDITIONS: 3. Select 'Football Bet Filter' item
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: Load SportBook > Go to Football > 'Coupons' tab > Select any coupon that contains events with 'Match result' market (In Console: search 'coupon' - find coupons with couponSortCode: "MR">)
    """
    keep_browser_open = True

    def test_001_verify_filters_default_value(self):
        """
        DESCRIPTION: Verify filters default value
        EXPECTED: None of the filters is selected
        """
        pass

    def test_002_check_off_a_few_random_filters_from_your_teams_and_the_opposition_tab(self):
        """
        DESCRIPTION: Check off a few random filters from YOUR TEAMS and THE OPPOSITION tab
        EXPECTED: The filters are checked off
        """
        pass

    def test_003_switch_over_tabs(self):
        """
        DESCRIPTION: Switch over tabs
        EXPECTED: The ticks are present on pages during switching over tabs
        """
        pass

    def test_004_check_details_on_find_bets_cta(self):
        """
        DESCRIPTION: Check details on 'Find Bets' CTA
        EXPECTED: 1. Results should show data from API CALL params according to the selected filters
        EXPECTED: 2. Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS" (beneath its label)
        """
        pass

    def test_005_tap_find_bets(self):
        """
        DESCRIPTION: Tap 'Find Bets'
        EXPECTED: 1. Football Filter Results page is opened
        EXPECTED: 2. Results number is correct
        EXPECTED: 3. List of selections is correct and corresponds to filters applied on both tabs
        """
        pass
