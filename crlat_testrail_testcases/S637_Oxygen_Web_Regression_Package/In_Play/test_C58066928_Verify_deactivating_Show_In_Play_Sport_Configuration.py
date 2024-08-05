import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C58066928_Verify_deactivating_Show_In_Play_Sport_Configuration(Common):
    """
    TR_ID: C58066928
    NAME: Verify deactivating "Show In Play"  Sport Configuration
    DESCRIPTION: This test case verifies deactivation of "Show In Play" Sport Configuration
    PRECONDITIONS: - CMS endpoints https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - CMS creds https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: - Football module  (for example) is available on Sports Carousel 'In-Play'
    """
    keep_browser_open = True

    def test_001__in_app___sports_carousel___in_play_verify_if_for_example_football_module_is_available(self):
        """
        DESCRIPTION: * In App -> Sports Carousel -> In-Play
        DESCRIPTION: * Verify if (for example) Football module is available
        EXPECTED: Football module is available
        """
        pass

    def test_002_open_ws_and_check_the_response(self):
        """
        DESCRIPTION: Open WS and check the response
        EXPECTED: INPLAY_SPORTS_RIBBON is present
        EXPECTED: Football module is present
        """
        pass

    def test_003__go_to_cms___sport_pages___sport_category_navigate_to_football_for_example_and_open_general_sport_configuration_uncheck_the_check_box_show_in_play(self):
        """
        DESCRIPTION: * Go to CMS -> Sport Pages -> Sport Category
        DESCRIPTION: * Navigate to Football (for example) and open 'General Sport Configuration'
        DESCRIPTION: * Uncheck the check box "Show In Play"
        EXPECTED: "Show In Play" configuration is switched off
        """
        pass

    def test_004_in_app_verify_if_current_module_is_available(self):
        """
        DESCRIPTION: In App: verify if current module is available
        EXPECTED: Football module is NOT available
        """
        pass

    def test_005_open_ws_and_check_the_response(self):
        """
        DESCRIPTION: Open WS and check the response
        EXPECTED: IN_PLAY_SPORTS_RIBBON_CHANGED is present
        EXPECTED: Football module is Not present
        """
        pass

    def test_006_in_cms_tick_the_check_box_show_in_play_for_current_module(self):
        """
        DESCRIPTION: In CMS: tick the check box "Show In Play" for current module
        EXPECTED: "Show In Play" configuration is switched on
        """
        pass

    def test_007_verify_presence_of_the_module_within_the_app_and_ws_response(self):
        """
        DESCRIPTION: Verify presence of the module within the app and WS response
        EXPECTED: * Football module is available in App
        EXPECTED: * Football module is available within WS response
        """
        pass

    def test_008_repeat_steps_1_7_for_coral(self):
        """
        DESCRIPTION: Repeat steps 1-7 for coral
        EXPECTED: 
        """
        pass