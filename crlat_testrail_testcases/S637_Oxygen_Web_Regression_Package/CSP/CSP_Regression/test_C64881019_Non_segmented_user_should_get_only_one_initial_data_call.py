import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64881019_Non_segmented_user_should_get_only_one_initial_data_call(Common):
    """
    TR_ID: C64881019
    NAME: Non segmented user should get only one initial data call
    DESCRIPTION: This test case verifies initial data call for non segmented user
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 2)User should not mapped to any of the segment
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_login_in_fe_with_user_from_precondition_1(self):
        """
        DESCRIPTION: Login in FE with user from precondition 1
        EXPECTED: User should get 2 initial data calls
        """
        pass

    def test_003_login_in_fe_with_user_from_precondition_2(self):
        """
        DESCRIPTION: Login in FE with user from precondition 2
        EXPECTED: Non segmented user should get only one initial data call
        """
        pass
