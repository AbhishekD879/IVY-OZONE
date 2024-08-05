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
class Test_C16394910_Verify_HR_Silks_on_Next_Races_tabs_modules_when_Silks_are_missing_in_Racing_Data_Hub_API(Common):
    """
    TR_ID: C16394910
    NAME: Verify HR Silks on Next Races tabs/modules when Silks are missing in Racing Data Hub API
    DESCRIPTION: This test case verifies that HR Next Races tab or module is properly displayed when data from Racing Post API or individual silk is unavailable
    PRECONDITIONS: - In CMS: Horse Racing (HR) Racing Data Hub toggle is turned on : System-configuration > RacingDataHub > isEnabledForHorseRacing = true
    PRECONDITIONS: - At least one Horse Racing Event from Next Races tab/module is mapped with Racing Post data
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

    def test_003_check_silks_when_racing_post_data_is_available_but_silk_id_is_not_availablein_charles_tool_remove_silk_id_in_response_from_racing_post_data(self):
        """
        DESCRIPTION: Check Silks when Racing Post data is available, but silk ID is not available
        DESCRIPTION: (in Charles tool remove silk id in response from Racing Post data)
        EXPECTED: Generic default Silk is displayed near the horse name
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
