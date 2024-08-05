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
class Test_C58208387_Verify_Special_events_filtering_on_the_Specials_tab(Common):
    """
    TR_ID: C58208387
    NAME: Verify Special events filtering on the  'Specials' tab
    DESCRIPTION: This test case verifies special events filtering on the 'Specials' tab
    DESCRIPTION: **Will be available from 102.0 Coral and 102.0 Ladbrokes**
    PRECONDITIONS: **CMS Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: **Special** events should contain the following settings:
    PRECONDITIONS: Set the **drilldownTagNames = MKTFLAG_SP** on market level
    PRECONDITIONS: ('Specials' flag to be ticked on market level in TI)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 'Specials' tab is enabled in CMS for 'Tier 1/2' Sport and data are available on SS
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Sports Landing Page
    PRECONDITIONS: 3. Choose the 'Specials' tab
    """
    keep_browser_open = True

    def test_001_verify_events_filtering_on_the_page(self):
        """
        DESCRIPTION: Verify events filtering on the page
        EXPECTED: All Special events available for particular Sports are present
        """
        pass

    def test_002_verify_filtering_for_special_events(self):
        """
        DESCRIPTION: Verify filtering for special events
        EXPECTED: Events with next attributes are shown:
        EXPECTED: - eventSortCode="MTCH"/"TNMT"
        EXPECTED: - drilldownTagNames: "MKTFLAG_SP" - **on market level**
        """
        pass

    def test_003__open_the_ob_system_set_specials_false_for_the_market_save_the_changes_back_to_the_app_refresh_the_page(self):
        """
        DESCRIPTION: * Open the OB system.
        DESCRIPTION: * Set 'Specials': False for the market.
        DESCRIPTION: * Save the changes.
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        EXPECTED: Events with next attributes are NOT shown:
        EXPECTED: - eventSortCode="MTCH"/"TNMT"
        EXPECTED: - **NO** drilldownTagNames:"MKTFLAG_SP" - **on market level**
        """
        pass
