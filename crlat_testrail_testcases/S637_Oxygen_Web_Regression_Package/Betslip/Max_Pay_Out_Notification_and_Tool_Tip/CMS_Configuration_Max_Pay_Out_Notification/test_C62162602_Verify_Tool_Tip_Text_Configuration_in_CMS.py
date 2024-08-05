import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C62162602_Verify_Tool_Tip_Text_Configuration_in_CMS(Common):
    """
    TR_ID: C62162602
    NAME: Verify Tool Tip Text Configuration in CMS
    DESCRIPTION: This test Case verifies the tool tip text configuration
    PRECONDITIONS: Login to CMS with admin user
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as Admin user
        EXPECTED: Login should be successful
        """
        pass

    def test_002_navigate_to_system_config__structure_maxpayout(self):
        """
        DESCRIPTION: Navigate to System Config -Structure-Maxpayout
        EXPECTED: Configure-maxPayoutMsg Messaging and click on save
        """
        pass

    def test_003_login_to_oxygen_application(self):
        """
        DESCRIPTION: Login to oxygen application
        EXPECTED: 
        """
        pass

    def test_004_click_on_any_selection_from_any_eventsportracing(self):
        """
        DESCRIPTION: Click on any selection from ANY event(Sport/Racing)
        EXPECTED: Desktop : Selection should be added to Betslip
        EXPECTED: Mobile: Click on Add to Betslip in Quick bet Overlay
        """
        pass

    def test_005_enter_stake_and_validate_the_display_of_max_payout_message_configure_in_cms(self):
        """
        DESCRIPTION: Enter Stake and Validate the display of Max payout message configure in CMS
        EXPECTED: MaxPayout message should be as per cms configuration
        """
        pass
