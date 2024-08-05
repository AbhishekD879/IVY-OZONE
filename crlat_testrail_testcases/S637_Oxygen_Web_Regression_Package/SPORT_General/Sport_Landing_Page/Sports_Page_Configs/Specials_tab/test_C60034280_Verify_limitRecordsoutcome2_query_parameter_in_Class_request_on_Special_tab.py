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
class Test_C60034280_Verify_limitRecordsoutcome2_query_parameter_in_Class_request_on_Special_tab(Common):
    """
    TR_ID: C60034280
    NAME: Verify  "limitRecords=outcome:2" query parameter in Class request on 'Special' tab
    DESCRIPTION: This test case verifies "limitRecords=outcome:2" query parameter in Class request on 'Special' tab for different Sports (Tier 1, Tier 2)
    DESCRIPTION: "limitRecords=outcome:2" query parameter is added to limit the number of outcomes to 2 as prices are displayed only in case if 1 outcome is available and in case if there are more outcomes - link to edp page is shown
    DESCRIPTION: NOTE: Specials data is received in /EventToOutcomeForClass not in Class request!
    PRECONDITIONS: Configurations:
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 1 (Tennis, Basketball), one event from Tier 2 and Tier 2 sport Outright(e.g. Golf, Cycling, Hurling, Motorbikes).
    PRECONDITIONS: To check SiteServ request go to dev tools -> Network -> XHR
    """
    keep_browser_open = True

    def test_001_navigate_to_football_landing_page__gt_special_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -&gt; 'Special' tab
        EXPECTED: 'Special' tab is opened, events are loaded
        """
        pass

    def test_002_check_class_request_on_special_tab_and_verify_limitrecordsoutcome_query_parameter(self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify "limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=outcome:2
        """
        pass

    def test_003_navigate_to_special_tab_on_any_other_sport_landing_page_with_tier_1_sport_configurationeg_tennis_basketball(self):
        """
        DESCRIPTION: Navigate to 'Special' tab on any other Sport Landing page with Tier 1 Sport configuration(e.g. Tennis, Basketball)
        EXPECTED: 'Special' tab is opened, events are loaded
        """
        pass

    def test_004_check_class_request_on_special_tab_and_verify_limitrecordsoutcome_query_parameter(self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify "limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=outcome:2
        """
        pass

    def test_005_navigate_to_special_tab_on_any_sport_landing_page_with_tier_2_sport_configurationeg_ice_hokey_volleyball_etc(self):
        """
        DESCRIPTION: Navigate to 'Special' tab on any Sport Landing page with Tier 2 Sport Configuration(e.g. Ice Hokey, Volleyball etc.)
        EXPECTED: 'Special' tab is opened, events are loaded
        """
        pass

    def test_006_check_class_request_on_special_tab_and_verify_limitrecordsoutcome_query_parameter(self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify "limitRecords=outcome" query parameter
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=outcome:2
        """
        pass

    def test_007_navigate_to_special_tab_on_any_sport_landing_page_with_tier_2_sport_outright_configurationeg_golf_cycling_hurling_motorbikes_etc(self):
        """
        DESCRIPTION: Navigate to 'Special' tab on any Sport Landing page with Tier 2 Sport Outright Configuration(e.g. Golf, Cycling, Hurling, Motorbikes etc.)
        EXPECTED: 'Special' tab is opened, events are loaded
        """
        pass

    def test_008_check_class_request_on_special_tab_and_verify_simplefilterclasshasopenevent_query_parameter_is_present_in_the_request(self):
        """
        DESCRIPTION: Check Class request on 'Special' tab and verify simpleFilter=class.hasOpenEvent query parameter is present in the request.
        EXPECTED: Class request to SS has query parameter:
        EXPECTED: limitRecords=outcome:2
        """
        pass
