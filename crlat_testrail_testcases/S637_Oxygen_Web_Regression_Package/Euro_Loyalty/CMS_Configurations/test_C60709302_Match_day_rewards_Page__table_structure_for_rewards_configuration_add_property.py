import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C60709302_Match_day_rewards_Page__table_structure_for_rewards_configuration_add_property(Common):
    """
    TR_ID: C60709302
    NAME: Match day rewards Page - table structure for rewards configuration add property
    DESCRIPTION: This test case is to validate add property of table structure for rewards configuration in match day rewards Page
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  configuration for  Euro Loyalty Page should done
    """
    keep_browser_open = True

    def test_001_hit_the_cms_url(self):
        """
        DESCRIPTION: Hit the CMS URL
        EXPECTED: User is on CMS application
        """
        pass

    def test_002_navigate_to_special_pages___match_day_rewards_page_table_creation_section(self):
        """
        DESCRIPTION: Navigate to special pages - Match day rewards page table creation section
        EXPECTED: Match day rewards page should display
        """
        pass

    def test_003_verify_ui_of_table_creation(self):
        """
        DESCRIPTION: Verify UI of table creation
        EXPECTED: UI should have following details
        EXPECTED: Titile : RewardsConfiguration
        EXPECTED: right corner tow buttons Edit table and add property should present
        EXPECTED: Table with following columns should present
        EXPECTED: Tier No : mandatory
        EXPECTED: Freebet Locations : mandatory
        EXPECTED: OfferID/Sequence : mandatory
        EXPECTED: Action : Delete
        """
        pass

    def test_004_click_on_add_property_and_enter_valid_data_and_hit_save(self):
        """
        DESCRIPTION: click on add property and enter valid data and hit save
        EXPECTED: Details should save and respective values should reflect in FE
        """
        pass

    def test_005_repeat_above_step_for_other_tier_with_different_values(self):
        """
        DESCRIPTION: repeat above step for other tier with different values
        EXPECTED: Details should save and respective values should reflect in FE
        """
        pass

    def test_006_enter_offerid_sequence_which_is_not_present_in_ob_and_verify(self):
        """
        DESCRIPTION: Enter offerID sequence which is not present in OB and verify
        EXPECTED: Details should save in CMS and respective error message should display in front end
        """
        pass

    def test_007_add_same_tier_info_in_multiple_rows_and_hit_save(self):
        """
        DESCRIPTION: Add same tier info in multiple rows and hit save
        EXPECTED: Details should save in CMS
        """
        pass

    def test_008_for_any_one_tier_give_different_freebet_location_and_offerids_in_multiple_rows_and_verify(self):
        """
        DESCRIPTION: For any one tier give different freebet location and offerids in multiple rows and verify
        EXPECTED: details should be saved and diplayed
        """
        pass
