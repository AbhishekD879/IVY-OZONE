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
class Test_C64663367_Verify_the_display_of_Player_Names_selection_links(Common):
    """
    TR_ID: C64663367
    NAME: Verify the display of Player Names selection links
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
        EXPECTED: ------2.Market Blurb (if applied) --OutOfScope for NOW
        EXPECTED: 3.List of Player Name Links
        EXPECTED: 4.Show More Link
        EXPECTED: 5.Show Less link
        """
        pass

    def test_004_verify_user_is_able_to_click_on_player_link(self):
        """
        DESCRIPTION: Verify User is able to click on Player link
        EXPECTED: Player link should be clickable and should navigate to Scoreline popup page
        """
        pass

    def test_005_player_names_are_displayed_in_list_view_with__gt_arrow_symbol(self):
        """
        DESCRIPTION: Player Names are displayed in LIST view with  &gt; Arrow Symbol
        EXPECTED: Player names should be in List View in Link form with &gt; Symbol
        """
        pass
