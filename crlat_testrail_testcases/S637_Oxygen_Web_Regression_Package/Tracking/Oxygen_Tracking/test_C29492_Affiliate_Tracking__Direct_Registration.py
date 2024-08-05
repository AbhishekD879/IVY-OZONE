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
class Test_C29492_Affiliate_Tracking__Direct_Registration(Common):
    """
    TR_ID: C29492
    NAME: Affiliate Tracking - Direct Registration
    DESCRIPTION: This test case verifies Affiliates tracking upon Registration
    DESCRIPTION: User Story: BMA-6470 Affiliate Tracking (IMS & Income Access)
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: *   Cache and cookies are cleared
    PRECONDITIONS: *   Browser console is opened (Network->WS)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_join_button(self):
        """
        DESCRIPTION: Tap 'Join' button
        EXPECTED: Registration page is displayed
        """
        pass

    def test_003_enter_all_required_fields_on_two_steps_of_registration_correctly_and_tap_complete_registration_button(self):
        """
        DESCRIPTION: Enter all required fields on two steps of Registration correctly and tap 'Complete Registration' button
        EXPECTED: 
        """
        pass

    def test_004_search_for_registration_request_id_31007_in_network_ws_frames(self):
        """
        DESCRIPTION: Search for registration request ID 31007 in Network->WS->Frames
        EXPECTED: 
        """
        pass

    def test_005_verify_the_following_parameters_in_the_request___advertiser___profileid___creferer(self):
        """
        DESCRIPTION: Verify the following parameters in the request:
        DESCRIPTION: *   advertiser
        DESCRIPTION: *   profileid
        DESCRIPTION: *   creferer
        EXPECTED: Parameters contain the following values:
        EXPECTED: *   "advertiser":"default9c"
        EXPECTED: *   "profileid":""
        EXPECTED: *   "creferer":""
        """
        pass

    def test_006_verify_values_set_in_ims_for_just_registered_user___referrer_advetiser___btag(self):
        """
        DESCRIPTION: Verify values set in IMS for just registered user:
        DESCRIPTION: *   Referrer advetiser
        DESCRIPTION: *   BTAG
        EXPECTED: The following values are saved in IMS:
        EXPECTED: *   Referrer advetiser: default9c ()
        EXPECTED: *   BTAG: -
        """
        pass
