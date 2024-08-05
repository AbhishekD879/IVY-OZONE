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
class Test_C29321_Promotions_Displaying_for_New_Users(Common):
    """
    TR_ID: C29321
    NAME: Promotions Displaying for New Users
    DESCRIPTION: This test case verifies display of promotions for new users
    DESCRIPTION: AUTOTEST Mobile: [C2861797]
    DESCRIPTION: AUTOTEST Desktop: [C2861823]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_new_promotion_in_cms_selectshow_for_new_users_option_and_save_changes(self):
        """
        DESCRIPTION: Add new Promotion in CMS, select **'Show for new users**' option and save changes
        EXPECTED: Promotion is added successfully
        """
        pass

    def test_002_clear_browsers_local_storage_and_cookies_and_load_invictus_app(self):
        """
        DESCRIPTION: Clear browser`s local storage and cookies and load Invictus app
        EXPECTED: **'OX.existingUser' **  is empty or not present in the local storage
        """
        pass

    def test_003_verify_presence_of_just_added_promotion(self):
        """
        DESCRIPTION: Verify presence of just added Promotion
        EXPECTED: Added on step #1 Promotion is present on front end
        """
        pass

    def test_004_log_in_into_app(self):
        """
        DESCRIPTION: Log in into app
        EXPECTED: 
        """
        pass

    def test_005_verify_value_creation_in_local_storage(self):
        """
        DESCRIPTION: Verify value creation in local storage
        EXPECTED: **'OX.existingUser = true'** value is added in the local storage
        """
        pass

    def test_006_verify_presence_of_added_on_step_1_promotion(self):
        """
        DESCRIPTION: Verify presence of added on step #1 Promotion
        EXPECTED: Added on step #1 Promotion is NOT present on front end
        """
        pass

    def test_007_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: 
        """
        pass

    def test_008_verify_presence_of_added_on_step_1_promotion(self):
        """
        DESCRIPTION: Verify presence of added on step #1 Promotion
        EXPECTED: *   Added on step #1 Promotion is NOT present on front end
        EXPECTED: *   **'OX.existingUser = true'** value is still present in the local storage
        """
        pass
