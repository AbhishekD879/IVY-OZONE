import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C667793_AEM_Banners_displaying_according_to_Anonymous__Existing_Users(Common):
    """
    TR_ID: C667793
    NAME: AEM Banners displaying according to Anonymous / Existing Users
    DESCRIPTION: This test case verifies AEM Banners displaying according to Anonymous/Existing Users (for Coral) or New/Existing Users (for Ladbrokes)
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. This test case should be checked on Mobile, Tablet, Desktop
    PRECONDITIONS: 3. To check data from **json** response open Dev tools -> Network tab
    PRECONDITIONS: 4. User is logged out
    PRECONDITIONS: 5. Local storage is cleared
    PRECONDITIONS: To check Request URL to banners please go to Dev tools -> Network -> All -> response.json -> Headers / Response
    PRECONDITIONS: To check Request URL to Target banners  please go to Dev tools -> Network -> All -> json?mbox=target-global-mbox... -> Headers / Response
    PRECONDITIONS: To check if target content is loaded on UI navigate to Console -> type window.adobe.target -> enter
    PRECONDITIONS: ![](index.php?/attachments/get/36029)
    """
    keep_browser_open = True

    def test_001_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        EXPECTED: * 'userType/anonymous'(Coral) or 'userType/new'(Ladbrokes)  parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items received in response
        """
        pass

    def test_002_go_to_any_sport__race_landing_page_and_repeat_step_1(self):
        """
        DESCRIPTION: Go to any <Sport> / <Race> landing page and repeat step #1
        EXPECTED: 
        """
        pass

    def test_003_register_new_user(self):
        """
        DESCRIPTION: Register new user
        EXPECTED: User is logged in
        """
        pass

    def test_004_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        EXPECTED: * 'userType/existing' parameter is present as path in request URL
        EXPECTED: * 'imsLevel/X/' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items received in response
        """
        pass

    def test_005_go_to_any_sport__race_landing_page_and_repeat_step_4(self):
        """
        DESCRIPTION: Go to any <Sport> / <Race> landing page and repeat step #4
        EXPECTED: 
        """
        pass

    def test_006_log_out_and_repeat_step_4(self):
        """
        DESCRIPTION: Log out and repeat step #4
        EXPECTED: 
        """
        pass

    def test_007_clear_local_storage(self):
        """
        DESCRIPTION: Clear local storage
        EXPECTED: 
        """
        pass

    def test_008_log_in_with_different_user_and_repeat_steps_4_6(self):
        """
        DESCRIPTION: Log in with different user and repeat steps #4-6
        EXPECTED: 
        """
        pass
