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
class Test_C64658689_Verify_manual_entry_in_Correct_Score_Template(Common):
    """
    TR_ID: C64658689
    NAME: Verify manual entry in Correct Score Template
    DESCRIPTION: Verify manual entry in Correct Score Template
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

    def test_004_verify_manual_correct_score_entry_field_for_home_and_draw(self):
        """
        DESCRIPTION: Verify Manual Correct Score Entry field for HOME and DRAW
        EXPECTED: 1.Manual entry fields should be displayed only for HOME and AWAY Teams
        EXPECTED: 2.Should not be displayed for DRAW Option
        """
        pass

    def test_005_verify_user_is_able_to_enter_manual_score_fields(self):
        """
        DESCRIPTION: Verify user is able to enter Manual Score fields
        EXPECTED: User should be able to enter values
        EXPECTED: 1.Number dropdowns on Desktop
        EXPECTED: 2.Number pop-up on Mobile
        """
        pass

    def test_006_verify_price_button_after_entered_values_into_home_and_away_manual_correct_score_fields(self):
        """
        DESCRIPTION: Verify Price Button After entered values into Home and Away manual correct score fields
        EXPECTED: Manual Correct Score Entry Price Button should be activated to display the correct odds for that scoreline
        """
        pass

    def test_007_update_the_score_and_verify_price_button_odd_value(self):
        """
        DESCRIPTION: Update the Score and verify Price Button Odd value
        EXPECTED: Price button ODD value should be updated to new ODD according latest manual entry
        """
        pass

    def test_008_click_on_price_button(self):
        """
        DESCRIPTION: Click on Price Button
        EXPECTED: Selection should be added to Betslip/Quickbet
        """
        pass

    def test_009_click_on_place_bet(self):
        """
        DESCRIPTION: Click on Place bet
        EXPECTED: bet should be placed successfully
        """
        pass

    def test_010_now_add_one_selection_from_manual_field_entry_and_other_one_from_pre_defined_odd_selections___gtgt_place_bet(self):
        """
        DESCRIPTION: Now add one selection from Manual field Entry and Other one from Pre defined odd selections --&gt;&gt; Place bet
        EXPECTED: 2 selections should be placed successfully
        """
        pass
