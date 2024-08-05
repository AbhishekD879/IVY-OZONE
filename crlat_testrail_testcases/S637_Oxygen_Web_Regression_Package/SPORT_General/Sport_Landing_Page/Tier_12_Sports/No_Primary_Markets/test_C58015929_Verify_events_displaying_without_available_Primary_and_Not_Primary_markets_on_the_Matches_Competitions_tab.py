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
class Test_C58015929_Verify_events_displaying_without_available_Primary_and_Not_Primary_markets_on_the_Matches_Competitions_tab(Common):
    """
    TR_ID: C58015929
    NAME: Verify events displaying without available Primary and Not Primary markets on the 'Matches'/'Competitions' tab
    DESCRIPTION: This test case verifies events displaying without available Primary and Not Primary markets on the 'Matches'/'Competitions' tab.
    DESCRIPTION: **Note: Football is out of scope**
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: The event should contain the following settings:
    PRECONDITIONS: Not Primary Market **=!** |Handicap Match Result| with 'dispSortName' **=!** "MH" or 'dispSortName' **=!** "WH"
    PRECONDITIONS: To check the Primary market per Sport use the following link https://confluence.egalacoral.com/display/SPI/Primary+Markets+and+dispSortNames+for+Different+Sports
    PRECONDITIONS: **CMS Configurations:**
    PRECONDITIONS: To configure filters for the particular sport use the following instruction:
    PRECONDITIONS: * Navigate to CMS -> Sports Pages -> Sports Categories -> choose <Sport e.g. Cricket>
    PRECONDITIONS: * Put the values in 'Disp sort name' field (MR, HH for Primary markets and MH, WH for NOT Primary markets)
    PRECONDITIONS: * Put the values in 'Primary markets' field (|Match Betting|, |Money Line|, |Match Winner|, etc. depends on Sport and |Handicap Match Result|)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To verify filtering for markets set via CMS use the following <sport-config> response:
    PRECONDITIONS: https://<particular env e.g. sports-tst2.ladbrokes.com>/cms/api/<Brand>/sport-config/<Category ID> -> config -> tabs -> today/tomorrow/future tab -> verify the presense of following parameters:
    PRECONDITIONS: - "marketTemplateMarketNameIntersects"
    PRECONDITIONS: - "dispSortName"
    PRECONDITIONS: ![](index.php?/attachments/get/99322540)
    PRECONDITIONS: **NOTE: In scope of BMA-55206 "marketTemplateMarketNameIntersects" and "dispSortName" will be received in <initial-data>:**
    PRECONDITIONS: ![](index.php?/attachments/get/121567991)
    PRECONDITIONS: - To verify simple filters in <EventToOutcomeForClass> request on 'Matches'/'Competitions' tab please check the Request URL:
    PRECONDITIONS: ![](index.php?/attachments/get/99322539)
    PRECONDITIONS: *The values set for "marketTemplateName" and "dispSortName" via CMS will be add to the filters in <EventToOutcomeForClass> request.*
    PRECONDITIONS: - To verify events filtering on 'Competitions' tab (Tier 2 only e.g. Cricket) see the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Sport+Page+Configs#SportPageConfigs-Competitions
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Sport Landing page
    PRECONDITIONS: 3. Choose the 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_event_displaying_on_the_page(self):
        """
        DESCRIPTION: Verify event displaying on the page
        EXPECTED: - Event is NOT displayed on the page
        EXPECTED: - Event is NOT received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - NOT Primary markets are NOT received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_002__navigate_to_competitions_tab_tier_2_only_eg_cricket_verify_event_displaying_on_the_page(self):
        """
        DESCRIPTION: * Navigate to 'Competitions' tab (Tier 2 only e.g. Cricket).
        DESCRIPTION: * Verify event displaying on the page.
        EXPECTED: - Event is NOT displayed on the page
        EXPECTED: - Event is NOT received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - NOT Primary markets are NOT received in <EventToOutcomeForClass> response from the SS
        """
        pass