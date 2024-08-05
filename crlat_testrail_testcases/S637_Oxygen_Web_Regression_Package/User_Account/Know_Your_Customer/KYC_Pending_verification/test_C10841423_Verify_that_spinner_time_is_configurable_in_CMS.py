import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C10841423_Verify_that_spinner_time_is_configurable_in_CMS(Common):
    """
    TR_ID: C10841423
    NAME: Verify that spinner time is configurable in CMS
    DESCRIPTION: This test case verifies ability to set verification spinner display time in CMS
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - STG CMS:
    PRECONDITIONS: https://cms-api-ui-stg0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: creds: qa@coral.co.uk/qas1234
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    """
    keep_browser_open = True

    def test_001___navigate_to_oxygen_app__tap_join_now__fill_out_required_fields_on_each_registration_page__tap_complete_registration_on_registration___account_details_page(self):
        """
        DESCRIPTION: - Navigate to Oxygen app
        DESCRIPTION: - Tap 'Join Now'
        DESCRIPTION: - Fill out required fields on each 'Registration' page
        DESCRIPTION: - Tap 'Complete Registration' on 'Registration - Account Details' page
        EXPECTED: 'Marketing Preferences' (GDPR) screen displayed with ability to select and Save Preferences
        """
        pass

    def test_002_navigate_to_cms____system_configuration___structure___kyc___pendingdialogtimeoutchange_display_time_value_set_in_ms_eg5000_equals_5_sec_and_save_changes(self):
        """
        DESCRIPTION: Navigate to CMS  -> System Configuration -> Structure -> KYC -> pendingDialogTimeout
        DESCRIPTION: Change display time (value set in ms, e.g."5000" equals 5 sec) and save changes
        EXPECTED: Changes successfully saved
        """
        pass

    def test_003_return_to_oxygen_app_and_click_on_save_my_preferences_button(self):
        """
        DESCRIPTION: Return to Oxygen app and click on Save My Preferences button
        EXPECTED: - Overlay with verification spinner displayed. Title "VERIFYING YOUR DETAILS" text: "Just a few more seconds, please wait" and loading spinner.
        EXPECTED: - Spinner display time equals to the time set in CMS
        """
        pass
