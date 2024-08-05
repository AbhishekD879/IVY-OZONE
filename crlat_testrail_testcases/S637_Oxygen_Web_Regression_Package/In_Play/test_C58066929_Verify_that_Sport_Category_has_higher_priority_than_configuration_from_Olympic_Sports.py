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
class Test_C58066929_Verify_that_Sport_Category_has_higher_priority_than_configuration_from_Olympic_Sports(Common):
    """
    TR_ID: C58066929
    NAME: Verify that "Sport Category" has higher priority than configuration from "Olympic Sports"
    DESCRIPTION: This test case verifies that "Sport Category" has higher priority than configuration from "Olympic Sports"
    PRECONDITIONS: - CMS endpoints https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - CMS creds https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: - Football module (for example) is available and activated in Sports Carousel 'In-Play'
    """
    keep_browser_open = True

    def test_001__in_app___sports_carousel___in_play_verify_if_for_example_football_module_is_available(self):
        """
        DESCRIPTION: * In App -> Sports Carousel -> In-Play
        DESCRIPTION: * Verify if (for example) Football module is available
        EXPECTED: Football module is available
        """
        pass

    def test_002__go_to_cms___sport_pages___olympic_sports_navigate_to_football_for_example_uncheck_the_check_box_active(self):
        """
        DESCRIPTION: * Go to CMS -> Sport Pages -> Olympic Sports
        DESCRIPTION: * Navigate to Football (for example)
        DESCRIPTION: * Uncheck the check box "Active"
        EXPECTED: Football module is deactivated
        """
        pass

    def test_003_in_app_verify_if_current_module_is_available(self):
        """
        DESCRIPTION: In App: verify if current module is available
        EXPECTED: Football module is available
        """
        pass

    def test_004_open_ws_and_check_the_response(self):
        """
        DESCRIPTION: Open WS and check the response
        EXPECTED: Any updates received
        """
        pass

    def test_005_in_cms_activate_current_module_for_olympic_sports(self):
        """
        DESCRIPTION: In CMS: Activate current module for Olympic Sports
        EXPECTED: Football module is activated
        """
        pass

    def test_006_verify_presence_of_the_module_within_the_app_and_ws_response(self):
        """
        DESCRIPTION: Verify presence of the module within the app and WS response
        EXPECTED: * Football module is available in App
        EXPECTED: * Any updates received
        """
        pass

    def test_007_repeat_steps_1_7_for_coral(self):
        """
        DESCRIPTION: Repeat steps 1-7 for coral
        EXPECTED: 
        """
        pass
