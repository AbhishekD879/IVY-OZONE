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
class Test_C11321576_KYC_journeys_are_started_for_multichannel_user_KYC_is_on_in_CMS(Common):
    """
    TR_ID: C11321576
    NAME: KYC journeys are started for multichannel user (KYC is on in CMS)
    DESCRIPTION: This test case verifies that KYC flows are started after login if KYC feature toggle is on in CMS
    PRECONDITIONS: Link to CMS:
    PRECONDITIONS: DEV0: https://cms-api-ui-dev0.coralsports.dev.cloud.ladbrokescoral.com/
    PRECONDITIONS: Login details: test.admin@coral.co.uk/admin
    PRECONDITIONS: 1. In CMS > System Configuration > Config:
    PRECONDITIONS: 'KYC' group is created
    PRECONDITIONS: Field added in 'KYC' group: 'Field Name' = "enabled; 'Field Type' = "checkbox"
    PRECONDITIONS: 2. In CMS > System Configuration > Structure:
    PRECONDITIONS: Checkbox "enabled" in 'KYC' table is ON
    PRECONDITIONS: In IMS: 'Age verification result' is set to 'Unknown' for a user
    PRECONDITIONS: 3. Oxygen app is loaded
    PRECONDITIONS: 4. In-shop user should be logged in. [How to create In-Shop user](https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: Link to CMS:
    PRECONDITIONS: - DEV0: https://cms-api-ui-dev0.coralsports.dev.cloud.ladbrokescoral.com/
    PRECONDITIONS: Login details: test.admin@coral.co.uk/admin
    PRECONDITIONS: Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    """
    keep_browser_open = True

    def test_001_upgrade_in_shop_user_to_multichannel__open_right_menu__tap_on_depositwithdrawalcancel_withdrawalmy_account__tap_upgrade__fill_all_required_fields_correctly_use_unique_data_for_mail_and_phone_number__tap_confirm_button(self):
        """
        DESCRIPTION: Upgrade in-shop user to multichannel:
        DESCRIPTION: - Open Right menu
        DESCRIPTION: - Tap on Deposit/Withdrawal/Cancel Withdrawal/My Account
        DESCRIPTION: - Tap 'Upgrade'
        DESCRIPTION: - Fill all required fields correctly (use unique data for mail and phone number)
        DESCRIPTION: - Tap 'Confirm' button
        EXPECTED: - 'Success' pop up with pending verification spinner appears
        EXPECTED: - User is upgraded to multi-channel
        EXPECTED: - User is logged in
        EXPECTED: - KYC flow is started
        """
        pass

    def test_002_verify_kyc_journey(self):
        """
        DESCRIPTION: Verify KYC journey
        EXPECTED: - 'Verification Needed' pop up (when 'ageVerificationStatus' = "unknown" is received in response with "ID":31083)
        EXPECTED: OR/AND
        EXPECTED: - User is redirected to 'Deposit' page, when 'ageVerificationStatus' = "review"
        """
        pass
