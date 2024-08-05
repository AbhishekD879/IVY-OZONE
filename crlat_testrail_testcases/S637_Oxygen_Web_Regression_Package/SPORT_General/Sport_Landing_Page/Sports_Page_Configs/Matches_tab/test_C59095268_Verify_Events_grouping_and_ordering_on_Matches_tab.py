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
class Test_C59095268_Verify_Events_grouping_and_ordering_on_Matches_tab(Common):
    """
    TR_ID: C59095268
    NAME: Verify Events grouping and ordering on 'Matches' tab
    DESCRIPTION: This test case verifies how events are grouped and ordered on 'Matches' tab
    PRECONDITIONS: Configurations:
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: Note:
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: Steps:
    PRECONDITIONS: 1. 'Matches' tab is enabled in CMS for 'Tier 1/2' Sport and data are available
    PRECONDITIONS: 3. Navigate to the selected 'Tier 1/2' Sports Landing Page
    PRECONDITIONS: 4. 'Matches'tab is opened by default
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
        EXPECTED: Accordion titles correspond to:
        EXPECTED: **for Football** Sports: **className** - **typeName**
        EXPECTED: **for other** Sports: **categoryName** - **typeName**
        """
        pass

    def test_003_verify_order_of_accordions(self):
        """
        DESCRIPTION: Verify order of accordions
        EXPECTED: Accordions are ordered by:
        EXPECTED: 1) Type **displayOrder ** in ascending
        EXPECTED: 2) Class **displayOrder ** in ascending
        EXPECTED: 3) Alphabetically (Accordion Title name)
        """
        pass

    def test_004_verify_matches_events_order_in_each_accordion(self):
        """
        DESCRIPTION: Verify 'Matches' events order in each accordion
        EXPECTED: 'Matches' events are ordered in the following way:
        EXPECTED: 1) startTime - chronological order in the first instance
        EXPECTED: 2) Event displayOrder in ascending
        EXPECTED: 3) Alphabetical order
        """
        pass
