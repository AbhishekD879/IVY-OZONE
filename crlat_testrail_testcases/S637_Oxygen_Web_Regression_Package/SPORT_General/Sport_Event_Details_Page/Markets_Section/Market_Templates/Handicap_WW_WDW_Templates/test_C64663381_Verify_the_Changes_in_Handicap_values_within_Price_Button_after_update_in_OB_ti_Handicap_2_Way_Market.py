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
class Test_C64663381_Verify_the_Changes_in_Handicap_values_within_Price_Button_after_update_in_OB_ti_Handicap_2_Way_Market(Common):
    """
    TR_ID: C64663381
    NAME: Verify the Changes in Handicap values within Price Button after update in OB ti- Handicap 2 Way Market
    DESCRIPTION: Verify the Changes in Handicap values within Price Button after update in OB ti- Handicap 2 Way Market
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

    def test_003_expand_any_handicap_2_way_market_ww_and_check_signpost_icon_is_displaying_at_right_side_of_market_name(self):
        """
        DESCRIPTION: Expand any Handicap 2-Way Market WW and Check Signpost icon is displaying at Right side of Market name
        EXPECTED: 1. Signpost icon should be displayed at the Right Side of the Market Header Name
        EXPECTED: 2.Market Header should be displayed along with signposting if available
        EXPECTED: Option 1 Label (Team Name) should be displayed
        EXPECTED: Option 2 Label (Team Name) should be displayed
        EXPECTED: 3.Handicap Value for Option 1 should be displayed within the price button (as per Zeplin CSS styles) up to "-100"
        EXPECTED: 4.Handicap Value for Option 3 should be displayed within the price button (as per Zeplin CSS styles) up to "+100"
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
