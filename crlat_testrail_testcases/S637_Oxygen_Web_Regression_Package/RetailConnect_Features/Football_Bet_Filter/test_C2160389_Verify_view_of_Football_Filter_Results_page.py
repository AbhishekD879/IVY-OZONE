import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.retail
@vtest
class Test_C2160389_Verify_view_of_Football_Filter_Results_page(Common):
    """
    TR_ID: C2160389
    NAME: Verify view of Football Filter Results page
    DESCRIPTION: This test case verify view and behavior of Football Filter Results page
    PRECONDITIONS: Make sure Football Bet Filter feature is turned on in CMS: System configuration > Connect > football Filter
    PRECONDITIONS: **Coral:**
    PRECONDITIONS: 1. Select 'Connect' from header sports ribbon -> Connect landing page is opened
    PRECONDITIONS: 2. Tap Football Bet Filter
    PRECONDITIONS: 3. Scroll down and tap 'Find Bets'
    PRECONDITIONS: **Ladbrokes:**
    PRECONDITIONS: Load SportBook > Go to Football > 'Coupons' tab > Select any coupon that contains events with 'Match result' market (In Console: search 'coupon' - find coupons with couponSortCode: "MR") > Scroll down and tap 'Find Bets'
    """
    keep_browser_open = True

    def test_001_football_filter_results_page_is_opened(self):
        """
        DESCRIPTION: Football Filter Results page is opened
        EXPECTED: 
        """
        pass

    def test_002_verify_football_filter_results_header(self):
        """
        DESCRIPTION: Verify 'Football filter results' header
        EXPECTED: **Coral:**
        EXPECTED: - Back button 'Football bet filter' returns user to 'Football filter' page
        EXPECTED: - Header with 'Results: (X)' label, where X - amount of displayed selections
        EXPECTED: **Ladbrokes:**
        EXPECTED: - Back button
        EXPECTED: - 'Football bet filter' header on the black background
        EXPECTED: - Header with 'Results: X' label, where X - number of displayed selections
        """
        pass

    def test_003_verify_events_representing(self):
        """
        DESCRIPTION: Verify events representing
        EXPECTED: - List of selections (all unselected by default) is represented in following way:
        EXPECTED: Team Name
        EXPECTED: Event Name: HomeTeam v AwayTeam
        EXPECTED: Event Start Date/Time: Day DD/MM HH:MM
        EXPECTED: Price/Odds (from the right)
        """
        pass

    def test_004_verify_priceodds_when_they_are_equal_11(self):
        """
        DESCRIPTION: Verify Price/Odds when they are equal 1/1
        EXPECTED: If for some events API returns Price/Odds equal to 1/1  then 'EVS' is displayed instead
        """
        pass

    def test_005_obsolete_step_check_off_of_2_selections_that_belong_to_one_event(self):
        """
        DESCRIPTION: Obsolete step. Check off of 2 selections that belong to one event
        EXPECTED: 'You can only bet on one selection in each match!' error message is displayed at the bottom
        """
        pass
