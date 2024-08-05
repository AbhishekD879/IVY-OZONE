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
class Test_C64658688_Verify_the_display_of_Markets_with_standard_Correct_Score_Template(Common):
    """
    TR_ID: C64658688
    NAME: Verify the display of Markets with standard Correct Score Template
    DESCRIPTION: Verify the display of Markets with standard Correct Score Template
    PRECONDITIONS: ![](index.php?/attachments/get/d92739be-5b37-4525-b0ba-9efda956428d)
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
        EXPECTED: ![](index.php?/attachments/get/45310456-da3c-4378-aad5-c9033f53b479)
        """
        pass

    def test_004_verify_user_is_able_to_enter_manual_score_fields(self):
        """
        DESCRIPTION: Verify user is able to enter Manual Score fields
        EXPECTED: User should be able to enter values
        EXPECTED: 1.Number dropdowns on Desktop
        EXPECTED: 2.Number pop-up on Mobile
        """
        pass

    def test_005_click_on_price_button(self):
        """
        DESCRIPTION: Click on Price Button
        EXPECTED: Selection should be added to Betslip/Quickbet
        """
        pass

    def test_006_add_one_more_selection_from_pre_defined_selections(self):
        """
        DESCRIPTION: Add one more selection from pre defined selections
        EXPECTED: Selection should be added to betslip
        """
        pass

    def test_007_verify_show_more_link_is_displayed_after_4th_row(self):
        """
        DESCRIPTION: Verify Show More Link is displayed after 4th row
        EXPECTED: SHOW MORE link should display at the bottom of the 4th row
        """
        pass

    def test_008_verify_hidden_pre_defined_selections_are_displayed_after_clicking_on_show_more_link(self):
        """
        DESCRIPTION: Verify hidden pre-defined selections are displayed after clicking on SHOW MORE link
        EXPECTED: Hidden pre defined selections should be displayed after SHOW MORE click
        """
        pass

    def test_009_add_one_more_selection_from_hidden_selection_which_are_revealed_after_show_more_link_click(self):
        """
        DESCRIPTION: add one more selection from hidden selection [Which are revealed after show more link click]
        EXPECTED: Selection should be added to Betslip
        """
        pass

    def test_010_now_place_bet_for_all_these_3_selections(self):
        """
        DESCRIPTION: Now Place Bet for all these 3 selections
        EXPECTED: Bet should be placed successfully
        """
        pass
