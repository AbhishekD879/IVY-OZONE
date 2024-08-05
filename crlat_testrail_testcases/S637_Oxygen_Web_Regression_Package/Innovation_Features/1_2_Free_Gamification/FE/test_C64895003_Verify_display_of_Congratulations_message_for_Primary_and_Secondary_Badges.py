import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C64895003_Verify_display_of_Congratulations_message_for_Primary_and_Secondary_Badges(Common):
    """
    TR_ID: C64895003
    NAME: Verify display of Congratulations message for Primary and Secondary Badges
    DESCRIPTION: This test case verifies display of Congratulations message for primary and secondary badges
    PRECONDITIONS: My Badges and Season should be configured in CMS
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes(self):
        """
        DESCRIPTION: Login to Ladbrokes
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_click_on_1_2_free_tab(self):
        """
        DESCRIPTION: Click on '1-2 Free' tab
        EXPECTED: User should be navigated to 1-2 Free page
        """
        pass

    def test_003_verify_display_of_my_badges_tab(self):
        """
        DESCRIPTION: Verify display of 'My Badges' tab
        EXPECTED: User should be able to view 'My Badges' tab
        """
        pass

    def test_004_click_on_my_badges_tab(self):
        """
        DESCRIPTION: Click on 'My Badges' tab
        EXPECTED: User should be able to view team jerseys
        """
        pass

    def test_005_trigger_number_of_primary_badges_collected_by_the_user_is_equal_to_the_primary_badges_values_mentioned_in_cms(self):
        """
        DESCRIPTION: Trigger number of primary badges collected by the user is equal to the Primary Badges values mentioned in CMS
        EXPECTED: 
        """
        pass

    def test_006_verify_display_of_primary_congratulations_message(self):
        """
        DESCRIPTION: Verify display of Primary congratulations message
        EXPECTED: Primary congratulations message should be displayed as per the message configured in CMS
        """
        pass

    def test_007_trigger_number_of_secondary_badges_collected_by_the_user_is_equal_to_the_secondary_badges_values_mentioned_in_cms(self):
        """
        DESCRIPTION: Trigger number of secondary badges collected by the user is equal to the secondary Badges values mentioned in CMS
        EXPECTED: Secondary congratulations message should be displayed as per the message configured in CMS
        """
        pass
