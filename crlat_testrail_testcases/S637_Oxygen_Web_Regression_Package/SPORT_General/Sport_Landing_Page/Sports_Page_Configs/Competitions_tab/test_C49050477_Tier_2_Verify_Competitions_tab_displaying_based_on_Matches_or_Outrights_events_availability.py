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
class Test_C49050477_Tier_2_Verify_Competitions_tab_displaying_based_on_Matches_or_Outrights_events_availability(Common):
    """
    TR_ID: C49050477
    NAME: [Tier 2] Verify 'Competitions' tab displaying based on Matches or Outrights events availability
    DESCRIPTION: This test case verifies 'Competitions' tab displaying based on Matches (Live and pre-match) or Outrights events availability [Tier 2]
    DESCRIPTION: 'Check Events' status active in CMS by default for the 'Competitions' tab for Tier 2 Sports only. It means that the availability of events on SS will be checked and based on received 'hasEvents' parameter (true or false) the particular tab will be displayed or no.
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Sports Landing page where 'Competitions' tab is enabled in CMS and 'CheckEvents' is active (Tier 2)
    PRECONDITIONS: 3. Make sure that Matches (Live and pre-match) and Outrights events are available for the particular sport
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
        """
        pass

    def test_002_trigger_the_unavailability_of_all_matches_events_live_and_pre_matchonly_outrights_events_are_availableverify_the_competitions_tab_displaying(self):
        """
        DESCRIPTION: Trigger the unavailability of all Matches events (Live and pre-match).
        DESCRIPTION: Only Outrights events are available.
        DESCRIPTION: Verify the 'Competitions' tab displaying.
        EXPECTED: * 'Competitions' tab is present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response with 'hidden': 'false' parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * Matches events are NOT received from SS
        EXPECTED: * Outrights events received from SS are displayed
        """
        pass

    def test_003_trigger_the_unavailability_of_all_outrights_eventsonly_matches_live_and_pre_match_events_are_availableverify_the_competitions_tab_displaying(self):
        """
        DESCRIPTION: Trigger the unavailability of all Outrights events.
        DESCRIPTION: Only Matches (Live and pre-match) events are available.
        DESCRIPTION: Verify the 'Competitions' tab displaying.
        EXPECTED: * 'Competitions' tab is present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response with 'hidden': 'false' parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        EXPECTED: * Matches events received from SS are displayed
        EXPECTED: * Outrights events are NOT received from SS
        """
        pass

    def test_004_trigger_the_unavailability_of_all_outrights_eventstrigger_the_unavailability_of_all_matches_live_and_pre_matcheventsverify_the_competitions_tab_displaying(self):
        """
        DESCRIPTION: Trigger the unavailability of all Outrights events.
        DESCRIPTION: Trigger the unavailability of all Matches (Live and pre-match)events.
        DESCRIPTION: Verify the 'Competitions' tab displaying.
        EXPECTED: * 'Competitions' tab is NOT present on Sports Landing page
        EXPECTED: * 'Competitions' tab is received in <сategory> response with 'hidden': 'true' parameter (NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead)
        """
        pass
