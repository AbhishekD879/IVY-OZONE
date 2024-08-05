import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C13948613_Ladbrokes_Verify_that_spinner_time_is_configurable_in_CMS(Common):
    """
    TR_ID: C13948613
    NAME: Ladbrokes. Verify that spinner time is configurable in CMS
    DESCRIPTION: This test case verifies the ability to set verification spinner display time in CMS
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: ________________
    PRECONDITIONS: User should have 'Age verification result' = 'unknown' in IMS:
    PRECONDITIONS: - Find a user
    PRECONDITIONS: - If needed - change 'Age verification result' to 'unknown'
    PRECONDITIONS: - Tap 'Update Info'
    """
    keep_browser_open = True

    def test_001_navigate_to_cms___system_configuration___structure___kyc___pendingdialogtimeoutchange_display_time_value_set_in_ms_eg5000_equals_5_sec_and_save_changes(self):
        """
        DESCRIPTION: Navigate to CMS -> System Configuration -> Structure -> KYC -> pendingDialogTimeout
        DESCRIPTION: Change display time (value set in ms, e.g."5000" equals 5 sec) and save changes
        EXPECTED: Changes successfully saved
        """
        pass

    def test_002_log_in_as_a_user_with_age_verification_result__unknown_in_ims(self):
        """
        DESCRIPTION: Log in as a user with 'Age verification result' = 'unknown' in IMS
        EXPECTED: * User is logged in successfully
        EXPECTED: * Overlay with verification spinner displayed. Title "VERIFYING YOUR DETAILS", text: "Just a few more seconds, please wait" and loading spinner.
        EXPECTED: * Spinner display time equals to the time set in CMS
        """
        pass
