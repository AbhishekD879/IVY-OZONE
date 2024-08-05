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
class Test_C60727646_Euro_loyalty_page_display_in_error_scenarios(Common):
    """
    TR_ID: C60727646
    NAME: Euro loyalty page display in error scenarios
    DESCRIPTION: This test case is to verify if there is error while page loading respective error should display
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  Euro Loyalty Page should created, activated and should be in valid date range in CMS special pages - Euro Loyalty page
    PRECONDITIONS: 3.  CMS->System Config->Structure->Euro Loyalty (Toggle-ON/OFF)
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch oxygen application and login with valid credentials
        EXPECTED: User is logged into the application
        """
        pass

    def test_002_verify_if_the_match_rewards_page_is_displayed_if_the_username_is_not_mapped_to_any_vip_level_is_logged_in(self):
        """
        DESCRIPTION: Verify if the Match Rewards page is displayed if the username is not mapped to any VIP level is logged in.
        EXPECTED: User should be displayed with "Something went wrong, please try again message". Match rewards page should not be displayed
        """
        pass

    def test_003_verify_if_the_match_rewards_page_is_displayed_when_the_username_is_mapped_to_a_vip_level_but_offer_is_not_mapped_to_the_corresponding_vip_level_is_logged_in(self):
        """
        DESCRIPTION: Verify if the Match Rewards page is displayed when the username is mapped to a VIP level, but offer is not mapped to the corresponding VIP level is logged in.
        EXPECTED: User should be displayed with "Something went wrong, please try again message". Match rewards page should not be displayed
        """
        pass

    def test_004_verify_if_the_match_rewards_page_is_displayed_when_the_username_is_mapped_to_a_vip_level_offer_is_mapped_to_the_vip_level_offer_is_not_mapped_to_any_cms_tier_level_is_logged_in(self):
        """
        DESCRIPTION: Verify if the Match Rewards page is displayed when the username is mapped to a VIP level, offer is mapped to the VIP level, Offer is not mapped to any CMS Tier level is logged in
        EXPECTED: User should be displayed with "Something went wrong, please try again message". Match rewards page should not be displayed
        """
        pass
