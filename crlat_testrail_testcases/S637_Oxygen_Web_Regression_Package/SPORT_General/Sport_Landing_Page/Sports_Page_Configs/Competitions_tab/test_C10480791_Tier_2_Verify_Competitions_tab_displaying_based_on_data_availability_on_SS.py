import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C10480791_Tier_2_Verify_Competitions_tab_displaying_based_on_data_availability_on_SS(Common):
    """
    TR_ID: C10480791
    NAME: [Tier 2] Verify 'Competitions' tab displaying based on data availability on SS
    DESCRIPTION: This test case verifies 'Competitions' tab displaying based on data availability on SS [Tier 2]
    DESCRIPTION: 'Check Events' status active in CMS by default for the 'Competitions' tab for Tier 2 Sports only. It means that the availability of events on SS will be checked and based on received 'hasEvents' parameter (true or false) the particular tab will be displayed or no.
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page where 'Competitions' tab is enabled in CMS and 'CheckEvents' is active (For Tier 2 only)
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
    PRECONDITIONS: ![](index.php?/attachments/get/121568064)
    """
    keep_browser_open = True

    def test_001_verify_competitions_tabs_displaying_when_check_events_status_is_active_and_data_is_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Competitions' tabs displaying when 'Check Events' status is active and data is received from SS
        EXPECTED: * 'Competitions' tab is present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response with 'hidden': 'false' parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * Data received from SS is displayed
        """
        pass

    def test_002_verify_competitions_tabs_displaying_when_check_events_is_active_and_data_is_not_received_from_ss(self):
        """
        DESCRIPTION: Verify 'Competitions' tabs displaying when 'Check Events' is active and data is NOT received from SS
        EXPECTED: * 'Competitions' tab is NOT present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response with 'hidden': 'true' parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        """
        pass
