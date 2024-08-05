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
class Test_C518213_OUTDATED_YourCall_Market_Name_displaying_depending_on_CMS_configuration(Common):
    """
    TR_ID: C518213
    NAME: [OUTDATED!] #YourCall Market Name displaying depending on CMS configuration
    DESCRIPTION: This test case verifies #YourCall Market Name displaying depending on CMS configuration
    PRECONDITIONS: 1. In CMS - Config YourCallMarket group is created with attributes: <Sport name> - input - #YourCall
    PRECONDITIONS: 2. In CMS - System Configuration - YOURCALLMARKET  parameter is specified
    PRECONDITIONS: 3. There is Sport's event with configured YourCall Markets in TI tool (markets with |YourCallSpecials| market template name are added for the event)
    PRECONDITIONS: 4. |YourCallSpecials| market template is available in TI tool for the following Football leagues:
    PRECONDITIONS: **Test 2:**
    PRECONDITIONS: Premier League - 597276
    PRECONDITIONS: La Liga - 599078
    PRECONDITIONS: Serie A - 599077
    PRECONDITIONS: Champions League - 599079
    PRECONDITIONS: **Stage:**
    PRECONDITIONS: Premier League 832526
    PRECONDITIONS: La Liga 832527
    PRECONDITIONS: Serie A 832528
    PRECONDITIONS: Champions League 832529
    PRECONDITIONS: **Production:**
    PRECONDITIONS: Premier League - 2308603
    PRECONDITIONS: La Liga - 2308604
    PRECONDITIONS: Serie A - 2308606
    PRECONDITIONS: Champions League - 2308607
    PRECONDITIONS: 8) |YourCallSpecials| market template is available in TI tool for the following leagues:
    PRECONDITIONS: NFL (American Football)
    PRECONDITIONS: NBA (Basketball)
    PRECONDITIONS: MLB (Baseball)
    PRECONDITIONS: AFL (Aussie Rules)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_select_sports_event_with_configured_yourcall_markets_and_go_to_event_details_page(self):
        """
        DESCRIPTION: Select Sport's event with configured YourCall Markets and go to event details page
        EXPECTED: - Event details page is opened
        EXPECTED: - #YourCall markets are displayed for the event
        """
        pass

    def test_003_verify_name_dispaying_for_yourcall_markets_header(self):
        """
        DESCRIPTION: Verify Name dispaying for #YourCall markets header
        EXPECTED: - Configured in CMS name is displayed in the Header
        """
        pass

    def test_004_verify_long_name_displaying_in_application_for_yourcall_markets_header(self):
        """
        DESCRIPTION: Verify long Name displaying in application for #YourCall markets header
        EXPECTED: Name is displayed fully without curtailment
        """
        pass

    def test_005_delete_value_for_yourcallmarket_parameter_in_cmsgo_to_event_details_page_and_verify_name_displaying_for_yourcall_markets_header(self):
        """
        DESCRIPTION: Delete value for YOURCALLMARKET parameter in CMS
        DESCRIPTION: Go to event details page and verify name displaying for #YourCall markets header
        EXPECTED: - default name '#YourCallSpecials' is displayed in the Header
        """
        pass

    def test_006_update_yourcallmarket_parameter_value_in_cms_and_save_changesgo_to_event_details_page_and_verify_name_displaying_for_yourcall_markets_header(self):
        """
        DESCRIPTION: Update YOURCALLMARKET parameter value in CMS and save changes
        DESCRIPTION: Go to event details page and verify name displaying for #YourCall markets header
        EXPECTED: - Updated name value is displayed in the Header
        """
        pass
