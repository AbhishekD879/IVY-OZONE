import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C60088421_Verify_Greyhound_Page_Banner_section_depending_on_CMS_config(Common):
    """
    TR_ID: C60088421
    NAME: Verify Greyhound Page Banner section depending on CMS config
    DESCRIPTION: This test case verifies Greyhound Page Banner section content depending on CMS config for Always On Stream Channel
    PRECONDITIONS: **TO BE FINISHED AFTER IMPLEMENTATION OF BMA-56791**
    PRECONDITIONS: List of CMS endpoints: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: In CMS: System Configuration > Structure > %future banner config name% -> set to **disabled**
    PRECONDITIONS: 1) Load app
    """
    keep_browser_open = True

    def test_001_navigate_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds landing page
        EXPECTED: Greyhounds landing page is successfully loaded
        """
        pass

    def test_002_observe_content_of_banner_area(self):
        """
        DESCRIPTION: Observe content of banner area
        EXPECTED: Regular AEM banner is displayed within banner area
        """
        pass

    def test_003__log_in_with_user_with_balance_0_or_placed_bet_in_last_24_hours_observe_content_of_banner_area_on_greyhound_page(self):
        """
        DESCRIPTION: * Log in with user (with balance >0 or placed bet in last 24 hours)
        DESCRIPTION: * Observe content of banner area on Greyhound page
        EXPECTED: Regular AEM banner is displayed within banner area
        """
        pass

    def test_004__in_cms_system_configuration__structure__future_banner_config_name___set_to_enabled_refresh_greyhounds_landing_page(self):
        """
        DESCRIPTION: * In CMS: System Configuration > Structure > %future banner config name% -> set to **enabled**
        DESCRIPTION: * Refresh Greyhounds landing page
        EXPECTED: * For logged in user with balance >0 or placed bet in last 24 hours:
        EXPECTED: Streaming window with play button available for customer to tap in order to start playing the always on streaming channel
        EXPECTED: * For logged out user:
        EXPECTED: placeholder within the Banner area is displayed that explains to customer that by logging in with positive balance or bet placed in last 24 hours they can view live content (text could be configured in CMS > Static Blocks )
        """
        pass
