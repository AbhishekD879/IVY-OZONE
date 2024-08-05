import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C63770679_Verify_Quickbet_not_removed_based_on_input_Model_as_At_RISK_and_Risk_Level_as_LOW_and_MoH_as_TBC_after_login(Common):
    """
    TR_ID: C63770679
    NAME: Verify Quickbet not removed based on input Model as At RISK and Risk Level as LOW and MoH as TBC after login
    DESCRIPTION: The test case verifies the quickbet feature not get removed for Low risk level users
    PRECONDITIONS: Configure in CMS like input Model as At Risk  and Risk Level as LOW AND MoH as TBC
    """
    keep_browser_open = True

    def test_001_login_into_oxygen_application_as_low_risk_user_gt_add_one_selection(self):
        """
        DESCRIPTION: Login into Oxygen Application as LOW risk User-&gt; add one selection
        EXPECTED: User logged in successfully
        """
        pass

    def test_002_verify_quick_bet_feature_removed_for_low_risk_level_user(self):
        """
        DESCRIPTION: Verify quick bet feature removed for LOW Risk level user
        EXPECTED: Quick bet feature should be displayed for Low risk User
        """
        pass

    def test_003_verify_selection_is_added_to_quickbet(self):
        """
        DESCRIPTION: Verify selection is added to QuickBet
        EXPECTED: Selection should be added to QuickBet screen
        """
        pass
