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
class Test_C28048_Offers_displaying_depending_on_Enabled_Disabled_option_value(Common):
    """
    TR_ID: C28048
    NAME: Offers displaying depending on Enabled/Disabled option value
    DESCRIPTION: This test case verifies Offers displaying depending on Enabled/Disabled option value in CMS.
    PRECONDITIONS: 1) To load CMS use the next links:
    PRECONDITIONS: DEV -  https://coral-cms-dev0.symphony-solutions.eu/login
    PRECONDITIONS: TST2 -  https://coral-cms-tst2.symphony-solutions.eu/login
    PRECONDITIONS: STG2 - https://coral-cms-stg2.symphony-solutions.eu/login
    PRECONDITIONS: HL -  https://coral-cms-hl.symphony-solutions.eu/login
    PRECONDITIONS: PROD -  https://coral-cms.symphony-solutions.eu/login
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 2) Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    """
    keep_browser_open = True

    def test_001_select_offer_with_disabled_option_value_checked_in_cmsload_oxygen_application_and_verify_the_offer_displaying(self):
        """
        DESCRIPTION: Select Offer with 'Disabled' option value checked in CMS.
        DESCRIPTION: Load Oxygen application and verify the Offer displaying.
        EXPECTED: Disabled Offer is NOT displayed in application
        """
        pass

    def test_002_select_offer_with_enabled_option_value_checked_in_cmsload_oxygen_application_and_verify_the_offer_displaying(self):
        """
        DESCRIPTION: Select Offer with 'Enabled' option value checked in CMS.
        DESCRIPTION: Load Oxygen application and verify the Offer displaying.
        EXPECTED: Enabled Offer is displayed in application
        """
        pass

    def test_003_select_offer_with_disabled_option_value_checked_in_cmsupdate_option_value_to_enabled_in_cmsload_oxygen_application_and_verify_offer_displaying(self):
        """
        DESCRIPTION: Select Offer with 'Disabled' option value checked in CMS.
        DESCRIPTION: Update option value to 'Enabled' in CMS.
        DESCRIPTION: Load Oxygen application and verify Offer displaying.
        EXPECTED: Newly enabled Offer appears in application
        """
        pass

    def test_004_select_offer_with_enabled_option_value_in_cmsupdate_option_value_to_disabled_in_cmsload_oxygen_application_and_verify_offer_displaying(self):
        """
        DESCRIPTION: Select Offer with 'Enabled' option value in CMS.
        DESCRIPTION: Update option value to 'Disabled' in CMS.
        DESCRIPTION: Load Oxygen application and verify Offer displaying.
        EXPECTED: Disabled Offer stops to display in application
        """
        pass
