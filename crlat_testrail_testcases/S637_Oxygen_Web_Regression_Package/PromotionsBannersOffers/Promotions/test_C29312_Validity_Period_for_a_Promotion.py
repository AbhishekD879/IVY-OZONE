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
class Test_C29312_Validity_Period_for_a_Promotion(Common):
    """
    TR_ID: C29312
    NAME: Validity Period for a Promotion
    DESCRIPTION: The purpose of this test case is to verify whether Show/Hide Date and Time are applied correctly for Promotions
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
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

    def test_003_verify_validity_period_start_date_and_time(self):
        """
        DESCRIPTION: Verify 'Validity Period Start' date and time
        EXPECTED: Date format: MM/DD/YYYY
        EXPECTED: Time format: HH:MM:SS
        EXPECTED: 'Today' button set up current time automatically
        """
        pass

    def test_004_verify_validity_period_end_date_and_time(self):
        """
        DESCRIPTION: Verify 'Validity Period End' date and time
        EXPECTED: Date format: MM/DD/YYYY
        EXPECTED: Time format: HH:MM:SS
        EXPECTED: 'Tommorrow' button set up current time automatically
        """
        pass

    def test_005_enter_valid_validity_period_start_and_validity_period_end_and_click_on_create_button(self):
        """
        DESCRIPTION: Enter valid Validity Period Start and Validity Period End and click on 'Create' button
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_006_load_oxygen_and_tap_on_promotions_on_left_hand_menu(self):
        """
        DESCRIPTION: Load Oxygen and tap on Promotions on left-hand menu
        EXPECTED: "Promotions" page is opened
        """
        pass

    def test_007_verify_presence_of_just_added_promotion(self):
        """
        DESCRIPTION: Verify presence of just added Promotion
        EXPECTED: Verified promotion is displayed on "Promotions" page if current date and time belong to time box set by Validity Period Start and Validity Period End date and time fields
        """
        pass

    def test_008_proceed_to_cms_and_set_validity_period_start_andvalidity_period_end_date_and_time_as_time_range_from_the_past(self):
        """
        DESCRIPTION: Proceed to CMS and set 'Validity Period Start' and 'Validity Period End' date and time as time range from the past
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_009_load_oxygen___promotions_page(self):
        """
        DESCRIPTION: Load Oxygen -> 'Promotions' page
        EXPECTED: Verified promotion is not shown within the application
        """
        pass

    def test_010_proceed_to_cms_and_set_validity_period_start_andvalidity_period_end_date_and_time_as_time_range_from_the_future(self):
        """
        DESCRIPTION: Proceed to CMS and set 'Validity Period Start' and 'Validity Period End' date and time as time range from the future
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_011_load_oxygen___promotions_page(self):
        """
        DESCRIPTION: Load Oxygen -> 'Promotions' page
        EXPECTED: Verified promotion is not shown within the application
        """
        pass

    def test_012_proceed_to_cms_and_set_validity_period_start_from_the_past_andvalidity_period_end_in_a_few_mins_from_current_time(self):
        """
        DESCRIPTION: Proceed to CMS and set 'Validity Period Start' from the past and 'Validity Period End' in a few mins from current time
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_013_load_oxygen___promotions_page___wait_till_time_set_in_validity_period_end_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -> 'Promotions' page -> Wait till time set in 'Validity Period End' is passed
        EXPECTED: After time set in 'Validity Period End' is passed verified promotion **is no more shown** within the application
        """
        pass

    def test_014_proceed_to_cms_and_set_validity_period_start_in_a_few_mins_from_current_time_andvalidity_period_end_from_the_future(self):
        """
        DESCRIPTION: Proceed to CMS and set 'Validity Period Start' in a few mins from current time and 'Validity Period End' from the future
        EXPECTED: The changes are saved and the data stored accordingly
        """
        pass

    def test_015_load_oxygen___promotions_page___wait_till_time_set_in_validity_period_end_is_passed(self):
        """
        DESCRIPTION: Load Oxygen -> 'Promotions' page -> Wait till time set in 'Validity Period End' is passed
        EXPECTED: After time set in 'Validity Period End' is passed verified promotion **appears to be shown** within the application
        """
        pass
