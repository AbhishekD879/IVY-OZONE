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
class Test_C48473971_Verify_events_filtering_on_the_Competitions_tab(Common):
    """
    TR_ID: C48473971
    NAME: Verify events filtering on the 'Competitions' tab
    DESCRIPTION: This test case verifies events filtering on the 'Competitions' tab
    DESCRIPTION: **From 102.0 for Coral and Ladbrokes**
    PRECONDITIONS: 1. 'Competitions' tab is enabled in CMS for 'Tier 2' Sport and data are available ( **MATCHES** including live and pre-match and **OUTRIGHTS** )
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Navigate to the selected 'Tier 2' Sports Landing Page
    PRECONDITIONS: 4. Choose the 'Competitions' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    """
    keep_browser_open = True

    def test_001_verify_events_filtering_on_the_page(self):
        """
        DESCRIPTION: Verify events filtering on the page
        EXPECTED: - All matches events available for particular Sports are present including live and pre-match
        EXPECTED: - All outright events available for particular Sports are present
        """
        pass

    def test_002_verify_filtering_for_matches_events(self):
        """
        DESCRIPTION: Verify filtering for matches events
        EXPECTED: **Pre-match events:**
        EXPECTED: Events with next attributes are shown:
        EXPECTED: - **eventSortCode="MTCH"**
        EXPECTED: AND/OR
        EXPECTED: - **dispSortName** is positive (e.g. dispSortName="MR" OR dispSortName="HH")
        EXPECTED: **Started events:**
        EXPECTED: Events with the following attributes are shown:
        EXPECTED: - **eventSortCode="MTHN"**
        EXPECTED: AND/OR
        EXPECTED: - **dispSortName** is positive (e.g. dispSortName="MR" OR dispSortName="HH")
        EXPECTED: AND
        EXPECTED: - **isMarketBetInRun="true"** (on the Market level)
        EXPECTED: AND
        EXPECTED: - **rawIsOffCode="Y"**
        EXPECTED: OR
        EXPECTED: - **(isStated="true" AND rawIsOffCode="-")**
        """
        pass

    def test_003_verify_filtering_for_outright_events(self):
        """
        DESCRIPTION: Verify filtering for outright events
        EXPECTED: **Pre-match events:**
        EXPECTED: Events with next attributes are shown:
        EXPECTED: - **eventSortCode="TNMT"/"TRxx"** (xx - numbers from 01 to 20)
        EXPECTED: AND/OR
        EXPECTED: - **dispSortName** is positive (e.g. dispSortName="3W")
        EXPECTED: **Started events:**
        EXPECTED: Events with the following attributes are shown:
        EXPECTED: - **eventSortCode="TNMT"/"TRxx"** (xx - numbers from 01 to 20)
        EXPECTED: AND/OR ​
        EXPECTED: - **dispSortName** is positive (e.g. dispSortName="3W")
        EXPECTED: AND
        EXPECTED: - **isMarketBetInRun="true"** (on the any Market level)
        EXPECTED: AND
        EXPECTED: - **rawIsOffCode="Y"**
        EXPECTED: OR
        EXPECTED: - **(isStated="true" AND rawIsOffCode="-")**
        """
        pass
