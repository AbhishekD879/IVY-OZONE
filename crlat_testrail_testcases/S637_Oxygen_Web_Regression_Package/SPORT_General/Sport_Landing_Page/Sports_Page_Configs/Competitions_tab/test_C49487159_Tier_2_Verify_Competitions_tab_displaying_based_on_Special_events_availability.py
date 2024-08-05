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
class Test_C49487159_Tier_2_Verify_Competitions_tab_displaying_based_on_Special_events_availability(Common):
    """
    TR_ID: C49487159
    NAME: [Tier 2] Verify 'Competitions' tab displaying based on Special events availability
    DESCRIPTION: Not clear what should be tested in step 1 ( Specials events are displayed in separate tab but not displayed in SS response)
    DESCRIPTION: This test case verifies 'Competitions' tab displaying based on Special events availability [Tier 2]
    DESCRIPTION: 'Check Events' status active in CMS by default for the 'Competitions' tab for Tier 2 Sports only. It means that the availability of events on SS will be checked and based on received 'hasEvents' parameter (true or false) the particular tab will be displayed or no.
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page where 'Competitions' tab is enabled in CMS and 'CheckEvents' is active (Tier 2)
    PRECONDITIONS: 3. Make sure that Matches (Live and pre-match) and Outrights events are available for the particular sport
    PRECONDITIONS: 4. Also, **SPECIAL** events are created for the particular Sport
    PRECONDITIONS: **Sports Page Configs documentation:**
    PRECONDITIONS: - https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Sport+Page+Configs
    PRECONDITIONS: **OB Configuration:**
    PRECONDITIONS: - **Specials** Events should be created only with **No Primary** markets
    PRECONDITIONS: - **Special** events should contain **drilldownTagNames = MKTFLAG_SP** for **Market level**
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: - To verify Sports Tabs received from the CMS use the following <sport-tab> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-tab/<Category ID> -> tabs -> choose particular tab id (e.g. tab-competitions) -> verify hidden value (true or false)
    PRECONDITIONS: ![](index.php?/attachments/get/60156743)
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead**
    """
    keep_browser_open = True

    def test_001_verify_the_competitions_tab_displaying(self):
        """
        DESCRIPTION: Verify the 'Competitions' tab displaying
        EXPECTED: * 'Competitions' tab is present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response with 'hidden': 'false' parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * Matches events received from SS are displayed
        EXPECTED: * Outrights events received from SS are displayed
        EXPECTED: * Specials events are NOT received from SS and NOT displayed
        """
        pass

    def test_002_trigger_the_unavailability_of_all_matches_events_live_and_pre_match_and_outrights_eventsonly_specials_events_are_availableverify_the_competitions_tab_displaying(self):
        """
        DESCRIPTION: Trigger the unavailability of all Matches events (Live and pre-match) and Outrights events.
        DESCRIPTION: Only Specials events are available.
        DESCRIPTION: Verify the 'Competitions' tab displaying.
        EXPECTED: * 'Competitions' tab is NOT present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response with 'hidden': 'true' parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * Matches and Outrights events are NOT received from SS
        EXPECTED: * Specials events are NOT received from SS
        """
        pass
