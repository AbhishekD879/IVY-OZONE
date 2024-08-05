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
class Test_C64663387_Verify_the_changes_in_Handicap_value_within_the_price_button_after_update_in_OB_ti_Handicap_3_Way_Market(Common):
    """
    TR_ID: C64663387
    NAME: Verify the changes in Handicap value within the price button  after update in OB ti- Handicap 3 Way Market
    DESCRIPTION: Verify the changes in Handicap value within the price button  after update in OB ti- Handicap 3 Way Market
    PRECONDITIONS: Market Should have handicap values
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_edp_page(self):
        """
        DESCRIPTION: Navigate to EDP page
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_any_handicap_3_way_market_wdw_and_check_signpost_icon_is_displaying_at_right_side_of_market_namehandicap_value_should_not_be_displayed_for_draw_option(self):
        """
        DESCRIPTION: Expand any Handicap 3-Way Market WDW and Check Signpost icon is displaying at Right side of Market name
        DESCRIPTION: Handicap value should not be displayed for DRAW option
        EXPECTED: 1.Signpost icon should be displayed at the Right Side of the Market Header Name
        EXPECTED: 2.Market Header should be displayed along with signposting if available
        EXPECTED: Option 1 Label (Team Name) should be displayed
        EXPECTED: Option 2 Label (Team Name) should be displayed
        EXPECTED: Option 3 Label (Team Name) should be displayed
        EXPECTED: 3.Handicap Value for Option 1 should be displayed within the price button (as per Zeplin CSS styles) up to "-100"
        EXPECTED: 4.Handicap Value for Option 2 [DRAW] should NOT be displayed within the price button (as per Zeplin CSS styles)
        EXPECTED: 5.Handicap Value for Option 3 should be displayed within the price button (as per Zeplin CSS styles) up to "+100"
        """
        pass

    def test_004_open_ti_and_change_the_handicap_valuevalidate_the_change_in_fe(self):
        """
        DESCRIPTION: Open TI and change the handicap value
        DESCRIPTION: Validate the change in FE
        EXPECTED: Handicap Value within the price button should be updated
        """
        pass

    def test_005_repeat_the_above_steps_for_all_tier_1_and_tier_2_sports_where_handicap_markets_are_applicable(self):
        """
        DESCRIPTION: Repeat the above steps for all Tier 1 and Tier 2 sports where Handicap markets are applicable
        EXPECTED: 
        """
        pass
