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
class Test_C28041_Offer_Modules_displaying_in_application_according_to_its_adding_editing_deletion_in_CMS(Common):
    """
    TR_ID: C28041
    NAME: Offer Modules displaying in application according to its adding/editing/deletion in CMS
    DESCRIPTION: This test case verifies Offer Modules displaying in the application according to its adding/editing/deletion in CMS
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

    def test_001_add_new_offer_module_with_valid_data_and_with_no_offer_related_to_the_module_in_cmsload_oxygen_application_and_verify_offer_module_displaying(self):
        """
        DESCRIPTION: Add new Offer Module with valid data and with no Offer related to the Module in CMS.
        DESCRIPTION: Load Oxygen application and verify Offer Module displaying.
        EXPECTED: Offer Module without offers is NOT displayed in application
        """
        pass

    def test_002_add_new_offer_module_with_valid_data_and_with_related_offers_in_cmsload_oxygen_application_and_verify_offer_module_displaying(self):
        """
        DESCRIPTION: Add new Offer Module with valid data and with related Offers in CMS.
        DESCRIPTION: Load Oxygen application and verify Offer Module displaying.
        EXPECTED: Offer Module with at least one Offer is displayed in the application
        """
        pass

    def test_003_for_already_existing_offer_module_update_title_in_cmsload_oxygen_application_and_verify_updated_title_displaying_for_the_module(self):
        """
        DESCRIPTION: For already existing Offer Module update title in CMS.
        DESCRIPTION: Load Oxygen application and verify updated title displaying for the Module
        EXPECTED: **For Tablet:**
        EXPECTED: Updated title is displaying for the Module
        EXPECTED: **For Desktop:**
        EXPECTED: Only related to particular Module Offers images are displayed in Offer section next to Banners
        """
        pass

    def test_004_select_already_existing_offer_module_and_delete_it_from_cmsload_oxygen_application_and_verify_deleted_offer_module_displaying(self):
        """
        DESCRIPTION: Select already existing Offer Module and delete it from CMS.
        DESCRIPTION: Load Oxygen application and verify deleted Offer Module displaying
        EXPECTED: Deleted Offer Module is NOT displayed in application
        """
        pass
