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
class Test_C64663368_Verify_the_display_of_Market_Header_and_Signposting_when_available(Common):
    """
    TR_ID: C64663368
    NAME: Verify the display of Market Header and Signposting when available
    DESCRIPTION: Verify the Score cast template
    PRECONDITIONS: Scorecast template should be configured/mapped to the event
    PRECONDITIONS: This will be a 2-phase selection template, with the first phase leading on to the second phase based on selection:
    PRECONDITIONS: Phase 1: Player Selection
    PRECONDITIONS: Phase 2: Scoreline Selection
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_any_sports__edp_page(self):
        """
        DESCRIPTION: Navigate to any sports  EDP page
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_the_markets_which_should_display_the_score_cast_template(self):
        """
        DESCRIPTION: Expand the markets which should display the Score cast Template
        EXPECTED: 1.Market Header (including signposting if applied)
        EXPECTED: --------2.Market Blurb (if applied)--OutOfScope for NOW
        EXPECTED: 3.List of Player Name Links
        EXPECTED: 4.Show More Link
        EXPECTED: 5.Show Less link
        """
        pass

    def test_004_configure_one_or_more_signposts_in_ob_and_verify_in_fe(self):
        """
        DESCRIPTION: Configure One or more signposts in OB and verify in FE
        EXPECTED: Signposting icons should be displayed right to the Market Header name
        """
        pass
