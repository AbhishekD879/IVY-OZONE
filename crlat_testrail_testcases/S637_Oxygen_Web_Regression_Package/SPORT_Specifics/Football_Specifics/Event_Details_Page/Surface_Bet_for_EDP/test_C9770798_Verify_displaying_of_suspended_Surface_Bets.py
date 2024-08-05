import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C9770798_Verify_displaying_of_suspended_Surface_Bets(Common):
    """
    TR_ID: C9770798
    NAME: Verify displaying of suspended Surface Bets
    DESCRIPTION: Test case verifies that suspended Surface Bet is marked as disabled
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Details page (EDP).
    PRECONDITIONS: 2. Open this EDP
    PRECONDITIONS: CMS path for the Surface Bets configuring: Sport Pages > Homepage > Surface Bets Module
    """
    keep_browser_open = True

    def test_001_in_the_ti_mark_the_selection_from_the_surface_bet_as_suspended(self):
        """
        DESCRIPTION: In the TI mark the selection from the Surface Bet as suspended
        EXPECTED: 
        """
        pass

    def test_002_in_the_application_verify_the_price_button_is_marked_as_suspended_without_page_refreshing(self):
        """
        DESCRIPTION: In the application verify the Price button is marked as suspended without page refreshing
        EXPECTED: Price button becomes suspended (disabled)
        """
        pass

    def test_003_in_the_ti_mark_the_selection_from_the_surface_bet_as_not_suspended(self):
        """
        DESCRIPTION: In the TI mark the selection from the Surface Bet as not suspended
        EXPECTED: 
        """
        pass

    def test_004_in_the_application_verify_the_price_button_is_marked_as_enabled_without_page_refreshing(self):
        """
        DESCRIPTION: In the application verify the Price button is marked as enabled without page refreshing
        EXPECTED: Price button becomes not suspended (enabled)
        """
        pass

    def test_005_pass_1_4_steps_with_suspending_on_market_and_event_levels(self):
        """
        DESCRIPTION: Pass 1-4 steps with suspending on market and event levels
        EXPECTED: 
        """
        pass