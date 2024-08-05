import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C16375071_Verify_handling_of_not_available_data_from_Racing_Data_Hub_on_Next_Races_tabs_modules(Common):
    """
    TR_ID: C16375071
    NAME: Verify handling of not available data from Racing Data Hub on Next Races tabs/modules
    DESCRIPTION: This test case verifies handling of Next races events when data from Aggregation MS is not available and displaying of those events on Next Races tabs/modules
    DESCRIPTION: NOTE: Next races tab on HR Landing page is available only for Ladbrokes brand
    PRECONDITIONS: - In CMS: Horse Racing (HR) Racing Data Hub toggle is turned on : System-configuration > RacingDataHub > isEnabledForHorseRacing = true
    PRECONDITIONS: - At least one Horse Racing Event from Next Races tab is mapped with Racing Data Hub data
    PRECONDITIONS: - List of Aggregation MS environments: https://confluence.egalacoral.com/display/SPI/Aggregation+Java
    """
    keep_browser_open = True

    def test_001_open_oxygenladbrokes_app(self):
        """
        DESCRIPTION: Open Oxygen/Ladbrokes app
        EXPECTED: 
        """
        pass

    def test_002_for_mobile_open_homepage__next_races_tabfor_desktop_open_homepage_and_check_presence_of_next_races_module(self):
        """
        DESCRIPTION: [For mobile]: Open Homepage > 'Next races' tab
        DESCRIPTION: [For desktop]: Open Homepage and check presence of 'Next races' module
        EXPECTED: 'Next races' tab/module is displayed
        """
        pass

    def test_003_check_the_correct_displaying_of_the_information_for_the_event_which_is_mapped_with_not_available_df_api_datain_browser_devtools_block_request_to_racing_post_api_from_which_data_jockey_name_trainer_name_silks_etc_is_receivedeg_block_requests_to_domain_ld_prd1apidatafabricprodawsladbrokescoralcomto_find_it___use_content_value_in_network_xhr_tab_search(self):
        """
        DESCRIPTION: Check the correct displaying of the information for the event which is mapped with not available DF API data
        DESCRIPTION: (in browser devtools block request to Racing Post API from which data (Jockey Name, Trainer Name, Silks etc) is received):
        DESCRIPTION: e.g. block requests to domain ld-prd1.api.datafabric.prod.aws.ladbrokescoral.com
        DESCRIPTION: To find it - use 'content?' value in Network XHR tab search
        EXPECTED: - Data from Racing Data Hub is not displayed (Jockey Name, Trainer Name, Silks, Draw, Form etc)
        EXPECTED: - Events with odds are displayed correctly
        """
        pass

    def test_004_repeat_step_3_for_next_races_module_on_hr_landing_page(self):
        """
        DESCRIPTION: Repeat step 3 for Next races module on HR Landing page
        EXPECTED: Results are the same
        """
        pass

    def test_005_for_ladbrokes_brand_only_repeat_step_3_for_next_races_tab_on_hr_landing_page(self):
        """
        DESCRIPTION: [For Ladbrokes brand only]: Repeat step 3 for Next races tab on HR Landing page
        EXPECTED: Results are the same
        """
        pass
