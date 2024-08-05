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
class Test_C16340974_Tier_1_and_2_Verify_Matches_tab_displaying_if_featured_modules_are_set_in_CMS(Common):
    """
    TR_ID: C16340974
    NAME: [Tier 1 and 2] Verify 'Matches' tab displaying if featured modules are set in CMS
    DESCRIPTION: This test case verifies 'Matches' tab displaying if featured modules are set in CMS for Tier 1 and Tier 2 sports
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Sports Landing page where 'Matches' tab is enabled in CMS
    PRECONDITIONS: 3. Quick Links or Highlights Carousel or Surface Bet or In-Play module is created on particular Sports Landing page
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: 2) CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: 3) Info about tabs displaying depends on Platforms or Tier Type could be found here: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-TabsdisplayingfordifferentPlatformsandTierTypes
    PRECONDITIONS: 4) To verify Matches availability on SS use the next link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForClass/XXXXX?&simpleFilter=event.categoryId:intersects:XX&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.startTime:greaterThanOrEqual:2019-03-20T22:00:00.000Z&existsFilter=event:simpleFilter:market.dispSortName:intersects:MR&simpleFilter=event.suspendAtTime:greaterThan:2019-03-21T13:32:30.000Z&translationLang=en&count=event:market
    PRECONDITIONS: - X.XX - the latest version of SS
    PRECONDITIONS: - XX - Category Id
    PRECONDITIONS: - XXXXX - Class Id
    PRECONDITIONS: 5) To verify Sports Tabs received from the CMS use <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-red-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID>
    PRECONDITIONS: **NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead:**
    PRECONDITIONS: ![](index.php?/attachments/get/100267212)
    PRECONDITIONS: ![](index.php?/attachments/get/100267213)
    """
    keep_browser_open = True

    def test_001_verify_matches_tabs_displaying_if_any_featured_module_is_created_and_data_is_received_from_ss_upcoming_and_live_events(self):
        """
        DESCRIPTION: Verify 'Matches' tabs displaying if any featured module is created and data is received from SS (upcoming and live events)
        EXPECTED: * 'Matches' tab is present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with **'hidden: false'** parameter
        EXPECTED: * Events received from SS are displayed
        EXPECTED: * Featured modules created in CMS are displayed
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass

    def test_002_verify_matches_tabs_displaying_if_in_play_featured_module_is_created_and_contains_live_events_and_no_other_upcoming_events_are_present(self):
        """
        DESCRIPTION: Verify 'Matches' tabs displaying if In-play featured module is created and contains live events and NO other upcoming events are present
        EXPECTED: * 'Matches' tab is present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with **'hidden: false'** parameter
        EXPECTED: * In-play featured module is displayed, containing live events
        EXPECTED: * 'No events found' message is NOT shown below In-play featured module
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass

    def test_003_verify_matches_tabs_displaying_if_any_featured_module_except_in_play_featured_module_is_created_and_data_is_not_received_from_ss_upcoming_and_live_events(self):
        """
        DESCRIPTION: Verify 'Matches' tabs displaying if any featured module (except In-play featured module) is created and data is NOT received from SS (upcoming and live events)
        EXPECTED: **Tier 2 Sports:**
        EXPECTED: * 'Matches' tab is NOT present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with **'hidden: true'** parameter
        EXPECTED: **Tier 1 Sports:**
        EXPECTED: * 'Matches' tab is present on Sports Landing page
        EXPECTED: * 'Matches' tab is received in <sport-config> response with **'hidden: false'** parameter
        EXPECTED: * Configured featured modules are displayed
        EXPECTED: * 'No events found' message is NOT shown below featured modules,if the feature module contains events, such as Surface Bet, in-play module, HighLIght Carousel.
        EXPECTED: NOTE: In scope of BMA-55205 <sport-tabs> call will be used instead
        """
        pass
