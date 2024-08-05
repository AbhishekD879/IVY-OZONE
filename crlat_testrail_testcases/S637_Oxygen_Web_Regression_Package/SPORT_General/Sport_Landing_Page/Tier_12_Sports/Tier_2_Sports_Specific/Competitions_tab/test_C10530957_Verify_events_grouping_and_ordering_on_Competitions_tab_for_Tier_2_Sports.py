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
class Test_C10530957_Verify_events_grouping_and_ordering_on_Competitions_tab_for_Tier_2_Sports(Common):
    """
    TR_ID: C10530957
    NAME: Verify events grouping and ordering on 'Competitions' tab for Tier 2 Sports
    DESCRIPTION: This test case verifies how events are grouped and ordered on 'Competitions' tab for Tier 2 Sports
    DESCRIPTION: **From 102.0 for Coral and Ladbrokes**
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. 'Competitions' tab is enabled in CMS for 'Tier 2' Sport and data are available ( **MATCHES** including live and pre-match and **OUTRIGHTS** )
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Navigate to the selected 'Tier 2' Sports Landing Page
    PRECONDITIONS: 4. Choose the 'Competitions' tab
    """
    keep_browser_open = True

    def test_001_verify_events_grouping(self):
        """
        DESCRIPTION: Verify event's grouping
        EXPECTED: * Events are grouped by **classId** and **typeId**
        EXPECTED: * Events are displayed in accordions
        EXPECTED: * First 3 accordions are expanded by default, the rest - collapsed
        """
        pass

    def test_002_verify_accordion_titles(self):
        """
        DESCRIPTION: Verify accordion titles
        EXPECTED: Accordion titles correspond to **className-typeName**
        """
        pass

    def test_003_verify_order_of_accordions(self):
        """
        DESCRIPTION: Verify order of accordions
        EXPECTED: Accordions are ordered by:
        EXPECTED: 1) Class **displayOrder ** in ascending
        EXPECTED: 2) Type **displayOrder ** in ascending
        """
        pass

    def test_004_verify_matches_and_outrights_events_order_in_each_accordion(self):
        """
        DESCRIPTION: Verify 'Matches' and 'Outrights' events order in each accordion
        EXPECTED: - 'Matches' events are displayed above the 'Outrights' within each 'Type' accordion
        EXPECTED: - 'Matches' events are ordered in the following way:
        EXPECTED: 1) startTime - chronological order in the first instance
        EXPECTED: 2) Event displayOrder in ascending
        EXPECTED: 3) Alphabetical order
        EXPECTED: - 'Outrights' events are ordered in the following way:
        EXPECTED: 1) Event displayOrder in ascending
        EXPECTED: 2) startTime - chronological order in the first instance
        EXPECTED: 3) Alphabetical order
        """
        pass
