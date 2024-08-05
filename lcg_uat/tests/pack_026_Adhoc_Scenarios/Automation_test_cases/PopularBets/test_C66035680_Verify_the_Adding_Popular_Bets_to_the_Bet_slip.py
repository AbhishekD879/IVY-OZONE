import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66035680_Verify_the_Adding_Popular_Bets_to_the_Bet_slip(Common):
    """
    TR_ID: C66035680
    NAME: Verify the Adding Popular Bets to the Bet slip
    DESCRIPTION: This test case verifies the Adding Popular Bets to the Bet slip
    PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: User should launch the Application Successfully
        """
        pass

    def test_000_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        pass

    def test_000_verify_the_display_of_popular_bets_section(self):
        """
        DESCRIPTION: Verify the display of Popular Bets section
        EXPECTED: User can able to see the Popular Bets section
        """
        pass

    def test_000_click_on_popular_bets_section(self):
        """
        DESCRIPTION: Click on Popular Bets section
        EXPECTED: Able to navigate to the Popular Bets section successfully
        """
        pass

    def test_000_click_on_any_odd_of_the_popular_bets(self):
        """
        DESCRIPTION: Click on any odd of the popular bets
        EXPECTED: Selected bet should be added to the bet slip successfully
        """
        pass

    def test_000_click_on_the_same_odd_again(self):
        """
        DESCRIPTION: Click on the same odd again
        EXPECTED: The selection should be removed from bet slip
        """
        pass

    def test_000_click_on_any_odd_of_the_popular_bets(self):
        """
        DESCRIPTION: Click on any odd of the popular bets
        EXPECTED: 1. For Desktop : Selection is added to Betslip.
        EXPECTED: 2. For Mobile : Selected bet should be added to Quick bet slip if it's the first selection made by the user
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Existing Bet placement journey remains same as in production
        """
        pass

    def test_000_click_on_multiple_odds_of_the_popular_bets(self):
        """
        DESCRIPTION: Click on multiple odds of the popular bets
        EXPECTED: 1. All the selected bets should be added to betslip and create relevant multiples as it happens in the existing production.
        EXPECTED: 2. Bet Placement journey remains same as in production.
        """
        pass

    def test_000_verify_display_of_popular_bets_content_in_popular_bets_sub_section_below_the_filters(self):
        """
        DESCRIPTION: Verify display of popular bets content in popular bets sub section below the filters
        EXPECTED: 1. Able to see the popular bets content.
        EXPECTED: 2. Can see the list of popular bets from different markets and events related to football sport.
        EXPECTED: 3. The top 10 most backed popular bet list is displayed as default.
        EXPECTED: 4. "Show more" is displayed under 10th popular bet
        """
        pass
