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
class Test_C10480790_Tier1_2_Verify_Competitions_tab_displaying_based_on_Enabled_status_in_CMS(Common):
    """
    TR_ID: C10480790
    NAME: [Tier1/2] Verify 'Competitions' tab displaying based on 'Enabled' status in CMS
    DESCRIPTION: This test case verifies 'Competitions' tab displaying based on 'Enabled' status in CMS [Tier1/2]
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page where 'Competitions' tab is enabled in CMS and 'CheckEvents' is active (Tier 2) or inactive (Tier 1)
    PRECONDITIONS: **Sports Page Configs documentation:**
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Sport+Page+Configs
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the following <sport-tab> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-tab/<Category ID> -> tabs -> choose particular tab id (e.g. tab-competitions) -> verify hidden value (true or false)
    PRECONDITIONS: ![](index.php?/attachments/get/60156743)
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/121568061)
    """
    keep_browser_open = True

    def test_001_verify_competitions_tabs_displaying_if_enabled_is_active_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Competitions' tabs displaying if 'Enabled' is active and data is available on SS
        EXPECTED: * 'Competitions' tab is present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response with 'hidden': 'false' parameter  (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * List of Competitions received from SS is displayed
        EXPECTED: * Response with available data for 'Competitions' tab is received from SS (see response example in Sports Page Configs documentation from preconditions)
        """
        pass

    def test_002_verify_competitions_tabs_displaying_if_enabled_is_active_and_data_is_not_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Competitions' tabs displaying if 'Enabled' is active and data is NOT available on SS
        EXPECTED: * 'Competitions' tab is NOT present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response with 'hidden': 'true' parameter  (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        """
        pass

    def test_003_verify_competitions_tabs_displaying_if_enabled_is_inactive_and_data_is_available_on_ss(self):
        """
        DESCRIPTION: Verify 'Competitions' tabs displaying if 'Enabled' is inactive and data is available on SS
        EXPECTED: * 'Competitions' tab is NOT present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response with 'hidden': 'true' parameter  (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        """
        pass
