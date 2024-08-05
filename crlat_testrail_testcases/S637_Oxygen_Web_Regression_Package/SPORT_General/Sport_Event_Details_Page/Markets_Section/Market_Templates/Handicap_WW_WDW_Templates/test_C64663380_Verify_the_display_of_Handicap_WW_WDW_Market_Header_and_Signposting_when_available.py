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
class Test_C64663380_Verify_the_display_of_Handicap_WW_WDW_Market_Header_and_Signposting_when_available(Common):
    """
    TR_ID: C64663380
    NAME: Verify the display of Handicap WW_WDW Market Header and Signposting when available
    DESCRIPTION: Verify the display of Handicap Market Header and Signposting when available
    PRECONDITIONS: Market should have Handicap values and Signpost
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_edp_page_where_handicap_markets_are_applicable(self):
        """
        DESCRIPTION: Navigate to EDP page where Handicap markets are applicable
        EXPECTED: EDP page should be displayed
        """
        pass

    def test_003_expand_any_handicap_3_way_market_wdw_and_check_signpost_icon_is_displaying_at_right_side_of_market_name(self):
        """
        DESCRIPTION: Expand any Handicap 3-Way Market WDW and Check Signpost icon is displaying at Right side of Market name
        EXPECTED: 1. Signpost icon should be displayed at the Right Side of the Market Header Name
        EXPECTED: 2. Market Header should be displayed along with signposting if available
        EXPECTED: Option 1 Label (Team Name) should be displayed
        EXPECTED: Option 2 Label (Team Name) should be displayed
        EXPECTED: Option 3 Label (Team Name) should be displayed
        EXPECTED: 3.Handicap Value for Option 1 should be displayed within the price button (as per Zeplin CSS styles) up to "-100"
        EXPECTED: 4.Handicap Value for Option 2 [DRAW] should NOT be displayed within the price button (as per Zeplin CSS styles)
        EXPECTED: 5.Handicap Value for Option 3 should be displayed within the price button (as per Zeplin CSS styles) up to "+100"
        """
        pass

    def test_004_expand_any_handicap_2_way_market_ww_and_check_signpost_icon_is_displaying_at_right_side_of_market_name(self):
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
