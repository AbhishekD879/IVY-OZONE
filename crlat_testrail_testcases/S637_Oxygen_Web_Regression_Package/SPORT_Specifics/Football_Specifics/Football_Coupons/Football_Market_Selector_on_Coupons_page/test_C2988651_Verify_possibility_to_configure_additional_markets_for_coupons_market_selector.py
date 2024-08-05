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
class Test_C2988651_Verify_possibility_to_configure_additional_markets_for_coupons_market_selector(Common):
    """
    TR_ID: C2988651
    NAME: Verify possibility to configure additional markets for coupons market selector
    DESCRIPTION: 1. To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    DESCRIPTION: 2. CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    DESCRIPTION: 3. TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    DESCRIPTION: 4. How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    DESCRIPTION: 5. Create the coupons for the upcoming event with the following markets:
    DESCRIPTION: * COUPON1: 'To Win to Nil' - default market
    DESCRIPTION: * COUPON2: 'Over/Under First Half Home Team Total Goals 0.5' - non-default market
    DESCRIPTION: 6. Activate, make displayed and add prices for the markets above
    DESCRIPTION: 7. Configure market selectors via CMS > Football Coupons > Market Selectors for the market 'Over/Under First Half Home Team Total Goals 0.5'
    DESCRIPTION: 8. Open Football > Coupons (Accas) page
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_verify_coupon1_with_default_market_to_win_to_nil_is_shown_within_the_coupons_list_on_the_coupons_details_page(self):
        """
        DESCRIPTION: Verify COUPON1 with default market 'To Win to Nil' is shown within the coupons list on the Coupons Details page
        EXPECTED: COUPON1 is in the coupons list
        """
        pass

    def test_002_open_coupon1_and_select_to_win_to_nil_from_the_market_selector_verify_prices_are_shown_properly(self):
        """
        DESCRIPTION: Open COUPON1 and select 'To Win to Nil' from the market selector. Verify prices are shown properly
        EXPECTED: Prices are received from BE and displayed properly
        """
        pass

    def test_003_verify_coupon2_with_non_default_configured_market_overunder_first_half_home_team_total_goals_05_is_shown_within_the_coupons_list_on_the_coupons_details_page(self):
        """
        DESCRIPTION: Verify COUPON2 with non-default, configured market 'Over/Under First Half Home Team Total Goals 0.5' is shown within the coupons list on the Coupons Details page
        EXPECTED: COUPON2 is in the coupons list
        """
        pass

    def test_004_open_coupon2_and_select_overunder_first_half_home_team_total_goals_05_from_the_market_selector_verify_prices_are_shown_properly(self):
        """
        DESCRIPTION: Open COUPON2 and select 'Over/Under First Half Home Team Total Goals 0.5' from the market selector. Verify prices are shown properly
        EXPECTED: Prices are received from BE and displayed properly
        """
        pass
