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
class Test_C28045_Offer_Mofules_displaying_for_desktop_tablet_both_when_Offer_Module_has_Show_for_Both_option_value(Common):
    """
    TR_ID: C28045
    NAME: Offer Mofules displaying for desktop/tablet/both when Offer Module has 'Show for Both' option value
    DESCRIPTION: This test case verifies Offer Mofules displaying for desktop/tablet/both when Offer Module has 'Show for Both' option value
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
    PRECONDITIONS: 3) Offer Modules with 'Show for Both' option value are available.
    """
    keep_browser_open = True

    def test_001_select_offer_module_with_show_for_both_option_value_in_cmsload_oxygen_application(self):
        """
        DESCRIPTION: Select Offer Module with 'Show for Both' option value in CMS.
        DESCRIPTION: Load Oxygen application.
        EXPECTED: *   Offer module is displayed on Desktop
        EXPECTED: *   Offer module is displayed on Tablets
        """
        pass

    def test_002_select_offer_module_with_show_for_both_option_value_in_cmssome_offers_have_show_for_desktop_option_value_in_cmssome_offers_have_show_for_tablet_option_value_in_cmsload_oxygen_application(self):
        """
        DESCRIPTION: Select offer Module with 'Show for both' option value in CMS.
        DESCRIPTION: Some Offers have 'Show for Desktop' option value in CMS.
        DESCRIPTION: Some Offers have 'Show for Tablet' option value in CMS.
        DESCRIPTION: Load Oxygen application.
        EXPECTED: *   Offer module is displayed on Desktop
        EXPECTED: *   Offer module is displayed on Tablets
        """
        pass
