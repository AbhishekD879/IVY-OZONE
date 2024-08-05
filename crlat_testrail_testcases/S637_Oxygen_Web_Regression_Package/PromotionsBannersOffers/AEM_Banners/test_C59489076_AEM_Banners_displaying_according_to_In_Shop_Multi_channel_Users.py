import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C59489076_AEM_Banners_displaying_according_to_In_Shop_Multi_channel_Users(Common):
    """
    TR_ID: C59489076
    NAME: AEM Banners displaying according to In-Shop/Multi-channel Users
    DESCRIPTION: This test case verifies AEM Banners displaying according to In-Shop/Multi-channel Users
    PRECONDITIONS: 1) AEM Banners should be enabled in CMS
    PRECONDITIONS: 2) To check data from json response open Dev tools -> Network tab
    PRECONDITIONS: 3) User is logged out
    PRECONDITIONS: 4) Local storage is cleared
    PRECONDITIONS: To check Request URL to banners please go to Dev tools -> Network -> All -> response.json -> Headers / Response
    PRECONDITIONS: To check Request URL to Target banners please go to Dev tools -> Network -> All -> json?mbox=target-global-mbox... -> Headers / Response
    PRECONDITIONS: Multi-channel user is an in-shop upgraded user or regular user with added Connect/Grid card
    """
    keep_browser_open = True

    def test_001_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        EXPECTED: * 'userType/anonymous'(Coral) or 'userType/new'(Ladbrokes) parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items received in response
        """
        pass

    def test_002_log_in_with_valid_non_upgraded_in_shop_user(self):
        """
        DESCRIPTION: Log in with valid non-upgraded In-Shop user
        EXPECTED: * 'userType/in-shop' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items received in response
        """
        pass

    def test_003_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application
        EXPECTED: User is successfully logged out
        """
        pass

    def test_004_clear_local_storage(self):
        """
        DESCRIPTION: Clear local storage
        EXPECTED: 
        """
        pass

    def test_005_log_in_with_valid_multi_channel_user(self):
        """
        DESCRIPTION: Log in with valid multi-channel user
        EXPECTED: * 'userType/multi-channel' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items received in response
        """
        pass
