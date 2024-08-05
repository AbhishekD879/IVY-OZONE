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
class Test_C16375070_Verify_Racing_Data_Hub_on_Next_races_tabs_module(Common):
    """
    TR_ID: C16375070
    NAME: Verify Racing Data Hub on Next races tabs/module
    DESCRIPTION: This test case verifies receiving and displaying data from Racing Post API on Next races tabs/modules
    DESCRIPTION: NOTE: Next races tab on HR Landing page available only for Ladbrokes brand
    PRECONDITIONS: - In CMS: Horse Racing (HR) Racing Data Hub toggle is turned on : System-configuration > RacingDataHub > isEnabledForHorseRacing = true
    PRECONDITIONS: - At least one Horse Racing Event from Next Races tab is mapped with DF API data (Racing Post)
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

    def test_003_check_the_correct_displaying_of_the_information_for_the_event_which_is_mapped_with_df_api_data_racing_post(self):
        """
        DESCRIPTION: Check the correct displaying of the information for the event which is mapped with DF API data (Racing Post)
        EXPECTED: Information is available and displayed (data for Jockey Name, Trainer Name, Silks, Runner Number(saddle), Draw, Form is present)
        EXPECTED: ![](index.php?/attachments/get/34237)
        """
        pass

    def test_004_check_that_data_for_the_race_is_taken_from_aggregation_ms_jockey_name_trainer_name_silks_runner_number_draw_form(self):
        """
        DESCRIPTION: Check that data for the race is taken from Aggregation MS (Jockey Name, Trainer Name, Silks, Runner Number, Draw, Form)
        EXPECTED: Displayed data is received from Racing Data Hub in response:
        EXPECTED: e.g. https://ld-prd1.api.datafabric.prod.aws.ladbrokescoral.com/v4/sportsbook-api/categories/21/events/228859733,228864955,228859734,228863900,228865712,228859736/content?locale=en-GB&api-key=LD755f5f6b195b4688969e7e976df86855
        """
        pass

    def test_005_repeat_steps_3_4_for_next_races_module_on_hr_landing_page(self):
        """
        DESCRIPTION: Repeat steps 3-4 for Next races module on HR Landing page
        EXPECTED: Results are the same
        """
        pass

    def test_006_for_ladbrokes_brand_only_repeat_steps_3_4_for_next_races_tab_on_hr_landing_page(self):
        """
        DESCRIPTION: [For Ladbrokes brand only]: Repeat steps 3-4 for Next races tab on HR Landing page
        EXPECTED: Results are the same
        """
        pass
