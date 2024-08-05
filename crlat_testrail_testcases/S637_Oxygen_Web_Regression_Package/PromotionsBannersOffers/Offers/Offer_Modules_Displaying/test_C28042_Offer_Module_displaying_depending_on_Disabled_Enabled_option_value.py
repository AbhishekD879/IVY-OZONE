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
class Test_C28042_Offer_Module_displaying_depending_on_Disabled_Enabled_option_value(Common):
    """
    TR_ID: C28042
    NAME: Offer Module displaying depending on 'Disabled'/'Enabled' option value
    DESCRIPTION: This test case verifies Offer Modules displaying depending on 'Disabled'/'Enabled' option value in CMS
    PRECONDITIONS: 1) To load CMS use the next links:
    PRECONDITIONS: DEV -  https://coral-cms-dev0.symphony-solutions.eu/login
    PRECONDITIONS: TST2/QA -  https://coral-cms-tst2.symphony-solutions.eu/login
    PRECONDITIONS: STG2 - https://coral-cms-stg2.symphony-solutions.eu/login
    PRECONDITIONS: HL -  https://coral-cms-hl.symphony-solutions.eu/login
    PRECONDITIONS: PROD -  https://coral-cms.symphony-solutions.eu/login
    PRECONDITIONS: BETA - https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 2) Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    PRECONDITIONS: 3) There are Offer Modules with 'Active' and 'Inactive' option value
    """
    keep_browser_open = True

    def test_001_select_offer_module_with_inactive_option_value_checked_in_cmsload_application_and_verify_the_module_displaying(self):
        """
        DESCRIPTION: Select Offer Module with 'Inactive' option value checked in CMS.
        DESCRIPTION: Load application and verify the Module displaying.
        EXPECTED: Inactive Offer Module is NOT displayed in application
        """
        pass

    def test_002_select_offer_module_with_active_option_value_checked_in_cmsload_application_and_verify_the_module_displaying(self):
        """
        DESCRIPTION: Select Offer Module with 'Active' option value checked in CMS.
        DESCRIPTION: Load application and verify the Module displaying
        EXPECTED: Active Offer Module is displayed in application
        """
        pass

    def test_003_select_offer_module_with_inactive_option_value_checked_and_update_option_value_to_active_in_cmsload_application_and_verify_offer_module_displaying(self):
        """
        DESCRIPTION: Select Offer Module with 'Inactive' option value checked and update option value to 'Active' in CMS.
        DESCRIPTION: Load application and verify Offer Module displaying.
        EXPECTED: Newly enabled Offer Module appears in application
        """
        pass

    def test_004_select_offer_module_with_active_option_value_and_update_option_value_to_inactiveload_application_and_verify_offer_module_displaying(self):
        """
        DESCRIPTION: Select Offer Module with 'Active' option value and update option value to 'Inactive'.
        DESCRIPTION: Load application and verify Offer Module displaying
        EXPECTED: Inactive Offer Module stops to display in application
        """
        pass
