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
class Test_C29313_Active_Inactive_Promotions(Common):
    """
    TR_ID: C29313
    NAME: Active/Inactive Promotions
    DESCRIPTION: The purpose of this test case is to verify whether "Active" field set in CMS is applied correctly for Promotions in the application
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_open_cms_promotions(self):
        """
        DESCRIPTION: Open CMS->Promotions
        EXPECTED: 
        """
        pass

    def test_002_add_new_promotion_with_valid_data_make_surevalidity_period_start_and_validity_period_end_date_and_time_fields_are_set_correctly(self):
        """
        DESCRIPTION: Add new Promotion with valid data, make sure Validity Period Start and Validity Period End date and time fields are set correctly
        EXPECTED: 
        """
        pass

    def test_003_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_004_tap_promotions_item_from_left_hand_menu(self):
        """
        DESCRIPTION: Tap Promotions item from left-hand menu
        EXPECTED: "Promotions" page is opened
        """
        pass

    def test_005_verify_presence_of_just_added_promotion(self):
        """
        DESCRIPTION: Verify presence of just added Promotion
        EXPECTED: Just added Promotion is displayed on "Promotions" page
        """
        pass

    def test_006_unselect_active_check_box_for_the_same_promotion_in_cms_and_save_it(self):
        """
        DESCRIPTION: Unselect "Active" check box for the same Promotion in CMS and save it
        EXPECTED: 
        """
        pass

    def test_007_open_invictus___promotions(self):
        """
        DESCRIPTION: Open Invictus -> Promotions
        EXPECTED: 
        """
        pass

    def test_008_verify_presence_of_just_added_promotion(self):
        """
        DESCRIPTION: Verify presence of just added Promotion
        EXPECTED: Promotion is no more present on "Promotions" page
        """
        pass

    def test_009_verify_existing_promotions(self):
        """
        DESCRIPTION: Verify existing Promotions
        EXPECTED: Only active Promotions configured in CMS are displayed in the application, inactive Promotions are not displayed
        """
        pass
