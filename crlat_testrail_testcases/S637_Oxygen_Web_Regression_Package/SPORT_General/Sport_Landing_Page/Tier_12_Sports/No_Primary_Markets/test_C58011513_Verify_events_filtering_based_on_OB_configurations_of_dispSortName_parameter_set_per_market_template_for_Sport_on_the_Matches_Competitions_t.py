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
class Test_C58011513_Verify_events_filtering_based_on_OB_configurations_of_dispSortName_parameter_set_per_market_template_for_Sport_on_the_Matches_Competitions_tab(Common):
    """
    TR_ID: C58011513
    NAME: Verify events filtering based on OB configurations of  'dispSortName' parameter set per market template for Sport on the 'Matches'/'Competitions' tab
    DESCRIPTION: This test case verifies events filtering based on OB configurations of 'dispSortName' parameter set per market template for Sport on the 'Matches'/'Competitions' tab.
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

    def test_001_verify_displaying_of_the_event_with_primary_market_by_set_dispsortnamemr_or_dispsortnamehh_parameter(self):
        """
        DESCRIPTION: Verify displaying of the event with Primary market by set **dispSortName="MR"** or **dispSortName="HH"** parameter
        EXPECTED: - Events that have Primary Market with the following attributes and outcomes are displayed:
        EXPECTED: - "marketTemplateName" = |Match Betting|, |Money Line|, |Match Winner|, etc. depends on Sport
        EXPECTED: - "dispSortName"='MR' or dispSortName='HH'
        EXPECTED: - Selections from the Primary Market are displayed on the event card
        EXPECTED: - Event is received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Primary and NOT Primary markets are received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_002_verify_simplefilter_in_eventtooutcomeforclass_request_to_the_ss(self):
        """
        DESCRIPTION: Verify 'simpleFilter' in <EventToOutcomeForClass> request to the SS
        EXPECTED: The following filter should be added to the request:
        EXPECTED: - market.templateMarketName:intersects:|<Primary market for Sport>|,|Handicap Match Result|
        EXPECTED: - market.dispSortName:intersects:HH or MR, MH or WH
        EXPECTED: - event:simpleFilter:market.dispSortName:intersects:MR or HH, MH or WH
        """
        pass

    def test_003__change_the_dispsortname_value_to__mr_or__hh_in_the_ob_system_for_the_primary_market_name_market_template_back_to_the_app_refresh_the_page(self):
        """
        DESCRIPTION: * Change the "dispSortName" value to =! 'MR' or =! 'HH' in the OB system for the |Primary Market Name| market template.
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        EXPECTED: - Event is displayed on the page
        EXPECTED: - Selections are NOT displayed on the event card (event card is used for navigation to EDP)
        EXPECTED: - Event is received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Only NOT Primary market is received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_004_verify_displaying_of_the_event_with_not_primary_market_by_set_dispsortnamemh_or_dispsortnamewh_parameter(self):
        """
        DESCRIPTION: Verify displaying of the event with NOT Primary market by set **dispSortName="MH"** or **dispSortName="WH"** parameter
        EXPECTED: - Events that have NOT Primary Market with the following attributes and outcomes are displayed:
        EXPECTED: - "marketTemplateName" = |Handicap Match Result|
        EXPECTED: - "dispSortName"='MH' or dispSortName='WH'
        EXPECTED: - Selections are NOT displayed on the event card (event card is used for navigation to EDP)
        EXPECTED: - Event is received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Only NOT Primary market is received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_005_verify_simplefilter_in_eventtooutcomeforclass_request_to_the_ss(self):
        """
        DESCRIPTION: Verify 'simpleFilter' in <EventToOutcomeForClass> request to the SS
        EXPECTED: The following filter should be added to the request:
        EXPECTED: - market.templateMarketName:intersects:|<Primary market for Sport>|,|Handicap Match Result|
        EXPECTED: - market.dispSortName:intersects:HH or MR, MH or WH
        EXPECTED: - event:simpleFilter:market.dispSortName:intersects:MR or HH, MH or WH
        """
        pass

    def test_006__change_the_dispsortname_value_to__mh_or__wh_in_the_ob_system_for_handicap_match_result_market_template_back_to_the_app_refresh_the_page(self):
        """
        DESCRIPTION: * Change the "dispSortName" value to =! 'MH' or =! 'WH' in the OB system for |Handicap Match Result| market template.
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        EXPECTED: - Event is NOT displayed on the page
        EXPECTED: - Event is NOT received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_007__navigate_to_the_competitions_tab_repeat_steps_1_6(self):
        """
        DESCRIPTION: * Navigate to the 'Competitions' tab.
        DESCRIPTION: * Repeat steps 1-6.
        EXPECTED: 
        """
        pass
