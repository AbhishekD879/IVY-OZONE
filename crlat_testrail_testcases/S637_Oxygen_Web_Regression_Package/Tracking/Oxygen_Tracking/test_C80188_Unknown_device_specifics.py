import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C80188_Unknown_device_specifics(Common):
    """
    TR_ID: C80188
    NAME: 'Unknown device' specifics
    DESCRIPTION: After successful registration or sign in user information are written to the IMS system
    DESCRIPTION: This test case verifies 2 fields in the IMS:
    DESCRIPTION: - deviceType
    DESCRIPTION: - clientPlatform
    DESCRIPTION: Any tablet devices determined to be a valid tablet type will be classified as a valid device type and a clientPlatform value of "mobile";
    DESCRIPTION: Any mobile devices determined to be a valid mobile type will be classified as a valid device type and a clientPlatform value of "mobile"; therefore using the non-3DS payment route
    DESCRIPTION: Any device classified as "Unknown Device" will have a default clientPlatform value of "mobile"; therefore using the non-3DS payment route.
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: *   List of all supported devices should be covered
    PRECONDITIONS: *   Guide "[How to debug emulator, real iOS and Android devices][1]"
    PRECONDITIONS: *   In order to verify correctness of **deviceType** value please use [Standards for recording deviceType attribute][2]
    PRECONDITIONS: *   [Playtech IMS][3] creds
    PRECONDITIONS: ![](index.php?/attachments/get/1234)
    PRECONDITIONS: Xiaomy devices could not be recognized
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/MOB/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    PRECONDITIONS: [2]: https://confluence.egalacoral.com/display/MOB/Standards+for+recording+deviceType+attribute
    PRECONDITIONS: [3]: https://confluence.egalacoral.com/display/MOB/Playtech+IMS
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_mobile_device_that_could_not_be_recognized(self):
        """
        DESCRIPTION: Load Oxygen app on **Mobile** device that could not be recognized
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_to_the_oxygen(self):
        """
        DESCRIPTION: Log in to the Oxygen
        EXPECTED: User is logged in
        """
        pass

    def test_003_open_network_tab_in_the_developers_console__tap_on_ws__choose_first_request(self):
        """
        DESCRIPTION: Open Network tab in the Developers console-> tap on WS-> Choose first request
        EXPECTED: User is logged in
        EXPECTED: 31001 request is opened
        """
        pass

    def test_004_verify_2_fields_valuesplus_clientplatformplus_devicetype(self):
        """
        DESCRIPTION: Verify 2 fields values:
        DESCRIPTION: + clientPlatform
        DESCRIPTION: + deviceType
        EXPECTED: The values are presented and corresponded to the device type mentioned in the Developer console:
        EXPECTED: + deviceType: Unknown Device
        EXPECTED: + clientPlatform: mobile
        """
        pass

    def test_005_load_and_login_into_ims_system(self):
        """
        DESCRIPTION: Load and login into IMS system
        EXPECTED: IMS system is opened
        """
        pass

    def test_006_tap_on_player_management___player_search(self):
        """
        DESCRIPTION: Tap on Player Management -> Player search
        EXPECTED: User account information is shown
        """
        pass

    def test_007_search_for_logins_tab_and_verify_the_last_loginor_general_player_information_last_login_section(self):
        """
        DESCRIPTION: Search for 'Logins' tab and verify the last login
        DESCRIPTION: or 'General Player information' last login section
        EXPECTED: Login info presented
        """
        pass

    def test_008_check_2_field_valueplus_client_platfomtypeplus_device_type(self):
        """
        DESCRIPTION: Check 2 field value:
        DESCRIPTION: + Client platfom/type
        DESCRIPTION: + Device type
        EXPECTED: Values are presented and corresponded to the values described in step 4
        """
        pass

    def test_009_log_out_from_oxygen(self):
        """
        DESCRIPTION: Log out from Oxygen
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_1_10_with_tablet_device_that_could_not_be_recognized(self):
        """
        DESCRIPTION: Repeat steps 1-10 with **tablet** device that could not be recognized
        EXPECTED: Check that client platform is **mobile** instead of tablet
        EXPECTED: + deviceType: Unknown Device
        EXPECTED: + clientPlatform: mobile
        """
        pass

    def test_011_repeat_steps_1_10_on_desktop(self):
        """
        DESCRIPTION: Repeat steps 1-10 on **desktop**
        EXPECTED: Check that client platform is **mobile** instead of web
        EXPECTED: + deviceType: Unknown Device
        EXPECTED: + clientPlatform: mobile
        """
        pass
