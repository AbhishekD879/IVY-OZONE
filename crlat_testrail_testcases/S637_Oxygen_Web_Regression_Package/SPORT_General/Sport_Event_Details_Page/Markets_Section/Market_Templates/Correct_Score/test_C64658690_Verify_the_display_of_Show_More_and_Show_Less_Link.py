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
class Test_C64658690_Verify_the_display_of_Show_More_and_Show_Less_Link(Common):
    """
    TR_ID: C64658690
    NAME: Verify the display of Show More and Show Less Link
    DESCRIPTION: Verify the display of Show More and Show Less Link
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_edp_pagefoot_ball_is_non_restrictivevolley_ball_is_restrictive(self):
        """
        DESCRIPTION: Navigate to EDP page
        DESCRIPTION: Foot Ball is Non Restrictive
        DESCRIPTION: Volley Ball is Restrictive
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_the_correct_score_market_and_verify_the_details(self):
        """
        DESCRIPTION: Expand the Correct score Market and verify the details
        EXPECTED: 1.Market Header should be displayed along with Signpost if available
        EXPECTED: 2.Manual Correct Score Entry Fields for Team A & Team B (with Labels)
        EXPECTED: 3.Manual Correct Score Entry Price Button
        EXPECTED: 4.Team Labels and Pre defined Price buttons for HOME, DRAW,AWAY teams
        EXPECTED: 5.Show More link should display at the bottom of the 4th row
        EXPECTED: 6. Show Less link should be displayed after clicking Show More Link
        """
        pass

    def test_004_verify_some_pre_defined_oddsselections_are_displayed_show_more_link_is_displayed_after_4th_row(self):
        """
        DESCRIPTION: Verify some pre-defined odds/selections are displayed &&
        DESCRIPTION: Show More Link is displayed after 4th row
        EXPECTED: 1.Pre-defined Odds should be displayed
        EXPECTED: 2.SHOW MORE link should display at the bottom of the 4th row
        """
        pass

    def test_005_verify_hidden_pre_defined_selections_are_displayed_after_clicking_on_show_more_link(self):
        """
        DESCRIPTION: Verify hidden pre-defined selections are displayed after clicking on SHOW MORE link
        EXPECTED: Hidden pre defined selections should be displayed after SHOW MORE clicking
        """
        pass

    def test_006_verify_show_less_link_is_displayed(self):
        """
        DESCRIPTION: Verify Show Less link is displayed
        EXPECTED: Show Less link should be displayed after click on SHOW MORE link within the Market
        """
        pass

    def test_007_click_on_show_less_link(self):
        """
        DESCRIPTION: Click on Show Less link
        EXPECTED: All other selection should be collapsed other than First 4 rows
        EXPECTED: and Show Less should be replaced with Show More link
        """
        pass
