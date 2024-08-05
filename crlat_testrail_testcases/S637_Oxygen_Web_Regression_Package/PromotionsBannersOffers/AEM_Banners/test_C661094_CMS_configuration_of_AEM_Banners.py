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
class Test_C661094_CMS_configuration_of_AEM_Banners(Common):
    """
    TR_ID: C661094
    NAME: CMS configuration of AEM Banners
    DESCRIPTION: This test case verifies CMS configuration of AEM Banners
    PRECONDITIONS: 1. To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/structure
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: 2. User is logged out
    """
    keep_browser_open = True

    def test_001_load_cms_choose_bma_brand(self):
        """
        DESCRIPTION: Load CMS, choose 'bma' brand
        EXPECTED: * CMS is opened
        EXPECTED: * 'bma' brand is opened
        """
        pass

    def test_002_go_to_system_configuration_section___dynamicbanners_item(self):
        """
        DESCRIPTION: Go to 'System Configuration' section -> 'DYNAMICBANNERS' item
        EXPECTED: 
        """
        pass

    def test_003_enable_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Enable checkbox and save changes
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * AEM banners are enabled within Oxygen app
        """
        pass

    def test_004_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_005_verify_aem_banners(self):
        """
        DESCRIPTION: Verify AEM banners
        EXPECTED: * AEM banners are displayed on Homepage
        EXPECTED: * CMS-controlled banners are NOT displayed
        """
        pass

    def test_006_go_to_any_sport_or_race_page_and_repeat_step_5(self):
        """
        DESCRIPTION: Go to any <Sport> or <Race> page and repeat step #5
        EXPECTED: 
        """
        pass

    def test_007_login_and_repeat_steps_5_6(self):
        """
        DESCRIPTION: Login and repeat steps #5-6
        EXPECTED: 
        """
        pass

    def test_008_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_1_3_but_on_step_3_disable_dynamicbanners_checkbox(self):
        """
        DESCRIPTION: Repeat steps #1-3 but on step #3 Disable 'DYNAMICBANNERS' checkbox
        EXPECTED: * Changes are submitted successfully
        EXPECTED: * AEM banners are disabled within Oxygen app
        """
        pass

    def test_010_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_011_verify_aem_banners(self):
        """
        DESCRIPTION: Verify AEM banners
        EXPECTED: * AEM banners are NOT displayed on Homepage
        EXPECTED: * CMS-controlled banners are displayed
        """
        pass

    def test_012_go_to_any_sport_or_race_page_and_repeat_step_11(self):
        """
        DESCRIPTION: Go to any <Sport> or <Race> page and repeat step #11
        EXPECTED: 
        """
        pass

    def test_013_login_and_repeat_steps_11_12(self):
        """
        DESCRIPTION: Login and repeat steps #11-12
        EXPECTED: 
        """
        pass

    def test_014_repeat_steps_1_14_for_connect_brand_on_steps_4_and_10_load_connect_app(self):
        """
        DESCRIPTION: Repeat steps #1-14 for 'connect' brand, on steps #4 and #10 load Connect app
        EXPECTED: 
        """
        pass
