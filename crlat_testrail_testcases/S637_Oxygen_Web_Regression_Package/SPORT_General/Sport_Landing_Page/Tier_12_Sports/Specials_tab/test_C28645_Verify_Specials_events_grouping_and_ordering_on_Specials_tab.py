import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28645_Verify_Specials_events_grouping_and_ordering_on_Specials_tab(Common):
    """
    TR_ID: C28645
    NAME: Verify 'Specials' events grouping and ordering on 'Specials' tab
    DESCRIPTION: This test case verifies how events are grouped and ordered on 'Specials' tab
    PRECONDITIONS: **CMS Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: **Special** events should contain the following settings:
    PRECONDITIONS: - |Not Primary market| should be created
    PRECONDITIONS: - Set the **drilldownTagNames = MKTFLAG_SP** for |Not Primary market| on market level  ('Specials' flag to be ticked on market level in TI)
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

    def test_001_verify_events_grouping(self):
        """
        DESCRIPTION: Verify events grouping
        EXPECTED: * Events are grouped by **classId** and **typeId**
        EXPECTED: * Events are displayed in accordions
        EXPECTED: * The first accordion is expanded by default, the rest - collapsed
        """
        pass

    def test_002_verify_accordion_titles(self):
        """
        DESCRIPTION: Verify accordion titles
        EXPECTED: Accordion titles correspond to **className - typeName** OR
        EXPECTED: **categoryName - typeName**
        """
        pass

    def test_003_verify_order_of_accordions(self):
        """
        DESCRIPTION: Verify order of accordions
        EXPECTED: Accordions are ordered by:
        EXPECTED: 1) Class **displayOrder** in ascending
        EXPECTED: 2) Type **displayOrder** in ascending
        """
        pass

    def test_004_expand_any_accordion_and_verify_order_of_events(self):
        """
        DESCRIPTION: Expand any accordion and verify order of events
        EXPECTED: 'Special' events are ordered in the following way:
        EXPECTED: 1) Event displayOrder in ascending
        EXPECTED: 2) startTime - chronological order in the first instance
        EXPECTED: 3) Alphabetical order
        EXPECTED: **Note:** 'Matches' events (eventSortCode: "MTCH") are displayed above the 'Outrights' (eventSortCode: "TNMT") within each 'Type' accordion
        """
        pass
