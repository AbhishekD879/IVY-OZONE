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
class Test_C28043_Offer_Modules_displaying_for_desktop_tablet_both_if_Module_has_Show_for_Desktop_option_value(Common):
    """
    TR_ID: C28043
    NAME: Offer Modules displaying for desktop/tablet/both if Module has 'Show for Desktop' option value
    DESCRIPTION: This test case verifies Offer Modules displaying for desktop or tablet or both if Offer Module has 'Show for Desktop' option value
    PRECONDITIONS: 1) To load CMS use the next links:
    PRECONDITIONS: DEV -  https://coral-cms-dev0.symphony-solutions.eu/login
    PRECONDITIONS: TST2 -  https://coral-cms-tst2.symphony-solutions.eu/login
    PRECONDITIONS: STG2 - https://coral-cms-stg2.symphony-solutions.eu/login
    PRECONDITIONS: HL -  https://coral-cms-hl.symphony-solutions.eu/login
    PRECONDITIONS: PROD -  https://coral-cms.symphony-solutions.eu/login
    PRECONDITIONS: BETA - https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 2) Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    PRECONDITIONS: 3) Offer Modules with 'Show for Desktop' option value are available.
    """
    keep_browser_open = True

    def test_001_select_offer_module_with_show_for_desktop_only_option_value_in_cmsload_application(self):
        """
        DESCRIPTION: Select Offer Module with 'Show for Desktop only' option value in CMS.
        DESCRIPTION: Load application.
        EXPECTED: *   Offer module is displayed on Desktop
        EXPECTED: *   Offer module is NOT displayed on Tablets
        """
        pass

    def test_002_select_offer_module_with_show_only_for_desktop_option_value_in_cmsall_offers_for_this_module_have_show_only_for_tablets_value_in_cmsload_application(self):
        """
        DESCRIPTION: Select Offer Module with 'Show only for desktop' option value in CMS.
        DESCRIPTION: All Offers for this module have 'Show only for tablets' value in CMS.
        DESCRIPTION: Load application.
        EXPECTED: *   Offer Module is NOT displayed on Desktop
        EXPECTED: *   Offer Module is NOT displayed on Tablet
        """
        pass

    def test_003_combine_values_of_offers_and_module_offers_in_a_similar_way_to_step_2egmodule__m__offer__obothm_____tabletodesktopm__bothobothm_____botho(self):
        """
        DESCRIPTION: Combine values of Offers and Module offers in a similar way to step 2:
        DESCRIPTION: e.g.:
        DESCRIPTION: **MODULE = (M)  OFFER = (O)**
        DESCRIPTION: Both(M)     Tablet(O)
        DESCRIPTION: Desktop(M)  Both(O)
        DESCRIPTION: Both(M)     Both(O)
        EXPECTED: Offer Module is displayed in application only on devices which were chosen:
        EXPECTED: e.g.
        EXPECTED: e.g.:
        EXPECTED: **MODULE = (M)  OFFER = (O)**
        EXPECTED: Both(M)     Tablet(O)       -> Tablet
        EXPECTED: Desktop(M)  Both(O)         -> Desktop
        EXPECTED: Both(M)     Both(O)         -> Both
        """
        pass
