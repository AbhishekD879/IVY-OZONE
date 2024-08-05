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
class Test_C28248_Verify_OXnetVerifyChecked_record_setting_after_happy_path(Common):
    """
    TR_ID: C28248
    NAME: Verify OX.netVerifyChecked record setting after happy path
    DESCRIPTION: This test case verifies added **OX.netVerifyChecked **record after happy path for Suspended or Not Suspended user.
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-4059 (Jumio/ NetVerify Integration)
    DESCRIPTION: ![](index.php?/attachments/get/3149)
    PRECONDITIONS: 1.  User is logged out
    PRECONDITIONS: 2.  The following attributes are set in IMS system for:
    PRECONDITIONS: Suspended user:** "suspended":"true" **and **"ageVerificationStatus":"inprocess"**
    PRECONDITIONS: Not Suspended user:** "suspended":"false" **and **"ageVerificationStatus":"inprocess"**
    PRECONDITIONS: Test users:
    PRECONDITIONS: *   TST2: username101/123456 (not suspended);  username102/123456 (suspended)
    PRECONDITIONS: *   PROD: testjumio2/123456 (not suspended); testjumio1/123456 (suspended)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is shown
        """
        pass

    def test_002_log_in_into_application_with_suspended_user(self):
        """
        DESCRIPTION: Log in into application with Suspended user
        EXPECTED: *   User is logged in
        EXPECTED: *   'Verify Your Account' pop-up is shown
        """
        pass

    def test_003_tap_verify_me_now_button(self):
        """
        DESCRIPTION: Tap 'Verify Me Now!' button
        EXPECTED: User is redirected to NetVerify vendor site (https://coral.netverify.com/v2?authorizationToken=<token>&locale=en_GB)
        """
        pass

    def test_004_verify_your_document_eg_passportdriving_licence_using_netverify_system(self):
        """
        DESCRIPTION: Verify your document e.g. Passport/Driving Licence using NetVerify system
        EXPECTED: *   Document is verified succesfully
        EXPECTED: *   User is presented with Coral Successfull page
        """
        pass

    def test_005_tap_visit_coralcouk_button(self):
        """
        DESCRIPTION: Tap 'VISIT CORAL.CO.UK' button
        EXPECTED: *   User is redirected to the Homepage of Invictus application
        EXPECTED: *   User is logged in
        """
        pass

    def test_006_open_dev_tools__application_tab___storage_section_and_verify_created_record_in_local_storage(self):
        """
        DESCRIPTION: Open Dev tools ->Application tab -> storage section and verify created record in local storage
        EXPECTED: *   The **OX.netVerifyChecked** record was created in local storage when Jumio returned success
        EXPECTED: *   Value: username
        EXPECTED: NOTE: Sometimes IMS doesn't unsuspend user immediately (after happy Jumio path), that is why the record in local storage is used in order to not show 'Verify Your Account' pop-up after re-logging.
        """
        pass

    def test_007_log_out_from_the_application(self):
        """
        DESCRIPTION: Log out from the application
        EXPECTED: 
        """
        pass

    def test_008_log_in_again_with_user_from_step_2(self):
        """
        DESCRIPTION: Log in again with user from step №2
        EXPECTED: *   User is logged in
        EXPECTED: *   'Verify Your Account' pop-up is not shown (even if IMS returns "suspended":"true" and "ageVerificationStatus":"inprocess")
        """
        pass

    def test_009_log_in_into_application_with_not_suspended_user(self):
        """
        DESCRIPTION: Log in into application with Not Suspended user
        EXPECTED: *   User is logged in
        EXPECTED: *   'Verify Your Account' pop-up is shown
        """
        pass

    def test_010_repeat_steps_3_8(self):
        """
        DESCRIPTION: Repeat steps №3-8
        EXPECTED: 
        """
        pass
