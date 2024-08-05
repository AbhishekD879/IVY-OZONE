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
class Test_C28053_Offers_displaying_for_desktop_tablet_both_if_Module_has_Show_only_for_desktop_option_value(Common):
    """
    TR_ID: C28053
    NAME: Offers displaying for desktop/tablet/both if Module has 'Show only for desktop' option value
    DESCRIPTION: This test case verifies Offers displaying for desktop/tablet/both if Module has 'Show only for desktop' option value
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
    PRECONDITIONS: 3) Offers with different 'Show for Desktop or Tablet or Both' option value are available.
    PRECONDITIONS: 4) All Offers are related to Offer Module with 'Show only for desktop' option value checked.
    """
    keep_browser_open = True

    def test_001_select_offer_with_show_for_desktop_only_option_value_from_this_moduleload_oxygen_application_and_verify_its_displaying_on_desktop_and_tablet_devices(self):
        """
        DESCRIPTION: Select Offer with 'Show for Desktop only' option value  from this Module
        DESCRIPTION: Load Oxygen application and verify it's displaying on desktop and tablet devices
        EXPECTED: *   Offer is displayed on Desktop
        EXPECTED: *   Offer is NOT displayed on Tablets
        """
        pass

    def test_002_select_offer_with_show_for_tablet_only_option_valueload_oxygen_application_and_verify_its_displaying_on_desktop_and_tablet_devices(self):
        """
        DESCRIPTION: Select Offer with 'Show for Tablet only' option value.
        DESCRIPTION: Load Oxygen application and verify it's displaying on desktop and tablet devices
        EXPECTED: *   Offer is NOT displayed on Desktop
        EXPECTED: *   Offer is NOT displayed on Tablets
        """
        pass

    def test_003_select_offer_with_show_for_both_option_valueload_oxygen_application_and_verify_offer_displaying_on_desktop_and_tablet_devices(self):
        """
        DESCRIPTION: Select Offer with 'Show for both' option value.
        DESCRIPTION: Load Oxygen application and verify Offer displaying on desktop and tablet devices
        EXPECTED: *   Offer is displayed on Desktop
        EXPECTED: *   Offer is NOT displayed on Tablets
        """
        pass
