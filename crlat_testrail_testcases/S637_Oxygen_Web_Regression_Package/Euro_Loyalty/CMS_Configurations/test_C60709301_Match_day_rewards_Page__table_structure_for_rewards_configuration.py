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
class Test_C60709301_Match_day_rewards_Page__table_structure_for_rewards_configuration(Common):
    """
    TR_ID: C60709301
    NAME: Match day rewards Page - table structure for rewards configuration
    DESCRIPTION: This test case is to validate CMS configuration for match day rewards Page - table structure for Stickers/Badges display
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

    def test_003_verify_ui_of_table_creation_section(self):
        """
        DESCRIPTION: Verify UI of table creation section
        EXPECTED: UI should have following details
        EXPECTED: Titile : RewardsConfiguration
        EXPECTED: right corner tow buttons Edit table and add property should present
        EXPECTED: Table with following columns should present
        EXPECTED: > Tier No : mandatory
        EXPECTED: > Freebet Locations : mandatory
        EXPECTED: > OfferID/Sequence : mandatory
        EXPECTED: > Action : Delete
        """
        pass

    def test_004_enter_single_tier_number_and_one_freebet_location_and_one_offerid_sequences_and_hit_save(self):
        """
        DESCRIPTION: Enter single tier Number and one freebet location and one offerID sequences and hit save
        EXPECTED: If user enter offerID sequence count less than than the freebet locations count details should not save
        EXPECTED: Message **"Offer ids should be one more than no. of freebet locations"** should display
        EXPECTED: if we give 3 free bet locations then offerID sequences should be 4
        """
        pass

    def test_005_enter_single_tier_number_and_two_freebet_locations_with_comma_separation_and_two_offerid_sequences_with_comma_separation_and_hit_save(self):
        """
        DESCRIPTION: Enter single tier Number and two freebet locations with comma separation and two offerID sequences with comma separation and hit save
        EXPECTED: If user enter offerID sequence count less than than the freebet locations count details should not save
        EXPECTED: Message **"Offer ids should be one more than no. of freebet locations"** should display
        EXPECTED: if we give 3 free bet locations then offerID sequences should be 4
        """
        pass

    def test_006_enter_single_tier_number_and_two_freebet_locations_without_comma_separation_and_two_offerid_sequences_without_comma_separation_and_hit_save(self):
        """
        DESCRIPTION: Enter single tier Number and two freebet locations without comma separation and two offerID sequences without comma separation and hit save
        EXPECTED: valid error message should display
        """
        pass

    def test_007_enter_single_tier_number_and_two_freebet_locations_with_comma_separation_and_three_offerid_sequences_with_comma_separation_and_hit_save(self):
        """
        DESCRIPTION: Enter single tier Number and two freebet locations with comma separation and three offerID sequences with comma separation and hit save
        EXPECTED: Details should update accordingly
        """
        pass

    def test_008_enter_multiple_tier_numbers_and_multiple_freebet_locations_with_comma_separation_and_three_offerid_sequences_with_comma_separation_and_hit_save(self):
        """
        DESCRIPTION: Enter multiple tier Numbers and multiple freebet locations with comma separation and three offerID sequences with comma separation and hit save
        EXPECTED: Details should update accordingly
        """
        pass
