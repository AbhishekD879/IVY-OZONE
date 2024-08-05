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
class Test_C60709300_Match_day_rewards_page__Turn_On_or_Turn_Off_configuration(Common):
    """
    TR_ID: C60709300
    NAME: Match day rewards page  - Turn On or Turn Off configuration
    DESCRIPTION: This test case is to validate CMS configuration for Match day rewards page  - Turn On or Turn Off
    PRECONDITIONS: 1.  User should have oxygen CMS access
    PRECONDITIONS: 2.  configuration for Match day rewards page should done
    """
    keep_browser_open = True

    def test_001_hit_the_cms_url(self):
        """
        DESCRIPTION: Hit the CMS URL
        EXPECTED: User is on CMS application
        """
        pass

    def test_002_navigate_to_sports_pages___sports_categories___euroloyaltyprogram(self):
        """
        DESCRIPTION: Navigate to sports pages - sports categories - EuroLoyaltyprogram
        EXPECTED: Euro Loyalty should be configured as untiered event with
        EXPECTED: Name = EuroLoyaltyProgram
        EXPECTED: CatoryID = 208
        EXPECTED: check Active , show in A-Z menu, Is top sports, show in APP check boxes and save changes
        """
        pass

    def test_003_perform_edit_or_delete_operation_each_section_and_verify(self):
        """
        DESCRIPTION: Perform edit or delete operation each section and verify
        EXPECTED: Details should update accordingly
        """
        pass
