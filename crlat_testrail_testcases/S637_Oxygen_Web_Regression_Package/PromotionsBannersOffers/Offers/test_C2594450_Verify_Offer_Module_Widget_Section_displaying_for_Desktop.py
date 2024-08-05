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
class Test_C2594450_Verify_Offer_Module_Widget_Section_displaying_for_Desktop(Common):
    """
    TR_ID: C2594450
    NAME: Verify Offer Module Widget/Section displaying for Desktop
    DESCRIPTION: This test case verifies Offer Module Widget/Section displaying for Desktop in case if AEM banners are not available
    DESCRIPTION: Be aware that case, when offers are not available, is not covered based on the comment from PO in https://jira.egalacoral.com/browse/BMA-28074 "It should always be available. It's responsibility of content/ marketing team to manage that area."
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    PRECONDITIONS: To disable AEM Banners:
    PRECONDITIONS: * System Configuration -> Structure -> DynamicBanners -> enabled (unchecked)
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_offer_section_in_hero_header_in_case_if_aem_banners_are_not_available(self):
        """
        DESCRIPTION: Verify displaying of Offer section in Hero Header in case if AEM banners are not available
        EXPECTED: * AEM Banners and Offer section are NOT present in Hero Header
        EXPECTED: * Offer widget is NOT displayed in Right column
        """
        pass
