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
class Test_C28246_Verify_happy_NetVerify_path_for_Not_Suspended_user(Common):
    """
    TR_ID: C28246
    NAME: Verify happy NetVerify path for Not Suspended user
    DESCRIPTION: This test case verifies happy NetVerify path for Not Suspended user.
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   BMA-4059 (Jumio/ NetVerify Integration)
    DESCRIPTION: *   BMA-5876 (Jumio Pop-Up Improvement)
    PRECONDITIONS: 1.  User is logged out
    PRECONDITIONS: 2.  The following attributes are set in IMS system for this user:
    PRECONDITIONS: **"suspended":"false" **and **"ageVerificationStatus":"inprocess"**
    PRECONDITIONS: Test users:
    PRECONDITIONS: *   TST2: username101/123456
    PRECONDITIONS: *   STG2: nopayment/111111
    PRECONDITIONS: *   PROD: testjumio2/123456
    PRECONDITIONS: **NOTE**: if other pop-up messages are expected after log in then the order of pop-up appearing should be the following:
    PRECONDITIONS: *   Terms and Conditions -> Verify Your Account (Netverify) -> Deposit Limits -> Quick Deposit
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is shown
        """
        pass

    def test_002_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log in' button
        EXPECTED: User is logged in
        """
        pass

    def test_003_verify_responce_31083_ofsent_request_31082_getplayerinfo(self):
        """
        DESCRIPTION: Verify responce (31083) of sent request (31082) ('GetPlayerInfo')
        EXPECTED: Responce contains:
        EXPECTED: *   "suspended":"**false**"
        EXPECTED: *   "ageVerificationStatus":"inprocess"
        """
        pass

    def test_004_verify_verify_your_account_pop_up(self):
        """
        DESCRIPTION: Verify 'Verify Your Account' pop-up
        EXPECTED: *   Pop-up is shown:
        EXPECTED: *   header '**Verify Your Account**'
        EXPECTED: *   body '**We just need a few details Due to our licensing commitments and for the safety of all our customers we are required to verify all players on our system. Unfortunately we have not been able to verify your details. Using your device you can quickly and safely upload a photo of your driving lisence or ID document(s) through our secure service so that we can complete your verification. This will prevent your account from being disabled**.'
        EXPECTED: *   '**Verify Me Now!**' button
        EXPECTED: *   Pop-up can be closed using 'x' icon
        EXPECTED: *   After page refreshing 'Verify Your Account' pop-up is not shown anymore
        """
        pass

    def test_005_tap_verify_me_now_button(self):
        """
        DESCRIPTION: Tap 'Verify Me Now!' button
        EXPECTED: User is redirected to NetVerify vendor site (https://coral.netverify.com/v2?authorizationToken=<token>&locale=en_GB)
        """
        pass

    def test_006_verify_your_document_eg_passportdriving_licence_using_netverify_system(self):
        """
        DESCRIPTION: Verify your document e.g. Passport/Driving Licence using NetVerify system
        EXPECTED: *   Document is verified succesfully
        EXPECTED: *   User is presented with Coral Successfull page
        """
        pass

    def test_007_tap_visit_coralcouk_button(self):
        """
        DESCRIPTION: Tap 'VISIT CORAL.CO.UK' button
        EXPECTED: *   User is redirected to the Homepage of Invictus application
        EXPECTED: *   User is logged in
        """
        pass

    def test_008_verify_verify_your_account_pop_up_appearing(self):
        """
        DESCRIPTION: Verify 'Verify Your Account' pop-up appearing
        EXPECTED: 'Verify Your Account' pop-up is not shown anymore in Invictus application if user navigated from Coral Successfull page
        """
        pass
