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
class Test_C58012983_Verify_filters_adding_to_request_based_on_CMS_configurations_of_Sports_on_the_Matches_Competitions_tab(Common):
    """
    TR_ID: C58012983
    NAME: Verify filters adding to request based on CMS configurations of Sports on the 'Matches'/'Competitions' tab
    DESCRIPTION: This test case verifies filters adding to request based on CMS configurations of Sports on the 'Matches'/'Competitions' tab.
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
    PRECONDITIONS: *The values set in CMS for 'Disp sort name' and 'Primary markets' fields will be added as filters "market.dispSortName","event:simpleFilter:market.dispSortName", and "market.templateMarketName:intersects" in <EventToOutcomeForClass> request.*
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

    def test_001_verify_sport_config_response_from_cms_for_particular_sport(self):
        """
        DESCRIPTION: Verify <sport-config> response from CMS for particular Sport
        EXPECTED: The following parameters are received in the <sport-config> response -> config -> request:
        EXPECTED: - marketTemplateMarketNameIntersects:|Primary Market Name| depends on Sport and |Handicap Match Result|
        EXPECTED: - dispSortName: ["MR", "HH", "MH", "WH"]
        EXPECTED: - dispSortNameIncludeOnly: ["MR", "HH", "MH", "WH"]
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
        EXPECTED: - Events are received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Primary and NOT Primary markets are received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_004__open_the_cms___sports_pages___sports_categories___choose_sport_eg_cricket_change_the_dispsortname_value_to__mr_or_hh_depends_on_sport_or_remove_back_to_the_app_refresh_the_page_verify_sport_config_response_from_cms_for_particular_sport(self):
        """
        DESCRIPTION: * Open the CMS -> Sports Pages -> Sports Categories -> choose <Sport e.g. Cricket>.
        DESCRIPTION: * Change the "dispSortName" value to =! 'MR' or 'HH' (depends on Sport) or remove.
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        DESCRIPTION: * Verify <sport-config> response from CMS for particular Sport
        EXPECTED: The following parameters are received in the <sport-config> response -> config -> request:
        EXPECTED: - marketTemplateMarketNameIntersects:|Primary Market Name| depends on Sport and |Handicap Match Result|
        EXPECTED: - dispSortName: ["=!MR" or **removed**, "=!HH" or **removed**, "MH", "WH"]
        EXPECTED: - dispSortNameIncludeOnly: ["=!MR" or **removed**, "=!HH" or **removed**, "MH", "WH"]
        """
        pass

    def test_005_verify_the_filters_added_to_eventtooutcomeforclass_request_to_the_ss(self):
        """
        DESCRIPTION: Verify the filters added to <EventToOutcomeForClass> request to the SS
        EXPECTED: The following filters should be added to the request:
        EXPECTED: - market.templateMarketName:intersects:|Primary Market Name|,|Handicap Match Result| depends on settings made via CMS
        EXPECTED: - market.dispSortName:intersects:"=!MR or **removed** ","=!MR or **removed** ",MH,WH depends on settings made via CMS
        EXPECTED: - event:simpleFilter:market.dispSortName:intersects:"=!MR or **removed**","=!MR or **removed** ",MH,WH depends on settings made via CMS
        """
        pass

    def test_006_verify_the_received_data_in_eventtooutcomeforclass_response_from_the_ss(self):
        """
        DESCRIPTION: Verify the received data in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Events are received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Only NOT Primary markets is received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_007__open_the_cms___sports_pages___sports_categories___choose_sport_eg_cricket_change_the_dispsortname_value_to_mr_or_hh_depends_on_sport_change_the_primary_markets_value_to__primary_market_name_depends_on_sport_or_remove_back_to_the_app_refresh_the_page_verify_sport_config_response_from_cms_for_particular_sport(self):
        """
        DESCRIPTION: * Open the CMS -> Sports Pages -> Sports Categories -> choose <Sport e.g. Cricket>.
        DESCRIPTION: * Change the "dispSortName" value to 'MR' or 'HH' (depends on Sport).
        DESCRIPTION: * Change the "Primary markets" value to =! |Primary Market Name| (depends on Sport) or remove.
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        DESCRIPTION: * Verify <sport-config> response from CMS for particular Sport
        EXPECTED: The following parameters are received in the <sport-config> response -> config -> request:
        EXPECTED: - marketTemplateMarketNameIntersects: **Edited** |Primary Market Name| depends on Sport or **Removed** and |Handicap Match Result|
        EXPECTED: - dispSortName: ["MR", "HH", "MH", "WH"]
        EXPECTED: - dispSortNameIncludeOnly: ["MR", "HH", "MH", "WH"]
        """
        pass

    def test_008_verify_the_filters_added_to_eventtooutcomeforclass_request_to_the_ss(self):
        """
        DESCRIPTION: Verify the filters added to <EventToOutcomeForClass> request to the SS
        EXPECTED: The following filters should be added to the request:
        EXPECTED: - market.templateMarketName:intersects: **Edited** |Primary Market Name| or **Removed** depends on settings made via CMS
        EXPECTED: - market.dispSortName:intersects:MR,HH,MH,WH depends on settings made via CMS
        EXPECTED: - event:simpleFilter:market.dispSortName:intersects:MR,HH,MH,WH depends on settings made via CMS
        """
        pass

    def test_009_verify_the_received_data_in_eventtooutcomeforclass_response_from_the_ss(self):
        """
        DESCRIPTION: Verify the received data in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Events are received in <EventToOutcomeForClass> response from the SS
        EXPECTED: - Only NOT Primary markets is received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_010__open_the_cms___sports_pages___sports_categories___choose_sport_eg_cricket_change_the_dispsortname_value_to_mr_or_hh_depends_on_sport_or_change_the_primary_markets_value_to__primary_market_name_depends_on_sport_or_remove_change_the_dispsortname_value_to_mh_or_wh_depends_on_sport_or_change_the_primary_markets_value_to__handicap_match_result_depends_on_sport_or_remove_back_to_the_app_refresh_the_page_verify_sport_config_response_from_cms_for_particular_sport(self):
        """
        DESCRIPTION: * Open the CMS -> Sports Pages -> Sports Categories -> choose <Sport e.g. Cricket>.
        DESCRIPTION: * Change the "dispSortName" value to '=!MR' or '=!HH' (depends on Sport) **OR** Change the "Primary markets" value to =! |Primary Market Name| (depends on Sport) or remove.
        DESCRIPTION: * Change the "dispSortName" value to '=!MH' or '=!WH' (depends on Sport) **OR** Change the "Primary markets" value to =! |Handicap Match Result| (depends on Sport) or remove.
        DESCRIPTION: * Back to the app.
        DESCRIPTION: * Refresh the page.
        DESCRIPTION: * Verify <sport-config> response from CMS for particular Sport
        EXPECTED: The following parameters are received in the <sport-config> response -> config -> request:
        EXPECTED: - marketTemplateMarketNameIntersects: **Edited/Removed** |Primary Market Name| depends on Sport AND **Edited/Removed** |Handicap Match Result|
        EXPECTED: - dispSortName: ["=!MR" or **removed** , "=!HH" or **removed** , "=!MH" or **removed** , "=!WH" or **removed** ]
        EXPECTED: - dispSortNameIncludeOnly: ["=!MR" or **removed** , "=!HH" or **removed** , "=!MH" or **removed** , "=!WH" or **removed** ]
        """
        pass

    def test_011_verify_the_filters_added_to_eventtooutcomeforclass_request_to_the_ss(self):
        """
        DESCRIPTION: Verify the filters added to <EventToOutcomeForClass> request to the SS
        EXPECTED: The following filters should be added to the request:
        EXPECTED: - market.templateMarketName:intersects: **Edited/Removed** |Primary Market Name| AND **Edited/Removed** |Handicap Match Result| depends on settings made via CMS
        EXPECTED: - market.dispSortName:intersects:"=!MR or **removed** ","=!MR or **removed** ","=!MH or **removed** ","=!WH or **removed** " depends on settings made via CMS
        EXPECTED: - event:simpleFilter:market.dispSortName:intersects:"=!MR or **removed** ","=!MR or **removed** ","=!MH or **removed** ","=!WH or **removed** " depends on settings made via CMS
        """
        pass

    def test_012_verify_the_received_data_in_eventtooutcomeforclass_response_from_the_ss(self):
        """
        DESCRIPTION: Verify the received data in <EventToOutcomeForClass> response from the SS
        EXPECTED: Events are NOT received in <EventToOutcomeForClass> response from the SS
        """
        pass

    def test_013__navigate_to_the_competitions_tab_repeat_steps_1_12(self):
        """
        DESCRIPTION: * Navigate to the 'Competitions' tab.
        DESCRIPTION: * Repeat steps 1-12.
        EXPECTED: 
        """
        pass
