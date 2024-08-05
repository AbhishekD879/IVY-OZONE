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
class Test_C64663351_Verify_the_display_of_Market_Header_and_Signposting_when_available(Common):
    """
    TR_ID: C64663351
    NAME: Verify the display of Market Header and Signposting when available
    DESCRIPTION: Verify the display of Market Header and Signposting when available
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

    def test_004_configure_one_more_signpost_and_verify(self):
        """
        DESCRIPTION: Configure one more Signpost and verify
        EXPECTED: All Signpost Icons should be displayed which are configured
        """
        pass
