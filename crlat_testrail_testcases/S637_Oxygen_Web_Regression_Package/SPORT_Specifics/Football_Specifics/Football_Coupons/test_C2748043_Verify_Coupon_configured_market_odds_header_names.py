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
class Test_C2748043_Verify_Coupon_configured_market_odds_header_names(Common):
    """
    TR_ID: C2748043
    NAME: Verify Coupon configured market odds header names
    DESCRIPTION: Note: cannot automate as we are not editing/deleting anything in CMS (as it may affect other users)
    PRECONDITIONS: 1. To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: 2. CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 3. TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 4. How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 5. You should have coupons created with available events and with default and not-default markets
    PRECONDITIONS: 6. Some markets from the default list (see below) should be configured via CMS >Football Coupon > Market Selectors: Title and Headers are changed to custom ones:
    PRECONDITIONS: 7. Some markets not from the default list (see below) should be configured via CMS >Football Coupon > Market Selectors: Title and Headers are changed to custom ones
    PRECONDITIONS: 8. Open Coupons (ACCAS) page and select a coupon with configured market and select this market
    """
    keep_browser_open = True

    def test_001_edit_the_market_selector_in_the_cms_type_correct_number_of_headers_three_for_3_way_marketreload_the_app_and_verify_odds_header_names(self):
        """
        DESCRIPTION: Edit the market selector in the CMS, type correct number of headers (three for 3 way market).
        DESCRIPTION: Reload the app and verify odds header names.
        EXPECTED: All three header names from the CMS are shown following the sequence from the CMS
        """
        pass

    def test_002_edit_the_market_selector_in_the_cms_type_correct_number_of_headers_and_long_header_namesreload_the_app_and_verify_odds_header_names(self):
        """
        DESCRIPTION: Edit the market selector in the CMS, type correct number of headers and long header names.
        DESCRIPTION: Reload the app and verify odds header names.
        EXPECTED: Long header names are shortened and placed properly
        """
        pass

    def test_003_edit_the_market_selector_in_the_cms_leave_headers_field_empty_and_savereload_the_app_and_verify_odds_header_names(self):
        """
        DESCRIPTION: Edit the market selector in the CMS, leave Headers field empty and save.
        DESCRIPTION: Reload the app and verify odds header names.
        EXPECTED: Default header names are shown
        """
        pass

    def test_004_edit_the_market_selector_in_the_cms_type_less_odds_headers_names__than_is_defined_for_this_market_e_g_2_for_3_way_marketreload_the_app_and_verify_odds_header_names(self):
        """
        DESCRIPTION: Edit the market selector in the CMS, type less Odds Headers names  than i's defined for this market (e. g. 2 for 3-way market)
        DESCRIPTION: Reload the app and verify odds header names.
        EXPECTED: Only the first and the second configured header names are shown and the third is empty
        """
        pass

    def test_005_edit_the_market_selector_in_the_cms_type_more_odds_headers_names_than_is_defined_for_this_market_e_g_4_for_3_way_marketreload_the_app_and_verify_odds_header_names(self):
        """
        DESCRIPTION: Edit the market selector in the CMS, type more Odds Headers names than i's defined for this market (e. g. 4 for 3-way market)
        DESCRIPTION: Reload the app and verify odds header names.
        EXPECTED: All three header names from the CMS are shown and the fourth is ignored
        """
        pass
