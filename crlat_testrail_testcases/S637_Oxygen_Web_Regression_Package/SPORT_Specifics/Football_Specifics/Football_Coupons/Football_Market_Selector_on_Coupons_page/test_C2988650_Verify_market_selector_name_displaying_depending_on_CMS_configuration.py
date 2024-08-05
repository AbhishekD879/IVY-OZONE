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
class Test_C2988650_Verify_market_selector_name_displaying_depending_on_CMS_configuration(Common):
    """
    TR_ID: C2988650
    NAME: Verify market selector name displaying depending on CMS configuration
    DESCRIPTION: 
    PRECONDITIONS: 1. To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: 2. CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 3. TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 4. How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 5. Create a coupon with any not default market and add a configuration for this market to the CMS > Football Coupons > Market Selectors
    PRECONDITIONS: 6. Activate, make displayed and add prices for some default, e.g. Match Betting and to the added not default market
    PRECONDITIONS: 7. Open Football > Coupons (Accas) page
    """
    keep_browser_open = True

    def test_001_verify_the_market_selector_contains_the_configured_title_of_non_default_market_and_the_hardcoded_name_of_the_default_market(self):
        """
        DESCRIPTION: Verify the Market Selector contains the configured title of non-default market and the hardcoded name of the default market
        EXPECTED: Default and non-market selector names are shown within the selector
        """
        pass

    def test_002_edit_the_non_default_market_selector_title_use_letters_numbers_special_symbols_and_spaces_verify_the_title_is_displayed_properly_within_the_market_selector(self):
        """
        DESCRIPTION: Edit the non-default market selector title, use letters, numbers, special symbols and spaces. Verify the title is displayed properly within the market selector
        EXPECTED: Configured title is displayed properly and can contain letters, numbers, special symbols and spaces
        """
        pass

    def test_003_edit_the_non_default_market_selector_title_use_1_symbol_in_the_name(self):
        """
        DESCRIPTION: Edit the non-default market selector title, use 1 symbol in the name
        EXPECTED: Short name is displayed properly
        """
        pass

    def test_004_edit_the_non_default_market_selector_title_use_a_very_long_name(self):
        """
        DESCRIPTION: Edit the non-default market selector title, use a very long name
        EXPECTED: Long name is shortened and displayed properly
        """
        pass

    def test_005_add_a_configuration_for_default_market_and_pass_steps_1_4(self):
        """
        DESCRIPTION: Add a configuration for default market and pass steps 1-4
        EXPECTED: 
        """
        pass
