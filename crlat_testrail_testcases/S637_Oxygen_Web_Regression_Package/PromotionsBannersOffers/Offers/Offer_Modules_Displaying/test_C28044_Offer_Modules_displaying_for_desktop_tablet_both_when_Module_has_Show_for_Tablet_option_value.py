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
class Test_C28044_Offer_Modules_displaying_for_desktop_tablet_both_when_Module_has_Show_for_Tablet_option_value(Common):
    """
    TR_ID: C28044
    NAME: Offer Modules displaying for desktop/tablet/both when Module has 'Show for Tablet' option value
    DESCRIPTION: This test case verifies Offer Modules displaying for desktop or tablet or both when Mofule has 'Show for tablet' option value
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
    PRECONDITIONS: 3) Offer Modules with 'Show for tablet' option value are available.
    """
    keep_browser_open = True

    def test_001_select_offer_module_with_show_for_tablet_option_value_in_cmsload_oxygen_application(self):
        """
        DESCRIPTION: Select Offer Module with 'Show for tablet' option value in CMS.
        DESCRIPTION: Load Oxygen application.
        EXPECTED: *   Offer module is NOT displayed on Desktop
        EXPECTED: *   Offer module is displayed on Tablets
        """
        pass

    def test_002_select_offer_module_with_show_only_for_tablets_option_value_in_cmsall_offers_for_this_module_have_show_only_for_desktop_value_in_cmsload_oxygen_application(self):
        """
        DESCRIPTION: Select Offer Module with 'Show only for tablets' option value in CMS.
        DESCRIPTION: All Offers for this module have 'Show only for desktop' value in CMS.
        DESCRIPTION: Load Oxygen application.
        EXPECTED: *   Offer Module is NOT displayed on Desktop
        EXPECTED: *   Offer Module is NOT displayed on Tablet
        """
        pass
