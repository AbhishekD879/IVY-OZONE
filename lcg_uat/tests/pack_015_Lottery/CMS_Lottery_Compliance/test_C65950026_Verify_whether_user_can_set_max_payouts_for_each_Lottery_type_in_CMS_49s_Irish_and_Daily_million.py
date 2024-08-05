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
class Test_C65950026_Verify_whether_user_can_set_max_payouts_for_each_Lottery_type_in_CMS_49s_Irish_and_Daily_million(Common):
    """
    TR_ID: C65950026
    NAME: Verify whether user can set max payouts for each Lottery type in CMS (49's, Irish and Daily million)
    DESCRIPTION: This testcase verifies whether user can set max payouts for each Lottery type in CMS (49's, Irish and Daily million)
    PRECONDITIONS: 1.Lotto Menu Item should be created from CMS EDIT Menu
    PRECONDITIONS: 2.SVG ID should be configured in CMS-> Image Manager.
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should able to login successfully
        """
        pass

    def test_002_click_on_lotto_item_from_cms_main_navigation(self):
        """
        DESCRIPTION: Click on Lotto Item from CMS Main Navigation
        EXPECTED: Lotto Page should open with the existing details
        """
        pass

    def test_003_click_on_lottery_type_49s__irish_or_daily_million(self):
        """
        DESCRIPTION: Click on Lottery type (49's , Irish or Daily Million)
        EXPECTED: Lottery type is opened with all the details
        """
        pass

    def test_004_verify_max_payout_field(self):
        """
        DESCRIPTION: Verify Max payout field
        EXPECTED: Able to enter and alter the amounts from dropdown
        """
        pass

    def test_005_verify_whether_user_can_set_max_payouts_for_each_lottery_type_in_cms_49s_irish_and_daily_million(self):
        """
        DESCRIPTION: Verify whether user can set max payouts for each Lottery type in CMS (49's, Irish and Daily million)
        EXPECTED: Able to set maximum payout in the feild given
        """
        pass

    def test_006_click_on_save_changes(self):
        """
        DESCRIPTION: Click on Save changes
        EXPECTED: Able to see the message- Are you sure you want to save this Lotto?
        """
        pass

    def test_007_click_on_yes(self):
        """
        DESCRIPTION: Click on Yes
        EXPECTED: Changes have been saved successfully message is displayed
        """
        pass
