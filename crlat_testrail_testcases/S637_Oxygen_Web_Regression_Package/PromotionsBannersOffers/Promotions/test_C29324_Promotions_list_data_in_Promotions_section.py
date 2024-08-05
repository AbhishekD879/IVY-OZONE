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
class Test_C29324_Promotions_list_data_in_Promotions_section(Common):
    """
    TR_ID: C29324
    NAME: Promotions list data in Promotions section
    DESCRIPTION: This test case verifies Promotions list data which are displayed in Promotions section
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-9235 Display "Show to customers" column in Banners and Promotions lists
    PRECONDITIONS: User is logged in to CMS
    """
    keep_browser_open = True

    def test_001_go_to_promotionssection_and_verify_data_displaying_for_each_promotionin_the_list(self):
        """
        DESCRIPTION: Go to Promotions section and verify data displaying for each Promotion in the list
        EXPECTED: Following data are displayed for each Promotion:
        EXPECTED: *   Title
        EXPECTED: *   Promo Key
        EXPECTED: *   Show on Competitions
        EXPECTED: *   Validity period start
        EXPECTED: *   Validity period end
        EXPECTED: *   Category ID
        EXPECTED: *   'Show for Customer' option value for selected Promotion
        EXPECTED: *   'Include VIP Levels'  option value for selected Promotion
        """
        pass

    def test_002_select_promotion_update_all_data_for_it_and_save_changes(self):
        """
        DESCRIPTION: Select promotion, update all data for it and save changes.
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_003_go_to_promotions_list_and_verify_updated_data_displaying_for_the_promotion(self):
        """
        DESCRIPTION: Go to Promotions list and verify updated data displaying for the Promotion
        EXPECTED: Updated data are displayed in the list
        """
        pass
