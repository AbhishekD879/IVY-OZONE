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
class Test_C29315_Edit_Promotion_Descriptions(Common):
    """
    TR_ID: C29315
    NAME: Edit Promotion Descriptions
    DESCRIPTION: This test case verifies ability of edition of promotion description
    DESCRIPTION: **Jira ticket: **BMA-834
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/promotions
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_open_cms_promotions(self):
        """
        DESCRIPTION: Open CMS->Promotions
        EXPECTED: 
        """
        pass

    def test_002_add_new_promotion_with_valid_data(self):
        """
        DESCRIPTION: Add new Promotion with valid data
        EXPECTED: 
        """
        pass

    def test_003_load_invictus_app(self):
        """
        DESCRIPTION: Load Invictus app
        EXPECTED: Homepage is opened
        """
        pass

    def test_004_go_to_promotions_section(self):
        """
        DESCRIPTION: Go to 'Promotions' section
        EXPECTED: 'Promotions' section is opened
        EXPECTED: List of all available promotions is present
        """
        pass

    def test_005_verify_just_added_promotion(self):
        """
        DESCRIPTION: Verify just added Promotion
        EXPECTED: Just added Promotion is displayed on "Promotions" page
        EXPECTED: All input data is displayed correctly
        """
        pass

    def test_006_go_to_cms_and_make_some_changes_in_description_field_of_new_promotion_and_save_it(self):
        """
        DESCRIPTION: Go to CMS and make some changes in 'Description' field of new Promotion and save it
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_007_load_invictus_app_promotions(self):
        """
        DESCRIPTION: Load Invictus app->Promotions
        EXPECTED: 
        """
        pass

    def test_008_verifychanges_made_on_new_promotion(self):
        """
        DESCRIPTION: Verify changes made on new Promotion
        EXPECTED: Changes made in CMS are displayed successfully
        """
        pass
