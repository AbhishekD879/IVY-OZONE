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
class Test_C29318_Supporting_Brands(Common):
    """
    TR_ID: C29318
    NAME: Supporting Brands
    DESCRIPTION: This test case verifies creating and displaying different Promotions for different Brands
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms_promotions(self):
        """
        DESCRIPTION: Load CMS->Promotions
        EXPECTED: 
        """
        pass

    def test_002_select_brand_sportsbook_from_brand_drop_down(self):
        """
        DESCRIPTION: Select brand "SportsBook" from Brand drop down
        EXPECTED: 
        """
        pass

    def test_003_add_new_promotion_with_all_required_data_and_image(self):
        """
        DESCRIPTION: Add new Promotion with all required data and image
        EXPECTED: Added Promotion appears in the list of Promotions of SportsBook brand in CMS.
        """
        pass

    def test_004_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_005_tap_promotions_item_on_sport_menu_ribbon(self):
        """
        DESCRIPTION: Tap Promotions item on Sport Menu Ribbon
        EXPECTED: Promotions page is opened
        EXPECTED: Just added Promotion is displayed on this page
        EXPECTED: The list of Promotions displayed corresponds to the list of Promotions configured in CMS for "SportsBook" brand
        """
        pass

    def test_006_open_cms_promotions(self):
        """
        DESCRIPTION: Open CMS->Promotions
        EXPECTED: 
        """
        pass

    def test_007_select_another_brand_from_brand_drop_down(self):
        """
        DESCRIPTION: Select another brand from Brand drop down
        EXPECTED: 
        """
        pass

    def test_008_add_new_promotion_with_all_required_data_and_image_for_another_brand(self):
        """
        DESCRIPTION: Add new Promotion with all required data and image for another brand
        EXPECTED: Added Promotion appears in the list of Promotions of corresponding brand in CMS
        """
        pass

    def test_009_verify_displaying_of_just_added_promotion_in_invictus_application_of_another_brandnote_this_step_can_be_verified_only_if_app_with_another_brand_is_available_skip_this_step_if_not_available(self):
        """
        DESCRIPTION: Verify displaying of just added Promotion in Invictus application of another brand
        DESCRIPTION: Note: This step can be verified only if app with another brand is available. Skip this step if not available
        EXPECTED: Added Promotion is displayed on Promotions page on front end of the Invictus app of corresponding brand.
        """
        pass
