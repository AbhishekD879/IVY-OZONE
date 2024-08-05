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
class Test_C44870209_Verify_Market_selector_is_displayed_for_football_only(Common):
    """
    TR_ID: C44870209
    NAME: Verify Market selector is displayed for football only
    DESCRIPTION: "Check Market selector is only displayed for football
    DESCRIPTION: - Football Landing pages for the upcoming section
    DESCRIPTION: - In-Play tab on the FB landing page
    DESCRIPTION: - FB competition type page - Matches tab
    DESCRIPTION: - FB coupons detail page
    DESCRIPTION: Verify user sees drop down when clicks on the market selector in below order
    DESCRIPTION: - Match Result
    DESCRIPTION: - Next Team to Score - design updated. Small tweak needed to show Xth goal
    DESCRIPTION: - Extra Time Result (need designs) Updated design below:
    DESCRIPTION: - Total Goals Over/Under 2.5
    DESCRIPTION: -  Both Teams to Score
    DESCRIPTION: - To Win & Both Teams to Score
    DESCRIPTION: - Draw No Bet
    DESCRIPTION: -  1st Half Result
    DESCRIPTION: - To Qualify
    DESCRIPTION: Verify display of the page with the new market template when user changes to a different market from market selector
    DESCRIPTION: Verify dropdown with the list of markets should be made scrollable
    DESCRIPTION: Verify user sees sticky market selector when scrolls through the upcoming module "
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        pass

    def test_002_go_to_football__competition__premier_league__market_selector_is_displayed_for_football(self):
        """
        DESCRIPTION: Go to Football > competition > premier league > Market selector is displayed for football
        EXPECTED: Market selector is displayed
        """
        pass

    def test_003_verify_match_result_market_is_selected_by_default(self):
        """
        DESCRIPTION: verify Match result market is selected by default
        EXPECTED: Match result market is selected by default
        """
        pass

    def test_004_verify_user_can_change_the_market_from_drop_down(self):
        """
        DESCRIPTION: verify user can change the market from drop down
        EXPECTED: user can change the market displayed in drop down
        EXPECTED: -Match Result
        EXPECTED: -Total Goals Over/Under
        EXPECTED: -Both teams to Score
        EXPECTED: -To Win & Both teams to score
        EXPECTED: -Draw no Bet
        EXPECTED: -1st Half Result
        """
        pass

    def test_005_verify_display_of_the_page_with_the_new_market_template_when_user_changes_to_a_different_market_from_market_selector(self):
        """
        DESCRIPTION: Verify display of the page with the new market template when user changes to a different market from market selector
        EXPECTED: Fixture is displayed as per the selected market
        """
        pass

    def test_006_verify_dropdown_with_the_list_of_markets_should_be_made_scrollable(self):
        """
        DESCRIPTION: Verify dropdown with the list of markets should be made scrollable
        EXPECTED: Drop down list of Events for the available markets are displayed and scrollable
        """
        pass

    def test_007_verify_user_can_change_the_competition_and_repeat_step_3_to_7_for_all_competition(self):
        """
        DESCRIPTION: Verify user can change the competition and repeat step #3 to #7 for all competition
        EXPECTED: 
        """
        pass
