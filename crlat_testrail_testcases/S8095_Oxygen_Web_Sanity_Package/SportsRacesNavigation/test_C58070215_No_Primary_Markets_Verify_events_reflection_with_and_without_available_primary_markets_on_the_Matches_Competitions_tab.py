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
class Test_C58070215_No_Primary_Markets_Verify_events_reflection_with_and_without_available_primary_markets_on_the_Matches_Competitions_tab(Common):
    """
    TR_ID: C58070215
    NAME: [No Primary Markets] Verify events reflection with and without available primary markets on the 'Matches'/'Competitions' tab
    DESCRIPTION: This test case verifies events displaying with the available primary market on the 'Matches'/'Competitions' tab.
    DESCRIPTION: **Note: Football is out of scope**
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: The event should contain the following settings:
    PRECONDITIONS: - Primary Market (|Match Betting|, |Money Line|, |Match Winner|, etc. depends on Sport) with **dispSortName="HH"** or **dispSortName="MR"**
    PRECONDITIONS: where
    PRECONDITIONS: HH = Head to Head
    PRECONDITIONS: MR = Match Result
    PRECONDITIONS: - Not Primary Market (|Handicap Match Result|) with **dispSortName="MH"** or **dispSortName="WH"**
    PRECONDITIONS: where
    PRECONDITIONS: MH = Match Handicap Result (3 way)
    PRECONDITIONS: WH = Match Handicap Result (2 Way)
    PRECONDITIONS: To configure the Primary market for Sport use the following link https://confluence.egalacoral.com/display/SPI/Primary+Markets+and+dispSortNames+for+Different+Sports
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
    PRECONDITIONS: - To verify simple filters in <EventToOutcomeForClass> request on 'Matches'/'Competitions' tab please check the Request URL:
    PRECONDITIONS: ![](index.php?/attachments/get/99322539)
    PRECONDITIONS: *The values set for "marketTemplateName" and "dispSortName" via CMS will be add to the filters in <EventToOutcomeForClass> request.*
    PRECONDITIONS: - To verify events filtering on 'Competitions' tab (Tier 2 only e.g. Cricket) see the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Sport+Page+Configs#SportPageConfigs-Competitions
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To trigger live updates use the OB system https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Updates on 'Matches' and 'Competitions' tab are received via 'push'
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Sport Landing page
    PRECONDITIONS: 3. Choose the 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_event_displaying_on_the_page(self):
        """
        DESCRIPTION: Verify event displaying on the page
        EXPECTED: - Event with available Primary Market and outcomes is displayed on the page
        EXPECTED: - Selections from the Primary Market are displayed on the event card
        """
        pass

    def test_002_verify_the_filters_added_to_eventtooutcomeforclass_request_to_the_ss(self):
        """
        DESCRIPTION: Verify the filters added to <EventToOutcomeForClass> request to the SS
        EXPECTED: The following filters should be added to the request:
        EXPECTED: - market.templateMarketName:intersects:|Primary Market Name|,|Handicap Match Result| depends on settings made via CMS
        EXPECTED: - market.dispSortName:intersects:MR,HH,MH,WH depends on settings made via CMS
        EXPECTED: - event:simpleFilter:market.dispSortName:intersects:MR,HH,MH,WH depends on settings made via CMS
        """
        pass

    def test_003_verify_the_received_data_in_eventtooutcomeforclass_response_from_the_ss(self):
        """
        DESCRIPTION: Verify the received data in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Event is received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Primary and NOT Primary markets are received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_004__trigger_the_undisplaying_of_the_primary_market_for_event_that_contains_not_primary_market_as_well_dont_refresh_the_page_verify_the_event_reflection(self):
        """
        DESCRIPTION: * Trigger the undisplaying of the Primary Market for event that contains Not Primary Market as well.
        DESCRIPTION: * Don't refresh the page.
        DESCRIPTION: * Verify the event reflection.
        EXPECTED: - General Event card is replaced by Outright card that contains the following elements:
        EXPECTED: - Event Name
        EXPECTED: - Navigation arrow
        EXPECTED: - 'Odds Card' header disappears in case the primary market is undisplayed for the last event in a 'Type' accordion
        EXPECTED: - Updates for the market with the parameter 'displayed': "N" is received in 'push'
        """
        pass

    def test_005__refesh_the_page_verify_the_filters_added_to_eventtooutcomeforclass_request_to_the_ss(self):
        """
        DESCRIPTION: * Refesh the page.
        DESCRIPTION: * Verify the filters added to <EventToOutcomeForClass> request to the SS
        EXPECTED: The following filters should be added to the request:
        EXPECTED: - market.templateMarketName:intersects:|Primary Market Name|,|Handicap Match Result| depends on settings made via CMS
        EXPECTED: - market.dispSortName:intersects:MR,HH,MH,WH depends on settings made via CMS
        EXPECTED: - event:simpleFilter:market.dispSortName:intersects:MR,HH,MH,WH depends on settings made via CMS
        """
        pass

    def test_006_verify_the_received_data_in_eventtooutcomeforclass_response_from_the_ss(self):
        """
        DESCRIPTION: Verify the received data in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Event is received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Only NOT Primary market is received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_007__navigate_to_competitions_tab_tier_2_only_eg_cricket_repeat_steps_1_6(self):
        """
        DESCRIPTION: * Navigate to 'Competitions' tab (Tier 2 only e.g. Cricket).
        DESCRIPTION: * Repeat steps 1-6.
        EXPECTED: 
        """
        pass
