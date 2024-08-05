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
class Test_C49328599_1012_Coral_and_1005_Ladbrokes_Verify_special_events_filtering_on_the_Competitions_tab(Common):
    """
    TR_ID: C49328599
    NAME: [101.2 Coral and 100.5 Ladbrokes]  Verify special events filtering on the 'Competitions' tab
    DESCRIPTION: This test case verifies special events filtering on the 'Competitions' tab
    DESCRIPTION: **Will be available from 101.2 Coral and 100.5 Ladbrokes**
    PRECONDITIONS: 1. 'Competitions' tab is enabled in CMS for 'Tier 2' Sport and data are available ( **MATCHES** including live and pre-match and **OUTRIGHTS** )
    PRECONDITIONS: 2. **SPECIAL** events are created for the particular Sport
    PRECONDITIONS: 3. Load the app
    PRECONDITIONS: 4. Navigate to the selected 'Tier 2' Sports Landing Page
    PRECONDITIONS: 5. Choose the 'Competitions' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: - Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: - **Specials** Events should be created only with **No Primary** markets
    PRECONDITIONS: - **Specials** Events should contain the following attributes:
    PRECONDITIONS: **Event level:**
    PRECONDITIONS: * drilldownTagNames = EVFLAG_SP
    PRECONDITIONS: * typeFlagCodes=SP
    PRECONDITIONS: **Market level:**
    PRECONDITIONS: * drilldownTagNames = MKTFLAG_SP
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
        EXPECTED: - Special events are NOT present on the page
        """
        pass

    def test_002_trigger_undisplaying_of_all_matches_and_outrights_events_except_specials(self):
        """
        DESCRIPTION: Trigger undisplaying of all Matches and Outrights events except Specials
        EXPECTED: 'Competitions' tab is not displayed at all
        """
        pass
