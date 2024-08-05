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
class Test_C29493_Affiliate_Tracking__Registration_from_Affiliates(Common):
    """
    TR_ID: C29493
    NAME: Affiliate Tracking - Registration from Affiliates
    DESCRIPTION: This test case verifies Affiliates tracking upon Registration
    DESCRIPTION: User Story: BMA-6470 Affiliate Tracking (IMS & Income Access)
    PRECONDITIONS: *   User is logged out
    PRECONDITIONS: *   Cache and cookies are cleared
    PRECONDITIONS: *   Browser console is opened (Network->WS)
    PRECONDITIONS: *   Up to date affiliate link is available
    PRECONDITIONS: *   UAT is available to check values set in IMS
    PRECONDITIONS: Examples of affiliate links (might be not valid):
    PRECONDITIONS: [http://affiliate.coral.co.uk/processing/clickthrgh.asp?btag=a\_19893b\_9096][1]
    PRECONDITIONS: [http://delivery.e.switchadhub.com/adserver/www/delivery/ck.php?oaparams=2\_\_bannerid=10966\_\_zoneid=3531\_\_OXLCA=1\_\_cb=1bb1135fb7\_\_tc=1453804921.1579\_\_origurl=http%3A%2F%2Fwww.oddschecker.com%2F\_\_ctk=T\_1brkj0n127e17s2lm3hgt5ag7sq\\_\_chain\_id=3bb1i3tghf3dqo04nvn3dijugj\\_\_d1e395ba9b0ac413=21e73851cd583932\_\_node=delivery3.e.switchadhub.com_\_oadest=http%3A%2F%2Faffiliate.coral.co.uk%2Fprocessing%2Fclickthrgh.asp%3Fbtag%3Da\_18718b_5690][2]
    PRECONDITIONS: [1]: http://affiliate.coral.co.uk/processing/clickthrgh.asp?btag=a_19893b_9096
    PRECONDITIONS: [2]: http://delivery.e.switchadhub.com/adserver/www/delivery/ck.php?oaparams=2__bannerid=10966__zoneid=3531__OXLCA=1__cb=1bb1135fb7__tc=1453804921.1579__origurl=http%3A%2F%2Fwww.oddschecker.com%2F__ctk=T_1brkj0n127e17s2lm3hgt5ag7sq__chain_id=3bb1i3tghf3dqo04nvn3dijugj__d1e395ba9b0ac413=21e73851cd583932__node=delivery3.e.switchadhub.com__oadest=http%3A%2F%2Faffiliate.coral.co.uk%2Fprocessing%2Fclickthrgh.asp%3Fbtag%3Da_18718b_5690
    """
    keep_browser_open = True

    def test_001_load_affiliates_link(self):
        """
        DESCRIPTION: Load affiliates link
        EXPECTED: User is redirected from Affiliates link to Invictus Registration page
        EXPECTED: Note: if user is not redirected to Registration page on right environment, it does not matter as long as right cookie has been created after launching affiliates link
        """
        pass

    def test_002_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_003_verify_that_cookie_banner_domainclick_is_created_in_browser(self):
        """
        DESCRIPTION: Verify that cookie "banner_domainclick" is created in browser
        EXPECTED: 
        """
        pass

    def test_004_tap_join_button(self):
        """
        DESCRIPTION: Tap 'Join' button
        EXPECTED: Registration page is displayed
        """
        pass

    def test_005_enter_all_required_fields_on_two_steps_of_registration_correctly_and_tap_complete_registration_button(self):
        """
        DESCRIPTION: Enter all required fields on two steps of Registration correctly and tap Complete Registration button
        EXPECTED: 
        """
        pass

    def test_006_search_for_registration_request_id_31007_in_network_ws_frames(self):
        """
        DESCRIPTION: Search for registration request ID 31007 in Network->WS->Frames
        EXPECTED: 
        """
        pass

    def test_007_verify_the_following_parameters_in_the_request___advertiser___profileid___creferer(self):
        """
        DESCRIPTION: Verify the following parameters in the request:
        DESCRIPTION: *   advertiser
        DESCRIPTION: *   profileid
        DESCRIPTION: *   creferer
        EXPECTED: These parameters contain the values from a cookie created after launching affiliates link, values should NOT be empty:
        EXPECTED: *   "advertiser":"advertiser_value"
        EXPECTED: *   "profileid":"profileid_value"
        EXPECTED: *   "creferer":"BTAG:creferer_value"
        """
        pass

    def test_008_verify_values_set_in_ims_for_just_registered_user___referrer_advertiser___btag(self):
        """
        DESCRIPTION: Verify values set in IMS for just registered user:
        DESCRIPTION: *   Referrer advertiser
        DESCRIPTION: *   BTAG
        EXPECTED: Values which were sent in Registration request are saved correctly in IMS:
        EXPECTED: *   Referrer advetiser: advertiser\_value (profileid\_value)
        EXPECTED: *   BTAG: creferer_value
        EXPECTED: where advertiser\_value, profileid\_value and creferer_value are values from the request checked in step №6
        """
        pass
