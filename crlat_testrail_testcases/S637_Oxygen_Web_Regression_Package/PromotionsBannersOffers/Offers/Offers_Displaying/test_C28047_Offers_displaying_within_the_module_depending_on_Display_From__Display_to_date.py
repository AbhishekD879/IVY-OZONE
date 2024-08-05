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
class Test_C28047_Offers_displaying_within_the_module_depending_on_Display_From__Display_to_date(Common):
    """
    TR_ID: C28047
    NAME: Offers displaying within the module depending on ‘Display From  –  Display to’ date
    DESCRIPTION: This test case verifies Offers displaying depending on ‘Display From  –  Display to’ date selected in CMS for the Offer
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

    def test_001_select_offer_with_date_range_which_includes_current_date_in_cmsload_oxygen_application_and_verify_offer_displaying(self):
        """
        DESCRIPTION: Select Offer with date range which includes current date in CMS.
        DESCRIPTION: Load Oxygen application and verify Offer displaying.
        EXPECTED: Offer is displayed in application
        """
        pass

    def test_002_select_offer_with_date_range_which_does_not_include_current_date_in_cmsload_oxygen_application_and_verify_offer_displaying(self):
        """
        DESCRIPTION: Select Offer with date range which does not include current date in CMS.
        DESCRIPTION: Load Oxygen application and verify offer displaying.
        EXPECTED: Offer is NOT displayed in application
        """
        pass
