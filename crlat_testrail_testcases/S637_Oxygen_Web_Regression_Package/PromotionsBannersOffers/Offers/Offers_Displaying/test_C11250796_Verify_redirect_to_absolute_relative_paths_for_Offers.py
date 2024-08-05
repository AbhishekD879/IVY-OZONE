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
class Test_C11250796_Verify_redirect_to_absolute_relative_paths_for_Offers(Common):
    """
    TR_ID: C11250796
    NAME: Verify redirect to absolute/relative paths for Offers
    DESCRIPTION: This test case verifies that redirection to 'target Uri' works fine for absolute and relative paths in Offers
    PRECONDITIONS: 1. Offer module should be created in CMS: Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: 2. Two Offers should be created: Offers -> Offers -> Create Offer
    PRECONDITIONS: * 1st with absolute path in 'target Uri' e.g. https://gaming.coral.co.uk/live-casino
    PRECONDITIONS: * 2nd with relative path in 'target Uri' e.g. /promotions/details/YourCall
    """
    keep_browser_open = True

    def test_001_load_the_app_on_desktop(self):
        """
        DESCRIPTION: Load the app on Desktop
        EXPECTED: Offers are displayed in Offer widget at the Right column
        """
        pass

    def test_002_click_on_1st_offer_with_absolute_path_in_target_uri(self):
        """
        DESCRIPTION: Click on 1st offer with absolute path in 'target Uri'
        EXPECTED: Redirection to 'target Uri' occurs
        """
        pass

    def test_003_click_on_2nd_offer_with_relative_path_in_target_uri(self):
        """
        DESCRIPTION: Click on 2nd offer with relative path in 'target Uri'
        EXPECTED: Redirection to 'target Uri' occurs
        """
        pass

    def test_004_load_the_app_on_tablet_and_repeat_steps_2_3_for_offers_within_offer_module_below_betslip(self):
        """
        DESCRIPTION: Load the app on Tablet and repeat steps 2-3 for offers within Offer module (below Betslip)
        EXPECTED: 
        """
        pass
