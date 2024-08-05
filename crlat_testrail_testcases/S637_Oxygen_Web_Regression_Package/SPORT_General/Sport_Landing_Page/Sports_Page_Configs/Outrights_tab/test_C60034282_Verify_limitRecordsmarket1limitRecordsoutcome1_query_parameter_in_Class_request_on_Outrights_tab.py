import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C60034282_Verify_limitRecordsmarket1limitRecordsoutcome1_query_parameter_in_Class_request_on_Outrights_tab(Common):
    """
    TR_ID: C60034282
    NAME: Verify  "limitRecords=market:1&limitRecords=outcome:1" query parameter in Class request on 'Outrights' tab
    DESCRIPTION: This test case verifies "limitRecords=market:1&limitRecords=outcome:1" query parameter in Class request on 'Outrights' tab for different Sports (Tier 1, Tier 2)
    DESCRIPTION: To Update: Class request never contained "limitRecords=market:1&limitRecords=outcome:1" query parameters, this is only available in data requests like:
    DESCRIPTION: https://ss-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/58?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.eventSortCode:intersects:TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20&simpleFilter=event.suspendAtTime:greaterThan:2020-11-12T11:59:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: Configurations:
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 1 (Tennis, Basketball), one event from Tier 2 and Tier 2 sport Outright(e.g. Golf, Cycling, Hurling, Motorbikes).
    PRECONDITIONS: To check SiteServ request go to dev tools -> Network -> XHR
    """
    keep_browser_open = True

    def test_001_navigate_to_football_landing_page__gt_outrights_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -&gt; 'Outrights' tab
        EXPECTED: 'Outrights' tab is opened, events are loaded
        """
        pass

    def test_002_search_eventtooutcomeforclass_in_dev_tools__gt_networkcheck_class_request_on_outrights_tab_and_verify_limitrecordsmarketlimitrecordsoutcome_query_parameter(self):
        """
        DESCRIPTION: Search 'EventToOutcomeForClass' in dev tools -&gt; Network
        DESCRIPTION: Check Class request on 'Outrights' tab and verify "limitRecords=market&limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=market:1&limitRecords=outcome:1
        """
        pass

    def test_003_navigate_to_outrights_tab_on_any_other_sport_landing_page_with_tier_1_sport_configurationeg_tennis_basketball(self):
        """
        DESCRIPTION: Navigate to 'Outrights' tab on any other Sport Landing page with Tier 1 Sport configuration(e.g. Tennis, Basketball)
        EXPECTED: 'Outrights' tab is opened, events are loaded
        """
        pass

    def test_004_search_eventtooutcomeforclass_in_dev_tools__gt_networkcheck_class_request_on_outrights_tab_and_verify_limitrecordsmarketlimitrecordsoutcome_query_parameter(self):
        """
        DESCRIPTION: Search 'EventToOutcomeForClass' in dev tools -&gt; Network
        DESCRIPTION: Check Class request on 'Outrights' tab and verify "limitRecords=market&limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=market:1&limitRecords=outcome:1
        """
        pass

    def test_005_navigate_to_outrights_tab_on_any_sport_landing_page_with_tier_2_sport_configurationeg_ice_hokey_volleyball_etc(self):
        """
        DESCRIPTION: Navigate to 'Outrights' tab on any Sport Landing page with Tier 2 Sport Configuration(e.g. Ice Hokey, Volleyball etc.)
        EXPECTED: 'Outrights' tab is opened, events are loaded
        """
        pass

    def test_006_search_eventtooutcomeforclass_in_dev_tools__gt_networkcheck_class_request_on_outrights_tab_and_verify_limitrecordsmarketlimitrecordsoutcome_query_parameter(self):
        """
        DESCRIPTION: Search 'EventToOutcomeForClass' in dev tools -&gt; Network
        DESCRIPTION: Check Class request on 'Outrights' tab and verify "limitRecords=market&limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=market:1&limitRecords=outcome:1
        """
        pass

    def test_007_navigate_to_outrights_tab_on_any_sport_landing_page_with_tier_2_sport_outright_configurationeg_golf_cycling_hurling_motorbikes_etc(self):
        """
        DESCRIPTION: Navigate to 'Outrights' tab on any Sport Landing page with Tier 2 Sport Outright Configuration(e.g. Golf, Cycling, Hurling, Motorbikes etc.)
        EXPECTED: 'Outrights' tab is opened, events are loaded
        """
        pass

    def test_008_search_eventtooutcomeforclass_in_dev_tools__gt_networkcheck_class_request_on_outrights_tab_and_verify_limitrecordsmarketlimitrecordsoutcome_query_parameter(self):
        """
        DESCRIPTION: Search 'EventToOutcomeForClass' in dev tools -&gt; Network
        DESCRIPTION: Check Class request on 'Outrights' tab and verify "limitRecords=market&limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=market:1&limitRecords=outcome:1
        """
        pass
