import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C13828787_Ladbrokes_KYC_Redirection_to_AccountOne_when_verification_failed(Common):
    """
    TR_ID: C13828787
    NAME: Ladbrokes. KYC. Redirection to AccountOne when verification failed
    DESCRIPTION: Test case verifies navigation to AccountOne when (the IMS AGE verification status = Unknown/Active grace period) OR (AGE verification status = Active grace period
    DESCRIPTION: AND the player tags POA_required/ AGP_Success_Upload =<5 OR AGP_Success_Upload > 5) are received after user login
    DESCRIPTION: AUTOTEST :
    DESCRIPTION: Mobile [C22892377]
    DESCRIPTION: Desktop [C22995256]
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: - Playtech IMS:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Ladbrokes+Environments
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: - User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: -------------------
    PRECONDITIONS: Unknown is the default status upon registration, but once you register, your status has to be either AGP, Passed or Under review from the comment in BMA-40102 story on 26/Jun/19 4:35 PM
    """
    keep_browser_open = True

    def test_001_log_in_as_a_user_with_ims_age_verification_status__unknown(self):
        """
        DESCRIPTION: Log in as a user with IMS 'Age verification status' = "Unknown"
        EXPECTED: A user is redirected to Account one page
        """
        pass

    def test_002_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: * User is navigated back to an app
        EXPECTED: * User is logged out
        """
        pass

    def test_003_log_in_as_a_user_with_ims_age_verification_status__active_grace_period(self):
        """
        DESCRIPTION: Log in as a user with IMS 'Age verification status' = "Active grace period"
        EXPECTED: A user is redirected to Account one page
        """
        pass

    def test_004_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: * User is navigated back to an app
        EXPECTED: * User is logged out
        """
        pass

    def test_005_log_in_as_a_user_with_ims_age_verification_status__active_grace_period_and_player_tags_are_poa_required_agp_success_upload__5(self):
        """
        DESCRIPTION: Log in as a user with IMS Age verification status = Active grace period AND Player tags are POA_Required, AGP_Success_Upload = 5
        EXPECTED: A user is redirected to Account one page
        """
        pass

    def test_006_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: * User is navigated back to an app
        EXPECTED: * User is logged out
        """
        pass

    def test_007_log_in_as_a_user_with_ims_age_verification_status__active_grace_period_and_player_tags_is_poa_required(self):
        """
        DESCRIPTION: Log in as a user with IMS Age verification status = Active grace period AND Player tags is POA_Required
        EXPECTED: A user is redirected to Account one page
        """
        pass

    def test_008_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: * User is navigated back to an app
        EXPECTED: * User is logged out
        """
        pass

    def test_009_log_in_as_a_user_with_ims_age_verification_status__active_grace_period_and_agp_success_upload__5(self):
        """
        DESCRIPTION: Log in as a user with IMS Age verification status = Active grace period AND AGP_Success_Upload > 5
        EXPECTED: A user is redirected to Account one page
        """
        pass

    def test_010_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: * User is navigated back to an app
        EXPECTED: * User is logged out
        """
        pass
